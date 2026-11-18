#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""推送前自检 Fuwari / Astro 文章的 front matter。

用法（在仓库根目录执行）：
    python scripts/check-frontmatter.py             # 检查 src/content/posts 下全部 .md
    python scripts/check-frontmatter.py 某篇文章.md  # 只检查指定文件/目录
    python scripts/check-frontmatter.py --staged    # 只检查 git 暂存区里的文章
    python scripts/check-frontmatter.py --strict    # 把警告也当作错误（退出码 1）
    python scripts/check-frontmatter.py --json      # 输出 JSON，便于接入其他工具

退出码：0 = 通过；1 = 有错误（或 --strict 下有警告）；2 = 用法/环境问题。

依赖：PyYAML（pip install pyyaml）。之所以用它，是因为 Astro 的 legacy
content collection 使用 js-yaml 解析 front matter，PyYAML 对日期、引号、
重复键的处理与之一致；而 Node 侧没有可直接引用的 YAML 依赖。
"""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Windows 下通过管道/重定向时，Python 默认用 GBK 输出，Git Bash 里会乱码
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass

try:
    import yaml
except ImportError:  # pragma: no cover - 环境问题
    sys.stderr.write(
        "缺少 PyYAML，无法解析 front matter。\n"
        "请先安装：python -m pip install pyyaml\n"
    )
    raise SystemExit(2)


# ---------------------------------------------------------------------------
# 常量：与 src/content/config.ts 的 zod schema 保持一致
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = REPO_ROOT / "src" / "content" / "posts"

TAG_PREFIX = "tag:yaml.org,2002:"
STR_TAG = TAG_PREFIX + "str"
BOOL_TAG = TAG_PREFIX + "bool"
INT_TAG = TAG_PREFIX + "int"
FLOAT_TAG = TAG_PREFIX + "float"
TIMESTAMP_TAG = TAG_PREFIX + "timestamp"
NULL_TAG = TAG_PREFIX + "null"
SEQ_TAG = TAG_PREFIX + "seq"
MAP_TAG = TAG_PREFIX + "map"

# 和 defineCollection 里的字段一一对应
ALLOWED_KEYS = [
    "title",
    "published",
    "updated",
    "draft",
    "description",
    "image",
    "tags",
    "category",
    "lang",
    # 下面四个由 Fuwari 构建时写入，正常不需要手写
    "prevTitle",
    "prevSlug",
    "nextTitle",
    "nextSlug",
]
INTERNAL_KEYS = {"prevTitle", "prevSlug", "nextTitle", "nextSlug"}

# src/i18n/translation.ts 中提供的语言
KNOWN_LANGS = {"en", "es", "id", "ja", "ko", "th", "tr", "vi", "zh_CN", "zh_TW"}

DATE_EXAMPLE = "2026-08-09"
DATE_PATTERN = re.compile(r"^\d{4}-\d{1,2}-\d{1,2}$")


# ---------------------------------------------------------------------------
# YAML loader：贴近 js-yaml / Astro 的行为
# ---------------------------------------------------------------------------


class FrontMatterLoader(yaml.SafeLoader):
    """SafeLoader 的去 YAML 1.1 化版本。

    PyYAML 默认按 YAML 1.1 把 yes/no/on/off 解析成布尔值，而 js-yaml 4
    只认 true/false。这里删掉旧的 bool resolver 并只保留 true/false，
    避免把 `title: Yes` 误报成类型错误。
    """


FrontMatterLoader.yaml_implicit_resolvers = {
    first_char: [
        (tag, regexp)
        for tag, regexp in resolvers
        if tag != BOOL_TAG
    ]
    for first_char, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}

FrontMatterLoader.add_implicit_resolver(
    BOOL_TAG,
    re.compile(r"^(?:true|True|TRUE|false|False|FALSE)$"),
    list("tTfF"),
)


def _construct_mapping(loader: yaml.Loader, node: yaml.MappingNode) -> dict:
    """构造 mapping，并像 js-yaml 一样对重复键报错。"""
    loader.flatten_mapping(node)
    mapping: dict = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=True)
        try:
            duplicate = key in mapping
        except TypeError:  # 理论上 YAML 键不会是 list/dict
            duplicate = False
        if duplicate:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key: {key}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=True)
    return mapping


FrontMatterLoader.add_constructor(MAP_TAG, _construct_mapping)


# ---------------------------------------------------------------------------
# 数据结构与输出
# ---------------------------------------------------------------------------


@dataclass
class Issue:
    path: Path
    line: int
    column: int
    level: str  # "error" | "warning"
    message: str
    snippet: str | None = None
    order: int = 0


@dataclass
class FileResult:
    path: Path
    issues: list[Issue] = field(default_factory=list)


@dataclass
class Stats:
    checked: int = 0
    errors: int = 0
    warnings: int = 0


class Colors:
    def __init__(self, enabled: bool) -> None:
        self.red = "\033[31m" if enabled else ""
        self.yellow = "\033[33m" if enabled else ""
        self.dim = "\033[2m" if enabled else ""
        self.bold = "\033[1m" if enabled else ""
        self.reset = "\033[0m" if enabled else ""


# ---------------------------------------------------------------------------
# 单文件检查
# ---------------------------------------------------------------------------


def _tag_name(node: yaml.Node | None) -> str:
    if node is None:
        return ""
    return node.tag.replace(TAG_PREFIX, "")


def _type_name(node: yaml.Node | None) -> str:
    if node is None:
        return "缺失"
    if isinstance(node, yaml.SequenceNode):
        return "列表"
    if isinstance(node, yaml.MappingNode):
        return "映射"
    return {
        "str": "字符串",
        "int": "数字",
        "float": "数字",
        "bool": "布尔值",
        "timestamp": "日期",
        "null": "空值",
        "binary": "二进制",
    }.get(_tag_name(node), _tag_name(node) or "未知类型")


def _pos(node: yaml.Node | None, fallback_line: int = 2) -> tuple[int, int]:
    """把 YAML node 的 0 基 mark 换算成文件里的 1 基行/列。

    front matter 的内容从文件第 2 行开始，所以 mark.line + 2。
    """
    if node is None or getattr(node, "start_mark", None) is None:
        return fallback_line, 1
    return node.start_mark.line + 2, node.start_mark.column + 1


def _bad_timestamp_value(node: yaml.Node | None) -> str | None:
    """返回“像日期但日期不存在”的原始文本，合法或不是日期时返回 None。"""
    if not isinstance(node, yaml.ScalarNode) or node.tag != TIMESTAMP_TAG:
        return None
    if node.style in ("'", '"', "|", ">"):
        return None
    raw = str(node.value)
    date_part = re.split(r"[Tt ]", raw, maxsplit=1)[0]
    try:
        dt.date.fromisoformat(date_part)
    except ValueError:
        return raw
    return None


def _yaml_hint(problem: str) -> str:
    lowered = problem.lower()
    if "mapping values are not allowed" in lowered:
        return "值里出现冒号时，需要用引号包起来，例如 title: \"A: B\""
    if "could not find expected ':'" in lowered:
        return "这一行缺少英文冒号，或缩进/引号没有配对"
    if "found character '\\t'" in lowered or "cannot start any token" in lowered:
        return "front matter 不能用 Tab 缩进，请换成空格"
    if "unexpected end of stream" in lowered:
        return "引号、方括号或花括号没有闭合"
    if "expected ',' or ']'" in lowered or "expected ',' or '}'" in lowered:
        return "列表/对象里的逗号或括号不完整"
    if "did not find expected key" in lowered:
        return "缩进层级不对，或者上一个值没有写完"
    return "请检查这一行的缩进、冒号和引号是否配对"


def _yaml_error_issue(
    path: Path, exc: yaml.MarkedYAMLError, lines: list[str], fallback_line: int
) -> Issue:
    mark = getattr(exc, "problem_mark", None) or getattr(exc, "context_mark", None)
    line = mark.line + 2 if mark else fallback_line
    column = mark.column + 1 if mark else 1
    problem = (getattr(exc, "problem", None) or str(exc)).strip()
    context = (getattr(exc, "context", None) or "").strip()
    detail = f"{context}: {problem}" if context else problem
    message = f"YAML 语法错误：{detail}。提示：{_yaml_hint(problem)}"
    return Issue(path, line, column, "error", message, _snippet(lines, line))


def _snippet(lines: list[str], line: int) -> str | None:
    if 1 <= line <= len(lines):
        return lines[line - 1].rstrip("\n")
    return None


def check_file(path: Path) -> list[Issue]:
    issues: list[Issue] = []
    counter = 0

    def add(
        level: str,
        line: int,
        column: int,
        message: str,
        snippet: str | None = None,
    ) -> None:
        nonlocal counter
        counter += 1
        issues.append(
            Issue(
                path,
                max(1, line),
                max(1, column),
                level,
                message,
                snippet if snippet is not None else _snippet(lines, line),
                counter,
            )
        )

    raw = path.read_bytes()
    bom_warning = raw.startswith(b"\xef\xbb\xbf")
    if bom_warning:
        raw = raw[3:]

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return [Issue(path, 1, 1, "error", f"文件不是 UTF-8 编码：{exc}", None)]

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")

    if bom_warning:
        add(
            "warning",
            1,
            1,
            "文件带有 UTF-8 BOM，建议另存为不带 BOM 的 UTF-8"
            "（有些工具会因此读不到 front matter）",
        )

    if not lines or lines[0].rstrip() != "---":
        hint = ""
        for i, candidate in enumerate(lines[:6], start=1):
            if candidate.rstrip() == "---":
                hint = f"（现在第 {i} 行才出现 ---）"
                break
        add(
            "error",
            1,
            1,
            f"front matter 的 --- 必须放在文件第一行{hint}"
            if hint
            else "front matter 必须以 --- 开头，而且 --- 必须在文件第一行",
        )
        return issues

    close_index = None
    for i in range(1, len(lines)):
        if lines[i].rstrip() == "---":
            close_index = i
            break

    if close_index is None:
        add(
            "error",
            1,
            1,
            "front matter 缺少结束的 ---。第二行 --- 之前是 front matter，之后才是正文",
        )
        return issues

    front = "\n".join(lines[1:close_index])
    if not front.strip():
        add(
            "error",
            2,
            1,
            "front matter 是空的，至少需要 title 和 published 两个字段",
        )
        return issues

    # --- 语法解析 -------------------------------------------------------
    try:
        root = yaml.compose(front, Loader=FrontMatterLoader)
    except yaml.MarkedYAMLError as exc:
        return issues + [_yaml_error_issue(path, exc, lines, 2)]

    if root is None:
        add("error", 2, 1, "front matter 解析结果为空，至少需要 title 和 published")
        return issues

    if not isinstance(root, yaml.MappingNode):
        line, column = _pos(root)
        add(
            "error",
            line,
            column,
            f"front matter 必须是一组 key: value（映射），当前是{_type_name(root)}",
        )
        return issues

    # 先单独验证“语法像日期、实际不存在”的值（如 2026-02-30），
    # 否则 yaml.load 会抛出不带位置信息的 ValueError。
    invalid_dates: list[Issue] = []
    for key_node, value_node in root.value:
        if not (
            isinstance(key_node, yaml.ScalarNode)
            and key_node.value in ("published", "updated")
        ):
            continue
        bad_value = _bad_timestamp_value(value_node)
        if bad_value is not None:
            line, column = _pos(value_node)
            invalid_dates.append(
                Issue(
                    path,
                    line,
                    column,
                    "error",
                    f"{key_node.value} 不是一个存在的日期：{bad_value}。"
                    " 请检查月份和天数（例如 2 月没有 30 日）",
                    _snippet(lines, line),
                )
            )
    if invalid_dates:
        return issues + invalid_dates

    try:
        data = yaml.load(front, Loader=FrontMatterLoader)
    except yaml.constructor.ConstructorError as exc:
        mark = exc.problem_mark
        line = mark.line + 2 if mark else 2
        column = mark.column + 1 if mark else 1
        problem = exc.problem or "重复的字段"
        if "duplicate key" in str(problem):
            message = f"front matter 里有重复字段：{problem.split(':', 1)[-1].strip()}"
        else:
            message = f"YAML 构造错误：{problem}"
        return issues + [Issue(path, line, column, "error", message, _snippet(lines, line))]
    except ValueError as exc:
        # 兜底：上面已经提前检查过，理论上不会走到这里
        line = 2
        for index, text_line in enumerate(lines, start=1):
            if re.match(r"^(?:published|updated)\s*:", text_line):
                line = index
                break
        add(
            "error",
            line,
            1,
            f"日期不存在：{exc}。请检查月份和天数（例如 2 月没有 30 日）",
        )
        return issues
    except yaml.MarkedYAMLError as exc:
        return issues + [_yaml_error_issue(path, exc, lines, 2)]

    if not isinstance(data, dict):
        add("error", 2, 1, "front matter 必须是一组 key: value（映射）")
        return issues

    # 建立 字段名 -> 值节点 的映射，用于拿引号/类型/行号
    nodes: dict[object, yaml.Node] = {}
    key_nodes: dict[object, yaml.Node] = {}
    for key_node, value_node in root.value:
        if isinstance(key_node, yaml.ScalarNode):
            key = key_node.value
            nodes[key] = value_node
            key_nodes[key] = key_node

    def line_of(key: str, default: int = 2) -> tuple[int, int]:
        return _pos(nodes.get(key), default)

    def is_scalar(node: yaml.Node | None) -> bool:
        return isinstance(node, yaml.ScalarNode)

    def is_quoted_or_block(node: yaml.Node | None) -> bool:
        return is_scalar(node) and node.style in ("'", '"', "|", ">")

    # --- 未知字段 / 内部字段 -------------------------------------------
    for key in data:
        node = key_nodes.get(key)
        line, column = _pos(node, 2)
        if key in INTERNAL_KEYS:
            add(
                "warning",
                line,
                column,
                f'"{key}" 是 Fuwari 构建时自动写入的内部字段，手写通常没有意义',
            )
        elif key not in ALLOWED_KEYS:
            key_text = str(key)
            close = difflib.get_close_matches(key_text, ALLOWED_KEYS, n=1, cutoff=0.6)
            hint = f"，是不是想写 {close[0]}？" if close else ""
            add(
                "warning",
                line,
                column,
                f'未知字段 "{key_text}"{hint}（Astro 会直接忽略它）',
            )

    # --- title ----------------------------------------------------------
    if "title" not in data:
        add("error", 1, 1, "缺少必填字段 title，例如：title: 我的文章")
    else:
        node = nodes.get("title")
        value = data.get("title")
        line, column = line_of("title")
        if not (is_scalar(node) and _tag_name(node) == "str"):
            add(
                "error",
                line,
                column,
                f"title 必须是字符串，当前是{_type_name(node)}。"
                " 数字/布尔值会被 YAML 解析成别的类型",
            )
        elif not isinstance(value, str) or not value.strip():
            add("error", line, column, "title 不能为空")

    # --- 日期字段 -------------------------------------------------------
    def check_date(key: str, required: bool) -> dt.date | None:
        if key not in data:
            if required:
                add(
                    "error",
                    1,
                    1,
                    f"缺少必填字段 {key}，例如：{key}: {DATE_EXAMPLE}",
                )
            return None

        node = nodes.get(key)
        value = data.get(key)
        line, column = line_of(key)

        if not is_scalar(node):
            add(
                "error",
                line,
                column,
                f"{key} 必须是日期，当前是{_type_name(node)}",
            )
            return None

        if _tag_name(node) == "null":
            add(
                "error",
                line,
                column,
                f"{key} 不能为空，请写成 {key}: {DATE_EXAMPLE}",
            )
            return None

        if is_quoted_or_block(node):
            add(
                "error",
                line,
                column,
                f"{key} 不能加引号，也不要使用 | 或 > 块文本。"
                f" 直接写：{key}: {DATE_EXAMPLE}（Astro 需要 YAML 日期类型，"
                "加引号会变成字符串而校验失败）",
            )
            return None

        if node.tag != TIMESTAMP_TAG:
            raw_text = str(value)
            padding_hint = ""
            if DATE_PATTERN.match(raw_text):
                padding_hint = "。月份和日期都要写两位，不能写成 2026-8-9"
            add(
                "error",
                line,
                column,
                f"{key} 不是合法日期：{raw_text!r}。"
                f" 请写成 YYYY-MM-DD，例如 {DATE_EXAMPLE}{padding_hint}",
            )
            return None

        if isinstance(value, dt.datetime):
            return value.date()
        if isinstance(value, dt.date):
            return value
        return None

    published = check_date("published", required=True)
    updated = check_date("updated", required=False)

    if published and updated and updated < published:
        line, column = line_of("updated")
        add(
            "warning",
            line,
            column,
            f"updated（{updated.isoformat()}）早于 published（{published.isoformat()}），"
            "确认一下是不是写反了",
        )

    # --- draft ----------------------------------------------------------
    if "draft" in data:
        node = nodes.get("draft")
        line, column = line_of("draft")
        if not (is_scalar(node) and _tag_name(node) == "bool"):
            extra = ""
            if str(data.get("draft", "")).strip().lower() in {"yes", "no", "on", "off"}:
                extra = "；YAML 里 yes/no 也不是布尔值，请用 true/false"
            add(
                "error",
                line,
                column,
                f"draft 必须是布尔值 true 或 false（不要加引号），"
                f"当前是{_type_name(node)}{extra}",
            )

    # --- 字符串字段 -----------------------------------------------------
    def check_string(key: str, allow_empty: bool = True) -> str | None:
        if key not in data:
            return None
        node = nodes.get(key)
        value = data.get(key)
        line, column = line_of(key)
        if not (is_scalar(node) and _tag_name(node) == "str"):
            add(
                "error",
                line,
                column,
                f"{key} 必须是字符串，当前是{_type_name(node)}。"
                " 空值请写成 ''，不要留空",
            )
            return None
        if not allow_empty and (not isinstance(value, str) or not value.strip()):
            add("error", line, column, f"{key} 不能为空")
            return None
        return value if isinstance(value, str) else None

    description = check_string("description")
    description_node = nodes.get("description")
    if (
        description is not None
        and (description_node is None or description_node.style not in ("|", ">"))
        and description != description.strip()
    ):
        line, column = line_of("description")
        add(
            "warning",
            line,
            column,
            "description 首尾有空白，构建后可能出现多余空格",
        )

    image = check_string("image")
    if image:
        line, column = line_of("image")
        # 和 src/components/misc/ImageWrapper.astro 的 isLocal 判断保持一致
        is_local = not (
            image.startswith("/")
            or image.startswith("http")
            or image.startswith("https")
            or image.startswith("data:")
        )
        if is_local:
            target = (path.parent / image).resolve()
            if not target.exists():
                add(
                    "error",
                    line,
                    column,
                    f"封面图不存在：{(target.relative_to(REPO_ROOT).as_posix() if target.is_relative_to(REPO_ROOT) else target.as_posix())}。"
                    " 相对路径是相对于这篇文章所在目录的",
                )
            elif target.is_dir():
                add("error", line, column, f"封面图指向的是目录，不是图片：{image}")
        elif image.startswith("/"):
            public_target = (REPO_ROOT / "public" / image.lstrip("/")).resolve()
            if not public_target.exists():
                add(
                    "warning",
                    line,
                    column,
                    f"public 目录下找不到 {image}，部署后这张图会 404",
                )

    lang = check_string("lang")
    if lang and lang.strip() and lang not in KNOWN_LANGS:
        line, column = line_of("lang")
        add(
            "warning",
            line,
            column,
            f'lang "{lang}" 不在站点语言列表里（{", ".join(sorted(KNOWN_LANGS))}），'
            "页面文案可能回退到默认语言",
        )

    # --- tags -----------------------------------------------------------
    if "tags" in data:
        node = nodes.get("tags")
        line, column = line_of("tags")
        if not isinstance(node, yaml.SequenceNode):
            hint = ""
            if is_scalar(node) and _tag_name(node) == "str":
                hint = "。不要写成 tags: A, B，要写成 tags: [A, B] 或每行一个 - A"
            add(
                "error",
                line,
                column,
                f"tags 必须是 YAML 列表（数组），当前是{_type_name(node)}{hint}",
            )
        else:
            seen: set[str] = set()
            for item in node.value:
                item_line, item_column = _pos(item)
                if not (is_scalar(item) and _tag_name(item) == "str"):
                    add(
                        "error",
                        item_line,
                        item_column,
                        f"tags 的每一项都必须是字符串，当前是{_type_name(item)}",
                    )
                    continue
                tag_value = str(item.value)
                stripped = tag_value.strip()
                if not stripped:
                    add(
                        "error",
                        item_line,
                        item_column,
                        "tags 里不能有空字符串",
                    )
                    continue
                if stripped != tag_value:
                    add(
                        "warning",
                        item_line,
                        item_column,
                        f'标签 "{tag_value}" 首尾有空白，会被去掉',
                    )
                if stripped in seen:
                    add(
                        "warning",
                        item_line,
                        item_column,
                        f'标签 "{stripped}" 重复了',
                    )
                seen.add(stripped)

    # --- category -------------------------------------------------------
    if "category" in data:
        node = nodes.get("category")
        value = data.get("category")
        line, column = line_of("category")
        if _tag_name(node) == "null":
            pass  # schema 允许 null
        elif not (is_scalar(node) and _tag_name(node) == "str"):
            add(
                "error",
                line,
                column,
                f"category 必须是字符串，当前是{_type_name(node)}",
            )
        elif (
            isinstance(value, str)
            and (node is None or node.style not in ("|", ">"))
            and value != value.strip()
        ):
            add(
                "warning",
                line,
                column,
                f'category "{value}" 首尾有空白，分类页面会显示成带空格的名字',
            )

    # 按行号排序，同一行 error 在前
    issues.sort(key=lambda item: (item.line, item.column, item.level != "error", item.order))
    return issues


# ---------------------------------------------------------------------------
# 文件发现
# ---------------------------------------------------------------------------


def _expand_paths(raw_paths: list[str]) -> list[Path]:
    found: list[Path] = []
    for raw in raw_paths:
        candidate = Path(raw)
        if not candidate.is_absolute():
            candidate = (Path.cwd() / candidate).resolve()
        if candidate.is_dir():
            found.extend(sorted(candidate.rglob("*.md")))
        elif candidate.is_file():
            if candidate.suffix.lower() == ".md":
                found.append(candidate)
            else:
                print(f"跳过非 Markdown 文件：{raw}", file=sys.stderr)
        else:
            print(f"找不到路径：{raw}", file=sys.stderr)

    unique: list[Path] = []
    seen: set[Path] = set()
    for item in found:
        resolved = item.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(resolved)
    return unique


def _staged_files() -> tuple[list[Path], str | None]:
    try:
        completed = subprocess.run(
            [
                "git",
                "-c",
                "core.quotepath=false",
                "diff",
                "--cached",
                "--name-only",
                "-z",
                "--diff-filter=ACMR",
                "--",
                "*.md",
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except FileNotFoundError:
        return [], "找不到 git 命令，确认已经安装 Git 并加入 PATH"
    except OSError as exc:
        return [], f"调用 git 失败：{exc}"

    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        return [], f"git diff 执行失败（退出码 {completed.returncode}）：{detail}"

    files: list[Path] = []
    for relative in completed.stdout.split("\0"):
        if not relative:
            continue
        candidate = (REPO_ROOT / relative).resolve()
        if (
            candidate.suffix.lower() == ".md"
            and candidate.is_file()
            and candidate.is_relative_to(POSTS_DIR)
        ):
            files.append(candidate)

    unique = sorted(set(files))
    return unique, None


# ---------------------------------------------------------------------------
# 输出
# ---------------------------------------------------------------------------


def _relative(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def print_human(
    results: list[FileResult], stats: Stats, colors: Colors, strict: bool = False
) -> None:
    for result in results:
        if not result.issues:
            continue
        print()
        print(f"{colors.bold}{_relative(result.path)}{colors.reset}")
        for issue in result.issues:
            if issue.level == "error":
                label = f"{colors.red}ERROR{colors.reset}"
            else:
                label = f"{colors.yellow}WARN {colors.reset}"
            location = f"{issue.line}:{issue.column}"
            print(f"  {label}  {location:<7} {issue.message}")

            if issue.snippet is not None:
                snippet = issue.snippet
                if "\t" not in snippet:
                    width = len(str(issue.line))
                    print(f"  {colors.dim}{' ' * width} |{colors.reset} {snippet}")
                    caret_padding = " " * (max(issue.column - 1, 0))
                    print(
                        f"  {colors.dim}{' ' * width} |{colors.reset} "
                        f"{caret_padding}{colors.red if issue.level == 'error' else colors.yellow}^{colors.reset}"
                    )

    print()
    error_color = colors.red if stats.errors else colors.reset
    warning_color = colors.yellow if stats.warnings else colors.reset
    print(
        f"检查完成：{stats.checked} 个文件，"
        f"{error_color}{stats.errors} 个错误{colors.reset}，"
        f"{warning_color}{stats.warnings} 个警告{colors.reset}"
    )
    if stats.errors == 0 and stats.warnings == 0:
        print("[OK] 所有 front matter 都通过了检查")
    elif stats.errors == 0 and not strict:
        print("[OK] 没有会导致构建失败的问题")
    elif stats.errors == 0:
        print("[FAIL] --strict 模式下警告也算失败，请修正上面的问题")
    else:
        print("[FAIL] 请修正上面的错误后再提交")


def print_json(results: list[FileResult], stats: Stats) -> None:
    payload = {
        "checked": stats.checked,
        "errors": stats.errors,
        "warnings": stats.warnings,
        "files": [
            {
                "file": _relative(result.path),
                "issues": [
                    {
                        "level": issue.level,
                        "line": issue.line,
                        "column": issue.column,
                        "message": issue.message,
                    }
                    for issue in result.issues
                ],
            }
            for result in results
            if result.issues
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------------------
# 入口
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="推送前检查 Fuwari / Astro 文章的 front matter",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="要检查的文件或目录（默认检查 src/content/posts 下的全部 .md）",
    )
    parser.add_argument(
        "--staged",
        action="store_true",
        help="只检查 git 暂存区里的文章（适合配合 pre-commit）",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="把警告也视为失败（退出码 1）",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="输出 JSON，便于接入编辑器或其他脚本",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="禁用彩色输出",
    )
    args = parser.parse_args(argv)

    if args.staged and args.paths:
        parser.error("--staged 不能同时指定 paths")

    colors = Colors(
        enabled=(
            not args.no_color
            and not args.json
            and sys.stdout.isatty()
            and os.environ.get("NO_COLOR") is None
            and os.environ.get("TERM") != "dumb"
        )
    )

    if args.staged:
        files, error = _staged_files()
        if error:
            print(f"[FAIL] {error}", file=sys.stderr)
            return 2
        if not files:
            print("暂存区里没有 src/content/posts 下的 Markdown 文件，跳过检查。")
            return 0
    elif args.paths:
        files = _expand_paths(args.paths)
        if not files:
            print("没有找到需要检查的 Markdown 文件。", file=sys.stderr)
            return 2
    else:
        if not POSTS_DIR.is_dir():
            print(f"[FAIL] 找不到文章目录：{POSTS_DIR}", file=sys.stderr)
            return 2
        files = sorted(POSTS_DIR.rglob("*.md"))

    results: list[FileResult] = []
    stats = Stats()
    for path in files:
        try:
            issues = check_file(path)
        except Exception as exc:  # 不让单个文件拖垮整次检查
            issues = [
                Issue(
                    path,
                    1,
                    1,
                    "error",
                    f"检查脚本内部错误：{type(exc).__name__}: {exc}",
                )
            ]
        stats.checked += 1
        stats.errors += sum(1 for issue in issues if issue.level == "error")
        stats.warnings += sum(1 for issue in issues if issue.level == "warning")
        results.append(FileResult(path, issues))

    results.sort(key=lambda result: _relative(result.path))

    if args.json:
        print_json(results, stats)
    else:
        print_human(results, stats, colors, strict=args.strict)

    failed = stats.errors > 0 or (args.strict and stats.warnings > 0)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
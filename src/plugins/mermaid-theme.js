/**
 * Mermaid 主题桥接层。
 *
 * 背景：mermaid 的 themeVariables 只接受十六进制颜色（其内部色彩引擎无法解析
 * oklch()，也无法解析 CSS 变量），而 Fuwari 的配色全部是 `oklch(... var(--hue))`
 * 且会在运行时随主题色选择器改变。因此颜色不能写死在 themeVariables 里。
 *
 * 做法：themeVariables 只提供一份接近的 hex 兜底值（保证 mermaid 自己派生不出
 * 离谱的颜色），真正的颜色全部由下面的 themeCSS 用 `var(--mmd-*)` 覆盖。
 * themeCSS 会被 mermaid 注入到图内联 SVG 的 <style> 中（选择器自动加 #id 前缀），
 * 而内联 SVG 继承页面的自定义属性，所以：
 *   - 切换浅色/深色（:root.dark）时浏览器自动重算，无需重新渲染；
 *   - 用户更换主题色（--hue）时图表跟着变。
 *
 * --mmd-* 这组 token 定义在 src/styles/main.css。
 */

/** themeVariables 兜底色（浅色模式，主题色 hue=320 时的近似值）。 */
export const mermaidThemeVariables = {
	darkMode: false,
	background: '#ffffff',
	primaryColor: '#c480d4',
	primaryTextColor: '#1c1c22',
	primaryBorderColor: '#c480d4',
	secondaryColor: '#f2e6f6',
	tertiaryColor: '#faf8ff',
	lineColor: '#6b7280',
	textColor: '#1c1c22',
	fontFamily: 'inherit',
	fontSize: '13px',
};

/** 用博客 CSS 变量覆盖 mermaid 内置主题。 */
export const mermaidThemeCSS = `
svg { background: transparent !important; }
text, .label, .nodeLabel, .messageText, .labelText { font-family: inherit !important; }

/* ── 节点：flowchart / state / class / sequence actor / note ───────────── */
.node rect, .node circle, .node ellipse, .node polygon, .node path,
.label-container, .actor, .note, .activation0, .activation1, .activation2,
.classGroup rect, .stateGroup rect, .statediagram-cluster rect {
	fill: var(--mmd-node-bg) !important;
	stroke: var(--mmd-node-border) !important;
	stroke-width: 1.2px !important;
}
.node rect, .label-container, .actor, .note, .classGroup rect {
	rx: 9px !important;
	ry: 9px !important;
}

/* ── 节点文字 ──────────────────────────────────────────────────────────── */
.nodeLabel, .nodeLabel p, .label, .edgeLabel, .edgeLabel p,
.messageText, .loopText, .labelText, .noteText,
.classTitle, .classText, .stateLabel, .state-title, .state-description,
text.actor, .actor > text, .actor > tspan, .legend text {
	color: var(--mmd-label) !important;
	fill: var(--mmd-label) !important;
	font-family: inherit !important;
	font-size: 13px !important;
	font-weight: 500 !important;
}
.classTitle { font-weight: 600 !important; }

/* ── 分组 / 泳道 / 状态容器 ────────────────────────────────────────────── */
.cluster rect, .statediagram-cluster rect, .statediagram-cluster.statediagram-cluster-alt rect {
	fill: var(--mmd-cluster-bg) !important;
	stroke: var(--mmd-cluster-border) !important;
	stroke-width: 1px !important;
	rx: 12px !important;
	ry: 12px !important;
}
.cluster span, .cluster-label span, .cluster-label p, .cluster-label div,
.cluster text, .statediagram-cluster rect + text {
	color: var(--mmd-muted) !important;
	fill: var(--mmd-muted) !important;
	font-size: 12px !important;
	font-weight: 500 !important;
	font-family: inherit !important;
}

/* ── 连线 / 箭头 ───────────────────────────────────────────────────────── */
.flowchart-link, .edgePath .path, path.relation, g.relation path,
.transition, .messageLine0, .messageLine1, .loopLine, .actor-line,
.statediagram-cluster rect + path {
	stroke: var(--mmd-line) !important;
	stroke-width: 1.4px !important;
}
.edgePath .path.arrowheadPath, .arrowheadPath,
marker path, marker polygon, marker circle {
	fill: var(--mmd-line) !important;
	stroke: var(--mmd-line) !important;
}

/* ── 连线上的标签底色 ──────────────────────────────────────────────────── */
.edgeLabel, .edgeLabel rect, .edgeLabel .labelBkg, .labelBkg {
	fill: var(--card-bg) !important;
	background: var(--card-bg) !important;
}

/* ── 图表标题 / 饼图 ───────────────────────────────────────────────────── */
.titleText, .pieTitleText {
	fill: var(--mmd-label) !important;
	font-family: inherit !important;
	font-size: 14px !important;
	font-weight: 600 !important;
}
.pieOuterCircle, .pieCircle + .pieOuterCircle {
	stroke: var(--mmd-node-border) !important;
}
`;
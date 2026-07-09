import json
import base64
import mimetypes
import posixpath
import shutil
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


APP_PORT = 8765
DEFAULT_ROOT = Path(r"C:\Users\35160\Desktop\中医古今书籍10200册\中医古今书籍10200册")
IGNORE_DIR_NAMES = {".git", ".venv", "__pycache__"}
REMOVED_PREFIX = "_removed_selection_"
EXPORT_MD_NAME = "knowledge_selection.md"
EXPORT_JSON_NAME = "directory_snapshot.json"
TEXT_PREVIEW_LIMIT = 16000
IMAGE_PREVIEW_LIMIT = 8 * 1024 * 1024
TEXT_EXTENSIONS = {
    ".txt", ".md", ".markdown", ".csv", ".tsv", ".json", ".yaml", ".yml",
    ".xml", ".html", ".htm", ".css", ".js", ".py", ".bat", ".ps1", ".log"
}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}


INDEX_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>知识库目录工作流整理器</title>
<style>
:root {
  --bg:#f4f6fb;
  --panel:#ffffff;
  --ink:#1f2937;
  --muted:#667085;
  --line:#d8dee9;
  --soft:#eef4ff;
  --accent:#1456d9;
  --accent-2:#0f766e;
  --danger:#b42318;
  --warn:#a15c00;
  --shadow:0 10px 30px rgba(31,41,55,.08);
  font-family:"Microsoft YaHei","PingFang SC","Noto Sans SC",sans-serif;
}
* { box-sizing:border-box; }
body { margin:0; background:linear-gradient(180deg,#f8fbff 0%, #f4f6fb 100%); color:var(--ink); }
header {
  position:sticky; top:0; z-index:5;
  padding:16px 22px;
  color:#fff;
  background:linear-gradient(135deg,#0f172a 0%, #1d4ed8 100%);
  box-shadow:var(--shadow);
}
h1 { margin:0; font-size:20px; font-weight:700; letter-spacing:0; }
.sub { margin-top:6px; color:#dbeafe; font-size:13px; line-height:1.5; }
main {
  max-width:1380px;
  margin:0 auto;
  padding:16px;
  display:grid;
  grid-template-columns:1fr 360px;
  gap:16px;
}
.bar, .panel {
  background:var(--panel);
  border:1px solid var(--line);
  border-radius:8px;
  box-shadow:var(--shadow);
}
.bar {
  grid-column:1 / -1;
  padding:12px;
  display:flex;
  gap:10px;
  flex-wrap:wrap;
  align-items:center;
}
input[type="text"], textarea, select {
  border:1px solid var(--line);
  border-radius:6px;
  padding:10px 12px;
  font-size:14px;
  background:#fff;
  color:var(--ink);
}
#rootPath { flex:1; min-width:360px; }
#search { width:240px; }
#planTarget { width:180px; }
button {
  border:1px solid var(--line);
  background:#fff;
  color:var(--ink);
  border-radius:6px;
  padding:9px 12px;
  cursor:pointer;
  font-size:14px;
}
button.primary { background:var(--accent); color:#fff; border-color:var(--accent); }
button.secondary { background:var(--accent-2); color:#fff; border-color:var(--accent-2); }
button.danger { background:var(--danger); color:#fff; border-color:var(--danger); }
button.warn { background:var(--warn); color:#fff; border-color:var(--warn); }
button:hover { filter:brightness(.98); transform:translateY(-1px); }
mark {
  background:#fde68a;
  color:#78350f;
  border-radius:3px;
  padding:0 2px;
}
.tree { padding:10px 0 16px; max-height:calc(100vh - 188px); overflow:auto; user-select:none; }
.tree-wrap { position:relative; min-width:0; }
.selection-box {
  display:none;
  position:fixed;
  z-index:20;
  border:1px solid #2563eb;
  background:rgba(37,99,235,.12);
  pointer-events:none;
  border-radius:4px;
}
.selection-box.active { display:block; }
.row {
  display:flex;
  align-items:center;
  gap:7px;
  min-height:30px;
  padding:3px 10px;
  border-radius:6px;
  margin:0 8px;
}
.row:hover { background:var(--soft); }
.row.active { background:#dbeafe; }
.row.box-hit { background:#e0f2fe; outline:1px solid #38bdf8; }
.indent { display:inline-block; flex:0 0 auto; }
.twisty {
  width:20px; height:20px;
  border:0; padding:0;
  background:transparent;
  color:var(--muted);
  font-size:12px;
}
.twisty.blank { visibility:hidden; }
input[type="checkbox"] { width:16px; height:16px; accent-color:var(--accent); }
.name { white-space:nowrap; cursor:pointer; }
.name:hover { color:var(--accent); text-decoration:underline; text-underline-offset:3px; }
.folder { font-weight:600; }
.badge {
  font-size:11px;
  color:var(--muted);
  border:1px solid var(--line);
  border-radius:999px;
  padding:1px 6px;
  background:#fff;
}
.path {
  color:var(--muted);
  font-size:12px;
  margin-left:6px;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
}
.side {
  padding:14px;
  position:sticky;
  top:82px;
  max-height:calc(100vh - 100px);
  overflow:auto;
}
.side h2 { margin:0 0 10px; font-size:16px; }
.side-head {
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:10px;
  margin-top:14px;
}
.side-head h2 { margin:0; }
.mini {
  padding:5px 8px;
  font-size:12px;
  border-radius:5px;
}
.stat {
  display:grid;
  grid-template-columns:1fr auto;
  gap:8px;
  padding:8px 0;
  border-bottom:1px solid var(--line);
  font-size:13px;
}
.preview {
  margin-top:12px;
  background:#0f172a;
  color:#e5e7eb;
  border-radius:8px;
  padding:12px;
  min-height:220px;
  max-height:340px;
  overflow:auto;
  white-space:pre-wrap;
  font-family:Consolas,"Courier New",monospace;
  font-size:12px;
  line-height:1.55;
}
.file-preview {
  margin-top:12px;
  border:1px solid var(--line);
  border-radius:8px;
  background:#fbfdff;
  overflow:hidden;
}
.file-preview.collapsed { display:none; }
.file-preview-title {
  padding:10px 12px;
  border-bottom:1px solid var(--line);
  font-size:13px;
  font-weight:700;
}
.file-preview-body {
  padding:12px;
  min-height:160px;
  max-height:340px;
  overflow:auto;
  font-size:12px;
  line-height:1.65;
  white-space:pre-wrap;
}
.file-preview-body pre {
  margin:0;
  white-space:pre-wrap;
  font-family:Consolas,"Courier New",monospace;
}
.file-preview-body img {
  display:block;
  max-width:100%;
  border-radius:6px;
  border:1px solid var(--line);
}
.plan-box {
  margin-top:12px;
  padding:10px;
  border:1px solid var(--line);
  border-radius:8px;
  background:#fff;
}
.plan-row {
  display:flex;
  gap:8px;
  margin-top:8px;
  flex-wrap:wrap;
}
.operation-log {
  margin-top:10px;
  max-height:150px;
  overflow:auto;
  padding-left:18px;
  color:var(--muted);
  font-size:12px;
  line-height:1.6;
}
.plan-preview {
  margin-top:10px;
  padding:10px;
  border:1px solid #dbeafe;
  border-radius:8px;
  background:#eff6ff;
  color:#1e3a8a;
  font-size:12px;
  line-height:1.6;
  max-height:160px;
  overflow:auto;
  white-space:pre-wrap;
}
.note {
  color:var(--muted);
  font-size:12px;
  line-height:1.7;
  margin-top:10px;
}
.status {
  grid-column:1 / -1;
  font-size:13px;
  color:var(--muted);
  padding-left:2px;
}
.tips {
  margin-top:12px;
  padding:10px 12px;
  border:1px dashed var(--line);
  border-radius:8px;
  background:#fbfdff;
  font-size:12px;
  color:var(--muted);
  line-height:1.7;
}
@media (max-width:980px) {
  main { grid-template-columns:1fr; }
  .side { position:static; max-height:none; }
  .tree { max-height:none; }
}
</style>
</head>
<body>
<header>
  <h1>知识库目录工作流整理器</h1>
  <div class="sub">先生成目录快照发给别人筛选，再把导出的清单带回本机执行保留/排除。当前工具也支持直接在本机筛选。</div>
</header>
<main>
  <section class="bar">
    <input id="rootPath" type="text" placeholder="输入要扫描的目录路径">
    <button id="pickFolder" class="primary">选择文件夹</button>
    <button id="load" class="primary">加载目录</button>
    <input id="search" type="text" placeholder="搜索文件或路径">
    <button id="selectAll">全选</button>
    <button id="clearAll">清空</button>
    <button id="undoSelection">撤销选择</button>
    <button id="redoSelection">重做选择</button>
    <button id="expandAll">展开</button>
    <button id="collapseAll">折叠</button>
    <button id="exportMd">导出 MD 清单</button>
    <button id="exportSnapshot" class="secondary">导出快照 JSON</button>
    <button id="importSnapshot">导入快照 JSON</button>
    <button id="exportBatch">导出整理 BAT</button>
    <button id="moveSelected" class="warn">把所选移出知识库</button>
    <button id="applyKeepList" class="danger">按 MD 清单自动保留</button>
    <input id="snapshotFile" type="file" accept=".json" style="display:none">
    <div id="status" class="status">等待加载目录。</div>
  </section>
  <section class="tree-wrap">
    <div id="selectionBox" class="selection-box"></div>
    <div class="panel tree" id="tree"></div>
  </section>
  <aside class="panel side">
    <div class="side-head">
      <h2>当前选择</h2>
      <button id="toggleFilePreview" class="mini">收起预览</button>
    </div>
    <div class="stat"><span>已选目录</span><strong id="dirCount">0</strong></div>
    <div class="stat"><span>已选文件</span><strong id="fileCount">0</strong></div>
    <div class="stat"><span>估算大小</span><strong id="sizeCount">0 KB</strong></div>
    <div class="stat"><span>当前模式</span><strong id="modeLabel">本机扫描</strong></div>
    <div class="stat"><span>工作流输出</span><strong id="exportName">knowledge_selection.md</strong></div>
    <div class="note">默认勾选的是“不需要进入知识库”的内容。你可以导出给别人做筛选，也可以在自己的机器上按清单自动保留需要的文件。</div>
    <div id="filePreviewWrap" class="file-preview">
      <div id="filePreviewTitle" class="file-preview-title">文件预览</div>
      <div id="filePreviewBody" class="file-preview-body">点击文件名或目录名，可在这里快速查看内容摘要。图片会显示缩略图，文本会显示前若干字符。</div>
    </div>
    <div class="plan-box">
      <strong>计划整理操作</strong>
      <div class="note">这里先只记录目录层面的整理动作，不立刻改动文件。确认后可导出 BAT，在本机运行执行。</div>
      <div class="plan-row">
        <input id="planTarget" type="text" placeholder="目标文件夹，如：待删除">
        <button id="recordMkdir">记录新建</button>
        <button id="recordMove">记录移动所选</button>
        <button id="undoOperation">撤销一步</button>
        <button id="redoOperation">重做一步</button>
        <button id="previewPlan">预演计划</button>
      </div>
      <ol id="operationLog" class="operation-log"></ol>
      <div id="planPreview" class="plan-preview">尚未生成预演。点击“预演计划”可查看即将新建和移动的项目。</div>
    </div>
    <div class="side-head">
      <h2>MD 导出预览</h2>
    </div>
    <pre class="preview" id="preview"></pre>
    <div class="tips">
      快捷操作：<br>
      - 单击：切换当前项<br>
      - Shift + 单击：范围连续选择<br>
      - Ctrl + 单击：跳过父子联动，仅反转当前项<br>
      - Alt + 单击目录名：仅展开/折叠<br>
      - 支持按住鼠标拖动经过多行连续勾选，靠近列表边缘会自动滚动<br>
      - Ctrl + 拖动：逐项反选，适合跳过或快速纠错<br>
      - 空白区域拖出矩形：框选可见行；Shift 框选追加，Ctrl 框选反选<br>
      - Alt + 拖动任意行：也可启动矩形框选，适合列表铺满屏幕时使用
    </div>
  </aside>
</main>
<script>
let rootPath = "";
let treeData = null;
let flat = [];
let byPath = new Map();
let state = new Map();
let collapsed = new Set();
let selectionOrder = [];
let lastClickedPath = null;
let dragMode = null;
let dragValue = null;
let dragSeen = new Set();
let dragScrollTimer = null;
let dragScrollSpeed = 0;
let lastMousePoint = { x:0, y:0 };
let currentMode = "scan";
let operations = [];
let operationRedoStack = [];
let filePreviewCollapsed = false;
let selectionUndoStack = [];
let selectionRedoStack = [];
let isRestoringSelection = false;
let boxSelect = null;

const DEFAULT_ROOT = __DEFAULT_ROOT__;
document.getElementById("rootPath").value = DEFAULT_ROOT;

function setStatus(text, ok=false) {
  const el = document.getElementById("status");
  el.textContent = text;
  el.style.color = ok ? "#047857" : "#667085";
}

function captureSelectionSnapshot() {
  return {
    checked: Array.from(state.entries()).filter(([, checked]) => checked === true).map(([path]) => path),
    indeterminate: flat.filter(node => node._indeterminate).map(node => node.path)
  };
}

function restoreSelectionSnapshot(snapshot) {
  const checked = new Set(snapshot.checked || []);
  const indeterminate = new Set(snapshot.indeterminate || []);
  isRestoringSelection = true;
  flat.forEach(node => {
    state.set(node.path, checked.has(node.path));
    node._indeterminate = indeterminate.has(node.path);
  });
  isRestoringSelection = false;
  render();
  updatePreview();
}

function withSelectionHistory(action, label="选择操作") {
  if (!treeData || isRestoringSelection) return action();
  const before = captureSelectionSnapshot();
  action();
  const after = captureSelectionSnapshot();
  if (JSON.stringify(before) !== JSON.stringify(after)) {
    selectionUndoStack.push({ before, after, label });
    if (selectionUndoStack.length > 80) selectionUndoStack.shift();
    selectionRedoStack = [];
  }
}

function undoSelection() {
  const item = selectionUndoStack.pop();
  if (!item) {
    setStatus("暂无可撤销的选择操作。");
    return;
  }
  selectionRedoStack.push(item);
  restoreSelectionSnapshot(item.before);
  setStatus("已撤销选择：" + item.label, true);
}

function redoSelection() {
  const item = selectionRedoStack.pop();
  if (!item) {
    setStatus("暂无可重做的选择操作。");
    return;
  }
  selectionUndoStack.push(item);
  restoreSelectionSnapshot(item.after);
  setStatus("已重做选择：" + item.label, true);
}

function setMode(modeText) {
  document.getElementById("modeLabel").textContent = modeText;
}

function escapeHtml(text) {
  return String(text).replace(/[&<>"']/g, ch => ({
    "&":"&amp;",
    "<":"&lt;",
    ">":"&gt;",
    '"':"&quot;",
    "'":"&#39;"
  }[ch]));
}

function escapeRegExp(text) {
  return String(text).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function highlightText(text, term) {
  const safe = escapeHtml(text);
  if (!term) return safe;
  const pattern = new RegExp("(" + escapeRegExp(term) + ")", "ig");
  return safe.replace(pattern, "<mark>$1</mark>");
}

function formatSize(bytes) {
  if (!bytes) return "0 KB";
  const units = ["B","KB","MB","GB","TB"];
  let n = bytes, i = 0;
  while (n >= 1024 && i < units.length - 1) { n /= 1024; i++; }
  return (i === 0 ? n : n.toFixed(1)) + " " + units[i];
}

function walk(node, parent=null, depth=0) {
  node.parent = parent;
  node.depth = depth;
  node._indeterminate = false;
  flat.push(node);
  byPath.set(node.path, node);
  state.set(node.path, false);
  (node.children || []).forEach(child => walk(child, node, depth + 1));
}

function resetData(data, modeText="本机扫描") {
  treeData = data;
  rootPath = data.root;
  flat = [];
  byPath = new Map();
  state = new Map();
  collapsed = new Set();
  selectionOrder = [];
  lastClickedPath = null;
  operations = [];
  operationRedoStack = [];
  selectionUndoStack = [];
  selectionRedoStack = [];
  walk(treeData);
  document.getElementById("rootPath").value = rootPath;
  setMode(modeText);
  render();
  updatePreview();
  updateOperationLog();
}

function descendants(node) {
  const list = [];
  (node.children || []).forEach(child => { list.push(child); list.push(...descendants(child)); });
  return list;
}

function isIndeterminate(node) { return !!node._indeterminate; }

function setNode(node, checked) {
  state.set(node.path, checked);
  descendants(node).forEach(child => {
    state.set(child.path, checked);
    child._indeterminate = false;
  });
  updateParents(node.parent);
}

function setNodeOnly(node, checked) {
  state.set(node.path, checked);
  node._indeterminate = false;
  updateParents(node.parent);
}

function updateParents(node) {
  while (node) {
    const children = node.children || [];
    if (!children.length) {
      node = node.parent;
      continue;
    }
    const all = children.every(child => state.get(child.path) === true && !isIndeterminate(child));
    const any = children.some(child => state.get(child.path) === true || isIndeterminate(child));
    state.set(node.path, all);
    node._indeterminate = any && !all;
    node = node.parent;
  }
}

function isVisible(node, term) {
  if (!term) return true;
  const hay = (node.name + " " + node.path).toLowerCase();
  if (hay.includes(term)) return true;
  return (node.children || []).some(child => isVisible(child, term));
}

function visibleRows() {
  const term = document.getElementById("search").value.trim().toLowerCase();
  return flat.filter(node => {
    if (node.path === ".") return false;
    if (!isVisible(node, term)) return false;
    if (!term) {
      let ancestor = node.parent;
      while (ancestor && ancestor.path !== ".") {
        if (collapsed.has(ancestor.path)) return false;
        ancestor = ancestor.parent;
      }
    }
    return true;
  });
}

function toggleNode(node, event, checkedOverride=null) {
  if (!isRestoringSelection) {
    return withSelectionHistory(() => toggleNodeRaw(node, event, checkedOverride), "切换选择");
  }
  return toggleNodeRaw(node, event, checkedOverride);
}

function toggleNodeRaw(node, event, checkedOverride=null) {
  const checked = checkedOverride === null ? !(state.get(node.path) === true) : checkedOverride;
  if (event && event.altKey && node.type === "dir") {
    collapsed.has(node.path) ? collapsed.delete(node.path) : collapsed.add(node.path);
    render();
    return;
  }
  if (event && event.shiftKey && lastClickedPath && byPath.has(lastClickedPath)) {
    const rows = visibleRows();
    const start = rows.findIndex(n => n.path === lastClickedPath);
    const end = rows.findIndex(n => n.path === node.path);
    if (start !== -1 && end !== -1) {
      const lo = Math.min(start, end);
      const hi = Math.max(start, end);
      rows.slice(lo, hi + 1).forEach(item => setNodeOnly(item, checked));
      rows.slice(lo, hi + 1).forEach(item => updateParents(item.parent));
      lastClickedPath = node.path;
      render();
      updatePreview();
      return;
    }
  }
  if (event && event.ctrlKey) {
    setNodeOnly(node, checked);
  } else {
    setNode(node, checked);
  }
  lastClickedPath = node.path;
  render();
  updatePreview();
}

function render() {
  const box = document.getElementById("tree");
  box.innerHTML = "";
  if (!treeData) return;
  const rawTerm = document.getElementById("search").value.trim();
  visibleRows().forEach(node => {
    const row = document.createElement("div");
    row.className = "row";
    row.dataset.path = node.path;
    const indent = document.createElement("span");
    indent.className = "indent";
    indent.style.width = (node.depth * 20) + "px";
    row.appendChild(indent);

    const twisty = document.createElement("button");
    twisty.className = "twisty" + (node.type === "dir" ? "" : " blank");
    twisty.textContent = node.type === "dir" ? (collapsed.has(node.path) ? "▶" : "▼") : "·";
    twisty.onclick = e => { e.stopPropagation(); collapsed.has(node.path) ? collapsed.delete(node.path) : collapsed.add(node.path); render(); };
    row.appendChild(twisty);

    const cb = document.createElement("input");
    cb.type = "checkbox";
    cb.checked = state.get(node.path) === true;
    cb.indeterminate = isIndeterminate(node);
    cb.onchange = e => toggleNode(node, e, cb.checked);
    row.appendChild(cb);

    const name = document.createElement("span");
    name.className = "name previewable " + (node.type === "dir" ? "folder" : "file");
    name.innerHTML = escapeHtml(node.type === "dir" ? "📁 " : "📄 ") + highlightText(node.name, rawTerm);
    name.title = "点击预览，勾选框用于选择";
    name.onclick = e => { e.stopPropagation(); loadNodePreview(node); };
    row.appendChild(name);

    const badge = document.createElement("span");
    badge.className = "badge";
    badge.textContent = node.type === "dir" ? (node.children || []).length + "项" : formatSize(node.size || 0);
    row.appendChild(badge);

    const path = document.createElement("span");
    path.className = "path";
    path.innerHTML = highlightText(node.path, rawTerm);
    path.title = "点击预览";
    path.onclick = e => { e.stopPropagation(); loadNodePreview(node); };
    row.appendChild(path);

    row.onmousedown = e => {
      if (e.button !== 0) return;
      if (e.target.closest("button,input,.previewable")) return;
      if (e.altKey) return;
      dragMode = e.ctrlKey ? "invert" : "paint";
      dragValue = !(state.get(node.path) === true);
      dragSeen = new Set();
      applyDragNode(node);
    };
    row.onmouseenter = e => {
      if (dragMode) applyDragNode(node);
    };
    box.appendChild(row);
  });
}

function applyDragNode(node) {
  if (!node || dragSeen.has(node.path)) return;
  dragSeen.add(node.path);
  if (dragMode === "invert") {
    toggleNode(node, { ctrlKey: true }, !(state.get(node.path) === true));
  } else if (dragMode === "paint") {
    toggleNode(node, { ctrlKey: true }, dragValue);
  }
}

function rectsIntersect(a, b) {
  return !(a.right < b.left || a.left > b.right || a.bottom < b.top || a.top > b.bottom);
}

function updateSelectionBoxVisual() {
  const box = document.getElementById("selectionBox");
  if (!boxSelect || !box) return;
  const left = Math.min(boxSelect.startX, boxSelect.currentX);
  const top = Math.min(boxSelect.startY, boxSelect.currentY);
  const width = Math.abs(boxSelect.currentX - boxSelect.startX);
  const height = Math.abs(boxSelect.currentY - boxSelect.startY);
  box.classList.add("active");
  box.style.left = left + "px";
  box.style.top = top + "px";
  box.style.width = width + "px";
  box.style.height = height + "px";
}

function applyBoxSelectionPreview() {
  if (!boxSelect) return;
  updateSelectionBoxVisual();
  const rect = {
    left: Math.min(boxSelect.startX, boxSelect.currentX),
    right: Math.max(boxSelect.startX, boxSelect.currentX),
    top: Math.min(boxSelect.startY, boxSelect.currentY),
    bottom: Math.max(boxSelect.startY, boxSelect.currentY)
  };
  document.querySelectorAll(".row.box-hit").forEach(row => row.classList.remove("box-hit"));
  boxSelect.paths = [];
  document.querySelectorAll(".row").forEach(row => {
    if (rectsIntersect(rect, row.getBoundingClientRect())) {
      row.classList.add("box-hit");
      if (row.dataset.path) boxSelect.paths.push(row.dataset.path);
    }
  });
}

function startBoxSelection(event) {
  if (event.button !== 0) return;
  if (event.target.closest("button,input,textarea,select")) return;
  if (event.target.closest(".row") && !event.altKey) return;
  boxSelect = {
    startX: event.clientX,
    startY: event.clientY,
    currentX: event.clientX,
    currentY: event.clientY,
    mode: event.ctrlKey ? "invert" : (event.shiftKey ? "add" : "replace"),
    paths: []
  };
  event.preventDefault();
  applyBoxSelectionPreview();
}

function moveBoxSelection(event) {
  if (!boxSelect) return;
  boxSelect.currentX = event.clientX;
  boxSelect.currentY = event.clientY;
  applyBoxSelectionPreview();
}

function finishBoxSelection() {
  if (!boxSelect) return;
  const selectedPaths = Array.from(new Set(boxSelect.paths || []));
  const mode = boxSelect.mode;
  const label = `框选 ${selectedPaths.length} 项`;
  document.getElementById("selectionBox").classList.remove("active");
  document.querySelectorAll(".row.box-hit").forEach(row => row.classList.remove("box-hit"));
  boxSelect = null;
  if (!selectedPaths.length) return;
  withSelectionHistory(() => {
    if (mode === "replace") {
      flat.forEach(node => { state.set(node.path, false); node._indeterminate = false; });
    }
    selectedPaths.forEach(path => {
      const node = byPath.get(path);
      if (!node) return;
      const checked = mode === "invert" ? !(state.get(node.path) === true) : true;
      setNodeOnly(node, checked);
    });
    selectedPaths.forEach(path => {
      const node = byPath.get(path);
      if (node) updateParents(node.parent);
    });
    render();
    updatePreview();
  }, label);
}

function updateDragAutoScroll(event) {
  if (!dragMode) return;
  lastMousePoint = { x:event.clientX, y:event.clientY };
  const tree = document.getElementById("tree");
  const rect = tree.getBoundingClientRect();
  const edge = 64;
  if (event.clientY < rect.top + edge) {
    dragScrollSpeed = -18;
  } else if (event.clientY > rect.bottom - edge) {
    dragScrollSpeed = 18;
  } else {
    dragScrollSpeed = 0;
  }
  if (!dragScrollTimer) {
    dragScrollTimer = setInterval(() => {
      if (!dragMode || dragScrollSpeed === 0) return;
      tree.scrollTop += dragScrollSpeed;
      const element = document.elementFromPoint(lastMousePoint.x, lastMousePoint.y);
      const row = element ? element.closest(".row") : null;
      if (row && row.dataset.path && byPath.has(row.dataset.path)) {
        applyDragNode(byPath.get(row.dataset.path));
      }
    }, 45);
  }
}

document.addEventListener("mouseup", () => {
  dragMode = null;
  dragValue = null;
  dragSeen = new Set();
  dragScrollSpeed = 0;
  if (dragScrollTimer) {
    clearInterval(dragScrollTimer);
    dragScrollTimer = null;
  }
  finishBoxSelection();
});
document.addEventListener("mousemove", updateDragAutoScroll);
document.addEventListener("mousemove", moveBoxSelection);

function selectedNodes() {
  return flat.filter(node => node.path !== "." && state.get(node.path) === true && !isIndeterminate(node));
}

function selectedFiles() {
  return flat.filter(node => node.type === "file" && state.get(node.path) === true);
}

function buildMarkdown() {
  const files = selectedFiles();
  const dirs = selectedNodes().filter(n => n.type === "dir");
  const size = files.reduce((sum, n) => sum + (n.size || 0), 0);
  const selectedSet = new Set(selectedNodes().map(n => n.path));
  let md = "# 知识库文件清单\n\n";
  md += `生成时间：${new Date().toLocaleString("zh-CN")}\n\n`;
  md += `扫描根目录：${rootPath}\n\n`;
  md += `已选目录：${dirs.length} 个\n\n`;
  md += `已选文件：${files.length} 个\n\n`;
  md += `估算大小：${formatSize(size)}\n\n`;
  md += "## 分级目录\n\n";
  flat.forEach(node => {
    if (node.path === "." || !selectedSet.has(node.path)) return;
    const prefix = "  ".repeat(Math.max(0, node.depth - 1));
    const mark = node.type === "dir" ? "- [目录]" : "- [文件]";
    const extra = node.type === "file" ? ` (${formatSize(node.size || 0)})` : "";
    md += `${prefix}${mark} ${node.name}${extra}\n`;
  });
  md += "\n## 文件路径清单\n\n";
  files.forEach(node => { md += `- ${node.path}\n`; });
  return md;
}

function updatePreview() {
  const files = selectedFiles();
  const dirs = selectedNodes().filter(n => n.type === "dir");
  const size = files.reduce((sum, n) => sum + (n.size || 0), 0);
  document.getElementById("dirCount").textContent = dirs.length;
  document.getElementById("fileCount").textContent = files.length;
  document.getElementById("sizeCount").textContent = formatSize(size);
  document.getElementById("preview").textContent = buildMarkdown();
}

async function pickFolder() {
  setStatus("正在打开系统文件夹选择窗口...");
  try {
    const currentPath = document.getElementById("rootPath").value.trim();
    const res = await fetch("/api/pick-folder?path=" + encodeURIComponent(currentPath));
    const data = await res.json();
    if (!res.ok) {
      setStatus(data.error || "选择文件夹失败，请手动输入路径。");
      return;
    }
    if (!data.path) {
      setStatus("已取消选择文件夹。");
      return;
    }
    document.getElementById("rootPath").value = data.path;
    await loadTree();
  } catch (err) {
    setStatus("选择文件夹失败：" + err.message);
  }
}

async function loadNodePreview(node) {
  if (!node) return;
  const wrap = document.getElementById("filePreviewWrap");
  wrap.classList.remove("collapsed");
  filePreviewCollapsed = false;
  document.getElementById("toggleFilePreview").textContent = "收起预览";
  document.getElementById("filePreviewTitle").textContent = "预览：" + node.name;
  document.getElementById("filePreviewBody").textContent = "正在读取预览...";
  try {
    const url = "/api/preview?root=" + encodeURIComponent(rootPath) + "&path=" + encodeURIComponent(node.path);
    const res = await fetch(url);
    const data = await res.json();
    if (!res.ok) {
      document.getElementById("filePreviewBody").textContent = data.error || "预览失败";
      return;
    }
    const body = document.getElementById("filePreviewBody");
    if (data.kind === "image" && data.dataUrl) {
      body.innerHTML = `<img src="${data.dataUrl}" alt="${escapeHtml(data.name)}"><div class="note">${escapeHtml(data.note || "")}</div>`;
    } else if (data.kind === "text" || data.kind === "dir") {
      body.innerHTML = `<pre>${escapeHtml(data.content || "")}</pre>`;
    } else {
      body.textContent = data.content || data.note || "该文件类型暂不支持直接预览。";
    }
  } catch (err) {
    document.getElementById("filePreviewBody").textContent = "预览失败：" + err.message;
  }
}

async function loadTree() {
  const path = document.getElementById("rootPath").value.trim();
  if (!path) return;
  currentMode = "scan";
  setStatus("正在加载目录...");
  const res = await fetch("/api/scan?path=" + encodeURIComponent(path));
  const data = await res.json();
  if (!res.ok) {
    setStatus(data.error || "加载失败");
    return;
  }
  resetData(data, "本机扫描");
  setStatus(`已加载：${data.root}，共 ${flat.length - 1} 项`, true);
}

function downloadBlob(blob, name) {
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = name;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}

function exportMd() {
  downloadBlob(new Blob([buildMarkdown()], { type:"text/markdown;charset=utf-8" }), EXPORT_MD_NAME_PLACEHOLDER);
}

function cleanTreeForExport(node) {
  const clean = {
    name: node.name,
    path: node.path,
    type: node.type
  };
  if (typeof node.size === "number") clean.size = node.size;
  if (node.root) clean.root = node.root;
  if (node.children && node.children.length) {
    clean.children = node.children.map(child => cleanTreeForExport(child));
  } else if (node.type === "dir") {
    clean.children = [];
  }
  return clean;
}

function exportSnapshot() {
  if (!treeData) {
    setStatus("还没有加载目录，不能导出快照。");
    return;
  }
  const payload = {
    meta: {
      exportedAt: new Date().toISOString(),
      root: rootPath,
      app: "知识库目录工作流整理器"
    },
    tree: cleanTreeForExport(treeData)
  };
  try {
    downloadBlob(new Blob([JSON.stringify(payload, null, 2)], { type:"application/json;charset=utf-8" }), EXPORT_JSON_NAME_PLACEHOLDER);
    setStatus("已导出目录快照 JSON，请查看浏览器下载列表或 Downloads 文件夹。", true);
  } catch (err) {
    setStatus("导出快照失败：" + err.message);
  }
}

function normalizePlanTarget() {
  return document.getElementById("planTarget").value.trim().replace(/\\/g, "/").replace(/^\/+|\/+$/g, "");
}

function describeOperation(op) {
  if (op.type === "mkdir") return `新建文件夹：${op.path}`;
  if (op.type === "move") return `移动 ${op.paths.length} 项 → ${op.target}`;
  return "未知操作";
}

function updateOperationLog() {
  const box = document.getElementById("operationLog");
  if (!box) return;
  box.innerHTML = "";
  if (!operations.length) {
    const li = document.createElement("li");
    li.textContent = "暂无计划操作";
    box.appendChild(li);
    return;
  }
  operations.forEach(op => {
    const li = document.createElement("li");
    li.textContent = describeOperation(op);
    box.appendChild(li);
  });
}

function pushOperation(op) {
  operations.push(op);
  operationRedoStack = [];
  updateOperationLog();
  updatePlanPreview(false);
}

function recordMkdir() {
  const target = normalizePlanTarget();
  if (!target) {
    setStatus("请先填写目标文件夹名称。");
    return;
  }
  pushOperation({ type:"mkdir", path:target });
  setStatus(`已记录：新建 ${target}`, true);
}

function recordMove() {
  const target = normalizePlanTarget();
  const nodes = selectedNodes();
  if (!target) {
    setStatus("请先填写目标文件夹名称。");
    return;
  }
  if (!nodes.length) {
    setStatus("请先勾选要移动的文件或文件夹。");
    return;
  }
  pushOperation({ type:"move", target, paths:nodes.map(n => n.path) });
  setStatus(`已记录：移动 ${nodes.length} 项到 ${target}`, true);
}

function undoOperation() {
  if (!operations.length) {
    setStatus("暂无可撤销的计划操作。");
    return;
  }
  const removed = operations.pop();
  operationRedoStack.push(removed);
  updateOperationLog();
  updatePlanPreview(false);
  setStatus("已撤销：" + describeOperation(removed), true);
}

function redoOperation() {
  const op = operationRedoStack.pop();
  if (!op) {
    setStatus("暂无可重做的计划操作。");
    return;
  }
  operations.push(op);
  updateOperationLog();
  updatePlanPreview(false);
  setStatus("已重做：" + describeOperation(op), true);
}

function updatePlanPreview(showStatus=true) {
  const box = document.getElementById("planPreview");
  if (!box) return;
  if (!operations.length) {
    box.textContent = "尚未生成预演。点击“预演计划”可查看即将新建和移动的项目。";
    return;
  }
  const mkdirs = new Set();
  const moves = [];
  operations.forEach(op => {
    if (op.type === "mkdir") mkdirs.add(op.path);
    if (op.type === "move") {
      mkdirs.add(op.target);
      (op.paths || []).forEach(path => moves.push({ path, target: op.target }));
    }
  });
  const previewLines = [
    `计划操作：${operations.length} 步`,
    `将新建/确保存在文件夹：${mkdirs.size} 个`,
    `将移动项目：${moves.length} 项`,
    "",
    "目标文件夹：",
    ...Array.from(mkdirs).map(path => `- ${path}`),
    "",
    "移动预演（前 80 项）：",
    ...moves.slice(0, 80).map(item => `- ${item.path}  →  ${item.target}`)
  ];
  if (moves.length > 80) previewLines.push(`... 其余 ${moves.length - 80} 项未显示`);
  box.textContent = previewLines.join("\n");
  if (showStatus) setStatus(`已生成预演：${operations.length} 步，移动 ${moves.length} 项。`, true);
}

async function exportBatch() {
  if (!operations.length) {
    setStatus("暂无计划操作，请先记录新建或移动操作。");
    return;
  }
  setStatus("正在生成 BAT 批处理...");
  const res = await fetch("/api/export-bat", {
    method:"POST",
    headers:{ "Content-Type":"application/json" },
    body:JSON.stringify({ root: rootPath, operations })
  });
  const blob = await res.blob();
  if (!res.ok) {
    const text = await blob.text();
    setStatus(text || "生成 BAT 失败");
    return;
  }
  const stamp = new Date().toISOString().slice(0,19).replace(/[-:T]/g, "");
  downloadBlob(blob, `file整理操作_${stamp}.bat`);
  setStatus("已生成 BAT。运行前请先右键编辑检查一遍。", true);
}

async function importSnapshotFile(file) {
  const text = await file.text();
  const payload = JSON.parse(text);
  if (!payload.tree || !payload.meta) throw new Error("快照文件格式不正确");
  currentMode = "snapshot";
  resetData(payload.tree, "快照模式");
  rootPath = payload.meta.root || rootPath;
  document.getElementById("rootPath").value = rootPath;
  setStatus(`已导入快照：${file.name}`, true);
}

async function moveSelected() {
  const nodes = selectedNodes();
  if (!nodes.length) {
    setStatus("还没有选择任何文件或文件夹。");
    return;
  }
  const ok = confirm(`确认把 ${nodes.length} 个所选项目移到独立文件夹？\n\n移动后可在根目录下找到 ${REMOVED_PREFIX_PLACEHOLDER}* 文件夹。`);
  if (!ok) return;
  setStatus("正在移动所选文件...");
  const res = await fetch("/api/move", {
    method:"POST",
    headers:{ "Content-Type":"application/json" },
    body:JSON.stringify({ root: rootPath, paths: nodes.map(n => n.path) })
  });
  const data = await res.json();
  if (!res.ok) {
    setStatus(data.error || "移动失败");
    return;
  }
  setStatus(`已移动 ${data.moved.length} 项到：${data.target}`, true);
  await loadTree();
}

async function applyKeepList() {
  const mdText = prompt("请粘贴由别人筛选后导出的 MD 清单内容。系统会保留清单中的文件，把其余文件移出。");
  if (!mdText) return;
  setStatus("正在解析 MD 清单...");
  const res = await fetch("/api/apply-keep-list", {
    method:"POST",
    headers:{ "Content-Type":"application/json" },
    body:JSON.stringify({ root: rootPath, markdown: mdText })
  });
  const data = await res.json();
  if (!res.ok) {
    setStatus(data.error || "应用清单失败");
    return;
  }
  setStatus(`已按清单保留文件，其余 ${data.moved.length} 项已移到：${data.target}`, true);
  await loadTree();
}

document.getElementById("load").onclick = loadTree;
document.getElementById("pickFolder").onclick = pickFolder;
document.getElementById("search").oninput = render;
document.getElementById("selectAll").onclick = () => { if (!treeData) return; withSelectionHistory(() => { setNode(treeData, true); render(); updatePreview(); }, "全选"); };
document.getElementById("clearAll").onclick = () => { if (!treeData) return; withSelectionHistory(() => { flat.forEach(n => { state.set(n.path, false); n._indeterminate = false; }); render(); updatePreview(); }, "清空"); };
document.getElementById("undoSelection").onclick = undoSelection;
document.getElementById("redoSelection").onclick = redoSelection;
document.getElementById("expandAll").onclick = () => { collapsed.clear(); render(); };
document.getElementById("collapseAll").onclick = () => { flat.filter(n => n.type === "dir" && n.path !== ".").forEach(n => collapsed.add(n.path)); render(); };
document.getElementById("exportMd").onclick = exportMd;
document.getElementById("exportSnapshot").onclick = exportSnapshot;
document.getElementById("exportBatch").onclick = exportBatch;
document.getElementById("importSnapshot").onclick = () => document.getElementById("snapshotFile").click();
document.getElementById("snapshotFile").onchange = async e => {
  const file = e.target.files[0];
  if (!file) return;
  try {
    await importSnapshotFile(file);
  } catch (err) {
    setStatus("导入快照失败：" + err.message);
  } finally {
    e.target.value = "";
  }
};
document.getElementById("moveSelected").onclick = moveSelected;
document.getElementById("applyKeepList").onclick = applyKeepList;
document.getElementById("recordMkdir").onclick = recordMkdir;
document.getElementById("recordMove").onclick = recordMove;
document.getElementById("undoOperation").onclick = undoOperation;
document.getElementById("redoOperation").onclick = redoOperation;
document.getElementById("previewPlan").onclick = () => updatePlanPreview(true);
document.getElementById("tree").onmousedown = startBoxSelection;
document.getElementById("toggleFilePreview").onclick = () => {
  filePreviewCollapsed = !filePreviewCollapsed;
  document.getElementById("filePreviewWrap").classList.toggle("collapsed", filePreviewCollapsed);
  document.getElementById("toggleFilePreview").textContent = filePreviewCollapsed ? "展开预览" : "收起预览";
};
updateOperationLog();
loadTree();
</script>
</body>
</html>
"""


def safe_resolve(path_text):
    if not path_text:
        return DEFAULT_ROOT
    return Path(path_text).expanduser().resolve()


def resolve_relative(root, rel):
    rel_path = Path(rel or ".")
    if rel_path.is_absolute() or ".." in rel_path.parts:
        raise RuntimeError("非法路径")
    target = (root / rel_path).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise RuntimeError("路径超出根目录") from exc
    return target


def choose_folder(initial_path):
    try:
        import tkinter as tk
        from tkinter import filedialog
    except Exception as exc:
        raise RuntimeError("当前 Python 环境无法打开系统文件夹选择窗口，请继续使用手动路径。") from exc

    initial = initial_path if initial_path and initial_path.exists() else DEFAULT_ROOT
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    try:
        folder = filedialog.askdirectory(
            initialdir=str(initial),
            title="选择要加载的文件夹",
            mustexist=True,
        )
    finally:
        root.destroy()
    return folder


def decode_text_sample(raw):
    for encoding in ("utf-8-sig", "utf-8", "gb18030", "big5"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def preview_path(root, rel):
    target = resolve_relative(root, rel)
    if not target.exists():
        raise RuntimeError(f"文件不存在：{rel}")
    if target.is_dir():
        dirs = []
        files = []
        for child in target.iterdir():
            if child.name in IGNORE_DIR_NAMES or child.name.startswith(REMOVED_PREFIX):
                continue
            if child.is_dir():
                dirs.append(child.name)
            else:
                files.append(child.name)
        lines = [
            f"目录：{target.name}",
            f"相对路径：{rel}",
            f"子目录：{len(dirs)} 个，文件：{len(files)} 个",
            "",
            "前 80 项：",
        ]
        names = [f"[目录] {name}" for name in sorted(dirs, key=str.lower)]
        names += [f"[文件] {name}" for name in sorted(files, key=str.lower)]
        lines.extend(names[:80])
        if len(names) > 80:
            lines.append(f"... 其余 {len(names) - 80} 项未显示")
        return {"kind": "dir", "name": target.name, "content": "\n".join(lines)}

    size = target.stat().st_size
    suffix = target.suffix.lower()
    mime, _ = mimetypes.guess_type(target.name)
    if suffix in IMAGE_EXTENSIONS and size <= IMAGE_PREVIEW_LIMIT:
        data = base64.b64encode(target.read_bytes()).decode("ascii")
        return {
            "kind": "image",
            "name": target.name,
            "dataUrl": f"data:{mime or 'image/*'};base64,{data}",
            "note": f"{target.name} · {size} bytes",
        }

    raw = target.read_bytes()[:TEXT_PREVIEW_LIMIT]
    looks_binary = b"\x00" in raw[:4096]
    if suffix in TEXT_EXTENSIONS or (not looks_binary and raw):
        text = decode_text_sample(raw)
        if size > TEXT_PREVIEW_LIMIT:
            text += f"\n\n... 已截断，仅显示前 {TEXT_PREVIEW_LIMIT} 字节。"
        return {"kind": "text", "name": target.name, "content": text}

    return {
        "kind": "binary",
        "name": target.name,
        "content": f"{target.name}\n类型：{mime or '未知二进制文件'}\n大小：{size} bytes\n\n该类型暂不直接预览。后续可接入 PDF/OCR/图片/视频解析器。",
    }


def build_tree(root, path):
    rel = "." if path == root else path.relative_to(root).as_posix()
    node = {
        "name": path.name if path != root else path.name,
        "path": rel,
        "type": "dir" if path.is_dir() else "file",
    }
    if path.is_file():
        node["size"] = path.stat().st_size
        return node
    children = []
    dirs = []
    files = []
    for child in path.iterdir():
        if child.name in IGNORE_DIR_NAMES:
            continue
        if child.name.startswith(REMOVED_PREFIX):
            continue
        if child.is_dir():
            dirs.append(child)
        else:
            files.append(child)
    for child in sorted(dirs, key=lambda p: p.name.lower()):
        children.append(build_tree(root, child))
    for child in sorted(files, key=lambda p: p.name.lower()):
        children.append(build_tree(root, child))
    node["children"] = children
    return node


def unique_destination(path):
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    for idx in range(1, 10000):
        candidate = parent / f"{stem}_{idx}{suffix}"
        if not candidate.exists():
            return candidate
    raise RuntimeError("无法生成不冲突的目标路径")


def normalize_selected(root, rel_paths):
    normalized = []
    skipped = []
    for rel in rel_paths:
        rel_path = Path(rel)
        if rel in {"", "."} or rel_path.is_absolute() or ".." in rel_path.parts:
            skipped.append({"path": rel, "reason": "非法路径"})
            continue
        src = (root / rel_path).resolve()
        try:
            src.relative_to(root)
        except ValueError:
            skipped.append({"path": rel, "reason": "超出根目录"})
            continue
        if not src.exists():
            skipped.append({"path": rel, "reason": "文件不存在"})
            continue
        normalized.append((rel_path.as_posix(), src))
    selected_set = {rel for rel, _ in normalized}
    final_items = []
    for rel, src in normalized:
        parts = Path(rel).parts
        has_selected_parent = False
        for idx in range(1, len(parts)):
            parent_rel = posixpath.join(*parts[:idx])
            if parent_rel in selected_set:
                has_selected_parent = True
                break
        if not has_selected_parent:
            final_items.append((rel, src))
    return final_items, skipped


def move_selected(root, rel_paths):
    target = root / f"{REMOVED_PREFIX}{time.strftime('%Y%m%d_%H%M%S')}"
    target.mkdir(exist_ok=False)
    moved = []
    final_items, skipped = normalize_selected(root, rel_paths)
    for rel, src in final_items:
        dst = unique_destination(target / Path(rel))
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        moved.append({"from": rel, "to": dst.relative_to(root).as_posix()})
    return target.name, moved, skipped


def collect_all_files(root):
    files = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if any(part in IGNORE_DIR_NAMES for part in rel.parts):
            continue
        if any(part.startswith(REMOVED_PREFIX) for part in rel.parts):
            continue
        files.append(rel.as_posix())
    return files


def parse_markdown_keep_list(markdown_text):
    keep = set()
    for raw in markdown_text.splitlines():
        line = raw.strip()
        if not line.startswith("- "):
            continue
        value = line[2:].strip()
        if value.startswith("[目录]") or value.startswith("[文件]"):
            continue
        keep.add(value)
    return keep


def apply_keep_list(root, markdown_text):
    keep = parse_markdown_keep_list(markdown_text)
    if not keep:
        raise RuntimeError("没有从 MD 清单中解析到任何文件路径")
    all_files = collect_all_files(root)
    remove_files = [rel for rel in all_files if rel not in keep]
    return move_selected(root, remove_files)


def bat_literal(text):
    if '"' in str(text):
        raise RuntimeError("路径中包含英文双引号，无法安全生成 BAT")
    return str(text).replace("%", "%%")


def validate_batch_rel_path(rel):
    rel = str(rel or "").strip().replace("\\", "/").strip("/")
    rel_path = Path(rel)
    if not rel or rel == "." or rel_path.is_absolute() or ".." in rel_path.parts:
        raise RuntimeError(f"非法相对路径：{rel}")
    if '"' in rel:
        raise RuntimeError(f"路径中包含英文双引号：{rel}")
    return rel


def prune_child_paths(rel_paths):
    safe_paths = []
    for rel in rel_paths:
        safe_paths.append(validate_batch_rel_path(rel))
    selected = set(safe_paths)
    result = []
    for rel in safe_paths:
        parts = Path(rel).parts
        if any(posixpath.join(*parts[:idx]) in selected for idx in range(1, len(parts))):
            continue
        if rel not in result:
            result.append(rel)
    return result


def to_batch_path(rel):
    return bat_literal(rel.replace("/", "\\"))


def generate_batch(root, operations):
    if not operations:
        raise RuntimeError("暂无计划操作")

    lines = [
        "@echo off",
        "chcp 65001 >nul",
        "setlocal EnableExtensions DisableDelayedExpansion",
        f'set "ROOT={bat_literal(root)}"',
        'echo 本脚本将按网页端记录执行文件整理操作。',
        'echo 根目录: "%ROOT%"',
        'if not exist "%ROOT%" (',
        '  echo 根目录不存在，请检查 ROOT 路径。',
        "  pause",
        "  exit /b 1",
        ")",
        "",
    ]

    for index, op in enumerate(operations, 1):
        op_type = op.get("type")
        lines.append(f"echo [{index}/{len(operations)}] {bat_literal(op_type or 'operation')}")
        if op_type == "mkdir":
            target = validate_batch_rel_path(op.get("path"))
            target_path = to_batch_path(target)
            lines.append(f'if not exist "%ROOT%\\{target_path}" mkdir "%ROOT%\\{target_path}"')
        elif op_type == "move":
            target = validate_batch_rel_path(op.get("target"))
            target_path = to_batch_path(target)
            lines.append(f'if not exist "%ROOT%\\{target_path}" mkdir "%ROOT%\\{target_path}"')
            for rel in prune_child_paths(op.get("paths", [])):
                src_path = to_batch_path(rel)
                lines.append(f'if exist "%ROOT%\\{src_path}" (')
                lines.append(f'  move /Y "%ROOT%\\{src_path}" "%ROOT%\\{target_path}\\"')
                lines.append(") else (")
                lines.append(f'  echo 跳过，不存在: "%ROOT%\\{src_path}"')
                lines.append(")")
        else:
            raise RuntimeError(f"未知操作类型：{op_type}")
        lines.append("")

    lines.extend([
        "echo.",
        "echo 整理操作执行完毕。",
        "pause",
    ])
    return "\r\n".join(lines).encode("utf-8-sig")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def send_bytes(self, body, content_type, status=200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, data, status=200):
        self.send_bytes(json.dumps(data, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8", status)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/":
            html = INDEX_HTML
            html = html.replace("__DEFAULT_ROOT__", json.dumps(str(DEFAULT_ROOT), ensure_ascii=False))
            html = html.replace("EXPORT_MD_NAME_PLACEHOLDER", json.dumps(EXPORT_MD_NAME, ensure_ascii=False))
            html = html.replace("EXPORT_JSON_NAME_PLACEHOLDER", json.dumps(EXPORT_JSON_NAME, ensure_ascii=False))
            html = html.replace("REMOVED_PREFIX_PLACEHOLDER", REMOVED_PREFIX)
            self.send_bytes(html.encode("utf-8"), "text/html; charset=utf-8")
            return
        if parsed.path == "/api/scan":
            qs = urllib.parse.parse_qs(parsed.query)
            root = safe_resolve(qs.get("path", [""])[0])
            if not root.exists() or not root.is_dir():
                self.send_json({"error": f"目录不存在：{root}"}, 400)
                return
            tree = build_tree(root, root)
            tree["root"] = str(root)
            self.send_json(tree)
            return
        if parsed.path == "/api/pick-folder":
            qs = urllib.parse.parse_qs(parsed.query)
            initial = safe_resolve(qs.get("path", [""])[0])
            try:
                folder = choose_folder(initial)
                self.send_json({"path": folder})
            except Exception as exc:
                self.send_json({"error": str(exc)}, 500)
            return
        if parsed.path == "/api/preview":
            qs = urllib.parse.parse_qs(parsed.query)
            root = safe_resolve(qs.get("root", [""])[0])
            rel = qs.get("path", ["."])[0]
            if not root.exists() or not root.is_dir():
                self.send_json({"error": f"目录不存在：{root}"}, 400)
                return
            try:
                self.send_json(preview_path(root, rel))
            except Exception as exc:
                self.send_json({"error": str(exc)}, 500)
            return
        self.send_json({"error": "Not found"}, 404)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0"))
        try:
            data = json.loads(self.rfile.read(length).decode("utf-8"))
        except Exception:
            self.send_json({"error": "请求体不是合法 JSON"}, 400)
            return

        if parsed.path == "/api/move":
            root = safe_resolve(data.get("root", ""))
            if not root.exists() or not root.is_dir():
                self.send_json({"error": f"目录不存在：{root}"}, 400)
                return
            try:
                target, moved, skipped = move_selected(root, data.get("paths", []))
                self.send_json({"target": target, "moved": moved, "skipped": skipped})
            except Exception as exc:
                self.send_json({"error": str(exc)}, 500)
            return

        if parsed.path == "/api/apply-keep-list":
            root = safe_resolve(data.get("root", ""))
            if not root.exists() or not root.is_dir():
                self.send_json({"error": f"目录不存在：{root}"}, 400)
                return
            try:
                target, moved, skipped = apply_keep_list(root, data.get("markdown", ""))
                self.send_json({"target": target, "moved": moved, "skipped": skipped})
            except Exception as exc:
                self.send_json({"error": str(exc)}, 500)
            return

        if parsed.path == "/api/export-bat":
            root = safe_resolve(data.get("root", ""))
            try:
                body = generate_batch(root, data.get("operations", []))
                self.send_bytes(body, "application/octet-stream")
            except Exception as exc:
                self.send_json({"error": str(exc)}, 400)
            return

        self.send_json({"error": "Not found"}, 404)


def main():
    server = ThreadingHTTPServer(("127.0.0.1", APP_PORT), Handler)
    print(f"知识库目录工作流整理器已启动：http://localhost:{APP_PORT}")
    print(f"默认目录：{DEFAULT_ROOT}")
    server.serve_forever()


if __name__ == "__main__":
    main()

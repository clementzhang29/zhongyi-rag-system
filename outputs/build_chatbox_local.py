# build_chatbox.py - generates the responsive chatbox HTML
import os

OUT = r"C:\Users\35160\Desktop\中医RAG系统\outputs\chatbox.html"

css = """/* === Design Tokens === */
:root{--ink:#2c2416;--ink-l:#5c4a32;--ink-m:#8a7a62;--bg:#faf7f2;--card:#fffef9;--acc:#8B4513;--acc-h:#a0522d;--acc-s:#c4a882;--acc-w:#fdf6ed;--bd:#e8e0d4;--bd-l:#f0ebe0;--sh:0 2px 16px rgba(44,36,22,.07);--sh-s:0 1px 4px rgba(44,36,22,.04);--r-s:6px;--r:12px;--r-l:18px;--fs:"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans SC",system-ui,sans-serif;--ff:"Noto Serif SC","Source Han Serif SC","PingFang SC","Hiragino Sans GB","Microsoft YaHei",Georgia,serif;--mw:720px}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{font-size:clamp(14px,1vw+10px,17px);-webkit-text-size-adjust:100%;-webkit-font-smoothing:antialiased}
body{font-family:var(--ff);background:var(--bg);color:var(--ink);min-height:100dvh;display:flex;flex-direction:column;line-height:1.75;overflow-x:hidden}
.hd{background:linear-gradient(135deg,#5a2d1a,#7a3d22,#8B4513);color:#fff;padding:clamp(10px,2vw,16px) clamp(14px,3vw,28px);text-align:center;box-shadow:0 2px 12px rgba(44,36,22,.15);position:sticky;top:0;z-index:20;flex-shrink:0}
.hd::after{content:'';display:block;height:2px;margin:8px auto 0;width:clamp(60px,15vw,160px);background:rgba(255,255,255,.25);border-radius:1px}
.hd h1{font-size:clamp(1rem,3vw,1.35rem);font-weight:700;letter-spacing:.03em;font-family:var(--fs)}
.hd .sub{font-size:clamp(.68rem,1.5vw,.8rem);opacity:.75;margin-top:2px;letter-spacing:.04em;font-family:var(--fs)}
.cv{flex:1;overflow-y:auto;overflow-x:hidden;padding:clamp(12px,2.5vw,28px) clamp(8px,3vw,24px);display:flex;flex-direction:column;align-items:center;gap:clamp(14px,2.5vw,22px);scroll-behavior:smooth;-webkit-overflow-scrolling:touch}
.cv::-webkit-scrollbar{width:4px}
.cv::-webkit-scrollbar-track{background:transparent}
.cv::-webkit-scrollbar-thumb{background:var(--acc-s);border-radius:4px}
.mw{width:100%;max-width:var(--mw);display:flex;flex-direction:column}
.mw.usr{align-items:flex-end}
.mw.ai{align-items:flex-start}
.mb{animation:fU .35s ease-out both;max-width:100%}
.mw.usr .mb{background:var(--acc);color:#fff;padding:clamp(8px,1.5vw,12px) clamp(12px,2vw,18px);border-radius:16px 16px 4px 16px;font-size:clamp(.85rem,1.8vw,.92rem);line-height:1.55;box-shadow:var(--sh-s);max-width:min(85%,400px);word-break:break-word;font-family:var(--fs)}
.mw.ai .mb{width:100%;background:var(--card);border-radius:var(--r-l);box-shadow:var(--sh);border:1px solid var(--bd);overflow:hidden}
.mw.ai .cp{padding:clamp(16px,3vw,26px) clamp(14px,3vw,26px)}
.sec{margin:clamp(14px,2.5vw,20px) 0}
.sec:first-child{margin-top:0}
.sec:last-child{margin-bottom:0}
.sech{display:flex;align-items:center;gap:clamp(6px,1.5vw,10px);margin-bottom:clamp(8px,1.5vw,12px);padding-bottom:clamp(6px,1vw,10px);border-bottom:1px solid var(--bd-l)}
.sech .si{font-size:clamp(1rem,2vw,1.15rem);width:clamp(26px,4vw,30px);height:clamp(26px,4vw,30px);display:flex;align-items:center;justify-content:center;border-radius:8px;flex-shrink:0}
.sech .sl{font-size:clamp(.82rem,1.8vw,.92rem);font-weight:700;color:var(--ink);font-family:var(--fs);letter-spacing:.02em}
.se .si{background:#fdf2e9;color:#c0392b}
.sc .si{background:var(--acc-w);color:var(--acc)}
.sd .si{background:#eaf2f8;color:#2c3e50}
.sl2 .si{background:#eafaf1;color:#1e8449}
.sr .si{background:#f4ecf7;color:#6c3483}
.et{font-size:clamp(.9rem,2vw,1rem);font-weight:600;color:var(--ink);line-height:1.65}
.cb{margin:clamp(10px,2vw,14px) 0;background:var(--acc-w);border-radius:var(--r);border:1px solid var(--bd);overflow:hidden}
.cbh{display:flex;align-items:center;gap:6px;padding:clamp(8px,1.5vw,11px) clamp(10px,2vw,14px);background:rgba(139,69,19,.04);border-bottom:1px solid var(--bd-l)}
.cbh .cm{font-size:clamp(.75rem,1.5vw,.85rem)}
.cbh .cbk{font-size:clamp(.78rem,1.6vw,.85rem);font-weight:700;color:var(--acc);font-family:var(--fs)}
.cbh .cbc{font-size:clamp(.7rem,1.4vw,.78rem);color:var(--ink-m)}
.cbb{padding:clamp(10px,2vw,14px)}
.cbo{font-size:clamp(.8rem,1.7vw,.88rem);color:var(--ink-l);line-height:1.75;padding:clamp(8px,1.5vw,10px) clamp(10px,2vw,14px);background:rgba(255,255,255,.65);border-radius:var(--r-s);border-left:3px solid var(--acc-s);margin-bottom:clamp(8px,1.5vw,10px)}
.cbv{font-size:clamp(.78rem,1.5vw,.85rem);color:var(--ink-m);line-height:1.7;display:flex;gap:6px;align-items:flex-start}
.cbv .vt{font-size:clamp(.65rem,1.2vw,.72rem);background:var(--acc);color:#fff;padding:1px 7px;border-radius:10px;flex-shrink:0;font-weight:600;font-family:var(--fs);letter-spacing:.04em;margin-top:2px}
.di{margin:clamp(10px,2vw,14px) 0}
.dt{font-size:clamp(.84rem,1.7vw,.9rem);font-weight:700;color:var(--ink);margin-bottom:4px;font-family:var(--fs);display:flex;align-items:baseline;gap:6px}
.dt::before{content:'';display:inline-block;width:clamp(4px,.8vw,5px);height:clamp(4px,.8vw,5px);background:var(--acc);border-radius:50%;flex-shrink:0;margin-top:-2px}
.db{font-size:clamp(.8rem,1.6vw,.88rem);color:var(--ink-l);line-height:1.75;padding-left:clamp(10px,2vw,13px)}
.lb{font-size:clamp(.8rem,1.6vw,.9rem);color:var(--ink-l);line-height:1.75;padding:clamp(10px,2vw,14px);background:#f9fdf7;border-radius:var(--r-s);border:1px solid #e0f0d8}
.ri{display:flex;align-items:baseline;gap:6px;margin:clamp(5px,1vw,7px) 0;font-size:clamp(.8rem,1.6vw,.88rem);flex-wrap:wrap}
.ri .bkic{color:var(--acc);font-size:clamp(.7rem,1.3vw,.8rem);flex-shrink:0}
.ri .bkn{font-weight:600;color:var(--ink);white-space:nowrap}
.ri .bkr{color:var(--ink-m);font-size:clamp(.75rem,1.4vw,.83rem)}
.rb{margin-top:clamp(14px,2.5vw,18px);padding-top:clamp(12px,2vw,14px);border-top:1px solid var(--bd)}
.rbt{font-size:clamp(.68rem,1.3vw,.75rem);font-weight:700;color:var(--ink-m);text-transform:uppercase;letter-spacing:.12em;margin-bottom:clamp(8px,1.5vw,10px);font-family:var(--fs)}
.rr{display:flex;gap:clamp(8px,1.5vw,10px);padding:clamp(7px,1.2vw,9px) 0;border-bottom:1px solid var(--bd-l);align-items:flex-start}
.rr:last-child{border-bottom:none}
.rn{background:var(--acc);color:#fff;border-radius:50%;min-width:clamp(20px,3vw,22px);height:clamp(20px,3vw,22px);display:flex;align-items:center;justify-content:center;font-size:clamp(.6rem,1.1vw,.68rem);font-weight:700;flex-shrink:0;font-family:var(--fs)}
.ri2{flex:1;min-width:0}
.rs{font-size:clamp(.78rem,1.5vw,.84rem);font-weight:600;color:var(--acc);margin-bottom:2px;font-family:var(--fs)}
.rx{font-size:clamp(.7rem,1.3vw,.78rem);color:var(--ink-m);line-height:1.5;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.wb{text-align:center;padding:clamp(20px,4vw,30px) clamp(8px,2vw,12px)}
.wb .wg{font-size:clamp(.95rem,2vw,1.1rem);color:var(--ink);margin-bottom:4px;font-weight:600}
.wb .wd{font-size:clamp(.78rem,1.5vw,.85rem);color:var(--ink-m);margin-bottom:clamp(14px,2.5vw,18px)}
.wh{display:flex;flex-wrap:wrap;gap:clamp(6px,1.2vw,8px);justify-content:center}
.whi{background:var(--bg);border:1px solid var(--bd);padding:clamp(6px,1vw,8px) clamp(12px,2vw,15px);border-radius:20px;font-size:clamp(.74rem,1.5vw,.8rem);color:var(--acc);cursor:pointer;transition:all .18s;font-family:var(--fs);white-space:nowrap;user-select:none;-webkit-tap-highlight-color:transparent}
.whi:active{background:var(--acc);color:#fff;border-color:var(--acc)}
@media(hover:hover){.whi:hover{background:var(--acc);color:#fff;border-color:var(--acc)}}
.ld{display:flex;gap:6px;padding:clamp(12px,2vw,16px) clamp(16px,3vw,22px);background:var(--card);border-radius:var(--r);box-shadow:var(--sh-s);border:1px solid var(--bd);align-self:flex-start}
.ld span{width:clamp(6px,1vw,7px);height:clamp(6px,1vw,7px);background:var(--acc-s);border-radius:50%;animation:dB 1.3s infinite;opacity:.45}
.ld span:nth-child(2){animation-delay:.2s}
.ld span:nth-child(3){animation-delay:.4s}
.ib{display:flex;gap:clamp(6px,1.5vw,10px);padding:clamp(8px,1.5vw,12px) clamp(10px,2vw,16px) max(clamp(8px,1.5vw,12px),env(safe-area-inset-bottom,8px));background:var(--card);border-top:1px solid var(--bd);flex-shrink:0;position:sticky;bottom:0;z-index:10;align-items:center;max-width:100%}
.ib input{flex:1;min-width:0;padding:clamp(9px,1.5vw,11px) clamp(12px,2vw,16px);border:1.5px solid var(--bd);border-radius:22px;font-size:clamp(.82rem,1.8vw,.9rem);font-family:var(--ff);outline:none;transition:border-color .2s,box-shadow .2s;background:var(--bg);-webkit-appearance:none}
.ib input:focus{border-color:var(--acc-s);box-shadow:0 0 0 3px rgba(139,69,19,.07)}
.ib button{background:var(--acc);color:#fff;border:none;padding:clamp(9px,1.5vw,11px) clamp(18px,3vw,24px);border-radius:22px;font-size:clamp(.82rem,1.7vw,.9rem);font-weight:600;cursor:pointer;transition:all .2s;font-family:var(--fs);letter-spacing:.03em;flex-shrink:0;white-space:nowrap;-webkit-tap-highlight-color:transparent}
.ib button:active{background:var(--acc-h);transform:scale(.97)}
@media(hover:hover){.ib button:hover{background:var(--acc-h);transform:scale(1.03)}}
.ib button:disabled{opacity:.35;transform:none;cursor:default}
.ap p{margin:clamp(3px,.5vw,5px) 0;font-size:clamp(.8rem,1.6vw,.88rem);color:var(--ink-l);line-height:1.75}
.ap strong{color:var(--ink);font-weight:700}
.ap em{font-style:italic}
.ae{color:#c0392b;font-size:clamp(.78rem,1.5vw,.85rem);line-height:1.6}
/* Numbered list styling inside ap */
.ap ol,.ap ul{padding-left:clamp(16px,3vw,20px);margin:clamp(4px,.8vw,8px) 0}
.ap li{margin:clamp(3px,.5vw,5px) 0;font-size:clamp(.8rem,1.6vw,.88rem);color:var(--ink-l);line-height:1.75}
@media(min-width:768px){:root{--mw:680px}.cv{padding:clamp(18px,3vw,32px) clamp(12px,5vw,48px)}.mw.usr .mb{max-width:min(75%,500px)}}
@media(min-width:1024px){:root{--mw:700px}.cv{padding:clamp(22px,3vw,36px) clamp(16px,8vw,80px)}}
@media(min-width:1400px){:root{--mw:740px}}
@keyframes fU{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
@keyframes dB{0%,80%,100%{transform:scale(.35);opacity:.35}40%{transform:scale(1);opacity:.85}}
"""

js = r'''
var API="http://localhost:8000/rag/query";
var cv=document.getElementById("cv");
var qi=document.getElementById("qi");
var qb=document.getElementById("qb");
document.getElementById("hb").addEventListener("click",function(e){var h=e.target.closest(".whi");if(h&&h.dataset.q){qi.value=h.dataset.q;go()}});
qi.addEventListener("keydown",function(e){if(e.key==="Enter")go()});
qb.addEventListener("click",go);

function go(){
  var t=qi.value.trim();
  if(!t)return;
  if(t.length<3){rai("请把问题说得更详细一些");return}
  rusr(t);qi.value="";qi.disabled=qb.disabled=true;
  var ld=rld();
  fetch(API,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({question:t})})
    .then(function(r){return r.json()})
    .then(function(d){ld.remove();rai(d.answer,d.references||[])})
    .catch(function(e){ld.remove();rai('<div class="ae"><strong>无法连接服务</strong></div><p style="margin-top:6px;font-size:.78rem;color:var(--ink-m)">请先启动RAG服务<br><code style="background:#f0ebe0;padding:1px 6px;border-radius:4px;font-size:.72rem">cd 中医RAG系统 && python run.py</code></p>')})
    .then(function(){qi.disabled=qb.disabled=false;qi.focus()});
}

function E(s){return String(s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")}

function MP(s){
  var h=E(s);
  // Bold
  h=h.replace(/\*\*(.+?)\*\*/g,"<strong>$1</strong>");
  // Clean up empty strong
  h=h.replace(/<strong>\s*<\/strong>/g,"");
  // Paragraphs: double newlines
  h=h.replace(/\n\n+/g,"</p><p>");
  h="<p>"+h+"</p>";
  h=h.replace(/<p>\s*<\/p>/g,"");
  // Single newlines
  h=h.replace(/\n/g,"<br>");
  return h;
}

// NEW approach: parse sections based on ## headers (old prompt format)
// Also handle emoji-only headers (new prompt format)
function pS(t){
  // First try emoji-based sections (new format)
  var emojiHeaders = [
    {e:"💡",c:"se",l:"一句话精要",i:"💡"},
    {e:"📖",c:"sc",l:"经典溯源",i:"📖"},
    {e:"🧠",c:"sd",l:"深度阐释",i:"🧠"},
    {e:"🌿",c:"sl2",l:"生活践行",i:"🌿"},
    {e:"📚",c:"sr",l:"延伸阅读",i:"📚"}
  ];
  var foundEmoji = [];
  emojiHeaders.forEach(function(d){
    var x = t.indexOf("**" + d.e); if(x<0) x = t.indexOf(d.e + " ");
    if(x<0) x = t.indexOf(d.e + "\n");
    if(x<0) x = t.indexOf(d.e);
    if(x>=0) foundEmoji.push({e:d.e,c:d.c,l:d.l,i:d.i,idx:x});
  });
  
  if(foundEmoji.length >= 2){
    // Use emoji-based sectioning
    foundEmoji.sort(function(a,b){return a.idx-b.idx});
    var h2="";
    foundEmoji.forEach(function(s,i){
      var st=s.idx;
      var ed=i+1<foundEmoji.length?foundEmoji[i+1].idx:t.length;
      var b=t.substring(st,ed).trim();
      b=b.replace(/^\*{0,2}[💡📖🧠🌿📚]\s*[^\n]*\n?/,"").trim();
      h2+=rS(s,b);
    });
    return h2;
  }

  // Try ## header-based sections (old format)
  var mdHeaders = [
    {re:/##\s*📌\s*(.+)/, c:"se", l:"核心要点", i:"📌"},
    {re:/##\s*🔍\s*(.+)/, c:"sd", l:"深度解读", i:"🔍"},
    {re:/##\s*📜\s*(.+)/, c:"sc", l:"引用出处", i:"📜"},
    {re:/##\s*💡\s*(.+)/, c:"sl2", l:"生活启发", i:"💡"},
    {re:/##\s*(.+)/, c:"sd", l:"", i:"📝"}
  ];
  
  var sections = [];
  var lines = t.split("\n");
  var currentSec = null;
  var currentBody = [];
  
  for(var i=0;i<lines.length;i++){
    var line = lines[i];
    var matched = false;
    for(var j=0;j<mdHeaders.length;j++){
      var m = line.match(mdHeaders[j].re);
      if(m){
        if(currentSec){
          sections.push({c:currentSec.c, l:currentSec.l, i:currentSec.i, body:currentBody.join("\n")});
        }
        currentSec = {c:mdHeaders[j].c, l:m[1]||mdHeaders[j].l||"", i:mdHeaders[j].i};
        currentBody = [];
        matched = true;
        break;
      }
    }
    if(!matched && currentSec){
      currentBody.push(line);
    }else if(!matched && !currentSec){
      // Text before any header
      if(!sections.length && line.trim()){
        if(!currentBody.length) currentBody = [];
        currentBody.push(line);
      }
    }
  }
  
  if(currentSec){
    sections.push({c:currentSec.c, l:currentSec.l, i:currentSec.i, body:currentBody.join("\n")});
  } else if(currentBody.length && !sections.length){
    sections.push({c:"sd", l:"", i:"📝", body:currentBody.join("\n")});
  }

  if(sections.length === 0){
    return '<div class="sec"><div class="ap">'+MP(t)+'</div></div>';
  }

  var h2="";
  sections.forEach(function(s){
    var cleanBody = s.body.trim();
    // Remove leading/trailing empty lines
    if(cleanBody){
      h2+=rS(s, cleanBody);
    }
  });
  return h2;
}

function rS(s,b){
  var h='<div class="sec '+s.c+'">';
  if(s.l){
    h+='<div class="sech"><span class="si">'+s.i+'</span><span class="sl">'+s.l+'</span></div>';
  }
  if(s.c==="se"){
    // Core point / essence
    h+='<div class="et">'+MP(b)+'</div>';
  }else if(s.c==="sc"){
    // Citations
    h+=pC(b);
  }else if(s.c==="sd"){
    // Deep interpretation
    h+=pD2(b);
  }else if(s.c==="sl2"){
    // Life practice
    h+='<div class="lb">'+MP(b)+'</div>';
  }else if(s.c==="sr"){
    // Extended reading
    h+=pR(b);
  }else{
    h+='<div class="ap">'+MP(b)+'</div>';
  }
  h+="</div>";
  return h;
}

// Citation parser: handles both old (> **Book**) and new (**出处：**) formats
function pC(b){
  // Strategy: split by **出处** pattern to get individual citations
  // Then parse each citation for book, chapter, original text, and vernacular explanation
  var h="";
  
  // Split by **出处 (handles both **出处： and **出处**：)
  var parts = b.split(/\*\*出处\*{0,2}[：:]/);
  
  if(parts.length > 1){
    // First part is intro text (if any)
    if(parts[0] && parts[0].trim()){
      h+='<p style="font-size:.82rem;color:var(--ink-m);margin-bottom:4px">'+MP(parts[0].trim())+'</p>';
    }
    
    for(var i=1;i<parts.length;i++){
      var block = parts[i].trim();
      
      // Extract book: 《书名》
      var book="";
      var bm = block.match(/《(.+?)》/);
      if(bm) book = bm[1].trim();
      
      // Extract chapter: everything between 》 and the next marker
      var chapter="";
      var afterBook = block.substring(block.indexOf('》')+1);
      // Chapter is text before 原文, 「, or newline
      var chEnd = afterBook.search(/原文|「|\n/);
      if(chEnd > 0){
        chapter = afterBook.substring(0, chEnd).replace(/^\s*[·．]\s*/,'').replace(/\*+$/,'').trim();
      }
      
      // Extract original text: 原文：「...」 or 原文："..."
      var orig="";
      var om = block.match(/原文[：:]\s*[「「"]([\s\S]*?)[」」"]/);
      if(om) orig = om[1].trim();
      
      // Extract vernacular: **白话解读：** ...
      var vern="";
      var vm = block.match(/白话解读[：:]\s*([\s\S]*?)(?=\n\s*\*\*出处|\n\s*$|$)/);
      if(vm) vern = vm[1].replace(/\*+$/,'').trim();
      
      if(book||orig||vern){
        h+='<div class="cb"><div class="cbh">';
        h+='<span class="cm">📜</span>';
        if(book) h+='<span class="cbk">《'+E(book)+'》</span>';
        if(chapter) h+='<span class="cbc">'+E(chapter)+'</span>';
        h+='</div><div class="cbb">';
        if(orig) h+='<div class="cbo">'+E(orig)+'</div>';
        if(vern) h+='<div class="cbv"><span class="vt">白话</span><span>'+E(vern)+'</span></div>';
        h+='</div></div>';
      }
    }
  } else {
    // Fallback: try > ** old blockquote format
    var blocks = b.split(/\n>\s*\*\*/);
    if(blocks.length > 1){
      if(blocks[0] && blocks[0].trim()){
        h+='<p style="font-size:.82rem;color:var(--ink-m);margin-bottom:4px">'+MP(blocks[0].trim())+'</p>';
      }
      for(var j=1;j<blocks.length;j++){
        var blk = blocks[j].trim();
        var book2="", orig2="", comment2="";
        var bm2 = blk.match(/《(.+?)》/); if(bm2) book2=bm2[1];
        var om2 = blk.match(/原文[：:]\s*[「「]([\s\S]*?)[」」]/); if(om2) orig2=om2[1].trim();
        var vm2 = blk.match(/白话解读[：:]\s*([\s\S]*?)(?=\n>|\n$|$)/); if(vm2) comment2=vm2[1].trim();
        if(book2||orig2||comment2){
          h+='<div class="cb"><div class="cbh"><span class="cm">📜</span>';
          if(book2) h+='<span class="cbk">《'+E(book2)+'》</span>';
          h+='</div><div class="cbb">';
          if(orig2) h+='<div class="cbo">'+E(orig2)+'</div>';
          if(comment2) h+='<div class="cbv"><span class="vt">白话</span><span>'+E(comment2)+'</span></div>';
          h+='</div></div>';
        }
      }
    }
  }
  
  if(!h) h='<div class="ap">'+MP(b)+'</div>';
  return h;
}

// Deep points: numbered items with **bold** headers
function pD2(b){
  var h="";
  // Split by numbered items: 1. **title** or 1. title
  var items = b.split(/\n(?=\d+[\.\、]\s)/);
  
  if(items.length > 1){
    // Has numbered sections
    for(var i=0;i<items.length;i++){
      var item = items[i].trim();
      if(!item) continue;
      var lines = item.split(/\n/);
      var title = "";
      var body = "";
      for(var j=0;j<lines.length;j++){
        var ln = lines[j].trim();
        if(j===0){
          // First line is the title
          title = ln.replace(/^\d+[\.\、]\s*/,"").replace(/\*\*/g,"");
        }else{
          body += (body?"\n":"") + ln;
        }
      }
      if(title){
        h+='<div class="di"><div class="dt">'+E(title)+'</div>';
        if(body.trim())h+='<div class="db">'+MP(body.trim())+'</div>';
        h+='</div>';
      }
    }
  } else {
    // Try bold headers
    var lines = b.split(/\n/);
    var ct="", cb="";
    for(var k=0;k<lines.length;k++){
      var l = lines[k].trim();
      if(!l) continue;
      var bm = l.match(/^\*\*(.+?)\*\*/);
      if(bm){
        if(ct){
          h+='<div class="di"><div class="dt">'+E(ct)+'</div>';
          if(cb.trim())h+='<div class="db">'+MP(cb.trim())+'</div>';
          h+='</div>';
        }
        ct=bm[1];
        cb=l.replace(/^\*\*.+?\*\*\s*/,"").trim();
      }else{
        cb+=(cb?"\n":"")+l;
      }
    }
    if(ct){
      h+='<div class="di"><div class="dt">'+E(ct)+'</div>';
      if(cb.trim())h+='<div class="db">'+MP(cb.trim())+'</div>';
      h+='</div>';
    }
  }
  if(!h)h='<div class="ap">'+MP(b)+'</div>';
  return h;
}

function pR(b){
  var h="";
  var ls=b.split(/\n/);
  for(var i=0;i<ls.length;i++){
    var l=ls[i].trim();if(!l)continue;
    var m=l.match(/^\d+[\.、\s]+(.+)/);
    var t=m?m[1]:l;
    var bk=t.match(/《(.+?)》(.*)/);
    if(bk){
      h+='<div class="ri"><span class="bkic">📘</span><span class="bkn">《'+E(bk[1])+'》</span>';
      if(bk[2].trim())h+='<span class="bkr">— '+E(bk[2].trim())+'</span>';
      h+='</div>';
    }else{
      h+='<div class="ri"><span class="bkic">📘</span><span>'+E(t)+'</span></div>';
    }
  }
  if(!h)h+='<div class="ap">'+MP(b)+'</div>';
  return h;
}

// References: supports both old (title/snippet) and new (book/excerpt) field names
function rR(r){
  if(!r||!r.length)return"";
  var h='<div class="rb"><div class="rbt">📖 参考来源</div>';
  r.forEach(function(x,i){
    var bk=x.book||x.title||"未知";
    var ch=x.chapter?" · "+x.chapter:"";
    var sn=x.excerpt||x.snippet||"";
    h+='<div class="rr"><span class="rn">'+(i+1)+'</span><div class="ri2"><div class="rs">《'+E(bk)+'》'+E(ch)+'</div><div class="rx">'+E(sn)+'</div></div></div>';
  });
  h+="</div>";
  return h;
}

function rai(a,r){
  var w=document.createElement("div");w.className="mw ai";
  w.innerHTML='<div class="mb"><div class="cp">'+pS(a)+rR(r)+'</div></div>';
  cv.appendChild(w);cv.scrollTop=cv.scrollHeight;
}
function rusr(t){
  var w=document.createElement("div");w.className="mw usr";
  w.innerHTML='<div class="mb">'+E(t)+'</div>';
  cv.appendChild(w);cv.scrollTop=cv.scrollHeight;
}
function rld(){
  var d=document.createElement("div");d.className="ld";
  d.innerHTML="<span></span><span></span><span></span>";
  cv.appendChild(d);cv.scrollTop=cv.scrollHeight;
  return d;
}
'''

html = '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n'
html += '<meta charset="UTF-8">\n'
html += '<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">\n'
html += '<title>中医国学 · 经典问答</title>\n<style>\n' + css + '</style>\n</head>\n<body>\n'
html += '<header class="hd"><h1>📚 中医国学 · 经典问答</h1><div class="sub">跨越千年的智慧，为今日之你而答</div></header>\n'
html += '<div class="cv" id="cv">\n'
html += '<div class="mw ai"><div class="mb"><div class="cp wb">\n'
html += '<p class="wg">你好，我是你的国学典籍助手。</p>\n'
html += '<p class="wd">中医与国学经典中的千年智慧已就绪，请随意提问。</p>\n'
html += '<div class="wh" id="hb">\n'
html += '<span class="whi" data-q="阴阳平衡的核心思想是什么？">☯ 阴阳平衡</span>\n'
html += '<span class="whi" data-q="什么是知行合一？">🧠 知行合一</span>\n'
html += '<span class="whi" data-q="曾国藩如何教导子弟修身？">📖 曾国藩家训</span>\n'
html += '<span class="whi" data-q="应无所住而生其心是什么意思？">🪷 金刚经</span>\n'
html += '<span class="whi" data-q="脾胃虚弱应该如何调理？">🌿 脾胃养生</span>\n'
html += '<span class="whi" data-q="黄帝内经中关于养生的核心论述">💎 黄帝内经养生</span>\n'
html += '</div>\n</div></div></div>\n</div>\n'
html += '<div class="ib">\n<input id="qi" placeholder="输入你的问题，按回车发送…" autofocus>\n<button id="qb">发送</button>\n</div>\n'
html += '<script>\n' + js + '\n</script>\n</body>\n</html>'

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)
print('Done:', len(html), 'chars')


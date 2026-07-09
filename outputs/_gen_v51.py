# -*- coding: utf-8 -*-
import os

OUT = r"C:\Users\35160\Desktop\中医RAG系统\outputs\chatbox.html"
OUT2 = r"C:\Users\35160\Desktop\outputs\chatbox.html"
CSS = r"""/* Design Tokens v5.1 */
:root{--ink:#2c2416;--ink-l:#5c4a32;--ink-m:#8a7a62;--ink-p:#b8a88a;--bg:#f7f3ed;--card:#fffcf7;--acc:#8B4513;--acc-h:#a0522d;--acc-gg:#c9b99a;--acc-s:#c4a882;--acc-w:#fdf6ed;--bd:#e6ddd0;--bd-l:#f0ebe0;--ff-think:"LXGW WenKai","KaiTi","STKaiti","Kai",serif;--sh:0 2px 20px rgba(44,36,22,.06);--sh-s:0 1px 4px rgba(44,36,22,.03);--r-s:8px;--r:14px;--r-l:20px;--mw:740px;--fs:"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans SC",system-ui,sans-serif;--ff:"Noto Serif SC","Source Han Serif SC","PingFang SC","Hiragino Sans GB","Microsoft YaHei",Georgia,serif}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{font-size:clamp(14px,1vw+10px,17px);-webkit-text-size-adjust:100%;-webkit-font-smoothing:antialiased}
body{font-family:var(--ff);background:var(--bg);color:var(--ink);min-height:100dvh;display:flex;flex-direction:column;line-height:1.8;overflow-x:hidden}
.hd{background:linear-gradient(135deg,#5a2d1a,#7a3d22,#8B4513);color:#fff;padding:clamp(10px,2vw,16px) clamp(14px,3vw,28px);text-align:center;box-shadow:0 2px 16px rgba(44,36,22,.18);position:sticky;top:0;z-index:20;flex-shrink:0}
.hd h1{font-size:clamp(1rem,3vw,1.4rem);font-weight:700;letter-spacing:.06em;font-family:var(--fs)}
.hd .sub{font-size:clamp(.65rem,1.4vw,.78rem);opacity:.7;margin-top:3px;letter-spacing:.08em;font-family:var(--fs)}
.cv{flex:1;overflow-y:auto;overflow-x:hidden;padding:clamp(14px,3vw,30px) clamp(8px,3vw,24px);display:flex;flex-direction:column;align-items:center;gap:clamp(16px,2.5vw,24px);scroll-behavior:smooth}
.cv::-webkit-scrollbar{width:4px}
.cv::-webkit-scrollbar-thumb{background:var(--acc-s);border-radius:4px}
.mw{width:100%;max-width:var(--mw);display:flex;flex-direction:column}
.mw.usr{align-items:flex-end}
.mw.ai{align-items:flex-start}
.mb{animation:fU .4s ease-out both;max-width:100%}
.mw.usr .mb{background:var(--acc);color:#fff;padding:clamp(8px,1.5vw,12px) clamp(12px,2vw,18px);border-radius:18px 18px 4px 18px;font-size:clamp(.85rem,1.8vw,.93rem);line-height:1.6;box-shadow:var(--sh-s);max-width:min(85%,400px);word-break:break-word;font-family:var(--fs)}
.mw.ai .mb{width:100%;background:var(--card);border-radius:var(--r-l);box-shadow:var(--sh);border:1px solid var(--bd);overflow:hidden}
.mw.ai .cp{padding:clamp(18px,3vw,28px) clamp(16px,3vw,28px)}
.wb{padding:clamp(20px,3vw,32px);text-align:center}
.wg{font-size:clamp(1rem,2.2vw,1.15rem);font-weight:700;color:var(--ink);margin-bottom:6px;font-family:var(--fs)}
.wd{font-size:clamp(.8rem,1.6vw,.88rem);color:var(--ink-l);line-height:1.7;margin-bottom:20px}
.wh{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
.whi{display:inline-block;padding:8px 14px;background:var(--acc-w);border:1px solid var(--bd);border-radius:var(--r-s);font-size:clamp(.72rem,1.4vw,.8rem);color:var(--ink-l);cursor:pointer;transition:all .2s ease;font-family:var(--fs)}
.whi:hover{background:var(--acc);color:#fff;border-color:var(--acc);transform:translateY(-1px);box-shadow:0 2px 8px rgba(139,69,19,.2)}
.tw-wrap{margin-bottom:14px;border-radius:var(--r);overflow:hidden;border:1px solid var(--acc-gg);background:#fcf9f4}
.tw-header{display:flex;align-items:center;gap:8px;padding:10px 14px;background:linear-gradient(135deg,#f5ede4,#fdf6ed);cursor:pointer;border-bottom:1px solid var(--acc-gg)}
.tw-header:hover{background:linear-gradient(135deg,#efe3d6,#f8efdf)}
.tw-icon{width:24px;height:24px;display:flex;align-items:center;justify-content:center;border-radius:50%;background:var(--acc-w);border:1px solid var(--acc-gg)}
.tw-title{font-size:clamp(.75rem,1.5vw,.82rem);font-weight:600;color:var(--acc);font-family:var(--fs);flex:1}
.tw-toggle{font-size:.7rem;color:var(--ink-m);transition:transform .3s ease}
.tw-toggle.open{transform:rotate(180deg)}
.tw-body{padding:0 16px;max-height:0;overflow:hidden;transition:all .4s cubic-bezier(.4,0,.2,1)}
.tw-body.open{max-height:500px;padding:14px 16px;overflow-y:auto}
.tw-text{font-family:var(--ff-think);font-size:clamp(.78rem,1.5vw,.85rem);line-height:1.7;color:var(--ink-l);white-space:pre-wrap}
.sec{margin:clamp(14px,2.5vw,20px) 0;scroll-margin-top:16px}
.sech{display:flex;align-items:center;gap:clamp(6px,1.5vw,10px);margin-bottom:clamp(8px,1.5vw,12px);padding-bottom:clamp(6px,1vw,10px);border-bottom:1px solid var(--bd-l)}
.sech .si{width:clamp(26px,4vw,30px);height:clamp(26px,4vw,30px);display:flex;align-items:center;justify-content:center;border-radius:8px;flex-shrink:0;font-size:clamp(1rem,2vw,1.15rem)}
.sech .sl{font-size:clamp(.82rem,1.8vw,.92rem);font-weight:700;color:var(--ink);font-family:var(--fs)}
.se .si{background:#fdf2e9;color:#c0392b}
.sc .si{background:var(--acc-w);color:var(--acc)}
.sd .si{background:#eaf2f8;color:#2c3e50}
.sl2 .si{background:#eafaf1;color:#1e8449}
.sr .si{background:#f4ecf7;color:#6c3483}
.cb{margin:clamp(12px,2vw,16px) 0;background:var(--acc-w);border-radius:var(--r);border:1px solid var(--bd);overflow:hidden}
.cbh{display:flex;align-items:center;gap:6px;padding:clamp(8px,1.5vw,11px) clamp(10px,2vw,14px);background:rgba(139,69,19,.04);border-bottom:1px solid var(--bd-l)}
.cbh .cm{font-size:clamp(.75rem,1.5vw,.85rem)}
.cbh .cbk{font-size:clamp(.78rem,1.6vw,.85rem);font-weight:700;color:var(--acc);font-family:var(--fs)}
.cbh .cbc{font-size:clamp(.7rem,1.4vw,.78rem);color:var(--ink-m)}
.cbb{padding:clamp(10px,2vw,14px)}
.cbo{font-size:clamp(.8rem,1.7vw,.88rem);color:var(--ink-l);line-height:1.8;padding:clamp(8px,1.5vw,10px) clamp(10px,2vw,14px);background:rgba(255,255,255,.65);border-radius:var(--r-s);border-left:3px solid var(--acc-s);margin-bottom:clamp(8px,1.5vw,10px)}
.cbv{font-size:clamp(.78rem,1.5vw,.85rem);color:var(--ink-m);line-height:1.7;display:flex;gap:6px;align-items:flex-start}
.cbv .vt{font-size:clamp(.65rem,1.2vw,.72rem);background:var(--acc);color:#fff;padding:1px 8px;border-radius:10px;flex-shrink:0;font-weight:600;font-family:var(--fs);margin-top:2px}
.di{margin:clamp(12px,2vw,16px) 0}
.dt{font-size:clamp(.86rem,1.7vw,.92rem);font-weight:700;color:var(--ink);margin-bottom:4px;font-family:var(--fs);display:flex;align-items:baseline;gap:6px}
.dt::before{content:"";display:inline-block;width:5px;height:5px;background:var(--acc);border-radius:50%;flex-shrink:0}
.db{font-size:clamp(.8rem,1.6vw,.88rem);color:var(--ink-l);line-height:1.75;padding-left:clamp(10px,1.5vw,14px)}
.ap{font-size:clamp(.85rem,1.7vw,.92rem);color:var(--ink-l);line-height:1.8;margin:clamp(8px,1.5vw,10px) 0}
.ap p{margin-bottom:.6em}
.rb{margin:16px 0 0;padding:14px 16px;background:#f8f5f0;border-radius:var(--r);border:1px solid var(--bd)}
.rbt{font-size:clamp(.78rem,1.5vw,.84rem);font-weight:700;color:var(--ink);margin-bottom:10px;font-family:var(--fs)}
.rr{display:flex;gap:10px;padding:6px 0;border-bottom:1px solid var(--bd-l);align-items:flex-start}
.rr:last-child{border-bottom:none}
.rn{flex-shrink:0;width:20px;height:20px;border-radius:50%;background:var(--acc);color:#fff;display:flex;align-items:center;justify-content:center;font-size:.65rem;font-weight:700;font-family:var(--fs);margin-top:2px}
.ri2{flex:1;min-width:0}
.rs{font-size:clamp(.75rem,1.4vw,.82rem);font-weight:600;color:var(--acc);margin-bottom:2px;font-family:var(--fs)}
.rx{font-size:clamp(.7rem,1.3vw,.78rem);color:var(--ink-m);line-height:1.5;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.ld{display:flex;align-items:center;gap:6px;padding:16px 20px;background:var(--card);border-radius:var(--r-l);box-shadow:var(--sh);border:1px solid var(--bd)}
.ld span{width:8px;height:8px;border-radius:50%;background:var(--acc-s);animation:ldB 1.2s ease-in-out infinite}
.ld span:nth-child(2){animation-delay:.15s}
.ld span:nth-child(3){animation-delay:.3s}
@keyframes ldB{0%,80%,100%{transform:scale(.6);opacity:.4}40%{transform:scale(1);opacity:1}}
.ib{position:sticky;bottom:0;background:linear-gradient(0deg,var(--bg) 60%,transparent);padding:clamp(10px,2vw,14px) clamp(10px,3vw,20px) clamp(14px,2.5vw,20px);display:flex;gap:10px;flex-shrink:0;z-index:10}
.ib input{flex:1;padding:clamp(10px,1.8vw,14px) clamp(14px,2.5vw,18px);border:2px solid var(--bd);border-radius:var(--r-l);font-size:clamp(.85rem,1.7vw,.92rem);font-family:var(--ff);outline:none;background:var(--card);color:var(--ink);transition:border-color .25s ease,box-shadow .25s ease}
.ib input:focus{border-color:var(--acc-s);box-shadow:0 0 0 3px rgba(196,168,130,.15)}
.ib input::placeholder{color:var(--ink-p)}
.ib button{padding:clamp(10px,1.5vw,14px) clamp(16px,2.5vw,24px);background:linear-gradient(135deg,#8B4513,#a0522d);color:#fff;border:none;border-radius:var(--r-l);font-size:clamp(.85rem,1.7vw,.92rem);font-weight:600;font-family:var(--fs);cursor:pointer;transition:all .2s ease;white-space:nowrap}
.ib button:hover{background:linear-gradient(135deg,#7a3d22,#8B4513);transform:translateY(-1px);box-shadow:0 3px 10px rgba(139,69,19,.25)}
@keyframes fU{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
.typing-cursor{display:inline-block;width:2px;height:1.1em;background:var(--acc);margin-left:1px;vertical-align:text-bottom;animation:blink .8s step-end infinite}
@keyframes blink{50%{opacity:0}}
"""
print("CSS part written")
JS = r"""
var cv=document.getElementById("cv"),qi=document.getElementById("qi"),qb=document.getElementById("qb"),isLoading=false;
function E(t){var d=document.createElement("div");d.appendChild(document.createTextNode(t));return d.innerHTML;}

function createThinkBox(text){
  var w=document.createElement("div");w.className="tw-wrap";
  var h=document.createElement("div");h.className="tw-header";
  h.innerHTML='<span class="tw-icon">\u{1F9E0}</span><span class="tw-title">思考过程</span><span class="tw-toggle open">\u25BC</span>';
  var b=document.createElement("div");b.className="tw-body open";
  var t=document.createElement("div");t.className="tw-text";t.textContent=text||"思考中…";
  b.appendChild(t);
  h.onclick=function(){b.classList.toggle("open");h.querySelector(".tw-toggle").classList.toggle("open");};
  w.appendChild(h);w.appendChild(b);
  return w;
}

function typeWriter(el,text,cb){
  var i=0;el.textContent="";
  var cs=document.createElement("span");cs.className="typing-cursor";el.appendChild(cs);
  function tp(){
    if(i<text.length){
      var ch=text.charAt(i);
      var d=20;
      if("，。！？；：".indexOf(ch)!==-1) d=100;
      else if("、；：".indexOf(ch)!==-1) d=70;
      else if("\n".indexOf(ch)!==-1) d=140;
      el.insertBefore(document.createTextNode(ch),cs);i++;
      var cve=document.getElementById("cv");if(cve)cve.scrollTop=cve.scrollHeight;
      setTimeout(tp,d);
    }else{if(cs.parentNode)cs.parentNode.removeChild(cs);if(cb)cb();}
  }
  tp();
}

// Strip ** markers completely
function cln(t){return t.replace(/\*\*/g,"");}

function renderAnswer(text,refs){
  var lines=text.split("\n"),html="",i=0;
  while(i<lines.length){
    var l=lines[i],t=l.trim();
    if(!t){i++;continue;}
    // Citation block (must check before section header!)
    if(t.indexOf("**出处：")===0||t.indexOf("出处：")===0){
      var ct="";
      while(i<lines.length){
        ct+=lines[i]+"\n";i++;
        var nn="";
        for(var j=i;j<lines.length;j++){if(lines[j].trim()){nn=lines[j].trim();break;}}
        if(/^\*\*.*\*\*$/.test(nn)&&nn.length<60) break;
        if(nn.indexOf("出处：")===0||nn.indexOf("**出处：")===0) continue;
        break;
      }
      html+=parseCiteBlocks(ct.trim());
      continue;
    }
    // Section header: **...**
    if(/^\*\*.*\*\*$/.test(t) && t.length<60){
      var inner=t.replace(/^\*\*/,"").replace(/\*\*$/,"").trim();
      var sec=renderSectionHeader(inner);
      if(sec){
        html+=sec;i++;
        var body=[];
        while(i<lines.length){
          var nl=lines[i].trim();
          if(!nl){i++;continue;}
          if(/^\*\*.*\*\*$/.test(nl)&&nl.length<60) break;
          if(nl.indexOf("出处：")===0||nl.indexOf("**出处：")===0) break;
          body.push(lines[i]);i++;
        }
        if(body.length>0){
          var bt=body.join("\n").trim();
          if(inner.indexOf("深度阐释")!==-1) html+=parseDeep(bt);
          else if(inner.indexOf("经典溯源")!==-1||inner.indexOf("溯源")!==-1) html+=parseCiteBlocks(bt);
          else html+='<div class="ap"><p>'+cln(bt).replace(/\n\n/g,"</p><p>").replace(/\n/g,"<br>")+"</p></div>";
        }
        html+="</div>";
        continue;
      }
    }
    html+='<div class="ap"><p>'+cln(t)+"</p></div>";i++;
  }
  if(refs&&refs.length>0){
    html+='<div class="rb"><div class="rbt">📖 参考来源</div>';
    refs.forEach(function(r,ri){
      var bk=r.book||r.title||"未知",ch=r.chapter?" · "+r.chapter:"",sn=r.excerpt||r.snippet||"";
      html+='<div class="rr"><span class="rn">'+(ri+1)+'</span><div class="ri2"><div class="rs">《'+E(bk)+"》"+E(ch)+'</div><div class="rx">'+E(sn)+"</div></div></div>";
    });
    html+="</div>";
  }
  return html;
}

function renderSectionHeader(inner){
  var icon="📌",cls="sc";
  if(inner.indexOf("精要")!==-1){icon="💡";cls="se";}
  else if(inner.indexOf("溯源")!==-1){icon="📖";cls="sc";}
  else if(inner.indexOf("阐释")!==-1){icon="🧠";cls="sd";}
  else if(inner.indexOf("践行")!==-1){icon="🌿";cls="sl2";}
  else if(inner.indexOf("阅读")!==-1){icon="📚";cls="sr";}
    var title=inner.replace(/^[^\x00-\x7f]+\s*/u,"").trim();  if(!title) return "";
  if(!title)return"";
  return '<div class="sec"><div class="sech"><span class="si">'+icon+'</span><span class="sl">'+E(title)+"</span></div>";
}

function parseCiteBlocks(text){
  var blocks=text.split(/(?=出处：)/),h="";
  for(var bi=0;bi<blocks.length;bi++){
    var b=blocks[bi].trim();if(!b)continue;
    var cm=b.match(/《(.+?)》\s*·\s*(.+?)(?:\*\*)?$/m)||b.match(/《(.+?)》/);
    if(!cm)continue;
    var book=cm[1],chapter=cm[2]||"";
    var origMatch=b.match(/原文：\s*「(.+?)」/);
    var orig=origMatch?origMatch[1]:"";
    var lines=b.split("\n"),interp="",inInterp=false;
    for(var li=0;li<lines.length;li++){
      var l=lines[li].trim();
      if(l.indexOf("释义解读")!==-1){
        inInterp=true;
        var after=l.replace(/.*释义解读[：:]\s*\*{0,2}\s*/,"");
        if(after)interp+=after;
      }else if(inInterp){if(!l)break;interp+=(interp?"\n":"")+l;}
    }
    h+='<div class="cb"><div class="cbh"><span class="cm">📖</span><span class="cbk">《'+E(book)+"》</span>";
    if(chapter)h+='<span class="cbc"> · '+E(chapter)+"</span>";
    h+='</div><div class="cbb">';
    if(orig)h+='<div class="cbo">原文：「'+E(orig)+'」</div>';
    if(interp)h+='<div class="cbv"><span class="vt">释义</span><span>'+cln(interp)+"</span></div>";
    h+="</div></div>";
  }
  return h;
}

function parseDeep(text){
  var lines=text.split("\n"),items=[],cur=null;
  for(var i=0;i<lines.length;i++){
    var l=lines[i].trim();if(!l)continue;
    var bm=l.match(/^\*\*(.+?)\*\*/);
    if(bm){
      if(cur)items.push(cur);
      var rest=l.replace(/^\*\*.+?\*\*/,"").trim();
      cur={title:cln(bm[1].trim()),body:rest};
    }else if(cur){cur.body+=(cur.body?"\n":"")+l;}
  }
  if(cur)items.push(cur);
  if(!items.length)return'<div class="ap"><p>'+cln(text)+"</p></div>";
  var h="";
  items.forEach(function(it){
    if(it.title)h+='<div class="di"><div class="dt">'+cln(it.title)+"</div>";
    else h+='<div class="di">';
    if(it.body)h+='<div class="db">'+cln(it.body).replace(/\n\n/g,"</p><p>").replace(/\n/g,"<br>")+"</div>";
    h+="</div>";
  });
  return h;
}

function showLoading(){
  var d=document.createElement("div");d.className="ld";
  d.innerHTML="<span></span><span></span><span></span>";cv.appendChild(d);cv.scrollTop=cv.scrollHeight;
  return d;
}
function addUserMsg(t){
  var w=document.createElement("div");w.className="mw usr";
  w.innerHTML='<div class="mb">'+E(t)+"</div>";cv.appendChild(w);cv.scrollTop=cv.scrollHeight;
}
function addAIResponse(answer,refs,thinkText){
  var w=document.createElement("div");w.className="mw ai";
  var mb=document.createElement("div");mb.className="mb";
  var cp=document.createElement("div");cp.className="cp";
  var tw=createThinkBox(thinkText||"分析中…");cp.appendChild(tw);
  var cd=document.createElement("div");cp.appendChild(cd);
  mb.appendChild(cp);w.appendChild(mb);cv.appendChild(w);cv.scrollTop=cv.scrollHeight;
  var te=document.createElement("div");te.className="ap";cd.appendChild(te);
  typeWriter(te,answer,function(){
    cd.innerHTML=renderAnswer(answer,refs);cv.scrollTop=cv.scrollHeight;
  });
  return w;
}
function sendQuery(){
  if(isLoading)return;
  var q=qi.value.trim();if(!q)return;
  isLoading=true;qb.disabled=true;qi.disabled=true;
  addUserMsg(q);qi.value="";
  var loader=showLoading();
  var xhr=new XMLHttpRequest();
  xhr.open("POST","/rag/query",true);
  xhr.setRequestHeader("Content-Type","application/json;charset=UTF-8");
  xhr.onload=function(){
    if(loader.parentNode)loader.parentNode.removeChild(loader);
    if(xhr.status===200){
      var data=JSON.parse(xhr.responseText);
      var steps="1. 理解查询意图\n2. 检索相关文献\n3. 筛选最佳参考\n4. 组织回答结构\n5. 精炼语言表达";
      addAIResponse(data.answer||"",data.references||[],steps);
    }else{
      var ed=document.createElement("div");ed.className="mw ai";
      ed.innerHTML='<div class="mb"><div class="cp" style="color:#c0392b;padding:16px;">请求失败：'+E(xhr.statusText||"未知错误")+"</div></div>";
      cv.appendChild(ed);
    }
    isLoading=false;qb.disabled=false;qi.disabled=false;qi.focus();
  };
  xhr.onerror=function(){
    if(loader.parentNode)loader.parentNode.removeChild(loader);
    var ed=document.createElement("div");ed.className="mw ai";
    ed.innerHTML='<div class="mb"><div class="cp" style="color:#c0392b;padding:16px;">网络错误，请检查连接后重试</div></div>';
    cv.appendChild(ed);
    isLoading=false;qb.disabled=false;qi.disabled=false;qi.focus();
  };
  xhr.send(JSON.stringify({question:q}));
}
document.addEventListener("click",function(e){
  var t=e.target.closest(".whi");
  if(t){qi.value=t.getAttribute("data-q")||t.textContent.trim();sendQuery();}
});
qi.addEventListener("keydown",function(e){
  if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();sendQuery();}
});
qb.addEventListener("click",sendQuery);
"""
html = '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">\n<title>中医国学 · 经典问答</title>\n<style>\n' + CSS + '\n</style>\n</head>\n<body>\n<header class="hd"><h1>📚 中医国学 · 经典问答</h1><div class="sub">跨越千年的智慧，为今日之你而答</div></header>\n<div class="cv" id="cv">\n<div class="mw ai"><div class="mb"><div class="cp wb">\n<p class="wg">你好，我是你的国学典籍助手。</p>\n<p class="wd">中医与国学经典中的千年智慧已就绪，请随意提问。</p>\n<div class="wh" id="hb">\n<span class="whi" data-q="阴阳平衡的核心思想是什么？">☯ 阴阳平衡</span>\n<span class="whi" data-q="什么是知行合一？">🧠 知行合一</span>\n<span class="whi" data-q="曾国藩如何教导子弟修身？">📖 曾国藩家训</span>\n<span class="whi" data-q="应无所住而生其心是什么意思？">🪷 金刚经</span>\n<span class="whi" data-q="脾胃虚弱应该如何调理？">🌿 脾胃养生</span>\n<span class="whi" data-q="黄帝内经中关于养生的核心论述">💎 黄帝内经养生</span>\n</div>\n</div></div></div>\n</div>\n<div class="ib">\n<input id="qi" placeholder="输入你的问题，按回车发送…" autofocus>\n<button id="qb">发送</button>\n</div>\n<script>\n' + JS + '\n</script>\n</body>\n</html>'

for p in [OUT, OUT2]:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(html)
print(f"Done! {len(html)} chars")

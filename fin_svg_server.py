#!/usr/bin/env python3
"""
fin_svg_server.py  –  single-file Flask app that hosts a styled, client-only
rocket-fin SVG generator.  Run:

    pip install flask
    python fin_svg_server.py
"""

from flask import Flask, Response
app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Fin SVG Generator</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">

<style>
:root{
  --bg:#f7f8fa;
  --card:#ffffff;
  --border:#d4d7dd;
  --accent:#4361ee;
}
*{box-sizing:border-box;font-family:'Inter',sans-serif;margin:0;padding:0}
body{
  background:var(--bg);
  display:flex;
  justify-content:center;
  align-items:center;
  min-height:100vh;
  padding:1rem;
}
.card{
  background:var(--card);
  border:1px solid var(--border);
  border-radius:12px;
  padding:1.5rem;
  box-shadow:0 4px 14px rgba(0,0,0,.06);
  width:clamp(300px,90vw,480px);
}
h1{font-size:1.4rem;margin-bottom:1rem;color:#111}
form label{
  display:flex;
  justify-content:space-between;
  align-items:center;
  margin:.55rem 0;
  font-size:.95rem;
}
form input{
  width:7.3rem;
  padding:.45rem .5rem;
  border:1px solid var(--border);
  border-radius:6px;
  font-size:.95rem;
}
form input:focus{outline:2px solid var(--accent33);border-color:var(--accent)}
button{
  margin-top:1rem;
  padding:.45rem 1.1rem;
  background:var(--accent);
  border:none;
  border-radius:6px;
  color:#fff;
  font-size:.95rem;
  cursor:pointer;
  transition:.2s;
}
button:hover{background:#3452d5}
#msg{margin-top:.8rem;font-size:.9rem;color:#444}
.object-wrap{
  border:1px dashed var(--border);
  border-radius:8px;
  margin-top:1rem;
  aspect-ratio:3/1.3;
  width:100%;
  display:flex;
  align-items:center;
  justify-content:center;
  overflow:hidden;
}
object{width:100%;height:100%}
a.download{
  display:inline-block;
  margin-top:.9rem;
  font-size:.95rem;
  color:var(--accent);
  text-decoration:none;
}
a.download:hover{text-decoration:underline}

@media (max-width: 480px) {
  .card {
    padding: 1rem;
  }
  h1 {
    font-size: 1.2rem;
  }
  form label {
    flex-direction: column;
    align-items: flex-start;
    margin: 0.8rem 0;
  }
  form input {
    width: 100%;
    margin-top: 0.3rem;
  }
}
</style>
</head>
<body>
  <div class="card">
    <h1>Fin Outline ➜ SVG</h1>

    <form id="f">
      <label>Root chord (mm)&nbsp;<input type="number" id="rc" step="1" value="28"></label>
      <label>Tip&nbsp;chord (mm)&nbsp;&nbsp;<input type="number" id="tc" step="1" value="8"></label>
      <label>Height (mm)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type="number" id="h"  step="1" value="61"></label>
      <label>Sweep length (mm)<input type="number" id="sw" step="1" value="-29"></label>
    </form>

    <div id="msg"></div>
    <div class="object-wrap"><object id="preview" type="image/svg+xml"></object></div>
    <a id="dlink" class="download" href="#" download="fin.svg" hidden>⇩ Download SVG</a>
  </div>

<script>
function buildSVG(rc, tc, h, sw, margin){
  // Convert mm to inches
  const mmToInch = 0.0393701;
  rc *= mmToInch;
  tc *= mmToInch;
  h *= mmToInch;
  sw *= mmToInch;
  margin *= mmToInch;
  
  const pts=[[0,0],[rc,0],[sw+tc,h],[sw,h]];
  const minX=Math.min(...pts.map(p=>p[0])),
        minY=Math.min(...pts.map(p=>p[1]));
  const s=pts.map(([x,y])=>[x-minX+margin, y-minY+margin]);
  const w=Math.max(...s.map(p=>p[0]))+margin,
        ht=Math.max(...s.map(p=>p[1]))+margin;
  const path='M '+s.map(([x,y])=>`${x},${ht-y}`).join(' L ')+' Z';
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${w}in" height="${ht}in" viewBox="0 0 ${w} ${ht}">
  <path d="${path}" stroke="black" fill="none" stroke-width="0.01"/>
</svg>`;
}

function generateSVG(){
  const rc=parseFloat(rc_in.value), tc=parseFloat(tc_in.value),
        h =parseFloat(h_in.value),  sw=parseFloat(sw_in.value),
        m = 5; // Margin in mm (was 0.2 inches)
  if([rc,tc,h,sw].some(isNaN)){
    msg.textContent='❌ Please enter valid numbers.'; return;
  }
  const svg=buildSVG(rc,tc,h,sw,m),
        blob=new Blob([svg],{type:'image/svg+xml'}),
        url=URL.createObjectURL(blob);
  preview.data=url;
  dlink.href=url;
  dlink.download=`fin_${Date.now()}.svg`;
  dlink.hidden=false;
  msg.textContent='';
}

const rc_in=document.getElementById('rc'),
      tc_in=document.getElementById('tc'),
      h_in =document.getElementById('h'),
      sw_in=document.getElementById('sw'),
      msg  =document.getElementById('msg'),
      preview=document.getElementById('preview'),
      dlink=document.getElementById('dlink');

// Add event listeners to all inputs
[rc_in, tc_in, h_in, sw_in].forEach(input => {
  input.addEventListener('input', generateSVG);
});

// Generate SVG on page load
window.addEventListener('load', generateSVG);
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return Response(HTML, mimetype="text/html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

#!/usr/bin/env python3
"""
fin_svg_server.py
Tiny Flask wrapper that hosts a pure-client-side fin-outline → SVG generator.
"""

from flask import Flask, Response

app = Flask(__name__)

# ------------------------------------------------------------------ HTML + JS
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Rocket-Fin SVG Generator</title>
<style>
  body{font-family:system-ui,Arial;margin:2rem;max-width:480px}
  label{display:block;margin:.4rem 0}
  input{width:7rem}
  #preview{border:1px dashed #888;margin-top:1rem}
  button{margin-top:1rem;padding:.3rem .8rem}
  a.download{display:inline-block;margin-top:.6rem}
</style>
</head>
<body>
<h2>Fin Outline → SVG (inches)</h2>

<label>Root chord&nbsp;<input type="number" id="rc"  step="any" value="1.1"></label>
<label>Tip&nbsp;chord&nbsp;&nbsp;<input type="number" id="tc"  step="any" value="0.3"></label>
<label>Height&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type="number" id="h"   step="any" value="2.4"></label>
<label>Sweep length<input type="number" id="sw"  step="any" value="-1.146"></label>
<label>Margin (opt.)<input type="number" id="m"   step="any" value="0.2"></label>

<button id="gen">Generate</button>
<div id="msg"></div>

<object id="preview" type="image/svg+xml" width="100%" height="200"></object>
<a id="dlink" class="download" href="#" download="fin.svg" hidden>Download SVG</a>

<script>
function buildSVG(rc, tc, h, sw, margin){
  const pts=[
    [0,0],
    [rc,0],
    [sw+tc,h],
    [sw,h]
  ];

  const minX=Math.min(...pts.map(p=>p[0]));
  const minY=Math.min(...pts.map(p=>p[1]));
  const shifted=pts.map(([x,y])=>[x-minX+margin, y-minY+margin]);
  const w=Math.max(...shifted.map(p=>p[0]))+margin;
  const ht=Math.max(...shifted.map(p=>p[1]))+margin;

  const path='M '+shifted.map(([x,y])=>`${x},${ht-y}`).join(' L ')+' Z';

  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="${w}in" height="${ht}in"
     viewBox="0 0 ${w} ${ht}">
  <path d="${path}" stroke="black" fill="none" stroke-width="0.01"/>
</svg>`;
}

document.getElementById('gen').onclick = () => {
  const rc=parseFloat(rc_input.value),
        tc=parseFloat(tc_input.value),
        h =parseFloat(h_input.value),
        sw=parseFloat(sw_input.value),
        m =parseFloat(m_input.value)||0;

  if([rc,tc,h,sw].some(isNaN)){
    msg.textContent='Please enter valid numbers.';
    return;
  }
  const svg=buildSVG(rc,tc,h,sw,m);
  const blob=new Blob([svg],{type:'image/svg+xml'});
  const url=URL.createObjectURL(blob);

  preview.data=url;
  dlink.href=url;
  dlink.download=`fin_${Date.now()}.svg`;
  dlink.hidden=false;
  msg.textContent='SVG generated – preview below.';
};

// shortcut handles
const rc_input=document.getElementById('rc'),
      tc_input=document.getElementById('tc'),
      h_input =document.getElementById('h'),
      sw_input=document.getElementById('sw'),
      m_input =document.getElementById('m'),
      msg     =document.getElementById('msg'),
      preview =document.getElementById('preview'),
      dlink   =document.getElementById('dlink');
</script>
</body>
</html>
"""

# ------------------------------------------------------------------ routes
@app.route("/")
def index():
    return Response(HTML, mimetype="text/html")

# ------------------------------------------------------------------ main
if __name__ == "__main__":
    app.run(debug=True)

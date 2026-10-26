# -*- coding: utf-8 -*-
"""Build a 1920x1080 anime-tech poster HTML from a JSON content config.

Usage: python build_poster.py <config.json> <out.html>

The layout is fixed by the skill (left info column / right character / bottom
ecosystem bar); only the content varies per post. Keeping the shell here and
the words in JSON is what makes the series look like one system.
"""
import json
import sys
from pathlib import Path
from string import Template

TEMPLATE = Template(r"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>$tech_rest poster</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{width:1920px;height:1080px;overflow:hidden}
  body{font-family:"Segoe UI","Microsoft YaHei",sans-serif;background:#E8EDF5;position:relative}
  .bg{position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover;object-position:center}
  .wrap{position:absolute;left:90px;top:58px;width:945px}
  .badges{display:flex;align-items:center;gap:12px;margin-bottom:18px}
  .b1{background:linear-gradient(135deg,#1F8FE0,#1F6FEB);color:#fff;font-size:16px;font-weight:600;
      padding:7px 18px;border-radius:999px;letter-spacing:.5px}
  .b2{color:#48607E;font-size:13px;font-weight:600;letter-spacing:2.2px;padding:7px 16px;
      border-radius:999px;border:1px solid rgba(72,96,126,.35)}
  .tech{font-size:134px;font-weight:900;letter-spacing:-3px;line-height:1;color:#16233A;margin-bottom:8px}
  .tech .n{color:#1F8FE0}
  .title{font-size:42px;font-weight:700;color:#1B2B44;letter-spacing:.5px;margin-bottom:12px}
  .slogan{font-size:21px;color:#5A6E86;margin-bottom:24px}
  .chips{display:flex;gap:10px;margin-bottom:26px}
  .chip{font-size:15px;color:#24405E;background:rgba(255,255,255,.8);
        border:1px solid rgba(31,143,224,.3);border-radius:999px;padding:7px 16px}
  .cards{display:grid;grid-template-columns:1fr 1fr;gap:18px 22px;margin-bottom:26px}
  .card{background:rgba(255,255,255,.72);border:1px solid rgba(255,255,255,.95);
        border-radius:14px;padding:14px 17px;box-shadow:0 4px 16px rgba(30,60,100,.07)}
  .card .h{display:flex;align-items:center;gap:9px;font-size:18px;font-weight:700;
           color:#1B2B44;margin-bottom:7px}
  .card .p{font-size:14px;line-height:1.5;color:#5E7590}
  .row{display:flex;gap:22px;height:236px}
  .code{width:543px;height:100%;background:#1A2233;border-radius:14px;padding:14px 18px;
        box-shadow:0 10px 26px rgba(20,40,70,.22);overflow:hidden}
  .code .bar{display:flex;align-items:center;gap:7px;margin-bottom:10px}
  .dot{width:10px;height:10px;border-radius:50%}
  .code .fn{margin-left:8px;font-family:"Cascadia Mono",Consolas,monospace;font-size:12.5px;color:#7C8DA6}
  .code pre{font-family:"Cascadia Mono",Consolas,monospace;font-size:12.5px;line-height:1.78;
            color:#C8D6E8;white-space:pre}
  .code .c{color:#5E7A9E}
  .code .k{color:#4FC3F7}
  .code .s{color:#7EE0A8}
  .why{flex:1;height:100%;background:rgba(255,255,255,.72);border:1px solid rgba(255,255,255,.95);
       border-radius:14px;padding:16px 18px;box-shadow:0 4px 16px rgba(30,60,100,.07)}
  .why .h{font-size:17px;font-weight:700;color:#1B2B44;margin-bottom:12px}
  .why li{list-style:none;font-size:14.5px;line-height:1.45;color:#4E6480;
          margin-bottom:11px;padding-left:24px;position:relative}
  .why li:before{content:"\2713";position:absolute;left:0;top:0;color:#1F8FE0;font-weight:700}
  .bbar{position:absolute;left:0;bottom:0;width:1920px;height:110px;
        background:linear-gradient(90deg,#14203A,#1B3054 55%,#1E3C66);
        display:flex;align-items:center;padding:0 90px}
  .bb-name{font-size:21px;font-weight:800;color:#fff;letter-spacing:.5px;
           display:flex;align-items:baseline;gap:10px}
  .bb-name span{font-size:13px;font-weight:500;color:#8FAFD4;letter-spacing:.5px}
  .bb-sep{width:1px;height:34px;background:rgba(255,255,255,.22);margin:0 30px}
  .bb-list{display:flex;align-items:center;list-style:none}
  .bb-list li{font-size:16px;color:#B7CBE4;padding:0 16px;position:relative}
  .bb-list li+li:before{content:"";position:absolute;left:0;top:50%;width:4px;height:4px;
                        margin-top:-2px;border-radius:50%;background:#2E7BC4}
  .bb-logo{margin-left:auto;font-size:13px;font-weight:700;letter-spacing:2.5px;color:#6E90BA}
</style>
</head>
<body>
<img class="bg" src="$bg" alt="">
<div class="wrap">
  <div class="badges"><div class="b1">$badge_main</div><div class="b2">$badge_sub</div></div>
  <div class="tech"><span class="n">$tech_lead</span>$tech_rest</div>
  <div class="title">$title</div>
  <div class="slogan">$slogan</div>
  <div class="chips">$chips</div>
  <div class="cards">$cards</div>
  <div class="row">
    <div class="code">
      <div class="bar"><span class="dot" style="background:#FF5F57"></span><span class="dot" style="background:#FEBC2E"></span><span class="dot" style="background:#28C840"></span><span class="fn">$code_file</span></div>
      <pre>$code</pre>
    </div>
    <div class="why">
      <div class="h">$why_title</div>
      <ul>$why</ul>
    </div>
  </div>
</div>
<div class="bbar">
  <div class="bb-name">$bar_name<span>$bar_sub</span></div>
  <div class="bb-sep"></div>
  <ul class="bb-list">$bar_items</ul>
  <div class="bb-logo">ANIME &times; TECH</div>
</div>
</body>
</html>
""")


def build(cfg: dict) -> str:
    chips = "".join(f'<div class="chip">{c}</div>' for c in cfg["chips"])
    cards = "".join(
        f'<div class="card"><div class="h"><span>{c["i"]}</span>{c["h"]}</div>'
        f'<div class="p">{c["p"]}</div></div>'
        for c in cfg["cards"]
    )
    why = "".join(f"<li>{w}</li>" for w in cfg["why"])
    bar_items = "".join(f"<li>{b}</li>" for b in cfg["bar_items"])

    return TEMPLATE.substitute(
        bg=cfg["bg"],
        badge_main=cfg["badge_main"],
        badge_sub=cfg["badge_sub"],
        tech_lead=cfg["tech_lead"],
        tech_rest=cfg["tech_rest"],
        title=cfg["title"],
        slogan=cfg["slogan"],
        chips=chips,
        cards=cards,
        code_file=cfg["code_file"],
        code="\n".join(cfg["code"]),
        why_title=cfg["why_title"],
        why=why,
        bar_name=cfg["bar_name"],
        bar_sub=cfg["bar_sub"],
        bar_items=bar_items,
    )


def main(cfg_path: str, out_html: str) -> None:
    cfg = json.loads(Path(cfg_path).read_text(encoding="utf-8"))
    Path(out_html).write_text(build(cfg), encoding="utf-8")
    print(f"OK -> {out_html}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

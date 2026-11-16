# -*- coding: utf-8 -*-
"""专柜+产品是主角：产品占主视觉、最清晰最亮，场景/价屏只做陪衬（staging only）。"""
import json, os, shutil, sys, threading, time
STG="/root/_stage_20261114_v5"; APP="/var/www/sunlei_520_v2"; H="/tmp/hero4"
OUT="/tmp/hero4_out"; os.makedirs(OUT,exist_ok=True)
for line in open(os.path.join(APP,"sunlei520.env"),encoding="utf-8",errors="replace"):
    line=line.strip()
    if line and not line.startswith("#") and "=" in line:
        k,v=line.split("=",1); os.environ.setdefault(k.strip(),v.strip())
try: kc=json.load(open(os.path.join(APP,"keys_config.json"),encoding="utf-8"))
except Exception: kc={}
os.environ.setdefault("TIANKONG_GPTIMAGE_KEY",str(kc.get("gptimage_key") or kc.get("ai_refine_key") or ""))
os.environ.setdefault("TIANKONG_GPTIMAGE_BASE",str(kc.get("gptimage_base") or kc.get("ai_refine_base") or ""))
os.environ["SUNLEI_V18_FUSION"]="0"; os.environ["SUNLEI_V18_CREATION"]="0"
shutil.rmtree(H,ignore_errors=True); os.makedirs(H)
code=open(os.path.join(STG,"server_v5_b2.py.c"),encoding="utf-8").read()
for call in ("_jm_ensure_thread()","_pp_ensure_thread()","_jm_trend_ensure_thread()","_wm_restore_on_boot()",
             "_wm_restore_fusion_guides_on_boot()","_wm_start_watchdog()","_wm_start_guide_sweeper()",
             "_guide_logo_start_boot_warm()","_wm_init_gpu_bridge()"):
    code=code.replace("\n"+call+"\n","\npass  # harness: "+call+"\n")
open(os.path.join(H,"srv_h.py"),"w",encoding="utf-8").write(code)
shutil.copy(os.path.join(STG,"wm_v18_v5.py.v5.c"),os.path.join(H,"wm_v18.py"))
for mn in ("product_identity.py","title_styles.py","title_modes.py","fusion_copy.py","price_text.py"):
    p=os.path.join(STG,mn)
    if os.path.isfile(p): shutil.copy(p,os.path.join(H,mn))
sys.path.insert(0,H); sys.path.append(APP); threading.Thread.start=lambda self: None; os.chdir(H)
import srv_h as m
v=m._wm_v18
imgs_dir=os.path.join(H,"img"); os.makedirs(imgs_dir,exist_ok=True); m._image_dir=lambda: imgs_dir
P={
 "P09":{"f":"wm_641df49080694bca_prod.jpg","cat":"眼影盘","group":"beauty","ident":"花知晓 粉色外壳眼影盘（多色眼影、镜子、浮雕外壳）","brand":"花知晓","name":"眼影盘","price":"159"},
 "P10":{"f":"wm_48be192afe2b4724_prod.jpg","cat":"首饰礼盒套装","group":"beauty","ident":"花知晓 首饰礼盒套装（浮雕镜、项链、耳饰、礼盒、刷具等全部件）","brand":"花知晓","name":"首饰礼盒套装","price":"399"},
}
def rd(n): return open(os.path.join(STG,"inputs2",n),"rb").read()
HERO=("PRODUCT IS THE HERO (highest priority, overrides scene beauty): the product is the biggest, sharpest and "
      "brightest subject - about 55-70% of the frame, centre or rule-of-thirds, best light; the counter, props, "
      "shoppers, blurred background and any LED screen are ONLY supporting: smaller, softer, dimmer, never competing; "
      "at first glance the viewer sees the product first; no other product of the same type steals attention; for a "
      "set, the complete set group is the hero with every piece visible, clearly dominating the frame.")
COUNTER=("REAL COSMETICS COUNTER: real department-store beauty floor with glass-top counters, lit product shelves, "
         "tester units and mirror panels; softly blurred shoppers; NOT a marble dining table, NOT a home vanity, NOT a studio set.")
LIVE=("IN USE, NOT DRY: tester shades/brushes or a mirror reflection show the counter is really in use; keep it clean, "
      "the product remains the hero; no empty product-shot feel.")
LOOK="PRODUCT LOOKS GOOD: crisp texture and logo, flattering angle, complete pieces; dull or flat is a failure."
REAL="REAL PHONE PHOTO: natural store light and grain, true reflections/contact shadows; no CGI/over-clean look."
NOSIGN="NO price sign, no price tag, no promo board and no price text or number anywhere in the frame."
PILLAR=("EXACTLY ONE price material: a real mall-corridor pillar LED screen in the BACKGROUND, CLEARLY SMALLER than the product and never the "
        "brightest thing; powered on; screen Chinese: brand \"%s\", product \"%s\", activity \"%s\", price \"¥%s\"; no other sign.")
FRONT=("EXACTLY ONE price material: a real LED screen mounted above the store front in the BACKGROUND, CLEARLY SMALLER than the product and "
       "never the brightest thing; powered on; screen Chinese: brand \"%s\", product \"%s\", activity \"%s\", price \"¥%s\"; no other sign.")
CASES=[
 ("B1_产品主角_眼影盘_近景","P09","close",
  "bright department-store beauty counter, glass top, lit shelves softly behind, one试色纸 with pink swatches at the edge",
  "open on a clear acrylic stand in the foreground, every shade sharp and clean",None),
 ("B2_产品主角_眼影盘_试妆台","P09","close",
  "real beauty test station, mirror panel softly behind, brush holder and试色纸 blurred at the side",
  "open in the foreground biggest and sharpest, a fan brush small beside it",None),
 ("B3_产品主角_礼盒_柱屏","P10","close",
  "glass display counter with lit shelf behind, mall pillar LED screen far in the background",
  "complete set open in the foreground, mirror and main box dominant, all pieces visible",("pillar","限时特惠")),
 ("B4_产品主角_礼盒_门头屏","P10","close",
  "brand store front inside a department store, LED screen above in the background, glass display case",
  "complete set open on the glass counter, the set group fills most of the frame",("front","清仓特惠")),
]
key=os.environ.get("TIANKONG_GPTIMAGE_KEY","").strip(); base=os.environ.get("TIANKONG_GPTIMAGE_BASE","").strip()
for name,k,shot,place,present,sk in CASES:
    d=P[k]
    look={"place":place,"mood":"bright clean real beauty counter, in use, product-focused",
          "present":present,"angle":"camera at eye level, straight on, product centred",
          "framing":"the product takes most of the frame, sharp; the counter and background are soft and secondary",
          "group":"beauty","multi":False,"sign":bool(sk)}
    p=v.build_gen(d["ident"], look, "", shot)
    p += "\n\n"+HERO+"\n"+COUNTER+"\n"+LIVE+"\n"+LOOK+"\n"+REAL
    if sk: p += "\n\n"+((PILLAR if sk[0]=="pillar" else FRONT) % (d["brand"],d["name"],sk[1],d["price"]))
    else: p += "\n"+NOSIGN
    try: p=m._wm_prompt_fit(p)
    except Exception: pass
    imgs=[(P[k]["f"],rd(P[k]["f"]))]
    t0=time.time(); out=""
    try: out=m._wm_fusion_edits(imgs,p,"2160x2880",key,base,OUT,job_context={})
    except Exception as e: print("[FAIL]",name,type(e).__name__,str(e)[:160],flush=True)
    print("[SAMPLE]",name,"len=",len(p),"sec=",round(time.time()-t0,1),"out=",os.path.basename(out) if out else "-",flush=True)
print("DONE_HERO4",flush=True)

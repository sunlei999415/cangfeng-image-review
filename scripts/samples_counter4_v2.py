# -*- coding: utf-8 -*-
"""美妆专柜风 v2：真专柜背景（玻璃柜台+灯箱层板+试妆台），价格屏按“商场柱子LED / 门店上方LED”，staging only。"""
import json, os, shutil, sys, threading, time
STG="/root/_stage_20261114_v5"; APP="/var/www/sunlei_520_v2"; H="/tmp/counter4v2"
OUT="/tmp/counter4v2_out"; os.makedirs(OUT,exist_ok=True)
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
COUNTER=("REAL COSMETICS COUNTER: a real department-store beauty floor: glass-top display counter with lit product "
         "shelves behind, tester units, acrylic stands and mirror panels, softly blurred shoppers and neighbouring "
         "counters; bright counter spotlights and warm backlit shelf glow. NOT a marble dining table, NOT a home "
         "vanity, NOT a studio set; no other brand names or logos.")
AESTH="PREMIUM BUT REAL beauty-counter styling: clean colour palette, elegant minimal props, the product is the hero, generous negative space."
LOOK="PRODUCT LOOKS GOOD (must sell): crisp texture and logo, flattering angle, complete pieces; dull or flat is a failure."
REAL="REAL PHONE PHOTO (must feel real, not AI): natural imperfect store light and grain, true reflections and contact shadows; no CGI/over-clean look."
NOSIGN="NO price sign, no price tag, no promo board and no price text or number anywhere in the frame."
PILLAR=("EXACTLY ONE price material in the whole frame: a real mall-corridor pillar wrapped with a tall vertical LED advertising screen, "
        "standing near the counter, powered on; screen Chinese: brand \"%s\", product \"%s\", activity \"%s\", price \"¥%s\"; "
        "readable, never covers the product; no second card or tag.")
FRONT=("EXACTLY ONE price material in the whole frame: a real LED screen mounted ABOVE the store front / counter with visible brackets "
       "(never floating), powered on; screen Chinese: brand \"%s\", product \"%s\", activity \"%s\", price \"¥%s\"; "
       "readable, never covers the product; no second card or tag.")
def build_case(k, shot, price_kind, activity):
    d=P[k]
    look={
      "place": "a real department-store cosmetics floor: the product displayed on the glass top of a beauty counter, with lit product shelves behind, tester units and acrylic stands, softly blurred shoppers and neighbouring counters",
      "mood": "bright clean premium beauty counter, real store lighting",
      "present": ("open on a clear acrylic display stand on the glass counter, lid wide open, every shade visible and clean"
                  if k=="P09" else "laid out open on the glass counter, every piece of the set visible and neatly arranged"),
      "angle": "camera at eye level, slightly above the counter, straight on",
      "framing": ("a close-up: the product fills about half the frame, fine texture sharp" if shot=="close" else "a wide shot: the product and the surrounding beauty counter readable, the mall corridor softly behind"),
      "group": "beauty",
      "multi": False,
      "sign": bool(price_kind),
    }
    p=v.build_gen(d["ident"], look, "", shot)
    p += "\n\n"+COUNTER+"\n"+AESTH+"\n"+LOOK+"\n"+REAL
    if price_kind=="pillar":
        p += "\n\n"+(PILLAR % (d["brand"],d["name"],activity,d["price"]))
    elif price_kind=="front":
        p += "\n\n"+(FRONT % (d["brand"],d["name"],activity,d["price"]))
    else:
        p += "\n"+NOSIGN
    try: p=m._wm_prompt_fit(p)
    except Exception: pass
    return p
CASES=[
 ("C1v2_counter_P09_close","P09","close",None,""),
 ("C2v2_counter_P09_pillar","P09","wide","pillar","限时特惠"),
 ("C3v2_counter_P10_close","P10","close",None,""),
 ("C4v2_counter_P10_front","P10","wide","front","清仓特惠"),
]
key=os.environ.get("TIANKONG_GPTIMAGE_KEY","").strip(); base=os.environ.get("TIANKONG_GPTIMAGE_BASE","").strip()
for name,k,shot,pk,act in CASES:
    p=build_case(k,shot,pk,act)
    imgs=[(P[k]["f"],rd(P[k]["f"]))]
    t0=time.time(); out=""
    try: out=m._wm_fusion_edits(imgs,p,"2160x2880",key,base,OUT,job_context={})
    except Exception as e: print("[FAIL]",name,type(e).__name__,str(e)[:160],flush=True)
    print("[SAMPLE]",name,"len=",len(p),"sec=",round(time.time()-t0,1),"out=",os.path.basename(out) if out else "-",flush=True)
print("DONE_COUNTER4V2",flush=True)

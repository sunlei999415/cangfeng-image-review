# -*- coding: utf-8 -*-
"""修价格牌文字：T1羽绒服/T2美妆/T4礼盒 重出，价格牌文字严格锁定（staging only）。"""
import json, os, shutil, sys, threading, time
STG="/root/_stage_20261114_v5"; APP="/var/www/sunlei_520_v2"; H="/tmp/fix3"
OUT="/tmp/fix3_out"; os.makedirs(OUT,exist_ok=True)
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
 "P03":{"f":"wm_77201abd085f4d2c_prod.jpg","cat":"羽绒服","group":"outer","ident":"波司登 白色连帽羽绒服（横向绗缝、前拉链、立领连帽）","brand":"波司登","name":"白色连帽羽绒服","price":"179"},
 "P09":{"f":"wm_641df49080694bca_prod.jpg","cat":"眼影盘","group":"beauty","ident":"花知晓 粉色外壳眼影盘（多色眼影、镜子、浮雕外壳）","brand":"花知晓","name":"眼影盘","price":"159"},
 "P10":{"f":"wm_48be192afe2b4724_prod.jpg","cat":"首饰礼盒套装","group":"beauty","ident":"花知晓 首饰礼盒套装（浮雕镜、项链、耳饰、礼盒、刷具等全部件）","brand":"花知晓","name":"首饰礼盒套装","price":"399"},
}
def rd(n): return open(os.path.join(STG,"inputs2",n),"rb").read()
HERO=("PRODUCT IS THE HERO: the product is the biggest, sharpest, brightest subject - about 55-65% of the frame; the store, "
      "racks, props and price panel are only supporting; no second product of the same type steals attention.")
REAL=("REAL STORE PHOTO, NOT AI: real shop light, true fabric/leather/plastic sheen, believable shadows and reflections, "
      "real hangers/racks/shelves; no CGI gloss, no plastic look, no over-smooth surfaces.")
GRAND=("GRAND, NOT PETTY: clean calm composition with breathing space, low-saturation harmonious colours, orderly merchandising, "
       "no clutter, no cheap stickers; premium but real, not a staged set.")
TEXT_LOCK=("PRICE PANEL TEXT LOCK (copy verbatim, do not improvise): the sign contains EXACTLY these four separate lines, top to bottom:\n"
           "line 1: %s\nline 2: %s\nline 3: %s\nline 4: ¥%s\n"
           "Do NOT repeat any line; do NOT add any other text; put the ¥ symbol ONLY before the price digits in line 4; "
           "the price digits are exactly %s - never change them to another number; the activity line is exactly \"%s\"; "
           "no other numbers anywhere in the frame. The price digits are the biggest text and readable at a 200px-wide preview.")
CASES=[
 ("F1_羽绒服_吊挂灯箱","P03",
  "a real clothing store in a mall: black racks of down jackets behind, warm ceiling spotlights, polished floor, softly blurred shoppers; a large hanging LED lightbox above the front rack",
  "hanging on a black hanger at the front of the rack, full length visible, hood and quilting sharp",
  "camera at chest height, straight on, slight 3/4",
  "the product fills about 55-65% of the frame height, centred; the hanging price lightbox above is large and readable",
  ("吊挂式门店灯箱","above the rack, aligned with the hero product","限时特惠")),
 ("F2_美妆_柜台屏","P09",
  "a real department-store beauty counter: glass-top counter, lit shelves behind, acrylic stands, mirror panel, softly blurred shoppers",
  "open on a clear acrylic stand at the front of the glass counter, lid wide open, every shade sharp",
  "camera at eye level slightly above, straight on",
  "the palette fills about 55% of the frame; the price panel stands on the counter beside it, large",
  ("柜台立牌","on the counter beside the product","限时特惠")),
 ("F4_礼盒_柜台立牌","P10",
  "a real department-store gift/beauty counter: glass display case, lit shelves, mirror, softly blurred shoppers",
  "the complete set open on the glass counter, mirror and main box dominant, all pieces visible",
  "camera at eye level, straight on, slight 3/4",
  "the set fills about 60% of the frame; the price standee on the counter beside it is large",
  ("柜台立牌","on the counter beside the product","清仓特惠")),
]
key=os.environ.get("TIANKONG_GPTIMAGE_KEY","").strip(); base=os.environ.get("TIANKONG_GPTIMAGE_BASE","").strip()
for name,k,place,present,angle,framing,(carrier,pos,act) in CASES:
    d=P[k]
    look={"place":place,"mood":"real store, warm spotlights, calm and orderly","present":present,"angle":angle,
          "framing":framing,"group":("beauty" if k in ("P09","P10") else "outer"),"multi":False,"sign":True}
    p=v.build_gen(d["ident"], look, "", "close")
    p += "\n\n"+HERO+"\n"+REAL+"\n"+GRAND
    p += ("\n\nPRICE PANEL: exactly one real %s, placed %s, occupying about 18-25%% of the frame, clean and premium.\n" % (carrier,pos))
    p += TEXT_LOCK % (d["brand"],d["name"],act,d["price"],d["price"],act)
    try: p=m._wm_prompt_fit(p)
    except Exception: pass
    imgs=[(P[k]["f"],rd(P[k]["f"]))]
    t0=time.time(); out=""
    try: out=m._wm_fusion_edits(imgs,p,"2160x2880",key,base,OUT,job_context={})
    except Exception as e: print("[FAIL]",name,type(e).__name__,str(e)[:160],flush=True)
    print("[SAMPLE]",name,"len=",len(p),"sec=",round(time.time()-t0,1),"out=",os.path.basename(out) if out else "-",flush=True)
print("DONE_FIX3",flush=True)
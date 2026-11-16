# -*- coding: utf-8 -*-
"""价格牌=LED屏特写（不是KT板/纸板/亚克力印刷牌）：羽绒服/美妆/礼盒 3 张，staging only。"""
import json, os, shutil, sys, threading, time
STG="/root/_stage_20261114_v5"; APP="/var/www/sunlei_520_v2"; H="/tmp/led3"
OUT="/tmp/led3_out"; os.makedirs(OUT,exist_ok=True)
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
HERO=("PRODUCT IS THE HERO: the product is the biggest, sharpest subject - about 50-60% of the frame, centre/right; "
      "the LED screen close-up is smaller than the product and never covers it; no second product steals attention.")
REAL=("REAL STORE PHOTO, NOT AI: real shop light, true fabric/leather sheen, believable shadows/reflections, real racks/shelves; "
      "no CGI gloss, no plastic look.")
GRAND=("GRAND, NOT PETTY: clean calm composition with breathing space, low-saturation harmonious colours, orderly merchandising, "
       "no clutter, no cheap stickers; premium but real.")
LED=("PRICE LED SCREEN CLOSE-UP (hard requirement): the price material is a REAL LED / digital display screen - self-lit, glowing, "
     "with backlight bloom and a thin dark frame, %s; it is a foreground close-up occupying about 25-35%% of the frame, bright and sharp; "
     "the price digits are huge (about 1/9 of the image height) and readable in a 150px-wide preview; exactly one screen; never covers the product; "
     "NOT a printed KT board, NOT a foam board, NOT a paper sign, NOT a printed acrylic standee, NOT a lightbox with paper poster.")
TEXT=("The screen shows EXACTLY four lines, top to bottom, no repetition, no extra text:\nline1: %s\nline2: %s\nline3: %s\nline4: ¥%s\n"
      "The ¥ symbol is only before line4 digits; the price digits are exactly %s, never another number; no other numbers anywhere; "
      "the screen has a dark border and a bright self-lit background.")
CASES=[
 ("K1_羽绒服_LED吊屏","P03",
  "a real clothing store: black racks of down jackets, warm spotlights, softly blurred shoppers; a real hanging LED screen mounted above the front rack",
  "hanging on a black hanger at the front rack, full length, hood and quilting sharp",
  "camera at chest height, straight on","the jacket fills centre-right; the hanging LED screen is a big foreground close-up upper-left",
  "hanging above the rack with visible metal brackets","限时特惠"),
 ("K2_美妆_LED柜台屏","P09",
  "a real department-store beauty counter: glass top, lit shelves, acrylic stands, softly blurred shoppers; a real counter LED screen on a thin stand",
  "open on an acrylic stand at the front of the glass counter, lid open, shades sharp",
  "camera at eye level slightly above","the palette fills centre-right; the counter LED screen is a big foreground close-up lower-left",
  "standing on the glass counter with a thin metal stand","限时特惠"),
 ("K4_礼盒_LED柜台屏","P10",
  "a real department-store gift counter: glass display case, lit shelves, mirror, softly blurred shoppers; a real LED screen above the counter",
  "the complete set open on the glass counter, mirror and box dominant",
  "camera at eye level, straight on","the set fills centre-right; the LED screen is a big foreground close-up upper-left",
  "mounted above the counter with visible brackets","清仓特惠"),
]
key=os.environ.get("TIANKONG_GPTIMAGE_KEY","").strip(); base=os.environ.get("TIANKONG_GPTIMAGE_BASE","").strip()
for name,k,place,present,angle,framing,pos,act in CASES:
    d=P[k]
    look={"place":place,"mood":"real store, warm spotlights, calm and orderly","present":present,"angle":angle,
          "framing":framing,"group":("beauty" if k in ("P09","P10") else "outer"),"multi":False,"sign":True}
    p=v.build_gen(d["ident"], look, "", "close")
    p += "\n\n"+HERO+"\n"+REAL+"\n"+GRAND
    p += "\n\n"+(LED % pos)
    p += "\n\n"+(TEXT % (d["brand"],d["name"],act,d["price"],d["price"]))
    try: p=m._wm_prompt_fit(p)
    except Exception: pass
    imgs=[(P[k]["f"],rd(P[k]["f"]))]
    t0=time.time(); out=""
    try: out=m._wm_fusion_edits(imgs,p,"2160x2880",key,base,OUT,job_context={})
    except Exception as e: print("[FAIL]",name,type(e).__name__,str(e)[:160],flush=True)
    print("[SAMPLE]",name,"len=",len(p),"sec=",round(time.time()-t0,1),"out=",os.path.basename(out) if out else "-",flush=True)
print("DONE_LED3",flush=True)

# -*- coding: utf-8 -*-
"""LED价格牌形式多样化（像参考账号那样）：门店门头屏/商场柱屏/货架吊屏/落地灯箱，4张，staging only。"""
import json, os, shutil, sys, threading, time
STG="/root/_stage_20261114_v5"; APP="/var/www/sunlei_520_v2"; H="/tmp/forms4"
OUT="/tmp/forms4_out"; os.makedirs(OUT,exist_ok=True)
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
 "P06":{"f":"wm_668fe98a9f4846a4_prod.jpg","cat":"女包","group":"bag","ident":"粉色菱格链条包（翻盖、金色链条、金属扣）","brand":"CHARLES & KEITH","name":"粉色链条包","price":"899"},
 "P09":{"f":"wm_641df49080694bca_prod.jpg","cat":"眼影盘","group":"beauty","ident":"花知晓 粉色外壳眼影盘（多色眼影、镜子、浮雕外壳）","brand":"花知晓","name":"眼影盘","price":"159"},
 "P10":{"f":"wm_48be192afe2b4724_prod.jpg","cat":"首饰礼盒套装","group":"beauty","ident":"花知晓 首饰礼盒套装（浮雕镜、项链、耳饰、礼盒、刷具等全部件）","brand":"花知晓","name":"首饰礼盒套装","price":"399"},
}
def rd(n): return open(os.path.join(STG,"inputs2",n),"rb").read()
HERO=("PRODUCT IS THE HERO: the product is the biggest, sharpest subject - about 50-60% of the frame; the LED screen is smaller "
      "than the product and never covers it; no second product steals attention.")
REAL=("REAL STORE PHOTO, NOT AI: real mall/store light, true material sheen, believable shadows/reflections, real racks/counters; "
      "no CGI gloss, no plastic look.")
GRAND=("GRAND, NOT PETTY: clean calm composition with breathing space, low-saturation colours, orderly merchandising, no clutter; "
       "premium but real.")
TEXT=("The LED screen shows EXACTLY four lines, top to bottom, no repetition, no extra text:\nline1: %s\nline2: %s\nline3: %s\nline4: ¥%s\n"
      "The ¥ symbol is only before line4 digits; the price digits are exactly %s, never another number; no other numbers anywhere; "
      "the screen background is bright and self-lit with a thin dark border.")
FORMS={
 "storefront":("PRICE = STORE-FRONT LED SCREEN: a large LED screen mounted above the store entrance / door frame inside a mall, "
   "self-lit, glowing, thin dark frame, with visible brackets; a prominent close-up corner occupying about 25-30% of the frame, "
   "still smaller than the product; price digits huge and readable at 150px; exactly one screen; NOT a KT/foam/paper board, NOT a printed standee."),
 "pillar":("PRICE = MALL PILLAR LED SCREEN: a tall vertical LED advertising pillar wrapped with a self-lit screen, standing in the mall "
   "corridor near the counter; the screen is a prominent close-up occupying about 25-30% of the frame, still smaller than the product; "
   "price digits huge and readable at 150px; exactly one screen; NOT a KT/foam/paper board, NOT a printed standee."),
 "hanging":("PRICE = HANGING LED SCREEN ABOVE THE SHELF: a large LED screen hung above the rack/shelf with slim brackets, self-lit, "
   "glowing, thin dark frame; prominent close-up occupying about 25-30% of the frame, still smaller than the product; price digits huge "
   "and readable at 150px; exactly one screen; NOT a KT/foam/paper board, NOT a printed standee."),
 "floor":("PRICE = FLOOR-STANDING LED LIGHTBOX: a real self-lit LED display on a floor stand at the store entrance (digital signage, "
   "thin dark frame), prominent close-up occupying about 25-30% of the frame, still smaller than the product; price digits huge and "
   "readable at 150px; exactly one screen; NOT a KT/foam/paper board, NOT a printed standee."),
}
CASES=[
 ("V1_羽绒服_门店门头LED","P03","storefront",
  "a real clothing store front inside a mall: glass window with jacket display, warm spotlights, softly blurred shoppers, the store entrance behind",
  "hanging on a black hanger in the window display, full length, hood and quilting sharp",
  "camera at chest height, straight on","the jacket fills centre; the store-front LED screen is a big close-up above-left","限时特惠"),
 ("V2_美妆_商场柱屏","P09","pillar",
  "a real mall beauty floor: glass counter with lit shelves, softly blurred shoppers; a tall vertical LED pillar screen nearby",
  "open on an acrylic stand at the front of the glass counter, lid open, shades sharp",
  "camera at eye level slightly above","the palette fills centre; the pillar LED screen is a big close-up left","限时特惠"),
 ("V3_包_货架吊屏","P06","hanging",
  "a real boutique bag wall: shelves of different designer bags softly blurred, warm spotlights; a LED screen hung above the shelf",
  "standing upright on a lit shelf in the foreground, strap falling naturally, quilting and hardware sharp",
  "camera at eye level, straight on","the bag fills centre-right; the hanging LED screen is a big close-up above-left","会员礼遇"),
 ("V4_礼盒_落地灯箱","P10","floor",
  "a real department-store gift counter: glass display case, lit shelves, softly blurred shoppers; a floor-standing LED lightbox at the entrance",
  "the complete set open on the glass counter, mirror and box dominant",
  "camera at eye level, straight on","the set fills centre-right; the floor-standing LED screen is a big close-up lower-left","清仓特惠"),
]
key=os.environ.get("TIANKONG_GPTIMAGE_KEY","").strip(); base=os.environ.get("TIANKONG_GPTIMAGE_BASE","").strip()
for name,k,form,place,present,angle,pos,act in CASES:
    d=P[k]
    look={"place":place,"mood":"real mall store, warm spotlights, calm and orderly","present":present,"angle":angle,
          "framing":"the product fills centre/right; the LED screen is a big close-up, %s"%pos,
          "group":("bag" if k=="P06" else ("beauty" if k in ("P09","P10") else "outer")),"multi":False,"sign":True}
    p=v.build_gen(d["ident"], look, "", "close")
    p += "\n\n"+HERO+"\n"+REAL+"\n"+GRAND
    p += "\n\n"+(FORMS[form])
    p += "\n\n"+(TEXT % (d["brand"],d["name"],act,d["price"],d["price"]))
    try: p=m._wm_prompt_fit(p)
    except Exception: pass
    imgs=[(P[k]["f"],rd(P[k]["f"]))]
    t0=time.time(); out=""
    try: out=m._wm_fusion_edits(imgs,p,"2160x2880",key,base,OUT,job_context={})
    except Exception as e: print("[FAIL]",name,type(e).__name__,str(e)[:160],flush=True)
    print("[SAMPLE]",name,"len=",len(p),"sec=",round(time.time()-t0,1),"out=",os.path.basename(out) if out else "-",flush=True)
print("DONE_FORMS4",flush=True)
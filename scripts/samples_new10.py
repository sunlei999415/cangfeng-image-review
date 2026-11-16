# -*- coding: utf-8 -*-
"""新标准 v2 覆盖 10 张：融图/创品/生图 × 服装/包/美妆/礼盒；LED价格牌特写+产品主角+真实+大气（staging only）。"""
import json, os, shutil, sys, threading, time
STG="/root/_stage_20261114_v5"; APP="/var/www/sunlei_520_v2"; H="/tmp/new10"
OUT="/tmp/new10_out"; os.makedirs(OUT,exist_ok=True)
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
 "P01":{"f":"wm_cc573d864cfd488d_prod.jpg","cat":"羽绒服","group":"outer","ident":"森马 深灰色连帽羽绒服（横向绗缝、立领、前拉链、两侧拉链口袋）","brand":"森马","name":"深灰色连帽羽绒服","price":"659"},
 "P03":{"f":"wm_77201abd085f4d2c_prod.jpg","cat":"羽绒服","group":"outer","ident":"波司登 白色连帽羽绒服（横向绗缝、前拉链、立领连帽）","brand":"波司登","name":"白色连帽羽绒服","price":"179"},
 "P06":{"f":"wm_668fe98a9f4846a4_prod.jpg","cat":"女包","group":"bag","ident":"粉色菱格链条包（翻盖、金色链条、金属扣）","brand":"CHARLES & KEITH","name":"粉色链条包","price":"899"},
 "P07":{"f":"wm_2a880894cf8d4317_prod.jpg","cat":"托特包","group":"bag","ident":"黑色托特包（大容量、毛绒挂件、挺括包身）","brand":"CHARLES & KEITH","name":"黑色托特包","price":"599"},
 "P09":{"f":"wm_641df49080694bca_prod.jpg","cat":"眼影盘","group":"beauty","ident":"花知晓 粉色外壳眼影盘（多色眼影、镜子、浮雕外壳）","brand":"花知晓","name":"眼影盘","price":"159"},
 "P10":{"f":"wm_48be192afe2b4724_prod.jpg","cat":"首饰礼盒套装","group":"beauty","ident":"花知晓 首饰礼盒套装（浮雕镜、项链、耳饰、礼盒、刷具等全部件）","brand":"花知晓","name":"首饰礼盒套装","price":"399"},
}
def rd(n): return open(os.path.join(STG,"inputs2",n),"rb").read()
HERO=("PRODUCT IS THE HERO: the product is the biggest, sharpest, brightest subject - about 50-60% of the frame; the LED screen "
      "is smaller than the product and never covers it; no other product steals attention.")
REAL=("REAL STORE PHOTO, NOT AI: real shop/mall light, true material sheen, believable shadows/reflections, real racks/shelves/counters; "
      "no CGI gloss, no plastic look.")
GRAND=("GRAND, NOT PETTY: clean calm composition with breathing space, low-saturation harmonious colours, orderly merchandising; "
       "premium but real; no clutter, no cheap stickers.")
FORMS={
 "hanging":"PRICE = HANGING LED SCREEN: a large LED screen hung above the rack/shelf with slim brackets, self-lit, glowing, thin dark frame; prominent close-up ~25-35% of the frame; price digits huge and readable at 150px; exactly one screen; NOT a KT/foam/paper board.",
 "storefront":"PRICE = STORE-FRONT LED SCREEN: a large LED screen mounted above the store entrance/window inside a mall, self-lit, thin dark frame with visible brackets; prominent close-up ~25-35% of the frame; price digits huge and readable at 150px; exactly one screen; NOT a KT/foam/paper board.",
 "pillar":"PRICE = MALL PILLAR LED SCREEN: a tall vertical LED advertising pillar in the mall corridor near the counter, self-lit, thin dark frame; prominent close-up ~25-35% of the frame; price digits huge and readable at 150px; exactly one screen; NOT a KT/foam/paper board.",
 "counter":"PRICE = COUNTER LED SCREEN: a real self-lit LED screen standing on the glass counter with a thin metal stand (digital display, thin dark frame); prominent close-up ~25-35% of the frame; price digits huge and readable at 150px; exactly one screen; NOT a KT/foam/paper board.",
 "floor":"PRICE = FLOOR-STANDING LED LIGHTBOX: a real self-lit LED display on a floor stand at the store entrance (digital signage, thin dark frame); prominent close-up ~25-35% of the frame; price digits huge and readable at 150px; exactly one screen; NOT a KT/foam/paper board.",
}
TEXT=("The LED screen shows EXACTLY four lines, top to bottom, no repetition, no extra text:\nline1: %s\nline2: %s\nline3: %s\nline4: ¥%s\n"
      "The ¥ symbol is only before line4 digits; the price digits are exactly %s, never another number; no other numbers anywhere; "
      "the screen background is bright and self-lit with a thin dark border.")
def clauses(led, k, act):
    d=P[k]
    return ("\n\n"+HERO+"\n"+REAL+"\n"+GRAND+"\n\n"+FORMS[led]+"\n\n"+(TEXT % (d["brand"],d["name"],act,d["price"],d["price"])))
CASES=[
 # name, mode, product, scene, place, present, angle, framing, ledform, act
 ("N1_F_服装_吊屏","fusion","P01","/tmp/o24.jpg",
  "a real multi-brand clothing store: racks of colourful down jackets, warm spotlights, polished floor, softly blurred shoppers",
  "hanging on a black hanger at the front rack, full length, hood and quilting sharp",
  "camera at chest height, straight on","the jacket fills centre-right; the hanging LED screen is a large close-up above-left","hanging","限时特惠"),
 ("N2_F_包_吊屏","fusion","P06","/tmp/g04.jpg",
  "a real bright handbag boutique: white backlit shelves, polished floor, softly blurred shoppers",
  "standing upright on a lit shelf in the foreground, strap falling naturally, quilting and hardware sharp",
  "camera at eye level, straight on","the bag fills centre-right; the hanging LED screen is a large close-up above-left","hanging","会员礼遇"),
 ("N3_F_美妆_柜台屏","fusion","P09","/tmp/a047.jpg",
  "a real department-store beauty counter: glass-top counter, lit shelves, mirror, softly blurred shoppers",
  "open on an acrylic stand at the front of the glass counter, lid open, shades sharp",
  "camera at eye level slightly above","the palette fills centre-right; the counter LED screen is a large close-up lower-left","counter","限时特惠"),
 ("N4_C_服装_门头屏","creation","P03","/tmp/o03.jpg",
  "a real clothing store inside a mall: racks of grey and black puffers, warm spotlights, softly blurred shoppers",
  "hanging on a black hanger at the front rack, full length, hood sharp",
  "camera at chest height, straight on","the jacket fills centre-right; the store-front LED screen is a large close-up above-left","storefront","限时特惠"),
 ("N5_C_包_吊屏","creation","P07","/tmp/g13.jpg",
  "a real boutique bag wall: shelves with different bags softly blurred, warm spotlights",
  "standing upright on a lit shelf in the foreground, handles upright, leather sharp",
  "camera at eye level, straight on","the bag fills centre-right; the hanging LED screen is a large close-up above-left","hanging","会员礼遇"),
 ("N6_C_礼盒_柱子屏","creation","P10","/tmp/a079.jpg",
  "a real department-store beauty/gift floor: glass counters, lit shelves, softly blurred shoppers, a tall LED pillar nearby",
  "the complete set open on the glass counter, mirror and box dominant",
  "camera at eye level, straight on","the set fills centre-right; the pillar LED screen is a large close-up left","pillar","清仓特惠"),
 ("N7_G_服装_门头屏","gen","P01",None,
  "a real clothing store front inside a mall: glass window with jacket display, warm spotlights, store entrance, softly blurred shoppers",
  "hanging on a black hanger in the window display, full length, hood and quilting sharp",
  "camera at chest height, straight on","the jacket fills centre-right; the store-front LED screen is a large close-up above-left","storefront","限时特惠"),
 ("N8_G_包_柱子屏","gen","P06",None,
  "a real mall corridor near a handbag counter: polished floor, glass displays, softly blurred shoppers, a tall LED pillar",
  "standing upright on a lit counter in the foreground, strap falling naturally",
  "camera at eye level, straight on","the bag fills centre-right; the pillar LED screen is a large close-up left","pillar","会员礼遇"),
 ("N9_G_美妆_柜台屏","gen","P09",None,
  "a real department-store beauty counter: glass-top counter, lit shelves, mirror, softly blurred shoppers",
  "open on an acrylic stand at the front of the glass counter, lid open, shades sharp",
  "camera at eye level slightly above","the palette fills centre-right; the counter LED screen is a large close-up lower-left","counter","限时特惠"),
 ("N10_G_礼盒_落地灯箱","gen","P10",None,
  "a real department-store gift counter: glass display case, lit shelves, softly blurred shoppers, a floor-standing LED lightbox at the entrance",
  "the complete set open on the glass counter, mirror and box dominant",
  "camera at eye level, straight on","the set fills centre-right; the floor LED lightbox is a large close-up lower-left","floor","清仓特惠"),
]
key=os.environ.get("TIANKONG_GPTIMAGE_KEY","").strip(); base=os.environ.get("TIANKONG_GPTIMAGE_BASE","").strip()
for name,mode,k,scene,place,present,angle,framing,led,act in CASES:
    d=P[k]
    look={"place":place,"mood":"real mall/store, warm spotlights, calm and orderly","present":present,"angle":angle,
          "framing":framing,"group":d["group"],"multi":False,"sign":True}
    if mode=="gen":
        p=v.build_gen(d["ident"], look, "", "close"); imgs=[(P[k]["f"],rd(P[k]["f"]))]
    else:
        if not scene or not os.path.isfile(scene): print("[NO-SCENE]",name,scene,flush=True); continue
        p=v.build_scene(mode, d["ident"], look, "", "close"); imgs=[(os.path.basename(scene),open(scene,"rb").read()),(P[k]["f"],rd(P[k]["f"]))]
    p += clauses(led,k,act)
    try: p=m._wm_prompt_fit(p)
    except Exception: pass
    t0=time.time(); out=""
    try: out=m._wm_fusion_edits(imgs,p,"2160x2880",key,base,OUT,job_context={})
    except Exception as e: print("[FAIL]",name,type(e).__name__,str(e)[:160],flush=True)
    print("[SAMPLE]",name,"mode=",mode,"len=",len(p),"sec=",round(time.time()-t0,1),"out=",os.path.basename(out) if out else "-",flush=True)
print("DONE_NEW10",flush=True)

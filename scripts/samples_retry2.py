# -*- coding: utf-8 -*-
"""自检后修 2 张：N4 品牌字错/款型偏长；N2 背景像货架不够大气。staging only。"""
import json, os, shutil, sys, threading, time
STG="/root/_stage_20261114_v5"; APP="/var/www/sunlei_520_v2"; H="/tmp/retry2"
OUT="/tmp/retry2_out"; os.makedirs(OUT,exist_ok=True)
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
 "P03":{"f":"wm_77201abd085f4d2c_prod.jpg","cat":"羽绒服","group":"outer","ident":"波司登 白色连帽羽绒服（横向绗缝、前拉链、立领连帽、短款）","brand":"波司登","name":"白色连帽羽绒服","price":"179"},
 "P06":{"f":"wm_668fe98a9f4846a4_prod.jpg","cat":"女包","group":"bag","ident":"粉色菱格链条包（翻盖、金色链条、金属扣、粉色亮面菱格）","brand":"CHARLES & KEITH","name":"粉色链条包","price":"899"},
}
def rd(n): return open(os.path.join(STG,"inputs2",n),"rb").read()
HERO=("PRODUCT IS THE HERO: the product is the biggest, sharpest subject - about 50-60% of the frame; the LED screen is smaller "
      "than the product and never covers it; no other product steals attention.")
REAL=("REAL STORE PHOTO, NOT AI: real mall/store light, true material sheen, believable shadows/reflections, real racks/shelves; "
      "no CGI gloss, no plastic look.")
GRAND=("GRAND, NOT PETTY: clean calm composition with breathing space, low-saturation colours, orderly merchandising; premium but real.")
TEXT=("The LED screen shows EXACTLY four lines, top to bottom, no repetition, no extra text:\nline1: %s\nline2: %s\nline3: %s\nline4: ¥%s\n"
      "The brand line is EXACTLY \"%s\" (never 波波司登 / never extra characters); the price digits are exactly %s, never another number; "
      "the ¥ symbol only before line4; no other numbers anywhere; the screen is a self-lit digital display with thin dark bezel, glossy surface.")
LED=("PRICE = %s: a real self-lit LED screen with thin dark bezel, glossy digital surface (not a KT board, not a printed lightbox), "
     "prominent close-up ~25-30%% of the frame, price digits huge and readable at 150px; exactly one screen.")
def prompt(mode, k, look, ledname, act):
    d=P[k]
    p = (v.build_scene(mode, d["ident"], look, "", "close") if mode!="gen" else v.build_gen(d["ident"], look, "", "close"))
    p += "\n\n"+HERO+"\n"+REAL+"\n"+GRAND
    p += "\n\n"+(LED % ledname)
    p += "\n\n"+(TEXT % (d["brand"],d["name"],act,d["price"],d["brand"],d["price"]))
    try: p=m._wm_prompt_fit(p)
    except Exception: pass
    return p
key=os.environ.get("TIANKONG_GPTIMAGE_KEY","").strip(); base=os.environ.get("TIANKONG_GPTIMAGE_BASE","").strip()
# R1 creation clothing (P03) scene o03
scene="/tmp/o03.jpg"
look={"place":"a real clothing store inside a mall: racks of grey and black puffers, warm spotlights, softly blurred shoppers",
      "mood":"real mall store, calm and orderly","present":"hanging on a black hanger at the front rack; SHORT white puffer (short款), hood sharp, hem above the hips",
      "angle":"camera at chest height, straight on","framing":"the jacket fills centre-right; the store-front LED screen is a large close-up above-left",
      "group":"outer","multi":False,"sign":True}
p=prompt("creation","P03",look,"STORE-FRONT LED SCREEN above the store entrance/window","限时特惠")
imgs=[(os.path.basename(scene),open(scene,"rb").read()),(P["P03"]["f"],rd(P["P03"]["f"]))]
t0=time.time(); out=m._wm_fusion_edits(imgs,p,"2160x2880",key,base,OUT,job_context={}) if os.path.isfile(scene) else ""
print("[SAMPLE] R1_C_服装 len=",len(p),"out=",os.path.basename(out) if out else "-",flush=True)
# R2 fusion bag (P06) scene g15
scene="/tmp/g15.jpg"
look={"place":"a real bright handbag boutique: white backlit shelves with a few different bags softly blurred, warm-white light, polished floor",
      "mood":"clean premium boutique","present":"standing upright on a lit shelf in the foreground, strap falling naturally, quilting and hardware sharp",
      "angle":"camera at eye level, straight on","framing":"the bag fills centre-right; the hanging LED screen is a large close-up above-left",
      "group":"bag","multi":False,"sign":True}
p=prompt("fusion","P06",look,"HANGING LED SCREEN above the shelf","会员礼遇")
imgs=[(os.path.basename(scene),open(scene,"rb").read()),(P["P06"]["f"],rd(P["P06"]["f"]))]
out=m._wm_fusion_edits(imgs,p,"2160x2880",key,base,OUT,job_context={}) if os.path.isfile(scene) else ""
print("[SAMPLE] R2_F_包 len=",len(p),"out=",os.path.basename(out) if out else "-",flush=True)
print("DONE_RETRY2",flush=True)
# -*- coding: utf-8 -*-
"""大气+真实+产品主角+价格牌特写（学参考布局，不学AI假感）4 张：羽绒服/美妆/包创品/礼盒。staging only。"""
import json, os, shutil, sys, threading, time
STG="/root/_stage_20261114_v5"; APP="/var/www/sunlei_520_v2"; H="/tmp/try4"
OUT="/tmp/try4_out"; os.makedirs(OUT,exist_ok=True)
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
HERO=("PRODUCT IS THE HERO (all modes, all categories; highest priority): the product is the biggest, sharpest, brightest "
      "subject - about 55-65% of the frame, centre or rule-of-thirds, best light; the store, racks, props, shoppers and "
      "price panel are ONLY supporting: smaller, softer, never competing; no second product of the same type steals attention.")
REAL=("REAL STORE PHOTO, NOT AI: like a real phone snapshot inside a real shop - natural mixed store light, true fabric/"
      "leather/plastic sheen, believable shadows and reflections, real hangers/racks/shelves, slightly imperfect; "
      "NO CGI gloss, no plastic texture, no over-smooth surfaces, no invented floating props.")
GRAND=("GRAND, NOT PETTY: clean calm composition with breathing space, low-saturation harmonious colours, orderly "
       "merchandising, no clutter, no cheap stickers/promo confetti; premium but REAL, not a staged set.")
BIG=("PRICE CLOSE-UP (must be obvious at thumbnail/feed size): %s occupies about 18-25%% of the frame, placed %s, "
     "with BIG Chinese text: brand \"%s\", product \"%s\", activity \"%s\", price \"¥%s\"; the price digits are the largest "
     "text and clearly readable in a small 200px-wide preview; exactly one price material in the frame; never covers the product.")
def hero(s): return "\n\n"+HERO+"\n"+REAL+"\n"+GRAND+"\n"+s
# ---- gen cases
GEN=[
 ("T1_羽绒服_吊挂灯箱","P03",
  "a real clothing store in a mall: black racks of down jackets receding behind, warm ceiling spotlights, polished floor, softly blurred shoppers; a large hanging LED lightbox above the front rack",
  "hanging on a black hanger at the front of the rack, full length visible, hood and quilting sharp, sleeves falling naturally",
  "camera at chest height, straight on, slight 3/4 view",
  "the product fills about 55-65% of the frame height, centred; the hanging price lightbox above is large and readable",
  ("above the rack","波司登","白色连帽羽绒服","限时特惠","179")),
 ("T2_美妆_柜台屏","P09",
  "a real department-store beauty counter: glass-top counter, lit shelves behind, acrylic stands, mirror panel, softly blurred shoppers",
  "open on a clear acrylic stand at the front of the glass counter, lid wide open, every shade sharp and clean",
  "camera at eye level slightly above, straight on",
  "the palette fills about 55% of the frame; the price panel stands on the counter beside it, large",
  ("on the counter beside the product","花知晓","眼影盘","限时特惠","159")),
 ("T4_礼盒_柜台立牌","P10",
  "a real department-store gift/beauty counter: glass display case, lit shelves, mirror, softly blurred shoppers",
  "the complete set open on the glass counter, mirror and main box dominant, all pieces visible",
  "camera at eye level, straight on, slight 3/4",
  "the set fills about 60% of the frame; the price standee on the counter beside it is large",
  ("on the counter beside the product","花知晓","首饰礼盒套装","清仓特惠","399")),
]
key=os.environ.get("TIANKONG_GPTIMAGE_KEY","").strip(); base=os.environ.get("TIANKONG_GPTIMAGE_BASE","").strip()
for name,k,place,present,angle,framing,sgn in GEN:
    d=P[k]
    look={"place":place,"mood":"real store, warm spotlights, calm and orderly","present":present,
          "angle":angle,"framing":framing,"group":("beauty" if k in ("P09","P10") else "outer"),
          "multi":False,"sign":True}
    p=v.build_gen(d["ident"], look, "", "close")
    sign=(BIG % ("a real hanging LED lightbox","above the rack, aligned with the hero product",d["brand"],d["name"],sgn[2],sgn[3]) if sgn[0].startswith("above")
          else BIG % ("a real clean price standee/screen","on the counter beside the product",d["brand"],d["name"],sgn[2],sgn[3]))
    p += hero(sign)
    try: p=m._wm_prompt_fit(p)
    except Exception: pass
    imgs=[(P[k]["f"],rd(P[k]["f"]))]
    t0=time.time(); out=""
    try: out=m._wm_fusion_edits(imgs,p,"2160x2880",key,base,OUT,job_context={})
    except Exception as e: print("[FAIL]",name,type(e).__name__,str(e)[:160],flush=True)
    print("[SAMPLE]",name,"len=",len(p),"sec=",round(time.time()-t0,1),"out=",os.path.basename(out) if out else "-",flush=True)
# ---- creation bag (Image1 = real boutique scene g04)
scene="/tmp/g04.jpg"
if os.path.isfile(scene):
    d=P["P06"]
    look={"place":"a real bright handbag boutique: white backlit shelves, polished floor, softly blurred shoppers",
          "mood":"clean premium boutique, warm-white light","present":"standing upright on a lit shelf in the foreground, straps falling naturally, quilting and hardware sharp",
          "angle":"camera at eye level, straight on, slight 3/4","framing":"the bag fills about 55% of the frame; the price standee beside it is large",
          "group":"bag","multi":False,"sign":True}
    p=v.build_scene("creation",d["ident"],look,"","close")
    sign=BIG % ("a clean minimal acrylic price standee with thin metal frame","on the shelf beside the bag",d["brand"],d["name"],"会员礼遇",d["price"])
    p += hero(sign)
    try: p=m._wm_prompt_fit(p)
    except Exception: pass
    imgs=[("g04.jpg",open(scene,"rb").read()),(P["P06"]["f"],rd(P["P06"]["f"]))]
    t0=time.time(); out=""
    try: out=m._wm_fusion_edits(imgs,p,"2160x2880",key,base,OUT,job_context={})
    except Exception as e: print("[FAIL] T3_包_创品",type(e).__name__,str(e)[:160],flush=True)
    print("[SAMPLE] T3_包_创品 len=",len(p),"sec=",round(time.time()-t0,1),"out=",os.path.basename(out) if out else "-",flush=True)
else:
    print("[NO-SCENE] g04.jpg",flush=True)
print("DONE_TRY4",flush=True)
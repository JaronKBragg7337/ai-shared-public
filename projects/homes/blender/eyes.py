# The Loft's people: paint the iris into the eye textures (Unreal layers it on in its eye shader; a web page can't).
# Run with normal Python before person.py:  python eyes.py Isaiah [iris_uv_radius=0.15]
import sys
from PIL import Image, ImageDraw, ImageFilter
NAME = sys.argv[1]; RAD = float(sys.argv[2]) if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else 0.15
D = f"C:/Users/lilli/Projects/necklace-unreal/Saved/LoftPeople/{NAME}/tex/"
for side in "LR":
    sc = Image.open(D + f"T_EyeSclera{side}_BC.png").convert("RGB").resize((512, 512))
    ir = Image.open(D + f"T_EyeIris{side}_BC.png").convert("RGB")
    R = int(512 * RAD); ir = ir.resize((2 * R, 2 * R))
    m = Image.new("L", (2 * R, 2 * R), 0); ImageDraw.Draw(m).ellipse((1, 1, 2 * R - 2, 2 * R - 2), fill=255); m = m.filter(ImageFilter.GaussianBlur(2))
    sc.paste(ir, (256 - R, 256 - R), m)
    rim = Image.new("L", (512, 512), 0); ImageDraw.Draw(rim).ellipse((256 - R, 256 - R, 256 + R, 256 + R), outline=150, width=max(2, R // 10))
    sc.paste(Image.new("RGB", (512, 512), (20, 14, 10)), (0, 0), rim.filter(ImageFilter.GaussianBlur(2)))   # dark limbal ring
    sc.save(D + f"_eye{side}.png"); print("eye", side, R)

# Hair: Epic's card atlases -> one RGBA texture per groom for the web (colour baked in, strands cut out by the alpha).
#   python eyes.py NAME [iris] --hair r,g,b   (linear colour, like person.py's other colours)
import glob, os
hc = [float(x) for x in sys.argv[sys.argv.index("--hair") + 1].split(",")] if "--hair" in sys.argv else [0.018, 0.012, 0.009]
srgb = [int(255 * min(1, c ** (1 / 2.2))) for c in hc]
G = D.replace("/tex/", "/groom/")
for att in sorted(glob.glob(G + "*_CardsAtlas_Attribute.png")):
    g = os.path.basename(att).split("_CardsAtlas")[0]
    a = Image.open(att).convert("RGBA").resize((1024, 1024), Image.LANCZOS)
    cov, u = a.getchannel("R"), a.getchannel("B")   # R: the strands (coverage), B: root -> tip along each card
    rgb = [Image.eval(u, lambda t, c=c: int(min(255, c * (0.72 + 0.5 * t / 255)))) for c in srgb]   # darker roots, lighter tips
    out = Image.merge("RGBA", rgb + [cov]); out.save(G + f"_{g}_card.png"); print("hair", g)

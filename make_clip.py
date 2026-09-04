#!/usr/bin/env python3
"""
สร้างคลิปคอนเทนต์ "รถโดนชนท้าย" แนวตั้ง 1080x1920
- ใช้ภาพความเสียหายจริงในโฟลเดอร์ assets/
- มีลูกศรเคลื่อนไหวชี้ตรงตำแหน่งที่โดนชนของแต่ละภาพ
- มีวงพัลส์ + กรอบไฮไลต์ + วงซูมขยายจุดที่ชน + คำบรรยายภาษาไทย

วิธีใช้:  python3 make_clip.py [-o out/rear_end_collision.mp4]
"""

import argparse
import math
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
FPS = 30
ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")

# ---------- สี ----------
YELLOW = (255, 209, 26)
RED = (255, 64, 64)
INK = (10, 12, 16)
WHITE = (255, 255, 255)

FONT_PATHS = [
    "/usr/share/fonts/truetype/tlwg/Garuda-Bold.ttf",
    "/usr/share/fonts/truetype/tlwg/Waree-Bold.ttf",
    "/usr/share/fonts/opentype/tlwg/Loma-Bold.otf",
]
FONT_REG_PATHS = [
    "/usr/share/fonts/truetype/tlwg/Garuda.ttf",
    "/usr/share/fonts/truetype/tlwg/Waree.ttf",
    "/usr/share/fonts/opentype/tlwg/Loma.otf",
]


def _pick(paths):
    for p in paths:
        if os.path.exists(p):
            return p
    raise SystemExit("ไม่พบฟอนต์ไทยในระบบ (ติดตั้ง: apt-get install -y fonts-thai-tlwg)")


FONT_BOLD = _pick(FONT_PATHS)
FONT_REG = _pick(FONT_REG_PATHS)
_font_cache = {}


def font(size, bold=True):
    key = (size, bold)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(
            FONT_BOLD if bold else FONT_REG, size, layout_engine=ImageFont.Layout.RAQM
        )
    return _font_cache[key]


# ---------- เนื้อหาแต่ละฉาก ----------
# focus / box เป็นพิกัดแบบสัดส่วน (0-1) เทียบกับภาพต้นฉบับ
SCENES = [
    dict(
        file="01-rear-right-scrape.jpg",
        head="ฝาท้ายฝั่งขวา",
        caption=["สีครูดเป็นรอยขาวยาว", "เนื้อสีถลอกจนเห็นรอยขูดชัด"],
        focus=(0.451, 0.305),
        box=(0.330, 0.195, 0.600, 0.425),
        tail=(240, 250),
    ),
    dict(
        file="02-bumper-corner-crease.jpg",
        head="มุมกันชนหลังด้านล่าง",
        caption=["พลาสติกยับ ย่นเป็นรอยพับ", "แนวกันชนบิดผิดรูปจากแรงชน"],
        focus=(0.470, 0.565),
        box=(0.320, 0.480, 0.610, 0.690),
        tail=(285, 165),
    ),
    dict(
        file="03-trim-scuff.jpg",
        head="คิ้วดำใต้ฝาท้าย",
        caption=["ครูดยาวตลอดแนวคิ้ว", "สีลอกเป็นคราบขาวเห็นชัด"],
        focus=(0.575, 0.520),
        box=(0.280, 0.435, 0.850, 0.605),
        tail=(130, 300),
    ),
    dict(
        file="04-bumper-panel.jpg",
        head="แผงกันชนหลัง",
        caption=["ผิวสีด้าน มีรอยถลอกทั่วแผง", "รอยลากยาวไปทางมุมขวา"],
        focus=(0.778, 0.390),
        box=(0.600, 0.250, 0.955, 0.530),
        tail=(-265, 245),
    ),
    dict(
        file="05-emblem-scratch.jpg",
        head="เหนือโลโก้ HR-V",
        caption=["รอยขูดลึกเป็นแนวเส้นถี่", "เป็นจุดที่กระแทกเต็ม ๆ"],
        focus=(0.505, 0.352),
        box=(0.265, 0.215, 0.780, 0.500),
        tail=(255, 265),
    ),
]

TITLE_DUR = 2.6
SCENE_DUR = 3.6
OUTRO_DUR = 3.0
XFADE = 0.35


# ---------- helper ----------
def ease_out(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def clamp(v, a, b):
    return max(a, min(b, v))


def cover(img, w, h):
    s = max(w / img.width, h / img.height)
    r = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))), Image.LANCZOS)
    x = (r.width - w) // 2
    y = (r.height - h) // 2
    return r.crop((x, y, x + w, y + h))


def backdrop(img):
    """พื้นหลังเบลอเข้ม + ขอบมืด"""
    bg = cover(img, W // 3, H // 3).filter(ImageFilter.GaussianBlur(22)).resize((W, H), Image.LANCZOS)
    dark = Image.new("RGB", (W, H), (6, 8, 12))
    bg = Image.blend(bg, dark, 0.62)
    # vignette
    vig = Image.new("L", (W // 4, H // 4), 0)
    d = ImageDraw.Draw(vig)
    d.ellipse((-W // 8, -H // 16, W // 4 + W // 8, H // 4 + H // 16), fill=140)
    vig = vig.filter(ImageFilter.GaussianBlur(40)).resize((W, H), Image.LANCZOS)
    shade = Image.new("RGB", (W, H), (0, 0, 0))
    return Image.composite(bg, Image.blend(bg, shade, 0.55), vig)


def rounded_mask(size, radius):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return m


def text_center(draw, xy, text, f, fill=WHITE, shadow=True):
    x, y = xy
    if shadow:
        draw.text((x + 2, y + 3), text, font=f, fill=(0, 0, 0, 170), anchor="mm")
    draw.text((x, y), text, font=f, fill=fill, anchor="mm")


def arrow_polygon(tip, tail, shaft=30, head_w=94, head_l=86):
    """คืนพิกัดรูปหลายเหลี่ยมของลูกศรจากหาง -> ปลาย"""
    tx, ty = tip
    ax, ay = tail
    dx, dy = tx - ax, ty - ay
    L = math.hypot(dx, dy) or 1.0
    ux, uy = dx / L, dy / L          # แกนลูกศร
    px, py = -uy, ux                 # แกนตั้งฉาก
    head_l = min(head_l, L * 0.6)
    bx, by = tx - ux * head_l, ty - uy * head_l   # โคนหัวลูกศร
    hw, sw = head_w / 2, shaft / 2
    P = lambda x, y, o, s: (x + px * o + ux * s, y + py * o + uy * s)
    return [
        (tx, ty),
        P(bx, by, hw, 0),
        P(bx, by, sw, 0),
        P(ax, ay, sw, 0),
        P(ax, ay, -sw, 0),
        P(bx, by, -sw, 0),
        P(bx, by, -hw, 0),
    ]


# ---------- ฉากภาพ ----------
class Scene:
    def __init__(self, spec, index, total):
        self.spec = spec
        self.index = index
        self.total = total
        self.img = Image.open(os.path.join(ASSETS, spec["file"])).convert("RGB")
        self.bg = backdrop(self.img)
        # กรอบภาพ
        landscape = self.img.width > self.img.height
        max_w, max_h = (1040, 1250) if landscape else (1000, 1250)
        s = min(max_w / self.img.width, max_h / self.img.height)
        self.cw, self.ch = int(self.img.width * s), int(self.img.height * s)
        self.card = self.img.resize((self.cw, self.ch), Image.LANCZOS)
        self.cx, self.cy = W // 2, (830 if landscape else 790)   # จุดกึ่งกลางกรอบภาพ

    # แปลงพิกัดสัดส่วนของภาพ -> พิกัดบนเฟรม ตามสเกลที่กำลังซูม
    def to_screen(self, nx, ny, zoom):
        w, h = self.cw * zoom, self.ch * zoom
        x0, y0 = self.cx - w / 2, self.cy - h / 2
        return x0 + nx * w, y0 + ny * h

    def magnifier(self, size=330, zoom_src=0.42):
        """ครอปวงกลมซูมบริเวณจุดชน"""
        bx0, by0, bx1, by1 = self.spec["box"]
        iw, ih = self.img.width, self.img.height
        cw = clamp((bx1 - bx0) * iw * 0.8, 260, iw * 0.6)
        fx, fy = self.spec["focus"]
        cx, cy = fx * iw, fy * ih
        half = cw / 2
        cx = clamp(cx, half, iw - half)
        cy = clamp(cy, half, ih - half)
        crop = self.img.crop((int(cx - half), int(cy - half), int(cx + half), int(cy + half)))
        crop = crop.resize((size, size), Image.LANCZOS)
        out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        out.paste(crop, (0, 0), rounded_mask((size, size), size // 2))
        return out

    def render(self, t):
        """t = เวลาในฉาก (วินาที)"""
        fr = self.bg.copy()
        prog = t / SCENE_DUR
        zoom = 1.0 + 0.045 * ease_out(min(1.0, t / SCENE_DUR))
        appear = ease_out(t / 0.45)

        # --- กรอบภาพ ---
        w, h = int(self.cw * zoom), int(self.ch * zoom)
        card = self.card.resize((w, h), Image.LANCZOS)
        x0, y0 = int(self.cx - w / 2), int(self.cy - h / 2)
        shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(shadow).rounded_rectangle(
            (x0 + 8, y0 + 16, x0 + w + 8, y0 + h + 20), radius=34, fill=(0, 0, 0, 150)
        )
        fr = Image.alpha_composite(fr.convert("RGBA"), shadow.filter(ImageFilter.GaussianBlur(18)))
        fr.paste(card, (x0, y0), rounded_mask((w, h), 30))

        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        d.rounded_rectangle((x0, y0, x0 + w - 1, y0 + h - 1), radius=30, outline=(255, 255, 255, 60), width=3)

        fx, fy = self.spec["focus"]
        sx, sy = self.to_screen(fx, fy, zoom)

        # --- กรอบไฮไลต์บริเวณที่เสียหาย ---
        bx0, by0, bx1, by1 = self.spec["box"]
        p0 = self.to_screen(bx0, by0, zoom)
        p1 = self.to_screen(bx1, by1, zoom)
        a = int(210 * appear)
        d.rounded_rectangle((p0[0], p0[1], p1[0], p1[1]), radius=26,
                            outline=YELLOW + (a,), width=5)
        # มุมกรอบเน้นหนา
        cl = 46
        for (px, py, ddx, ddy) in [
            (p0[0], p0[1], 1, 1), (p1[0], p1[1], -1, -1),
            (p0[0], p1[1], 1, -1), (p1[0], p0[1], -1, 1),
        ]:
            d.line([(px, py + ddy * 10), (px, py + ddy * cl)], fill=YELLOW + (a,), width=9)
            d.line([(px + ddx * 10, py), (px + ddx * cl, py)], fill=YELLOW + (a,), width=9)

        # --- วงพัลส์ที่จุดชน ---
        for k in (0.0, 0.5):
            ph = ((t * 0.85) + k) % 1.0
            r = 46 + 130 * ph
            al = int(200 * (1 - ph) * appear)
            if al > 4:
                d.ellipse((sx - r, sy - r, sx + r, sy + r), outline=RED + (al,), width=6)
        d.ellipse((sx - 13, sy - 13, sx + 13, sy + 13), fill=RED + (int(240 * appear),))

        # --- ลูกศรชี้จุดที่ชน ---
        tdx, tdy = self.spec["tail"]
        bounce = 16 * math.sin(t * 2 * math.pi * 1.25)
        L = math.hypot(tdx, tdy)
        ux, uy = tdx / L, tdy / L
        grow = 1.0 if t > 0.45 else (0.25 + 0.75 * appear)
        tail = (sx + ux * (L * grow + bounce), sy + uy * (L * grow + bounce))
        tip = (sx + ux * (26 + bounce * 0.35), sy + uy * (26 + bounce * 0.35))
        poly = arrow_polygon(tip, tail)
        d.polygon(poly, fill=(0, 0, 0, int(120 * appear)))       # เงา
        poly = [(x - 4, y - 5) for x, y in poly]
        d.polygon(poly, fill=YELLOW + (int(255 * appear),), outline=INK + (255,))
        d.line(poly + [poly[0]], fill=INK + (int(255 * appear),), width=5, joint="curve")

        fr = Image.alpha_composite(fr, ov)

        # --- วงซูมขยาย ---
        mag = self.magnifier()
        msz = mag.size[0]
        pad = 26
        corners = {
            "tl": (x0 + pad, y0 + pad), "tr": (x0 + w - msz - pad, y0 + pad),
            "bl": (x0 + pad, y0 + h - msz - pad), "br": (x0 + w - msz - pad, y0 + h - msz - pad),
        }
        best = max(corners.items(),
                   key=lambda kv: math.hypot(kv[1][0] + msz / 2 - sx, kv[1][1] + msz / 2 - sy))
        mx, my = best[1]
        my = clamp(my, 200, H - msz - 420)
        ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        rd = ImageDraw.Draw(ring)
        rd.ellipse((mx - 7, my - 7, mx + msz + 7, my + msz + 7), fill=(0, 0, 0, int(150 * appear)))
        fr = Image.alpha_composite(fr, ring)
        if appear > 0.05:
            m2 = mag.copy()
            m2.putalpha(m2.getchannel("A").point(lambda v: int(v * appear)))
            fr.alpha_composite(m2, (int(mx), int(my)))
        ring2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        r2 = ImageDraw.Draw(ring2)
        r2.ellipse((mx, my, mx + msz, my + msz), outline=YELLOW + (int(255 * appear),), width=7)
        f_zoom = font(30)
        chip_w = int(f_zoom.getlength("ซูมจุดที่ชน")) + 34
        r2.rounded_rectangle((mx + msz / 2 - chip_w / 2, my + msz - 22,
                              mx + msz / 2 + chip_w / 2, my + msz + 28),
                             radius=25, fill=INK + (int(230 * appear),))
        r2.text((mx + msz / 2, my + msz + 3), "ซูมจุดที่ชน", font=f_zoom,
                fill=YELLOW + (int(255 * appear),), anchor="mm")
        fr = Image.alpha_composite(fr, ring2)

        # --- ส่วนหัว / คำบรรยาย / แถบความคืบหน้า ---
        ui = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        u = ImageDraw.Draw(ui)
        badge = "HONDA HR-V · เคสรถโดนชนท้าย"
        fb = font(34)
        bw = int(fb.getlength(badge)) + 60
        u.rounded_rectangle((W / 2 - bw / 2, 70, W / 2 + bw / 2, 138), radius=34, fill=(0, 0, 0, 190))
        u.text((W / 2, 104), badge, font=fb, fill=WHITE, anchor="mm")

        # แผงคำบรรยาย
        top = 1500
        u.rounded_rectangle((56, top, W - 56, top + 250), radius=30, fill=(8, 10, 14, 214))
        u.rounded_rectangle((56, top + 24, 70, top + 226), radius=8, fill=YELLOW)
        num = f"จุดที่ {self.index + 1}/{self.total}"
        fn = font(34)
        nw = int(fn.getlength(num)) + 44
        u.rounded_rectangle((96, top - 34, 96 + nw, top + 30), radius=32, fill=YELLOW)
        u.text((96 + nw / 2, top - 2), num, font=fn, fill=INK, anchor="mm")
        u.text((100, top + 78), self.spec["head"], font=font(56), fill=YELLOW, anchor="lm")
        u.text((100, top + 148), self.spec["caption"][0], font=font(40), fill=WHITE, anchor="lm")
        u.text((100, top + 202), self.spec["caption"][1], font=font(36, bold=False),
               fill=(214, 219, 228), anchor="lm")

        # แถบบอกลำดับ
        seg_w = (W - 200) / self.total
        for i in range(self.total):
            x = 100 + i * seg_w
            fill = (255, 255, 255, 70)
            if i < self.index:
                fill = YELLOW + (200,)
            elif i == self.index:
                fill = YELLOW + (255,)
            width_done = seg_w - 12 if i != self.index else (seg_w - 12) * clamp(prog, 0, 1)
            u.rounded_rectangle((x, 1810, x + seg_w - 12, 1820), radius=6, fill=(255, 255, 255, 55))
            if width_done > 2:
                u.rounded_rectangle((x, 1810, x + width_done, 1820), radius=6, fill=fill)

        return Image.alpha_composite(fr, ui).convert("RGB")


class CardScene:
    """ฉากเปิด / ฉากปิด"""

    def __init__(self, base_img, lines, dur, footer=None):
        self.bg = backdrop(base_img)
        dark = Image.new("RGB", (W, H), (5, 6, 9))
        self.bg = Image.blend(self.bg, dark, 0.28)
        self.lines = lines
        self.dur = dur
        self.footer = footer

    def render(self, t):
        fr = self.bg.copy().convert("RGBA")
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        y = H / 2 - 210
        for i, (txt, size, color) in enumerate(self.lines):
            a = ease_out((t - 0.18 * i) / 0.6)
            dy = (1 - a) * 40
            f = font(size)
            d.text((W / 2 + 3, y + dy + 4), txt, font=f, fill=(0, 0, 0, int(150 * a)), anchor="mm")
            d.text((W / 2, y + dy), txt, font=f, fill=color + (int(255 * a),), anchor="mm")
            y += size + 46
        # ลูกศรตกแต่ง
        a = ease_out((t - 0.5) / 0.6)
        if a > 0.02:
            cxp, cyp = W / 2, y + 60
            bounce = 12 * math.sin(t * 2 * math.pi * 1.1)
            poly = arrow_polygon((cxp, cyp + 110 + bounce), (cxp, cyp - 30 + bounce),
                                 shaft=26, head_w=80, head_l=70)
            d.polygon(poly, fill=YELLOW + (int(255 * a),), outline=INK + (255,))
        if self.footer:
            fa = ease_out((t - 0.9) / 0.6)
            d.text((W / 2, H - 220), self.footer, font=font(36, bold=False),
                   fill=(210, 216, 226, int(255 * fa)), anchor="mm")
        return Image.alpha_composite(fr, ov).convert("RGB")


def build_timeline():
    scenes = [Scene(s, i, len(SCENES)) for i, s in enumerate(SCENES)]
    first = Image.open(os.path.join(ASSETS, SCENES[0]["file"])).convert("RGB")
    last = Image.open(os.path.join(ASSETS, SCENES[-1]["file"])).convert("RGB")
    intro = CardScene(first, [
        ("รถโดนชนท้าย", 104, WHITE),
        ("ตามลูกศร ดูจุดที่โดนชน", 56, YELLOW),
        ("Honda HR-V · เสียหาย 5 จุด", 40, (214, 219, 228)),
    ], TITLE_DUR, footer="เลื่อนดูทีละจุดจนครบ")
    outro = CardScene(last, [
        ("ถ่ายเก็บให้ครบทุกจุด", 84, WHITE),
        ("ก่อนแจ้งเคลมประกัน", 64, YELLOW),
        ("ถ่ายใกล้ + ถ่ายไกล ให้เห็นตำแหน่งชัด", 38, (214, 219, 228)),
    ], OUTRO_DUR, footer="เซฟไว้เลย เผื่อวันที่ต้องใช้")
    items = [(intro, TITLE_DUR)] + [(s, SCENE_DUR) for s in scenes] + [(outro, OUTRO_DUR)]
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default=os.path.join(ROOT, "out", "rear_end_collision.mp4"))
    args = ap.parse_args()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    items = build_timeline()
    starts, acc = [], 0.0
    for _, dur in items:
        starts.append(acc)
        acc += dur
    total = acc
    n_frames = int(round(total * FPS))

    try:
        import imageio_ffmpeg
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        ffmpeg = "ffmpeg"

    cmd = [
        ffmpeg, "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-shortest",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-c:a", "aac", "-b:a", "96k",
        args.out,
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    for i in range(n_frames):
        t = i / FPS
        idx = 0
        for k, st in enumerate(starts):
            if t >= st:
                idx = k
        local = t - starts[idx]
        frame = items[idx][0].render(local)
        if idx > 0 and local < XFADE:                      # เฟดข้ามฉาก
            prev, pdur = items[idx - 1]
            prev_frame = prev.render(pdur + local)
            frame = Image.blend(prev_frame, frame, ease_out(local / XFADE))
        proc.stdin.write(frame.tobytes())
        if i % 60 == 0:
            print(f"  เรนเดอร์ {i}/{n_frames} เฟรม", flush=True)

    proc.stdin.close()
    if proc.wait() != 0:
        sys.exit("ffmpeg ล้มเหลว")
    print(f"เสร็จแล้ว: {args.out}  ({total:.1f} วินาที, {n_frames} เฟรม)")


if __name__ == "__main__":
    main()

from PIL import Image, ImageDraw, ImageFont
import math, os

# ---------- canvas ----------
W, H = 1800, 1310
S = 2
img = Image.new("RGB", (W * S, H * S), "white")
d = ImageDraw.Draw(img)

FONT = r"C:\Windows\Fonts\msyh.ttc"
FONTB = r"C:\Windows\Fonts\msyhbd.ttc"
def f(size, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, size * S, index=0)

# ---------- colours ----------
BLUE   = (31, 95, 191)
ORANGE = (214, 106, 8)
INK    = (35, 35, 35)
GREY   = (115, 115, 115)
LGREY  = (170, 170, 170)
WATER  = (221, 239, 250)
WALL   = (35, 35, 35)
RED    = (180, 30, 30)

class Panel:
    def __init__(self, baseline):
        self.baseline = baseline
        self.x0 = 140
        self.xs = 151.5
        self.zs = 80.0
    def p(self, x, z):
        return ((self.x0 + (x + 2.0) * self.xs) * S,
                (self.baseline - z * self.zs) * S)
    def line(self, pts, fill, width=3, dash=None):
        q = [self.p(x, z) for x, z in pts]
        if dash is None:
            d.line(q, fill=fill, width=int(width * S), joint="curve")
        else:
            self.dashed(q, fill, width, dash)
    def dashed(self, q, fill, width, dash):
        on, off = dash
        dist_left = on * S
        drawing = True
        for (x1, y1), (x2, y2) in zip(q[:-1], q[1:]):
            seg = math.hypot(x2 - x1, y2 - y1)
            t = 0.0
            while t < seg:
                step = min(dist_left, seg - t)
                a = (x1 + (x2 - x1) * t / seg, y1 + (y2 - y1) * t / seg)
                b = (x1 + (x2 - x1) * (t + step) / seg, y1 + (y2 - y1) * (t + step) / seg)
                if drawing:
                    d.line([a, b], fill=fill, width=int(width * S))
                t += step
                dist_left -= step
                if dist_left <= 1e-6:
                    drawing = not drawing
                    dist_left = (on if drawing else off) * S
    def txt(self, x, z, s, size=25, fill=INK, bold=False, anchor="mm", stroke=4, stroke_fill="white"):
        d.text(self.p(x, z), s, font=f(size, bold), fill=fill, anchor=anchor,
               stroke_width=stroke, stroke_fill=stroke_fill)
    def dot(self, x, z, r=5, fill=INK, outline="white"):
        px, py = self.p(x, z)
        rr = r * S
        d.ellipse((px - rr, py - rr, px + rr, py + rr), fill=fill, outline=outline, width=int(1.4 * S))
    def arrow(self, x1, z1, x2, z2, fill=INK, width=2.4, head=11):
        p1, p2 = self.p(x1, z1), self.p(x2, z2)
        d.line([p1, p2], fill=fill, width=int(width * S))
        ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
        h = head * S
        w = h * 0.45
        a = (p2[0] - h * math.cos(ang) + w * math.sin(ang), p2[1] - h * math.sin(ang) - w * math.cos(ang))
        b = (p2[0] - h * math.cos(ang) - w * math.sin(ang), p2[1] - h * math.sin(ang) + w * math.cos(ang))
        d.polygon([p2, a, b], fill=fill)
    def darrow(self, x, z1, z2, fill=INK, width=2.4, head=10):
        p1, p2 = self.p(x, z1), self.p(x, z2)
        d.line([p1, p2], fill=fill, width=int(width * S))
        for p, sign in ((p1, 1), (p2, -1)):
            a = (p[0] - head * S * 0.45, p[1] + sign * head * S)
            b = (p[0] + head * S * 0.45, p[1] + sign * head * S)
            d.polygon([p, a, b], fill=fill)

def draw_panel(P, mode):
    r1, r2 = 0.38, 0.268
    xin, x1, xc, x2, xout = -0.55, 3.85, 4.05, 7.35, 7.35
    # water in reservoir + pipe
    d.rectangle([P.p(-2.0, 4.0), P.p(-0.55, -0.55)], fill=WATER)
    pipe_poly = [P.p(xin, -r1), P.p(x1, -r1), P.p(xc, -r2), P.p(x2, -r2),
                 P.p(x2, r2), P.p(xc, r2), P.p(x1, r1), P.p(xin, r1)]
    d.polygon(pipe_poly, fill=WATER)
    # reservoir walls
    P.line([(-2.0, 4.0), (-2.0, -0.55), (-0.55, -0.55)], WALL, 4.2)
    P.line([(-2.0, 4.0), (-0.55, 4.0)], WALL, 3.2)
    P.line([(-0.55, 4.0), (-0.55, r1)], WALL, 4.2)
    P.line([(-0.55, -r1), (-0.55, -0.55)], WALL, 4.2)
    # pipe walls
    P.line([(xin, r1), (x1, r1), (xc, r2), (x2, r2)], WALL, 4.2)
    P.line([(xin, -r1), (x1, -r1), (xc, -r2), (x2, -r2)], WALL, 4.2)
    # water surface
    P.line([(-2.0, 4.0), (-0.55, 4.0)], (65, 125, 190), 2.2)
    # free-surface triangle
    px, py = P.p(-1.28, 4.0)
    tri = [(px, py), (px - 11 * S, py - 17 * S), (px + 11 * S, py - 17 * S)]
    d.polygon(tri, fill=(65, 125, 190))
    # centreline / datum
    P.line([(xin, 0), (xout, 0)], LGREY, 1.1, dash=(9, 6))
    # H arrow
    P.darrow(-1.42, 0.0, 4.0, fill=INK, width=2.2, head=10)
    P.txt(-1.30, 2.05, "H = 4 m", 25, INK, True, anchor="lm")
    # A point
    P.dot(xin, 0, r=5.2, fill=RED)
    P.txt(xin - 0.13, -0.40, "A", 25, RED, True, anchor="rm")
    # flow arrow
    P.arrow(xout, 0, 8.06, 0, fill=INK, width=2.6, head=12)
    P.txt(7.72, 0.22, "流向", 20, GREY, False, anchor="mm", stroke=3)

    # ---- head lines ----
    if mode == "ideal":
        # EGL / HGL in reservoir coincide
        P.line([(-2.0, 4.0), (xin, 4.0)], BLUE, 5.0)
        P.line([(xin, 4.0), (xin, 3.0)], ORANGE, 4.6, dash=(8, 5))
        P.line([(xin, 3.0), (xc, 3.0)], ORANGE, 5.0)
        P.line([(xc, 3.0), (xc, 0.0)], ORANGE, 4.6, dash=(8, 5))
        P.line([(xc, 0.0), (xout, 0.0)], ORANGE, 5.0)
        P.line([(xin, 4.0), (xout, 4.0)], BLUE, 5.0)
        # labels
        P.txt(-1.33, 4.20, "EGL = HGL = 4.00", 20, BLUE, True, anchor="mm", stroke=5)
        P.txt(2.15, 4.16, "总水头线 EGL = 4.00 m", 23, BLUE, True, anchor="mm")
        P.txt(1.72, 3.14, "HGL = 3.00 m", 23, ORANGE, True, anchor="mm")
        P.txt(6.10, 0.46, "HGL = 0（管轴）", 20, ORANGE, True, anchor="mm")
        P.dot(6.10, 0.0, r=3.8, fill=ORANGE)
        P.line([(6.10, 0.36), (6.10, 0.03)], ORANGE, 1.3, dash=(5, 4))
        P.txt(1.95, 3.50, "v1²/(2g) = 1.00 m", 20, GREY, False, anchor="mm")
        P.txt(5.95, 2.00, "v2²/(2g) = 4.00 m", 20, GREY, False, anchor="mm")
        P.dot(xc, 3.0, r=4.2, fill=ORANGE)
        P.dot(xc, 0.0, r=4.2, fill=ORANGE)
    else:
        # EGL
        P.line([(-2.0, 4.0), (xin, 4.0)], BLUE, 5.0)
        P.line([(xin, 4.0), (xc, 3.2)], BLUE, 5.0)
        P.line([(xc, 3.2), (xout, 0.8)], BLUE, 5.0)
        # HGL
        P.line([(xin, 4.0), (xin, 3.8)], ORANGE, 4.6, dash=(8, 5))
        P.line([(xin, 3.8), (xc, 3.0)], ORANGE, 5.0)
        P.line([(xc, 3.0), (xc, 2.4)], ORANGE, 4.6, dash=(8, 5))
        P.line([(xc, 2.4), (xout, 0.0)], ORANGE, 5.0)
        # labels
        P.txt(-1.38, 4.20, "EGL = HGL = 4.00", 20, BLUE, True, anchor="mm", stroke=5)
        P.txt(1.85, 3.78, "总水头线 EGL", 23, BLUE, True, anchor="mm")
        P.txt(4.30, 3.46, "3.20", 21, BLUE, True, anchor="mm")
        P.line([(4.14, 3.34), (4.07, 3.22)], BLUE, 1.2, dash=(4, 3))
        P.txt(7.02, 1.34, "0.80", 21, BLUE, True, anchor="mm")
        P.line([(7.12, 1.24), (7.30, 0.84)], BLUE, 1.2, dash=(4, 3))
        P.txt(0.55, 3.32, "HGL 3.80", 21, ORANGE, True, anchor="mm")
        P.line([(0.30, 3.44), (0.06, 3.72)], ORANGE, 1.2, dash=(4, 3))
        P.txt(3.62, 2.66, "3.00", 21, ORANGE, True, anchor="mm")
        P.line([(3.72, 2.80), (4.01, 3.00)], ORANGE, 1.2, dash=(4, 3))
        P.txt(1.78, 2.92, "3.40（中点）", 20, ORANGE, True, anchor="mm")
        P.line([(1.78, 3.06), (1.78, 3.38)], ORANGE, 1.2, dash=(4, 3))
        P.txt(4.38, 1.96, "2.40", 21, ORANGE, True, anchor="mm")
        P.line([(4.26, 2.10), (4.08, 2.37)], ORANGE, 1.2, dash=(4, 3))
        P.txt(5.70, 1.56, "1.20（中点）", 20, ORANGE, True, anchor="mm")
        P.line([(5.70, 1.43), (5.70, 1.22)], ORANGE, 1.2, dash=(4, 3))
        P.dot(5.70, 1.20, r=3.4, fill=ORANGE)
        P.txt(7.48, 0.10, "0", 21, ORANGE, True, anchor="lm")
        P.dot(xc, 3.2, r=4.2, fill=BLUE)
        P.dot(xc, 3.0, r=4.2, fill=ORANGE)
        P.dot(xc, 2.4, r=4.2, fill=ORANGE)
        # loss summary
        P.txt(6.55, 3.78, "沿程损失\nh_f1 = 0.80 m\nh_f2 = 2.40 m", 20, GREY, False, anchor="mm", stroke=5)

def draw_panel_frame(P):
    # section labels
    P.txt(1.55, 0.86, "S1 = 0.2 m²", 23, INK, True, anchor="mm")
    P.txt(5.65, 0.70, "S2 = 0.1 m²", 23, INK, True, anchor="mm")

def draw_common():
    # main title
    d.text((900 * S, 30 * S), "题 3-19　总水头线与测压管水头线", font=f(37, True),
           fill=INK, anchor="ma")
    # legend
    y = 83
    d.line([(410 * S, y * S), (475 * S, y * S)], fill=BLUE, width=int(5 * S))
    d.text((486 * S, y * S), "总水头线 EGL", font=f(23), fill=INK, anchor="lm")
    d.line([(680 * S, y * S), (745 * S, y * S)], fill=ORANGE, width=int(5 * S))
    d.text((756 * S, y * S), "测压管水头线 HGL（p/γ + z）", font=f(23), fill=INK, anchor="lm")
    d.line([(1245 * S, y * S), (1310 * S, y * S)], fill=LGREY, width=int(1.4 * S))
    d.text((1321 * S, y * S), "管轴 / 基准面 z = 0", font=f(23), fill=INK, anchor="lm")

# create panels
P1 = Panel(600)
P2 = Panel(1200)
draw_common()

# titles
P1.txt(-1.95, 4.72, "（1）不计损失", 29, INK, True, anchor="lm")
P1.txt(0.0, 4.72, "v1 = 4.43 m/s，v2 = 8.85 m/s", 24, RED, True, anchor="lm")
P2.txt(-1.95, 4.72, "（2）计入损失", 29, INK, True, anchor="lm")
P2.txt(0.0, 4.72, "h_f1 = 4v1²/(2g)，h_f2 = 3v2²/(2g)", 23, RED, True, anchor="lm")

for P, mode in ((P1, "ideal"), (P2, "loss")):
    draw_panel(P, mode)
    draw_panel_frame(P)
    P.txt(1.35, -0.52, "v1 = 4.43 m/s" if mode == "ideal" else "v1 = 1.98 m/s",
          20, INK, False, anchor="mm")
    P.txt(5.55, -0.52, "v2 = 8.85 m/s" if mode == "ideal" else "v2 = 3.96 m/s",
          20, INK, False, anchor="mm")

# separator line
d.line([(90 * S, 665 * S), (1710 * S, 665 * S)], fill=(225, 225, 225), width=int(1.2 * S))

# bottom notes
P1.txt(-1.90, -0.92, "水库内 EGL 与 HGL 重合；进口和收缩处 HGL 的竖直跌落由速度水头变化引起。",
       17, GREY, False, anchor="lm", stroke=0)
P2.txt(-1.90, -0.92, "沿程损失使 EGL 沿程下降；HGL 与 EGL 的竖直间距为速度水头 v²/(2g)。",
       17, GREY, False, anchor="lm", stroke=0)
d.text((1710 * S, 1293 * S), "水平长度仅示意，未按比例", font=f(17), fill=GREY, anchor="ra")

# save
img = img.resize((W, H), Image.LANCZOS)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "题3-19_水头线图.png")
img.save(out, dpi=(300, 300))
print(out)

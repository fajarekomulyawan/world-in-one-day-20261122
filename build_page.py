#!/usr/bin/env python3
"""Build v2 of the news-image-20261122 entry: a denser newspaper
front page summing up Saturday 22 November 2026 in one image.

2048 px wide. Cream paper, ink text, one red accent, flat
geometric illustrations drawn with PIL. 60 stories: 1 lead,
2 secondary, 13 illustrated cards, 44 index lines, plus a
dotted world map and a day-in-numbers panel.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = 2048
M = 64
CW = W - 2 * M

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_O = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

PAPER = (247, 243, 233)
INK = (26, 24, 20)
RED = (154, 32, 38)
FAINT = (110, 102, 90)
PANEL = (238, 231, 214)
CHIP_COLORS = {
    "EUROPE": (122, 44, 34), "MIDDLE EAST": (146, 64, 20),
    "US": (30, 58, 95), "ASIA": (24, 92, 80), "GLOBAL": (60, 60, 60),
    "AMERICAS": (96, 62, 110), "AFRICA": (120, 84, 20),
    "WORLD": (70, 90, 40), "SCIENCE": (40, 70, 110),
}


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, font, fill, maxw, leading):
    for ln in wrap(d, text, font, maxw):
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


# ---------------- illustrations (flat, geometric) ----------------

def ill_chart_down(d, box, color=RED):
    x0, y0, x1, y1 = box
    pts = [(x0 + 20, y0 + 30), (x0 + 90, y0 + 55), (x0 + 150, y0 + 40),
           (x0 + 210, y0 + 85), (x0 + 280, y1 - 25)]
    d.line(pts, fill=color, width=9, joint="curve")
    for i, bh in enumerate((55, 80, 45, 95)):
        bx = x0 + 45 + i * 62
        d.rectangle([bx, y1 - 20 - bh, bx + 34, y1 - 20], fill=(190, 90, 80))


def ill_chart_up(d, box):
    x0, y0, x1, y1 = box
    pts = [(x0 + 20, y1 - 35), (x0 + 95, y1 - 60), (x0 + 160, y1 - 50),
           (x0 + 225, y0 + 45), (x0 + 285, y0 + 22)]
    d.line(pts, fill=(146, 110, 30), width=9, joint="curve")


def ill_missiles(d, box):
    x0, y0, x1, y1 = box
    d.polygon([(x0 + 30, y1), (x0 + 120, y0 + 30), (x0 + 230, y1)],
              fill=(120, 118, 112))
    d.polygon([(x0 + 95, y1), (x0 + 150, y0 + 70), (x0 + 205, y1)],
              fill=(90, 88, 84))
    for bx, by in ((120, 120), (185, 95)):
        d.polygon([(x0 + bx, y1 - by - 26), (x0 + bx + 13, y1 - by),
                   (x0 + bx, y1 - by + 26), (x0 + bx - 13, y1 - by)],
                  fill=(230, 130, 40))
        d.ellipse([x0 + bx - 8, y1 - by - 8, x0 + bx + 8, y1 - by + 8],
                  fill=(250, 190, 60))


def ill_ship(d, box):
    x0, y0, x1, y1 = box
    d.rectangle([x0 + 20, y1 - 45, x1 - 20, y1 - 18], fill=(40, 60, 110))
    d.rectangle([x0 + 60, y1 - 78, x0 + 130, y1 - 45], fill=(200, 200, 205))
    d.rectangle([x0 + 150, y1 - 70, x1 - 70, y1 - 45], fill=(160, 60, 50))
    d.line([x0 + 10, y1 - 12, x1 - 10, y1 - 12], fill=(70, 120, 170), width=6)


def ill_bridge(d, box):
    x0, y0, x1, y1 = box
    d.rectangle([x0 + 15, y1 - 60, x0 + 130, y1 - 48], fill=(90, 90, 95))
    d.rectangle([x0 + 185, y1 - 60, x1 - 15, y1 - 48], fill=(90, 90, 95))
    d.polygon([(x0 + 130, y1 - 48), (x0 + 185, y1 - 48), (x0 + 170, y1 - 18),
               (x0 + 140, y1 - 18)], fill=(60, 60, 66))
    d.line([x0 + 10, y1 - 10, x1 - 10, y1 - 10], fill=(70, 120, 170), width=6)


def ill_van(d, box, cross=True):
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0 + 35, y0 + 45, x1 - 55, y1 - 35], 10,
                        fill=(235, 235, 238), outline=INK, width=4)
    for wx in (x0 + 85, x1 - 105):
        d.ellipse([wx, y1 - 52, wx + 34, y1 - 18], fill=INK)
    if cross:
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 8
        d.rectangle([cx - 8, cy - 26, cx + 8, cy + 26], fill=RED)
        d.rectangle([cx - 26, cy - 8, cx + 26, cy + 8], fill=RED)


def ill_chip(d, box):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle([cx - 55, cy - 55, cx + 55, cy + 55], fill=(24, 92, 80))
    d.rectangle([cx - 30, cy - 30, cx + 30, cy + 30], fill=(16, 60, 52))
    for i in range(5):
        p = cx - 52 + i * 26
        d.line([p, cy - 78, p, cy - 55], fill=INK, width=6)
        d.line([p, cy + 55, p, cy + 78], fill=INK, width=6)


def ill_protest(d, box):
    x0, y0, x1, y1 = box
    for i, cx in enumerate((x0 + 70, x0 + 150, x0 + 230)):
        d.ellipse([cx - 16, y1 - 85, cx + 16, y1 - 53], fill=(30, 58, 95))
        d.rectangle([cx - 18, y1 - 53, cx + 18, y1 - 15], fill=(30, 58, 95))
    d.rectangle([x0 + 105, y0 + 18, x0 + 205, y0 + 46], fill=(245, 240, 230),
                outline=INK, width=3)


def ill_capitol(d, box):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    d.polygon([(cx - 30, y0 + 30), (cx + 30, y0 + 30), (cx, y0 + 2)],
              fill=(30, 58, 95))
    d.rectangle([cx - 70, y0 + 34, cx + 70, y0 + 48], fill=(30, 58, 95))
    for i in range(5):
        px = cx - 60 + i * 30
        d.rectangle([px, y0 + 52, px + 10, y1 - 30], fill=(30, 58, 95))
    d.rectangle([x0 + 25, y1 - 26, x1 - 25, y1 - 14], fill=(30, 58, 95))
    d.polygon([(x1 - 62, y0 + 52), (x1 - 40, y0 + 74), (x1 - 88, y0 + 70)],
              fill=(60, 160, 90))


def ill_quake(d, box):
    x0, y0, x1, y1 = box
    for bx, bh, tilt in ((x0 + 30, 95, 0), (x0 + 120, 120, 4), (x0 + 215, 80, -3)):
        d.rectangle([bx, y1 - 15 - bh, bx + 62, y1 - 15], fill=(120, 110, 100))
    d.line([x0 + 10, y1 - 12, x0 + 90, y1 - 20, x0 + 150, y1 - 8,
            x0 + 230, y1 - 18, x1 - 12, y1 - 10], fill=RED, width=6)


def ill_globe(d, box):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.ellipse([cx - 62, cy - 62, cx + 62, cy + 62], outline=(70, 90, 40), width=6)
    d.ellipse([cx - 26, cy - 62, cx + 26, cy + 62], outline=(70, 90, 40), width=4)
    d.line([cx - 62, cy, cx + 62, cy], fill=(70, 90, 40), width=4)
    d.polygon([(cx + 78, cy - 70), (cx + 92, cy - 34), (cx + 64, cy - 34)],
              fill=RED)


def ill_probe(d, box):
    x0, y0, x1, y1 = box
    cx, cy = x0 + 120, (y0 + y1) // 2
    d.ellipse([cx - 62, cy - 62, cx + 62, cy + 62], outline=INK, width=6)
    d.rectangle([cx + 55, cy - 10, cx + 130, cy + 10], fill=(90, 90, 95))
    d.rectangle([cx + 128, cy - 34, cx + 168, cy + 34], fill=(200, 170, 60))
    for sx, sy in ((x1 - 60, y0 + 25), (x1 - 110, y0 + 60), (x1 - 45, y1 - 40)):
        d.polygon([(sx, sy - 10), (sx + 3, sy - 3), (sx + 10, sy), (sx + 3, sy + 3),
                   (sx, sy + 10), (sx - 3, sy + 3), (sx - 10, sy), (sx - 3, sy - 3)],
                  fill=(150, 150, 160))


def ill_fire(d, box):
    x0, y0, x1, y1 = box
    d.rectangle([x0 + 30, y1 - 50, x1 - 30, y1 - 24], fill=(50, 50, 55))
    d.rectangle([x0 + 120, y1 - 78, x0 + 190, y1 - 50], fill=(50, 50, 55))
    for fx in (x0 + 80, x0 + 160, x0 + 235):
        d.polygon([(fx, y1 - 78), (fx + 16, y1 - 118), (fx + 30, y1 - 80),
                   (fx + 22, y1 - 62), (fx + 8, y1 - 62)], fill=(235, 120, 40))


ILL = {
    "chart_down": ill_chart_down, "chart_up": ill_chart_up,
    "missiles": ill_missiles, "ship": ill_ship, "bridge": ill_bridge,
    "van": ill_van, "chip": ill_chip, "protest": ill_protest,
    "capitol": ill_capitol, "quake": ill_quake, "globe": ill_globe,
    "probe": ill_probe, "fire": ill_fire,
}

CARDS = [
    ("MIDDLE EAST", "HORMUZ", "ship",
     "Iran strikes US bases in Bahrain",
     "Tehran claims two US bases hit; Bahrain reports a fire; a tanker struck."),
    ("MIDDLE EAST", "RIYADH", "missiles",
     "Saudi Arabia downs three Houthi missiles over Riyadh",
     "Missiles and a drone aimed at the capital are downed; jets answer at Hodeidah."),
    ("EUROPE", "CRIMEA", "bridge",
     "Ukraine brings down part of the Kerch Bridge",
     "Kyiv drops a span of Putin's flagship link; Moscow hit 109 bridges first."),
    ("MIDDLE EAST", "GAZA CITY", "van",
     "Strike on aid vehicle kills three in Gaza City",
     "World Central Kitchen says it was not theirs; Israel says Islamic Jihad."),
    ("ASIA", "TECH — THE AI ROUT", "chip",
     "Asia's AI giants shed $190bn in a single session",
     "Nikkei -5.1%, Seoul -5.2%, Taipei -6.2% as the chip rout circles the globe."),
    ("EUROPE", "UKRAINE WAR — KRYVYI RIH", "van",
     "'Double-tap' strike kills a paramedic and a boy of seven",
     "Missiles, then drones as rescuers work: 60 hurt in Zelensky's hometown."),
    ("EUROPE", "THE BALTIC — FINLAND", "fire",
     "Drone-hit Russian freighter burns in Finnish waters",
     "The Sparta II drifts ablaze into NATO waters; Finland blames Ukraine."),
    ("EUROPE", "FRANCE — PROTESTS", "protest",
     "Cost-of-living protests roll into a sixth Saturday",
     "Turnout thins to 82,500 as unions demand EU action on prices and pay."),
    ("US", "MIDTERMS — WASHINGTON", "capitol",
     "Democrats reclaim Congress in midterm rout",
     "Democrats take both chambers; largest Black Democratic class since 1993."),
    ("AMERICAS", "PERU — LIMA", "quake",
     "Magnitude 6.8 quake sends Lima into the streets",
     "The late-night tremor empties blocks across the capital; no toll yet."),
    ("WORLD", "CLIMATE — COP31", "globe",
     "COP31 climate talks stall over oil and gas",
     "Negotiators deadlock as producers block any fossil-fuel phase-out text."),
    ("SCIENCE", "DEEP SPACE", "probe",
     "Voyager 1 closes on one light-day from Earth",
     "The 1977 probe nears a full light-day away, still whispering home."),
    ("AFRICA", "HEALTH — KENYA", "van",
     "Kenya discharges its last Ebola patient",
     "The final patient walks out; the countdown to outbreak-over begins."),
]

INDEX = [
    "Zelensky: timing of four-party talks rests on Washington",
    "Melania Trump floats a Christmas humanitarian ceasefire",
    "Macron warns of a 'new level' of Russian aggression",
    "UK defence secretary Streeting meets Zelensky in Kyiv",
    "Russia's overnight barrage: 400 drones, 110 missiles",
    "Saudi-led coalition strikes Hodeidah port in reply",
    "Araghchi: Iran ready for talks to reopen Hormuz",
    "CENTCOM calls Iran's downed F-16 claim false",
    "Gaza civil defence: four killed Saturday despite truce",
    "Trump: China agrees to join trilateral nuclear talks",
    "Trump says all G20 leaders expected in Florida",
    "Cyberattacks reported at the FBI and farm ministry",
    "White House removes cyber director after outages",
    "US growth hit 3.4% in Q3; inflation stuck at 3.6%",
    "JPMorgan flips: sees hikes in January and March",
    "Anthropic slides back toward its $83 IPO price",
    "$1.54bn in crypto liquidations across 24 hours",
    "Spot bitcoin ETFs bleed $582m in a single day",
    "India's Nifty is Asia's lone gainer, up 1.1%",
    "Mexico arrests cartel boss 'El Chapo Isidro'",
    "Thousands march against inflation in Lisbon",
    "States agree 'killer robot' rules by 2028",
    "Estonia shuts road crossings with Russia for 6 months",
    "At least 11 die from bootleg liquor in Manipur",
    "Virginia's first child measles death since 1978",
    "Al-Shabaab claims hundreds of Somali troops killed",
    "RSF accused of killing children in South Kordofan",
    "Ghana unveils banknotes honouring Nkrumah, Annan",
    "Norway's top court voids disputed oil licences",
    "Australia bowl first in South Africa decider",
    "Grammy hopes: Tyla, Tems and Kidjo lead Africa",
    "Brent crude jumps as Hormuz traffic halts again",
    "Gold's 4.6% slide is its worst day in over a year",
    "VIX fear gauge leaps 26% in the rout",
    "Seventh straight loss for the S&P 500",
    "December hike odds near 90% on prediction markets",
    "Waller floats a half-point December move",
    "Rutte: NATO will defend every inch of Poland",
    "Kyiv mourns nine dead in the overnight barrage",
    "World Central Kitchen denies Gaza vehicle was theirs",
    "Finland blames Ukraine for the Sparta II fire",
    "Turnout thins at France's sixth protest Saturday",
    "Largest Black Democratic class in Congress since 1993",
    "No toll yet in Lima after the 6.8 tremor",
]

# coarse dotted world map, 92 x 40 grid
MAP = [
    "        oooo                                                                                    ",
    "     oooooooooo      ooo                 oooooooooooooooo        oo                               ",
    "   oooooooooooooo  ooooooo          oooooooooooooooooooooooooo oooooo        ooooo                ",
    "  oooooooooooooooooooooooo        ooooooooooooooooooooooooooooooooooooooo  ooooooooo              ",
    "   ooooooooooooooooooooo         oooooooooooooooooooooooooooooooooooooooooooooooooooo             ",
    "    ooooooooooooooooooo           oooooooooooooooooooooooooooooooooooooooooooooooooooo            ",
    "     ooooooooooooooooo             ooooooooooooooooooooooooooooooooooooooooooooooooo              ",
    "      ooooooooooooooo               ooooooooooooooooooooooooooooooooooooooooooooo                 ",
    "       ooooooooooooo                 oooooooooooooooooooooooooooooooooooooooo                     ",
    "        oooooooooo                    ooooooooooooooooooooooooooooooooooooo                       ",
    "         ooooooooo                     oooooooooooooooooooooooooooooooooo                         ",
    "          ooooooo                       ooooooooooooooooooooooooooooooo                           ",
    "          ooooooo                        ooooooooooooooooooooooooooooo                            ",
    "           ooooo                          ooooooooooooooooooooooooo                               ",
    "           ooooo                           ooooooooooooooooooooo                                  ",
    "            oooo                            oooooooooooooooooo                                    ",
    "            oooo                             ooooooooooooooo                                      ",
    "            oooo                              oooooooooooo                                        ",
    "            ooo                                ooooooooo                                          ",
    "            ooo                                 ooooooo                                           ",
    "            ooo                                  ooooo                                            ",
    "            oo                                   ooooo                                            ",
    "            oo                                    ooo                                             ",
    "            oo                                    oo                                              ",
    "            oo                                                                                    ",
    "            oo                                                                                    ",
]
PINS = [(13, 3), (47, 2), (50, 3), (53, 4), (57, 5), (61, 6), (66, 7), (72, 8),
        (30, 10), (44, 6), (16, 14), (78, 12), (84, 16)]


def main():
    H = 3980
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.line([M, 46, W - M, 46], fill=INK, width=3)
    d.text((M, 62), "THE WORLD'S NEWS IN ONE PICTURE", font=F(SANS_B, 30), fill=INK)
    r = "60 STORIES · 6 CONTINENTS · ALL FROM SATURDAY"
    d.text((W - M - d.textlength(r, font=F(SANS_B, 30)), 62), r,
           font=F(SANS_B, 30), fill=INK)
    title = "Saturday 22 November 2026"
    tf = F(SERIF_B, 118)
    d.text(((W - d.textlength(title, font=tf)) / 2, 108), title, font=tf, fill=INK)
    d.line([M, 262, W - M, 262], fill=INK, width=5)
    d.line([M, 272, W - M, 272], fill=INK, width=2)

    # ticker band
    stats = [("-3.70%", "S&P: 7TH STRAIGHT LOSS"), ("$3,515", "GOLD: LOWEST IN A YEAR"),
             ("$58k", "BITCOIN BREAKS BELOW"), ("35.89", "VIX FEAR GAUGE +26%"),
             ("-14%", "NVIDIA'S ROUT DAY"), ("~90%", "DEC FED HIKE ODDS")]
    y = 292
    colw = CW // 6
    for i, (big, small) in enumerate(stats):
        x = M + i * colw
        bf = F(SERIF_B, 56)
        d.text((x + (colw - d.textlength(big, font=bf)) / 2, y), big, font=bf, fill=INK)
        sf = F(SANS_B, 17)
        d.text((x + (colw - d.textlength(small, font=sf)) / 2, y + 68), small,
               font=sf, fill=FAINT)
        if i:
            d.line([x, y + 4, x, y + 92], fill=FAINT, width=2)
    d.line([M, y + 108, W - M, y + 108], fill=INK, width=3)

    # lead story
    y = 436
    lh = 470
    d.rectangle([M, y, W - M, y + lh], outline=INK, width=3)
    ill_missiles(d, (M + 30, y + 170, M + 800, y + lh - 26))
    d.rectangle([M + 30, y + 22, M + 420, y + 62], fill=RED)
    d.text((M + 48, y + 30), "THE DAY'S BIGGEST STORY", font=F(SANS_B, 24), fill=(255, 255, 255))
    lx = M + 850
    d.text((lx, y + 26), "1  EUROPE · UKRAINE WAR — POLAND", font=F(SANS_B, 26), fill=RED)
    ly = text_block(d, lx, y + 66, "Russian missiles land in Poland; NATO vows defence",
                    F(SERIF_B, 64), INK, W - M - lx - 26, 78)
    text_block(d, lx, ly + 10,
               "Moscow's huge overnight barrage kills nine in Kyiv as missiles cross into "
               "NATO Poland. Rutte: the alliance will defend every inch of Polish soil. "
               "Warsaw scrambles jets and closes two airports as debris falls near Lublin.",
               F(SERIF, 31), INK, W - M - lx - 26, 42)

    # secondary row
    y += lh + 22
    sh = 400
    half = (CW - 22) // 2
    for i, (kick, head, deck, ill) in enumerate([
        ("2  GLOBAL · MARKETS — BLACK FRIDAY", "Wall Street's $8.3tn rout caps a brutal week",
         "The S&P 500 falls 3.7% for a seventh straight loss as AI stocks crater: Nvidia "
         "sheds 14% in a day, gold drops 4.6% and Bitcoin breaks under $58,000.", "chart_down"),
        ("3  US · THE FED — WASHINGTON", "Trump demands world's lowest rates; Fed leans to hike",
         "Trump calls rates 'too high' and political. Traders give ~90% odds of a December "
         "hike to 4.00-4.25%; Waller floats a half-point move.", "chart_up"),
    ]):
        x = M + i * (half + 22)
        d.rectangle([x, y, x + half, y + sh], outline=INK, width=3)
        ILL[ill](d, (x + half - 330, y + 16, x + half - 24, y + 150))
        d.text((x + 24, y + 20), kick, font=F(SANS_B, 24), fill=RED)
        hy = text_block(d, x + 24, y + 58, head, F(SERIF_B, 44), INK, half - 380, 54)
        text_block(d, x + 24, max(hy + 8, y + 168), deck, F(SERIF, 27), INK, half - 48, 36)

    # card grid: 13 cards, rows of 5/4/4
    y += sh + 22
    rows = [CARDS[:5], CARDS[5:9], CARDS[9:]]
    num = 4
    for row in rows:
        n = len(row)
        cw_ = (CW - (n - 1) * 18) // n
        ch = 396
        for i, (region, place, ill, head, deck) in enumerate(row):
            x = M + i * (cw_ + 18)
            d.rectangle([x, y, x + cw_, y + ch], outline=INK, width=2)
            ILL[ill](d, (x + 16, y + 10, x + cw_ - 16, y + 136))
            chip = CHIP_COLORS[region]
            d.rectangle([x, y + 146, x + cw_, y + 182], fill=chip)
            d.text((x + 14, y + 153), f"{region} · {place}", font=F(SANS_B, 18),
                   fill=(255, 255, 255))
            d.text((x + 14, y + 192), f"{num}", font=F(SANS_B, 24), fill=RED)
            hy = text_block(d, x + 54, y + 190, head, F(SERIF_B, 26), INK, cw_ - 68, 32)
            text_block(d, x + 14, hy + 4, deck, F(SERIF, 21), INK, cw_ - 28, 27)
            num += 1
        y += ch + 18

    # map + numbers band
    mh = 360
    d.line([M, y, W - M, y], fill=INK, width=3)
    d.text((M, y + 14), "WHERE IT HAPPENED", font=F(SANS_B, 28), fill=INK)
    cell = 11
    mx, my = M + 6, y + 62
    for ri, rowline in enumerate(MAP):
        for ci, ch_ in enumerate(rowline):
            if ch_ == "o":
                cx, cy = mx + ci * cell, my + ri * cell
                d.ellipse([cx, cy, cx + 6, cy + 6], fill=(178, 164, 128))
    for pi, (px, py) in enumerate(PINS):
        cx, cy = mx + px * cell, my + py * cell
        d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=RED)
        t = str(pi + 1)
        tf2 = F(SANS_B, 17)
        d.text((cx - d.textlength(t, font=tf2) / 2, cy - 10), t, font=tf2,
               fill=(255, 255, 255))
    d.text((M, y + mh - 8), "Pins: stories 1-13 above. One picture, one day — every story "
             "happened or was first reported on Saturday 22 November 2026.",
           font=F(SANS_O, 21), fill=FAINT)
    nx = M + 1090
    d.text((nx, y + 14), "THE DAY IN NUMBERS", font=F(SANS_B, 28), fill=INK)
    nums = [("$8.3tn", "wiped off world stocks in the rout"),
            ("510", "drones & missiles in one night on Ukraine"),
            ("6.8", "the Lima earthquake's magnitude"),
            ("82,500", "marchers at France's sixth protest Saturday"),
            ("1", "light-day: Voyager 1's distance, nearly"),
            ("0", "FOMC friends Trump made at the Fed")]
    ny = y + 58
    for big, small in nums:
        d.text((nx, ny), big, font=F(SERIF_B, 40), fill=RED)
        d.text((nx + 240, ny + 12), small, font=F(SERIF, 24), fill=INK)
        ny += 46
    y += mh + 16

    # index
    d.line([M, y, W - M, y], fill=INK, width=3)
    d.text((M, y + 12), "ALSO ON SATURDAY 22 NOVEMBER", font=F(SANS_B, 28), fill=INK)
    iy = y + 56
    colw2 = (CW - 40) // 2
    per = (len(INDEX) + 1) // 2
    for ci in range(2):
        x = M + ci * (colw2 + 40)
        yy = iy
        for j, item in enumerate(INDEX[ci * per:(ci + 1) * per]):
            n = ci * per + j + 1
            d.text((x, yy), f"{n}.", font=F(SANS_B, 21), fill=RED)
            lines = wrap(d, item, F(SERIF, 22), colw2 - 52)
            for li, ln in enumerate(lines):
                d.text((x + 52, yy + li * 28), ln, font=F(SERIF, 22), fill=INK)
            yy += 28 * len(lines) + 7
            d.line([x, yy - 3, x + colw2, yy - 3], fill=(214, 206, 188), width=1)
    y = iy + per * 35 + 30

    d.line([M, H - 64, W - M, H - 64], fill=INK, width=2)
    d.text((M, H - 52), "Compiled from the day's wire and public reports. Claims by officials are reported as claims.",
           font=F(SANS_O, 20), fill=FAINT)
    r = "Original drawings."
    d.text((W - M - d.textlength(r, font=F(SANS_O, 20)), H - 52), r,
           font=F(SANS_O, 20), fill=FAINT)

    out = os.path.join(HERE, "entry.png")
    img.save(out)
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Draw entry.png for the make.fun bounty
"Sum up 20 November's world news in one image".

A 1024x1024 flat infographic: a dated header plus six story panels.
All artwork is original, drawn with PIL; no photos or third-party art.
Run: python3 draw.py  (writes entry.png next to this file)
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

NAVY = (13, 27, 46)        # page background
PANEL = (23, 41, 63)       # panel background
PANEL_EDGE = (38, 62, 92)  # panel outline
WHITE = (245, 247, 250)
MUTED = (196, 208, 222)    # summary text
AMBER = (245, 166, 35)     # date / rules
GREY = (140, 155, 175)     # footer text

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


STORIES = [
    {
        "tag": "WAR  ·  EUROPE",
        "color": (231, 76, 60),
        "headline": "Russia's biggest blitz hits Kyiv",
        "summary": "400+ drones and 110 missiles hit 3 bridges over the Dnipro "
                   "and the power grid; 8 killed. Two missiles fall in Poland.",
    },
    {
        "tag": "ENERGY  ·  MIDDLE EAST",
        "color": (245, 166, 35),
        "headline": "US blockade chokes the Strait of Hormuz",
        "summary": "A tanker is hit and catches fire off Oman; UKMTO logs the "
                   "strike 8 miles north of Khasab as the US blockade holds.",
    },
    {
        "tag": "TECH  ·  MARKETS",
        "color": (26, 188, 156),
        "headline": "AI selloff drags S&P 500 and Dow into correction",
        "summary": "Nasdaq plunges 5.3% as Nvidia tumbles 14%; the S&P 500 "
                   "falls 3.7% for a seventh straight day into correction.",
    },
    {
        "tag": "CLIMATE",
        "color": (46, 204, 113),
        "headline": "COP31 runs into overtime",
        "summary": "Draft deal in Antalya drops all mention of fossil fuels; "
                   "talks spill past Friday's deadline as activists protest.",
    },
    {
        "tag": "EUROPE  ·  DIPLOMACY",
        "color": (52, 152, 219),
        "headline": "UK floats \u2018Breturn\u2019 at EU summit",
        "summary": "Britain and the EU seal deals in Brussels: food checks end "
                   "and 100,000 youth visas a year. Burnham eyes rejoining.",
    },
    {
        "tag": "HEALTH  ·  SCIENCE",
        "color": (155, 89, 182),
        "headline": "Cancer pill shrinks tumours in 6 in 10",
        "summary": "Daraxonrasib plus chemo shrinks or clears tumours in 60.7% "
                   "of pancreatic cancer patients in Barcelona trial results.",
    },
]


def draw_panel(draw, x, y, pw, ph, story, num):
    draw.rounded_rectangle([x, y, x + pw, y + ph], radius=14,
                           fill=PANEL, outline=PANEL_EDGE, width=1)
    # accent bar on the left
    draw.rounded_rectangle([x, y, x + 9, y + ph], radius=4,
                           fill=story["color"])
    # number badge
    cx, cy, r = x + 34, y + 34, 17
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=story["color"])
    nf = font(SANS_BOLD, 20)
    t = str(num)
    draw.text((cx - draw.textlength(t, font=nf) / 2, cy - 13), t,
              font=nf, fill=NAVY)
    # tag, top right of the badge line
    tf = font(SANS_BOLD, 15)
    draw.text((x + 62, y + 22), story["tag"], font=tf, fill=story["color"])
    # headline
    hf = font(SANS_BOLD, 27)
    inner = pw - 62
    lines = wrap(draw, story["headline"], hf, inner)
    hy = y + 62
    for line in lines[:2]:
        draw.text((x + 26, hy), line, font=hf, fill=WHITE)
        hy += 33
    # summary
    sf = font(SANS, 19)
    slines = wrap(draw, story["summary"], sf, pw - 52)
    sy = hy + 10
    for line in slines[:3]:
        draw.text((x + 26, sy), line, font=sf, fill=MUTED)
        sy += 25


def main():
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    # header
    title_f = font(SANS_BOLD, 56)
    title = "THE WORLD IN ONE DAY"
    tw = draw.textlength(title, font=title_f)
    draw.text(((W - tw) / 2, 34), title, font=title_f, fill=WHITE)

    date_f = font(SANS_BOLD, 36)
    date = "FRIDAY  ·  20 NOVEMBER 2026"
    dw = draw.textlength(date, font=date_f)
    draw.text(((W - dw) / 2, 104), date, font=date_f, fill=AMBER)

    draw.line([(48, 162), (W - 48, 162)], fill=AMBER, width=3)

    # 2 x 3 grid of panels
    margin, gutter = 24, 20
    pw = (W - 2 * margin - gutter) // 2
    ph = 236
    top = 184
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = margin + col * (pw + gutter)
        y = top + row * (ph + gutter)
        draw_panel(draw, x, y, pw, ph, story, i + 1)

    # footer
    ff = font(SANS, 16)
    foot1 = "All six stories happened or were first reported on Friday 20 November 2026."
    fw = draw.textlength(foot1, font=ff)
    draw.text(((W - fw) / 2, 952), foot1, font=ff, fill=GREY)
    foot2 = "Sources: Reuters  ·  WSJ  ·  The Times  ·  Le Monde  ·  Investopedia  ·  EORTC"
    fw2 = draw.textlength(foot2, font=ff)
    draw.text(((W - fw2) / 2, 976), foot2, font=ff, fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()

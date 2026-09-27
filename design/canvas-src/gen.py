import json, os, datetime

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "canvas", "project")
os.makedirs(ROOT, exist_ok=True)

ICONS = {
    "plus": '<path d="M12 5v14M5 12h14"></path>',
    "more": '<circle cx="5" cy="12" r="1.2"></circle><circle cx="12" cy="12" r="1.2"></circle><circle cx="19" cy="12" r="1.2"></circle>',
    "clip": '<path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48"></path>',
    "gear": '<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"></path><circle cx="12" cy="12" r="3"></circle>',
    "send": '<path d="M12 19V5M5 12l7-7 7 7"></path>',
    "pencil": '<path d="M12 20h9"></path><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"></path>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><path d="M14 2v6h6"></path>',
    "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>',
    "check": '<path d="M20 6 9 17l-5-5"></path>',
    "pin": '<path d="M12 17v5"></path><path d="M9 10.76a2 2 0 0 1-1.11 1.79l-1.78.9A2 2 0 0 0 5 15.24V16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-.76a2 2 0 0 0-1.11-1.79l-1.78-.9A2 2 0 0 1 15 10.76V7a1 1 0 0 1 1-1 2 2 0 0 0 0-4H8a2 2 0 0 0 0 4 1 1 0 0 1 1 1z"></path>',
    "star": '<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path>',
    "left": '<path d="M19 12H5M12 19l-7-7 7-7"></path>',
    "right": '<path d="M5 12h14M12 5l7 7-7 7"></path>',
}

def icon(name, size, color, sw=1.8):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')

THEMES = {
    "wire": dict(
        name="Wireframe", fonts="family=IBM+Plex+Sans:wght@400;500;600;700&amp;family=IBM+Plex+Mono:wght@500",
        display="'IBM Plex Sans', sans-serif", body="'IBM Plex Sans', sans-serif", mono="'IBM Plex Mono', monospace",
        bg="#FFFFFF", surface="#FFFFFF", surfaceAlt="#EDEDED", ink="#222222", inkMuted="#666666", line="#BDBDBD",
        accent="#444444", onAccent="#FFFFFF", bubbleSelf="#E6E6E6", danger="#B42318"),
    "paper": dict(
        name="Paper", fonts="family=Fraunces:opsz,wght@9..144,600&amp;family=Instrument+Sans:wght@400;500;600&amp;family=IBM+Plex+Mono:wght@500",
        display="'Fraunces', Georgia, serif", body="'Instrument Sans', sans-serif", mono="'IBM Plex Mono', monospace",
        bg="#F4F1EA", surface="#FFFFFF", surfaceAlt="#EBE6DB", ink="#1E1C19", inkMuted="#6A655C", line="#DCD5C7",
        accent="#C2410C", onAccent="#FFFFFF", bubbleSelf="#FBE3D6", danger="#B42318"),
    "night": dict(
        name="Night Desk", fonts="family=IBM+Plex+Sans:wght@400;500;600&amp;family=IBM+Plex+Mono:wght@500",
        display="'IBM Plex Sans', sans-serif", body="'IBM Plex Sans', sans-serif", mono="'IBM Plex Mono', monospace",
        bg="#111315", surface="#1B1E22", surfaceAlt="#24282D", ink="#E9EBED", inkMuted="#9AA1A9", line="#2E3339",
        accent="#7CC4FF", onAccent="#0B1A26", bubbleSelf="#1F3547", danger="#FF8A80"),
    "mint": dict(
        name="Mint", fonts="family=Plus+Jakarta+Sans:wght@400;500;600;700&amp;family=IBM+Plex+Mono:wght@500",
        display="'Plus Jakarta Sans', sans-serif", body="'Plus Jakarta Sans', sans-serif", mono="'IBM Plex Mono', monospace",
        bg="#EAF2EE", surface="#FFFFFF", surfaceAlt="#DCE9E3", ink="#13201B", inkMuted="#55655E", line="#C9DAD2",
        accent="#0F766E", onAccent="#FFFFFF", bubbleSelf="#D2ECE4", danger="#B42318"),
}

MARK = "#E0532F"

def page(title, t, w, h, body):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{t['fonts']}&amp;display=swap">
<style>
body{{margin:0;font-family:{t['body']};color:{t['ink']}}}
a{{color:{t['accent']}}}a:hover{{color:{t['ink']}}}
button{{font:inherit}}
input::placeholder{{color:{t['inkMuted']}}}
</style>
</helmet>
{body}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
class Component extends DCLogic {{
renderVals() {{
return {{}};
}}
}}
</script>
</body>
</html>
'''

def screen(t, platform, wire=False):
    W = 390 if platform == "phone" else 400
    H = 844 if platform == "phone" else 780
    def m(n):
        if not wire:
            return ""
        return (f'<span style="display: inline-flex; align-items: center; justify-content: center; width: 18px; height: 18px; '
                f'border-radius: 9px; background: {MARK}; color: #FFFFFF; font-size: 10px; font-weight: 700; flex-shrink: 0; '
                f'font-family: {t["body"]}">{n}</span>')
    iconbtn = (f'width: 44px; height: 44px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; '
               f'border: 0; border-radius: 22px; background: transparent; color: {t["ink"]}; padding: 0; cursor: pointer')
    meta = f'font-size: 11px; color: {t["inkMuted"]}; font-family: {t["mono"]}'

    top = ""
    if platform == "mac":
        top = f'''<div style="height: 30px; display: flex; align-items: center; gap: 8px; padding: 0 12px; flex-shrink: 0">
<span style="width: 12px; height: 12px; border-radius: 6px; background: #FF5F57"></span>
<span style="width: 12px; height: 12px; border-radius: 6px; background: #FEBC2E"></span>
<span style="width: 12px; height: 12px; border-radius: 6px; background: #28C840"></span>
<span style="flex-grow: 1"></span>
{m(11)}
<button aria-label="Keep on top (on)" aria-pressed="true" style="height: 26px; display: flex; align-items: center; gap: 4px; padding: 0 8px; border: 1px solid {t['line']}; border-radius: 13px; background: {t['surface']}; color: {t['accent']}; font-size: 11px; font-weight: 600; cursor: pointer">{icon('pin', 13, t['accent'], 2)}<span>On top</span></button>
</div>'''

    dots = "".join(
        f'<span style="width: {18 if i == 1 else 6}px; height: 6px; border-radius: 3px; background: {t["accent"] if i == 1 else t["line"]}"></span>'
        for i in range(5))

    header = f'''<header style="display: flex; flex-direction: column; gap: 2px; padding: {50 if platform == 'phone' else 2}px 8px 8px 16px; flex-shrink: 0">
<div style="display: flex; align-items: center; gap: 2px">
<button aria-label="Edit group name: Work" style="flex-grow: 1; min-height: 44px; display: flex; align-items: center; gap: 8px; background: transparent; border: 0; padding: 0; text-align: left; color: {t['ink']}; cursor: text">
<span style="font-family: {t['display']}; font-size: 26px; font-weight: 600; letter-spacing: -0.01em">Work</span>
{icon('pencil', 15, t['inkMuted'])}
{m(1)}
</button>
{m(2)}
<button aria-label="Add group" style="{iconbtn}">{icon('plus', 22, t['ink'])}</button>
{m(3)}
<button aria-label="More" style="{iconbtn}">{icon('more', 22, t['ink'])}</button>
</div>
<div style="display: flex; align-items: center; justify-content: space-between; padding-right: 8px; font-size: 12px; color: {t['inkMuted']}">
<span>‹ Inbox</span>
<div style="display: flex; align-items: center; gap: 5px" aria-label="Group 2 of 5">{dots}{m(4)}</div>
<span>Ideas ›</span>
</div>
</header>'''

    bubble = (f'align-self: flex-end; max-width: 80%; display: flex; flex-direction: column; align-items: flex-end; gap: 3px')
    bub_in = (f'background: {t["bubbleSelf"]}; color: {t["ink"]}; padding: 10px 13px; border-radius: 16px 16px 4px 16px; '
              f'font-size: 15px; line-height: 1.45')
    card = f'background: {t["surface"]}; border: 1px solid {t["line"]}; border-radius: 14px'

    def task(text, done, time):
        box = (f'<span style="width: 20px; height: 20px; flex-shrink: 0; border-radius: 6px; display: flex; align-items: center; justify-content: center; '
               + (f'background: {t["accent"]}">{icon("check", 14, t["onAccent"], 2.6)}</span>' if done else
                  f'border: 1.5px solid {t["inkMuted"]}"></span>'))
        txt_style = f'text-decoration: line-through; color: {t["inkMuted"]}' if done else f'color: {t["ink"]}'
        return f'''<div style="{bubble}">
<label style="position: relative; display: flex; align-items: center; gap: 10px; padding: 11px 13px; {card}; border-radius: 16px 16px 4px 16px; font-size: 15px; cursor: pointer"><input type="checkbox"{' checked' if done else ''} style="position: absolute; opacity: 0; width: 1px; height: 1px; margin: 0">{box}<span style="{txt_style}">{text}</span></label>
<span style="{meta}">{time}</span>
</div>'''

    items = f'''<div style="align-self: center; font-size: 11px; font-weight: 600; color: {t['inkMuted']}; background: {t['surfaceAlt']}; padding: 4px 10px; border-radius: 999px">Today · Thu, Sep 25</div>
<div style="{bubble}"><div style="{bub_in}">Call the printer about the flyer proof before 3 pm</div><span style="{meta}">09:12</span></div>
{task('Send invoice #0923 to Studio Ahn', True, '09:40')}
{task('Book a room for Friday’s review', False, '10:05')}
<div style="{bubble}; width: 78%">
<a href="https://m3.material.io" style="display: flex; flex-direction: column; width: 100%; {card}; overflow: hidden; text-decoration: none; color: {t['ink']}">
<div style="height: 96px; background: {t['surfaceAlt']}; display: flex; align-items: center; justify-content: center">{icon('link', 26, t['inkMuted'])}</div>
<div style="padding: 10px 12px; display: flex; flex-direction: column; gap: 2px">
<span style="font-size: 14px; font-weight: 600">Layout basics — Material Design 3</span>
<span style="font-size: 12px; color: {t['inkMuted']}">m3.material.io</span>
</div>
</a>
<span style="{meta}">10:48</span>
</div>
<div style="{bubble}">
<div style="display: flex; align-items: center; gap: 10px; padding: 10px 14px 10px 10px; {card}; border-radius: 16px 16px 4px 16px">
<div style="width: 40px; height: 40px; border-radius: 10px; background: {t['surfaceAlt']}; display: flex; align-items: center; justify-content: center">{icon('file', 20, t['accent'])}</div>
<div style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 14px; font-weight: 600">Q4-budget-draft.xlsx</span><span style="{meta}">1.8 MB</span></div>
</div>
<span style="{meta}">11:20</span>
</div>
<div style="{bubble}"><div style="{bub_in}">Idea: 15-min weekly review, Fridays 5 pm</div><span style="{meta}">11:34</span></div>'''

    marker5 = f'<div style="position: absolute; top: 8px; left: 12px; display: flex; gap: 6px; align-items: center; font-size: 11px; color: {MARK}; font-weight: 600">{m(5)}<span>scroll ↕</span></div>' if wire else ""

    lst = f'''<main aria-label="Items in Work" style="flex-grow: 1; min-height: 0; overflow: hidden; position: relative; display: flex; flex-direction: column; justify-content: flex-end; gap: 10px; padding: 8px 16px 14px">
{items}
{marker5}
</main>'''

    inputbar = f'''<div style="display: flex; align-items: center; gap: 2px; padding: 8px 8px 8px 4px; border-top: 1px solid {t['line']}; background: {t['surface']}; flex-shrink: 0">
{m(6)}<button aria-label="Settings" style="{iconbtn}; width: 40px">{icon('gear', 21, t['inkMuted'])}</button>
{m(7)}<button aria-label="Attach file" style="{iconbtn}; width: 40px">{icon('clip', 21, t['inkMuted'])}</button>
<input aria-label="Write a memo or task" placeholder="Memo, task, or link…" style="flex-grow: 1; min-width: 0; height: 40px; box-sizing: border-box; padding: 0 14px; margin: 0 4px; border-radius: 20px; border: 1px solid {t['line']}; background: {t['bg']}; color: {t['ink']}; font: inherit; font-size: 15px">
{m(8)}{m(9)}
<button aria-label="Send" style="{iconbtn}; background: {t['accent']}; width: 40px; height: 40px">{icon('send', 20, t['onAccent'], 2.2)}</button>
</div>'''

    if platform == "phone" or wire:
        ad_inner = f'''<div style="width: 320px; height: 50px; box-sizing: border-box; border: 1px dashed {t['line']}; border-radius: 6px; background: {t['surfaceAlt']}; display: flex; align-items: center; justify-content: center; gap: 8px; font-size: 12px; color: {t['inkMuted']}">
<span style="font-size: 10px; font-weight: 700; padding: 1px 5px; border-radius: 4px; border: 1px solid {t['inkMuted']}">Ad</span>
<span>[AdMob banner · 320 × 50]</span>{m(10)}
</div>'''
        if wire and platform == "mac":
            ad_inner = ad_inner.replace("[AdMob banner · 320 × 50]", "[House banner · 320 × 50]")
    else:
        ad_inner = f'''<div style="width: 100%; height: 50px; box-sizing: border-box; border-radius: 10px; background: {t['surfaceAlt']}; display: flex; align-items: center; gap: 10px; padding: 0 12px; font-size: 13px">
{icon('star', 18, t['accent'])}
<span style="flex-grow: 1; color: {t['ink']}">Pro: no ads, 30 GB of storage</span>
<a href="#upgrade" style="font-weight: 600; text-decoration: none">Upgrade</a>
</div>'''
    banner = f'''<div style="display: flex; justify-content: center; padding: 8px 12px {22 if platform == 'phone' else 8}px; border-top: 1px solid {t['line']}; background: {t['bg']}; flex-shrink: 0">
{ad_inner}
</div>'''

    radius = "border-radius: 10px; " if platform == "mac" else ""
    root = f'''<div style="width: {W}px; height: {H}px; box-sizing: border-box; {radius}overflow: hidden; display: flex; flex-direction: column; background: {t['bg']}; color: {t['ink']}; font-family: {t['body']}">
{top}
{header}
{lst}
{inputbar}
{banner}
</div>'''
    return W, H, root

files = {}

def add(name, title, theme, w, h, body):
    files[name] = page(title, THEMES[theme], w, h, body)

# Screens
for fname, theme, plat, wire, title in [
    ("Main.dc.html", "wire", "phone", True, "Wireframe · iPhone"),
    ("WireMac.dc.html", "wire", "mac", True, "Wireframe · Mac window"),
    ("MockPaperPhone.dc.html", "paper", "phone", False, "Paper · iPhone"),
    ("MockNightPhone.dc.html", "night", "phone", False, "Night Desk · iPhone"),
    ("MockMintPhone.dc.html", "mint", "phone", False, "Mint · iPhone"),
    ("MockPaperMac.dc.html", "paper", "mac", False, "Paper · Mac window"),
    ("MockNightMac.dc.html", "night", "mac", False, "Night Desk · Mac window"),
]:
    W, H, body = screen(THEMES[theme], plat, wire)
    add(fname, title, theme, W, H, body)

# ---------- Flows artboard (wireframe style) ----------
t = THEMES["wire"]
def mini(title, current=False, dashed=False, body=""):
    border = f'2px dashed {t["line"]}' if dashed else (f'2px solid {t["ink"]}' if current else f'1.5px solid {t["line"]}')
    return f'''<div style="width: 180px; height: 320px; box-sizing: border-box; border: {border}; border-radius: 22px; padding: 18px 12px 10px; display: flex; flex-direction: column; gap: 8px; background: #FFFFFF; flex-shrink: 0">
<div style="display: flex; align-items: center; gap: 6px"><span style="flex-grow: 1; font-size: 15px; font-weight: 600">{title}</span>{icon('plus', 14, t['ink'])}{icon('more', 14, t['ink'])}</div>
{body}
</div>'''

def bars(n, widths=(70, 55, 80, 45, 65, 50)):
    out = []
    for i in range(n):
        out.append(f'<div style="align-self: flex-end; width: {widths[i % len(widths)]}%; height: 22px; border-radius: 8px; background: {t["bubbleSelf"]}"></div>')
    return "\n".join(out)

def mini_list(n):
    return f'''<div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: flex-end; gap: 7px">{bars(n)}</div>
<div style="height: 26px; border-radius: 13px; border: 1px solid {t['line']}"></div>
<div style="height: 18px; border-radius: 4px; background: {t['surfaceAlt']}; border: 1px dashed {t['line']}"></div>'''

arrow = f'<div style="display: flex; flex-direction: column; align-items: center; gap: 4px; color: {t["inkMuted"]}; font-size: 11px">{icon("left", 18, t["inkMuted"])}{icon("right", 18, t["inkMuted"])}<span>swipe</span></div>'

new_group_body = f'''<div style="flex-grow: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px; text-align: center; font-size: 12px; color: {t['inkMuted']}">{icon('plus', 22, t['inkMuted'])}<span>+ inserts a new group here, after the current one</span></div>'''

def panel(title, desc, inner, w=270):
    return f'''<section style="width: {w}px; flex-shrink: 0; display: flex; flex-direction: column; gap: 10px">
<h3 style="margin: 0; font-size: 15px; font-weight: 600">{title}</h3>
<p style="margin: 0; font-size: 12px; line-height: 1.45; color: {t['inkMuted']}">{desc}</p>
{inner}
</section>'''

def menu(rows):
    out = []
    for label, extra, danger in rows:
        color = t['danger'] if danger else t['ink']
        out.append(f'<div style="display: flex; align-items: center; justify-content: space-between; min-height: 36px; padding: 0 12px; font-size: 13px; color: {color}; border-top: 1px solid {t["surfaceAlt"]}"><span>{label}</span>{extra}</div>')
    return f'<div style="border: 1px solid {t["line"]}; border-radius: 12px; background: #FFFFFF; overflow: hidden; box-shadow: 0 6px 18px rgba(0,0,0,0.08)">{"".join(out)}</div>'

toggle = f'<span style="width: 30px; height: 18px; border-radius: 9px; background: {t["ink"]}; display: flex; align-items: center; justify-content: flex-end; padding: 2px; box-sizing: border-box"><span style="width: 14px; height: 14px; border-radius: 7px; background: #FFFFFF"></span></span>'
more_menu = menu([("Rename group", "", False), ("Group color", f'<span style="width: 14px; height: 14px; border-radius: 7px; background: {t["inkMuted"]}"></span>', False),
                  ("Reorder groups", "", False), ("Keep on top (Mac)", toggle, False), ("Search in group", "", False),
                  ("Export group", "", False), ("Delete group", "", True)])
item_menu = menu([("Copy", "", False), ("Edit", "", False), ("Convert to task", "", False), ("Pin", "", False),
                  ("Move to group…", "", False), ("Delete", "", True)])

add_group = f'''<div style="border: 1px solid {t['line']}; border-radius: 12px; padding: 12px; display: flex; flex-direction: column; gap: 10px; background: #FFFFFF">
<div style="display: flex; align-items: center; gap: 6px">
<label style="flex-grow: 1; display: flex; flex-direction: column; gap: 4px; font-size: 11px; color: {t['inkMuted']}">Group name
<input value="New group" aria-label="Group name" style="height: 36px; box-sizing: border-box; padding: 0 10px; border: 2px solid {t['ink']}; border-radius: 8px; font: inherit; font-size: 16px; font-weight: 600; color: {t['ink']}">
</label>
</div>
<span style="font-size: 11px; color: {t['inkMuted']}">Enter = save · Esc = cancel</span>
<div style="height: 120px; border-radius: 8px; background: {t['surfaceAlt']}; display: flex; align-items: center; justify-content: center; text-align: center; padding: 0 16px; font-size: 12px; color: {t['inkMuted']}">Nothing here yet. Send yourself a memo.</div>
</div>'''

legend_rows = [
    (1, "Group title — tap / click to rename inline"), (2, "Add group (+)"), (3, "More (…) menu"),
    (4, "Group pager — swipe ← → between groups"), (5, "Item list — scroll ↕, newest at bottom"),
    (6, "Settings (account, storage meter, plan)"), (7, "Attach file / photo"), (8, "Message input"),
    (9, "Send"), (10, "Ad banner — very bottom, Free plan only"), (11, "Keep on top (Mac only)")]
legend = "\n".join(
    f'<li style="display: flex; gap: 8px; align-items: flex-start; font-size: 12px; line-height: 1.4"><span style="display: inline-flex; align-items: center; justify-content: center; width: 18px; height: 18px; border-radius: 9px; background: {MARK}; color: #FFFFFF; font-size: 10px; font-weight: 700; flex-shrink: 0">{n}</span><span>{txt}</span></li>'
    for n, txt in legend_rows)

flows = f'''<div style="width: 1280px; height: 844px; box-sizing: border-box; padding: 32px 40px; display: flex; flex-direction: column; gap: 28px; background: #FAFAFA; color: {t['ink']}">
<section style="display: flex; flex-direction: column; gap: 14px">
<div style="display: flex; align-items: baseline; gap: 16px">
<h2 style="margin: 0; font-size: 20px; font-weight: 600">Swipe between groups</h2>
<p style="margin: 0; font-size: 13px; color: {t['inkMuted']}">Horizontal = groups (Flutter PageView). Vertical = items. Mac: two-finger swipe, ⌘[ / ⌘], or click the dots.</p>
</div>
<div style="display: flex; align-items: center; gap: 22px">
{mini('Inbox', body=mini_list(5))}
{arrow}
{mini('Work', current=True, body=mini_list(6))}
{arrow}
{mini('Ideas', body=mini_list(4))}
{arrow}
{mini('Shopping', body=mini_list(3))}
{arrow}
{mini('New group', dashed=True, body=new_group_body)}
</div>
</section>
<div style="display: flex; gap: 32px; align-items: flex-start">
{panel('More (…) menu', 'Opens from the header. Keep on top only appears on the Mac.', more_menu, 250)}
{panel('Add group (+)', 'Creates a group after the current one, swipes to it, and focuses the name.', add_group, 250)}
{panel('Item actions', 'Long-press on iPhone, right-click on Mac.', item_menu, 230)}
<section style="flex-grow: 1; display: flex; flex-direction: column; gap: 10px">
<h3 style="margin: 0; font-size: 15px; font-weight: 600">Legend</h3>
<ol style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 7px">
{legend}
</ol>
</section>
</div>
</div>'''
add("WireFlows.dc.html", "Wireframe · interactions", "wire", 1280, 844, flows)

# ---------- Tokens artboard ----------
def token_col(key):
    th = THEMES[key]
    names = ["bg", "surface", "surfaceAlt", "ink", "inkMuted", "line", "accent", "onAccent", "bubbleSelf", "danger"]
    sw = "\n".join(
        f'<div style="display: flex; align-items: center; gap: 8px"><span style="width: 26px; height: 26px; border-radius: 7px; background: {th[n]}; border: 1px solid {th["line"]}; flex-shrink: 0"></span><div style="display: flex; flex-direction: column"><span style="font-size: 12px; font-weight: 600; color: {th["ink"]}">{n}</span><span style="font-size: 11px; color: {th["inkMuted"]}; font-family: {th["mono"]}">{th[n]}</span></div></div>'
        for n in names)
    fonts = {"paper": "Fraunces · Instrument Sans", "night": "IBM Plex Sans · Plex Mono", "mint": "Plus Jakarta Sans"}[key]
    return f'''<section style="flex: 1 1 0; min-width: 0; box-sizing: border-box; padding: 22px; border-radius: 20px; background: {th['bg']}; color: {th['ink']}; font-family: {th['body']}; display: flex; flex-direction: column; gap: 18px; border: 1px solid {th['line']}">
<div style="display: flex; flex-direction: column; gap: 4px">
<h2 style="margin: 0; font-family: {th['display']}; font-size: 26px; font-weight: 600">{th['name']}</h2>
<span style="font-size: 12px; color: {th['inkMuted']}">{fonts}</span>
</div>
<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px">
{sw}
</div>
<div style="display: flex; flex-direction: column; gap: 6px; padding-top: 14px; border-top: 1px solid {th['line']}">
<span style="font-family: {th['display']}; font-size: 22px; font-weight: 600">Work · title 22</span>
<span style="font-size: 15px; line-height: 1.45">Body 15 — Call the printer before 3 pm</span>
<span style="font-size: 11px; color: {th['inkMuted']}; font-family: {th['mono']}">META 11 · 09:12 · 1.8 MB</span>
</div>
<div style="display: flex; align-items: center; gap: 10px">
<span style="background: {th['bubbleSelf']}; padding: 9px 12px; border-radius: 16px 16px 4px 16px; font-size: 14px">bubbleSelf</span>
<span style="background: {th['accent']}; color: {th['onAccent']}; padding: 9px 14px; border-radius: 999px; font-size: 14px; font-weight: 600">Send</span>
</div>
<div style="display: flex; gap: 10px; align-items: flex-end">
<div style="width: 44px; height: 44px; border-radius: 8px; background: {th['surfaceAlt']}"></div>
<div style="width: 44px; height: 44px; border-radius: 14px; background: {th['surfaceAlt']}"></div>
<div style="width: 44px; height: 44px; border-radius: 20px; background: {th['surfaceAlt']}"></div>
<span style="font-size: 11px; color: {th['inkMuted']}; font-family: {th['mono']}">radius 8 · 14 · 20</span>
</div>
</section>'''

tok_fonts = "family=Fraunces:opsz,wght@9..144,600&amp;family=Instrument+Sans:wght@400;500;600&amp;family=IBM+Plex+Sans:wght@400;500;600&amp;family=IBM+Plex+Mono:wght@500&amp;family=Plus+Jakarta+Sans:wght@400;500;600;700"
tok_theme = dict(THEMES["wire"], fonts=tok_fonts)
tokens_body = f'''<div style="width: 1040px; height: 844px; box-sizing: border-box; padding: 32px; display: flex; flex-direction: column; gap: 20px; background: #F7F7F5; color: #1E1C19">
<div style="display: flex; align-items: baseline; justify-content: space-between">
<h1 style="margin: 0; font-size: 22px; font-weight: 600">Design tokens — one structure, three themes</h1>
<span style="font-size: 12px; color: #5F5F5F; font-family: 'IBM Plex Mono', monospace">design/tokens.json</span>
</div>
<div style="flex-grow: 1; display: flex; gap: 18px">
{token_col('paper')}
{token_col('night')}
{token_col('mint')}
</div>
</div>'''
files["Tokens.dc.html"] = page("Design tokens", tok_theme, 1040, 844, tokens_body)

# ---------- Desk context ----------
n = THEMES["night"]
gb = "\n".join(f'<div style="height: 12px; width: {w}%; border-radius: 6px; background: #DADCDF"></div>' for w in (62, 88, 75, 91, 54, 80, 70, 85, 40))
desk = f'''<div style="width: 1280px; height: 800px; box-sizing: border-box; background: #3F4A52; display: flex; gap: 28px; padding: 10px 28px 20px 28px; align-items: flex-start; font-family: {n['body']}">
<div style="flex-grow: 1; display: flex; flex-direction: column; gap: 14px; margin-top: 30px">
<div style="height: 680px; border-radius: 10px; background: #F2F3F4; overflow: hidden; display: flex; flex-direction: column">
<div style="height: 30px; display: flex; align-items: center; gap: 8px; padding: 0 12px; background: #E4E6E8">
<span style="width: 12px; height: 12px; border-radius: 6px; background: #FF5F57"></span>
<span style="width: 12px; height: 12px; border-radius: 6px; background: #FEBC2E"></span>
<span style="width: 12px; height: 12px; border-radius: 6px; background: #28C840"></span>
</div>
<div style="flex-grow: 1; padding: 40px 56px; display: flex; flex-direction: column; gap: 16px">
<span style="font-size: 13px; color: #5B6167">[Your main work app — docs, code, design…]</span>
{gb}
</div>
</div>
<p style="margin: 0; font-size: 13px; color: #E6E9EC">ToDoDesk stays pinned on top at the screen edge · ⌥Space jumps to the input from anywhere</p>
</div>
<dc-import name="MockNightMac" hint-size="400px,780px"></dc-import>
</div>'''
add("DeskContext.dc.html", "Mac desktop in context", "night", 1280, 800, desk)

for name, src in files.items():
    with open(os.path.join(ROOT, name), "w") as f:
        f.write(src)

boards = {
    "Main.dc.html": dict(x=0, y=0, w=390, h=844, title="Wireframe · iPhone"),
    "WireMac.dc.html": dict(x=470, y=0, w=400, h=780, title="Wireframe · Mac window (tall)"),
    "WireFlows.dc.html": dict(x=950, y=0, w=1280, h=844, title="Wireframe · swipe, menus, legend"),
    "MockPaperPhone.dc.html": dict(x=0, y=1300, w=390, h=844, title="Paper · iPhone"),
    "MockNightPhone.dc.html": dict(x=470, y=1300, w=390, h=844, title="Night Desk · iPhone"),
    "MockMintPhone.dc.html": dict(x=940, y=1300, w=390, h=844, title="Mint · iPhone"),
    "MockPaperMac.dc.html": dict(x=1410, y=1300, w=400, h=780, title="Paper · Mac (house banner)"),
    "MockNightMac.dc.html": dict(x=1890, y=1300, w=400, h=780, title="Night Desk · Mac (house banner)"),
    "Tokens.dc.html": dict(x=2370, y=1300, w=1040, h=844, title="Design tokens"),
    "DeskContext.dc.html": dict(x=0, y=2564, w=1280, h=800, title="Night Desk pinned on a Mac desktop"),
}
canvas = {
    "v": 3,
    "createdOnFiles": {"v": 1, "at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")},
    "title": "ToDoDesk Wireframes & Mockups",
    "launch": {"view": "canvas"},
    "pages": [],
    "boards": boards,
    "order": list(boards.keys()),
    "notes": {
        "wf": {"x": 0, "y": -300, "text": "Wireframes", "kind": "title1", "maxW": 2230},
        "mk": {"x": 0, "y": 1000, "text": "Mockups — three token themes", "kind": "title1", "maxW": 3410},
        "dk": {"x": 0, "y": 2264, "text": "Always visible on the Mac desktop", "kind": "title1", "maxW": 1280},
    },
    "designSystems": [],
}
with open(os.path.join(ROOT, "canvas.json"), "w") as f:
    json.dump(canvas, f, ensure_ascii=False, indent=1)
print(sorted(os.listdir(ROOT)))

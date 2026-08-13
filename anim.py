#!/usr/bin/env python3
"""Animation de démarrage XRAT (même séquence que Void Panel, rebrandée XRAT).

Logo et couleurs (dégradé bleu -> rouge) identiques au panel de base Xrat.py.
Séquence : pluie digitale -> figlet XRAT -> logo XRAT -> glitch reveal
-> barres de boot -> panneau ALL SYSTEMS ONLINE.
"""

import os, sys, time, shutil, random, math
from colorama import init, Fore
init(autoreset=True)

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from rich.console  import Console
from rich.panel    import Panel
from rich.text     import Text
from rich.align    import Align
from rich.live     import Live
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich          import box
import pyfiglet

console = Console(highlight=False)

BLUE   = (0x00, 0x00, 0xFF)
RED    = (0xFF, 0x00, 0x00)
B_BRIGHT = "#8888FF"
B_DARK   = "#3333AA"

LOGO_LINES = [
    r"▀████    ▐████▀    ▄████████    ▄████████     ███",
    r"  ███▌   ████▀    ███    ███   ███    ███ ▀█████████▄",
    r"   ███  ▐███      ███    ███   ███    ███    ▀███▀▀██",
    r"   ▀███▄███▀     ▄███▄▄▄▄██▀   ███    ███     ███   ▀",
    r"   ████▀██▄     ▀▀███▀▀▀▀▀   ▀███████████     ███",
    r"  ▐███  ▀███    ▀███████████   ███    ███     ███",
    r" ▄███     ███▄    ███    ███   ███    ███     ███",
    r"████       ███▄   ███    ███   ███    █▀     ▄████▀",
    r"                  ███    ███",
]

_RAIN = list("01▓▒░│┤╣║╗╝┐└┴┬├─┼╚╔╩╦╠═╬┘┌AB3F9E#%&?$")
_NOISE = list("#%&!?$@+-=~^/*|\\><▓▒░")


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def tw():
    return shutil.get_terminal_size((100, 30)).columns


def th():
    return shutil.get_terminal_size((100, 30)).lines


def _lerp(a, b, f):
    return tuple(int(a[i] + (b[i] - a[i]) * f) for i in range(3))


def _hex(rgb):
    return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"


def _rain_frame(w, h, t):
    f = Text()
    for row in range(h):
        for col in range(w):
            spd = 1.0 + (col % 7) * 0.3
            ph  = int((t * spd * 12 + col * 3.7)) % len(_RAIN)
            ch  = _RAIN[(col * 17 + row * 3 + ph) % len(_RAIN)]
            base = _lerp(BLUE, RED, col / max(w - 1, 1))
            k = 0.18 + abs(math.sin(col * 0.4 + t * 0.8)) * (0x99 - 0x18) / 0xFF
            r = int(base[0] * k); g = int(base[1] * k); b = int(base[2] * k)
            if random.random() < 0.03:
                r, g, b = 0xFF, 0xFF, 0xFF
            f.append(ch, style=f"#{r:02X}{g:02X}{b:02X}")
        if row < h - 1:
            f.append("\n")
    return f


def play_intro():
    w = tw(); h = max(th() - 2, 20); t0 = time.monotonic()
    with Live(console=console, screen=True, refresh_per_second=24, transient=True) as live:
        while time.monotonic() - t0 < 1.0:
            live.update(_rain_frame(w, h, time.monotonic() - t0))
            time.sleep(1 / 24)
    fl = pyfiglet.figlet_format("XRAT", font="big", width=w - 4).splitlines()
    fh = len(fl); ly = max(0, h // 2 - fh // 2)
    lc = [_hex(_lerp(BLUE, RED, i / max(fh - 1, 1))) for i in range(fh)]
    with Live(console=console, screen=True, refresh_per_second=24, transient=True) as live:
        t2 = time.monotonic()
        while time.monotonic() - t2 < 1.8:
            t  = time.monotonic() - t0
            fd = min((time.monotonic() - t2) / 1.8, 1.0)
            frame = Text()
            for row in range(h):
                rel = row - ly
                if 0 <= rel < fh and random.random() < fd:
                    frame.append(f"  {fl[rel]}\n", style=f"{lc[rel]} bold")
                else:
                    for col in range(w):
                        spd = 1.0 + (col % 7) * 0.3
                        ph  = int((t * spd * 12 + col * 3.7)) % len(_RAIN)
                        ch  = _RAIN[(col * 17 + row * 3 + ph) % len(_RAIN)]
                        base = _lerp(BLUE, RED, col / max(w - 1, 1))
                        k = 0.10 + (1 - fd) * 0.35
                        r = int(base[0] * k); g = int(base[1] * k); b = int(base[2] * k)
                        frame.append(ch, style=f"#{r:02X}{g:02X}{b:02X}")
                    frame.append("\n")
            live.update(frame)
            time.sleep(1 / 24)


def draw_logo():
    rows = len(LOGO_LINES)
    cols = max(len(l) for l in LOGO_LINES)
    t = Text()
    for r, line in enumerate(LOGO_LINES):
        for c, ch in enumerate(line):
            frac = (r + c) / (rows - 1 + cols - 1)
            t.append(ch, style=f"{_hex(_lerp(BLUE, RED, frac))} bold")
        t.append("\n")
    return t


def reveal_text(text, delay=0.04):
    for line in str(text).split("\n"):
        print(line)
        time.sleep(delay)


def gradient_line(text):
    t = Text(); n = len(text)
    for i, ch in enumerate(text):
        t.append(ch, style=f"{_hex(_lerp(BLUE, RED, i / max(n - 1, 1)))} bold")
    return t


def glitch_reveal_rich(text):
    n = len(text); revealed = [False] * n
    with Live(console=console, refresh_per_second=30, transient=True) as live:
        for _ in range(6):
            t = Text()
            for ch in text:
                if random.random() < 0.6:
                    t.append(random.choice(_NOISE), style=B_DARK)
                else:
                    t.append(ch, style=f"{B_BRIGHT} bold")
            live.update(Align.center(t)); time.sleep(0.04)
        s = 0
        while not all(revealed):
            if s < n:
                revealed[s] = True
            if n - 1 - s >= 0:
                revealed[n - 1 - s] = True
            t = Text()
            for i, ch in enumerate(text):
                if revealed[i]:
                    t.append(ch, style=f"{_hex(_lerp(BLUE, RED, i / max(n - 1, 1)))} bold")
                else:
                    t.append(random.choice(_NOISE), style=B_DARK)
            live.update(Align.center(t)); time.sleep(0.028); s += 1
    console.print(Align.center(gradient_line(text)))


def rich_boot_bars():
    tasks_cfg = [
        ("KERNEL LOAD",     0.18), ("MEMORY ALLOC",    0.22),
        ("NET INTERFACE",   0.19), ("CRYPTO ENGINE",   0.15),
        ("OSINT MODULE",    0.20), ("RAT MODULE",      0.17),
        ("RENDER PIPELINE", 0.16), ("DARK WEB LAYER",  0.21),
    ]
    with Progress(
        SpinnerColumn(style=f"{B_BRIGHT} bold"),
        TextColumn(f"[#CCCCCC]{{task.description:<20}}"),
        BarColumn(bar_width=32, style=B_DARK, complete_style=B_BRIGHT, finished_style="#FF4444"),
        TextColumn(f"[#FFFFFF]{{task.percentage:>5.1f}}%"),
        console=console, transient=False,
    ) as progress:
        job_ids = [progress.add_task(label, total=100) for label, _ in tasks_cfg]
        while not all(progress.tasks[jid].finished for jid in job_ids):
            for idx, jid in enumerate(job_ids):
                if not progress.tasks[jid].finished:
                    progress.advance(jid, random.uniform(3, 14))
                    time.sleep(tasks_cfg[idx][1] * random.uniform(0.5, 1.5) / 10)


def boot():
    play_intro()
    cls(); console.print()
    console.print(draw_logo())
    console.print()
    glitch_reveal_rich("XRAT  //  SYSTEM INITIALIZATION")
    console.print()
    rich_boot_bars()
    console.print()
    console.print(Panel(
        Align.center(Text.from_markup(
            f"[{B_BRIGHT} bold][ ALL SYSTEMS ONLINE ]\n"
            f"[#CCCCCC]XRAT  ·  by 3.vlt & 16_id  ·  discord.gg/PPN5wMqG3F"
        )),
        border_style=B_BRIGHT, box=box.DOUBLE_EDGE, padding=(0, 2),
    ))
    time.sleep(0.5)
    cls()

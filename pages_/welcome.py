import re

import streamlit as st

from theme import inject_css

inject_css()


def flat(s):
    """Collapse to one line so Streamlit's markdown never treats indented lines as code."""
    return re.sub(r"\s*\n\s*", " ", s).strip()


# ------------------------------------------------------------------ page-only styles
st.markdown(
    """<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

.stApp {
  background:
    radial-gradient(900px 540px at 14% -6%, rgba(37,99,235,.38), transparent 60%),
    radial-gradient(760px 520px at 96% 38%, rgba(14,165,233,.17), transparent 60%),
    linear-gradient(rgba(96,165,250,.05) 1px, transparent 1px) 0 0 / 48px 48px,
    linear-gradient(90deg, rgba(96,165,250,.05) 1px, transparent 1px) 0 0 / 48px 48px,
    #040816 !important;
}
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] {display:none;}
.block-container {padding-top:1.6rem; max-width:1200px;}

/* top bar */
.lp-nav {display:flex; align-items:center; justify-content:space-between; margin-bottom:2.2rem;}
.lp-brand {display:flex; align-items:center; gap:.75rem;}
.lp-logo {width:42px; height:42px; border-radius:12px; display:flex; align-items:center; justify-content:center;
          font-size:21px; background:linear-gradient(135deg,#2563eb,#0ea5e9);
          box-shadow:0 8px 24px rgba(37,99,235,.45);}
.lp-brand-name {font-family:'Plus Jakarta Sans','Inter',sans-serif; font-size:1.3rem; font-weight:800; color:#fff;
                letter-spacing:-.01em;}
.lp-pill {padding:6px 14px; border-radius:999px; font-size:.78rem; font-weight:600; color:#bae6fd;
          background:rgba(14,165,233,.10); border:1px solid rgba(56,189,248,.35);}

/* hero text */
.lp-eyebrow {display:inline-flex; align-items:center; gap:.55rem; padding:6px 14px; border-radius:999px;
             font-size:.78rem; font-weight:600; letter-spacing:.04em; text-transform:uppercase; color:#7dd3fc;
             background:rgba(37,99,235,.16); border:1px solid rgba(96,165,250,.35);}
.lp-eyebrow .dot {width:7px; height:7px; border-radius:50%; background:#38bdf8; box-shadow:0 0 10px #38bdf8;}
.lp-h1 {font-family:'Plus Jakarta Sans','Inter',sans-serif; font-size:3.5rem; font-weight:800; line-height:1.08;
        letter-spacing:-.035em; color:#f8fafc; margin:1.2rem 0 1.1rem;}
.lp-hl {background:linear-gradient(90deg,#7dd3fc 0%,#38bdf8 45%,#3b82f6 100%); -webkit-background-clip:text;
        background-clip:text; color:transparent; filter:drop-shadow(0 0 22px rgba(56,189,248,.45));}
.lp-p {color:#9fb0d0; font-size:1.06rem; line-height:1.7; max-width:470px; margin-bottom:1.6rem;}
.lp-p mark {background:rgba(56,189,248,.14); color:#bae6fd; padding:1px 8px; border-radius:6px; font-weight:600;}

/* buttons on this page */
button[kind="primary"], button[data-testid="stBaseButton-primary"] {
  background:linear-gradient(135deg,#2563eb,#0ea5e9) !important; border:none !important; color:#fff !important;
  font-weight:600 !important; font-size:1rem !important; padding:.7rem 1.7rem !important; border-radius:12px !important;
  box-shadow:0 12px 32px rgba(37,99,235,.5) !important;}
.stButton button:not([kind="primary"]) {padding:.7rem 1.4rem; border-radius:12px; border-color:rgba(96,165,250,.4);
  background:rgba(37,99,235,.08); color:#cfe4ff;}
.stButton button:not([kind="primary"]):hover {border-color:#38bdf8; background:rgba(14,165,233,.16); color:#fff;}

/* illustration */
.lp-art {position:relative;}
.lp-art svg {width:100%; height:auto; display:block;}
.float-tag {position:absolute; padding:8px 15px; border-radius:11px; font-size:.8rem; font-weight:600;
            color:#dbeafe; background:rgba(15,32,84,.72); border:1px solid rgba(96,165,250,.45);
            box-shadow:0 8px 30px rgba(37,99,235,.35), inset 0 0 14px rgba(59,130,246,.15);
            backdrop-filter:blur(6px); white-space:nowrap; animation:floaty 5.5s ease-in-out infinite;}
.float-tag.green {color:#bbf7d0; background:rgba(6,78,59,.6); border-color:rgba(52,211,153,.55);
                  box-shadow:0 8px 30px rgba(16,185,129,.28);}
@keyframes floaty {0%,100% {transform:translateY(0);} 50% {transform:translateY(-9px);}}
@keyframes orbit {to {stroke-dashoffset:-240;}}
@keyframes pulse {0%,100% {opacity:.8;} 50% {opacity:1;}}
.orbit {stroke-dasharray:6 10; animation:orbit 16s linear infinite;}
.brain {animation:pulse 3.6s ease-in-out infinite;}

/* feature cards */
.fc-row {display:grid; grid-template-columns:repeat(3,1fr); gap:1.1rem; margin-top:2.4rem;}
.fc {padding:1.4rem 1.5rem; border-radius:18px; border:1px solid rgba(96,165,250,.22);
     background:linear-gradient(180deg, rgba(37,99,235,.15), rgba(10,18,50,.55)); backdrop-filter:blur(6px);}
.fc-ic {width:44px; height:44px; border-radius:12px; display:flex; align-items:center; justify-content:center;
        background:linear-gradient(135deg, rgba(37,99,235,.55), rgba(14,165,233,.35));
        border:1px solid rgba(125,211,252,.4); margin-bottom:.9rem;}
.fc-t {font-family:'Plus Jakarta Sans','Inter',sans-serif; font-size:1.08rem; font-weight:700; color:#f1f5f9;}
.fc-s {margin-top:.35rem; color:#9fb0d0; font-size:.9rem; line-height:1.55;}
@media (max-width: 900px) {.fc-row {grid-template-columns:1fr;} .lp-h1 {font-size:2.5rem;}}
</style>""",
    unsafe_allow_html=True,
)


# ------------------------------------------------------------------ isometric 3D-style illustration
def box(cx, cy, hw, h, top, left, right, edge="#60a5fa"):
    """Isometric box. (cx, cy) is the centre of the top face, hw its half-width."""
    hd = hw // 2
    t = f"{cx},{cy - hd} {cx + hw},{cy} {cx},{cy + hd} {cx - hw},{cy}"
    l = f"{cx - hw},{cy} {cx},{cy + hd} {cx},{cy + hd + h} {cx - hw},{cy + h}"
    r = f"{cx},{cy + hd} {cx + hw},{cy} {cx + hw},{cy + h} {cx},{cy + hd + h}"
    return (
        f'<polygon points="{l}" fill="url(#{left})"/>'
        f'<polygon points="{r}" fill="url(#{right})"/>'
        f'<polygon points="{t}" fill="url(#{top})" stroke="{edge}" stroke-width="1" stroke-opacity=".75"/>'
    )


def slab(cx, cy, hw, h):
    """A server slab: box plus LED strips on both visible faces."""
    hd = hw // 2
    s = box(cx, cy, hw, h, "topG", "leftG", "rightG")
    s += (
        f'<g transform="matrix(1,.5,0,1,{cx - hw},{cy})">'
        f'<rect x="{hw * .14:.1f}" y="{h * .30:.1f}" width="{hw * .5:.1f}" height="3" rx="1.5" fill="#93c5fd" opacity=".9"/>'
        f'<rect x="{hw * .14:.1f}" y="{h * .58:.1f}" width="{hw * .34:.1f}" height="3" rx="1.5" fill="#60a5fa" opacity=".65"/>'
        f'<circle cx="{hw * .82:.1f}" cy="{h * .45:.1f}" r="2.4" fill="#22d3ee"/></g>'
        f'<g transform="matrix(1,-.5,0,1,{cx},{cy + hd})">'
        f'<rect x="{hw * .16:.1f}" y="{h * .30:.1f}" width="{hw * .5:.1f}" height="3" rx="1.5" fill="#67e8f9" opacity=".75"/>'
        f'<rect x="{hw * .16:.1f}" y="{h * .58:.1f}" width="{hw * .3:.1f}" height="3" rx="1.5" fill="#38bdf8" opacity=".55"/></g>'
    )
    return s


def rhombus(cx, cy, hw, **attrs):
    hd = hw / 2
    pts = f"{cx},{cy - hd} {cx + hw},{cy} {cx},{cy + hd} {cx - hw},{cy}"
    a = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<polygon points="{pts}" {a}/>'


DEFS = """<defs>
<linearGradient id="brainG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#a5f3fc"/><stop offset="1" stop-color="#3b82f6"/></linearGradient>
<linearGradient id="beam" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#38bdf8" stop-opacity=".6"/><stop offset="1" stop-color="#38bdf8" stop-opacity="0"/></linearGradient>
<linearGradient id="topG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3b82f6"/><stop offset="1" stop-color="#1e3a8a"/></linearGradient>
<linearGradient id="leftG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1d4ed8"/><stop offset="1" stop-color="#0b1a4d"/></linearGradient>
<linearGradient id="rightG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e3a8a"/><stop offset="1" stop-color="#050d33"/></linearGradient>
<linearGradient id="platTop" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#17347f"/><stop offset="1" stop-color="#0a1648"/></linearGradient>
<radialGradient id="halo" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#2563eb" stop-opacity=".5"/><stop offset="1" stop-color="#2563eb" stop-opacity="0"/></radialGradient>
<filter id="glow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="platClip"><polygon points="260,305 470,410 260,515 50,410"/></clipPath>
</defs>"""

HEMI = (
    '<path d="M205,62 C172,38 118,52 104,94 C78,104 64,138 78,168 C62,194 74,228 102,240 '
    'C108,268 142,284 172,270 C186,284 205,280 205,262 Z" fill="rgba(56,189,248,.18)" '
    'stroke="url(#brainG)" stroke-width="4" stroke-linejoin="round"/>'
    '<g fill="none" stroke="url(#brainG)" stroke-width="3" stroke-linecap="round">'
    '<path d="M150,84 C128,104 152,124 130,146"/><path d="M112,186 C146,176 156,202 188,190"/>'
    '<path d="M108,222 C136,212 152,232 180,222"/><path d="M168,112 C186,128 166,148 192,160"/>'
    '<path d="M140,246 C158,238 174,254 196,248"/><path d="M126,132 C142,128 146,140 160,138"/></g>'
)


def build_art():
    p = ['<svg viewBox="0 0 520 560" xmlns="http://www.w3.org/2000/svg" role="img" '
         'aria-label="Glowing brain above a stack of servers">', DEFS]
    p.append('<circle cx="260" cy="200" r="240" fill="url(#halo)"/>')
    p.append('<ellipse cx="260" cy="542" rx="235" ry="24" fill="rgba(2,6,23,.65)"/>')

    # platform with grid and glowing rings
    p.append(box(260, 410, 210, 18, "platTop", "leftG", "rightG", edge="#3b82f6"))
    grid = "".join(
        f'<line x1="0" y1="{c}" x2="520" y2="{c + 260}"/><line x1="0" y1="{c + 260}" x2="520" y2="{c}"/>'
        for c in range(40, 520, 30)
    )
    p.append(f'<g clip-path="url(#platClip)" stroke="#60a5fa" stroke-opacity=".16" stroke-width="1">{grid}</g>')
    p.append(rhombus(260, 410, 150, fill="none", stroke="#38bdf8", stroke_opacity=".55", stroke_width="1.5"))
    p.append(rhombus(260, 410, 186, fill="none", stroke="#38bdf8", stroke_opacity=".28", stroke_width="1.2",
                     stroke_dasharray="6 8"))

    # server stack (bottom to top), then the two small cubes in front
    for cy in (376, 336, 296):
        p.append(slab(260, cy, 108, 34))
    p.append(slab(150, 400, 34, 38))
    p.append(slab(370, 400, 34, 38))

    # glowing chip on the top slab and the light beam
    p.append(f'<g filter="url(#glow)">{rhombus(260, 296, 60, fill="#22d3ee", opacity=".9")}'
             f'{rhombus(260, 296, 30, fill="#e0f7ff", opacity=".95")}</g>')
    p.append('<polygon points="234,294 286,294 312,226 208,226" fill="url(#beam)"/>')

    # orbit rings around the brain
    p.append('<g transform="rotate(-14 260 160)" fill="none" stroke="#38bdf8" stroke-width="1.4">'
             '<ellipse class="orbit" cx="260" cy="160" rx="158" ry="40" stroke-opacity=".6"/>'
             '<circle cx="418" cy="160" r="4.5" fill="#67e8f9" stroke="none"/>'
             '<circle cx="102" cy="160" r="3.5" fill="#93c5fd" stroke="none"/></g>')
    p.append('<g transform="rotate(12 260 170)" fill="none" stroke="#60a5fa" stroke-width="1.1">'
             '<ellipse class="orbit" cx="260" cy="170" rx="182" ry="50" stroke-opacity=".32"/>'
             '<circle cx="260" cy="120" r="3" fill="#bae6fd" stroke="none"/></g>')

    # the brain (two mirrored hemispheres) with glow
    p.append('<g class="brain" filter="url(#glow)" transform="translate(260,150) scale(.62) translate(-210,-160)">'
             f'{HEMI}<g transform="translate(420,0) scale(-1,1)">{HEMI}</g></g>')

    # sparkles
    for x, y, r, c in [(96, 96, 2.5, "#7dd3fc"), (430, 70, 2, "#bae6fd"), (60, 250, 2, "#60a5fa"),
                       (470, 260, 3, "#38bdf8"), (140, 40, 1.8, "#bae6fd"), (390, 40, 2.4, "#93c5fd"),
                       (30, 340, 1.8, "#7dd3fc"), (495, 350, 2, "#7dd3fc")]:
        p.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity=".85"/>')
    p.append("</svg>")
    return "".join(p)


ICONS = {
    "db": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#bae6fd" stroke-width="1.8" '
          'stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="6" rx="8" ry="3"/>'
          '<path d="M4 6v6c0 1.7 3.6 3 8 3s8-1.3 8-3V6"/><path d="M4 12v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/></svg>',
    "loop": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#bae6fd" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-3-6.7"/>'
            '<polyline points="21 3 21 9 15 9"/></svg>',
    "trend": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#bae6fd" stroke-width="1.8" '
             'stroke-linecap="round" stroke-linejoin="round"><polyline points="3 17 9 11 13 15 21 7"/>'
             '<polyline points="15 7 21 7 21 13"/></svg>',
}

# ------------------------------------------------------------------ top bar
st.markdown(
    flat("""
    <div class="lp-nav">
      <div class="lp-brand"><div class="lp-logo">🧠</div><div class="lp-brand-name">RecallOps</div></div>
      <div class="lp-pill">Powered by Hindsight memory</div>
    </div>
    """),
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ hero
left, right = st.columns([1.02, 1], gap="large")

with left:
    st.markdown(
        flat("""
        <div class="lp-eyebrow"><span class="dot"></span>AI-powered incident memory</div>
        <div class="lp-h1">Your team's <span class="lp-hl">memory</span><br>for production incidents.</div>
        <div class="lp-p">RecallOps pairs AI with long-term memory so you resolve incidents faster by learning
        from past experience, including <mark>what didn't work</mark>.</div>
        """),
        unsafe_allow_html=True,
    )
    b1, b2, _ = st.columns([1, 1.25, 1.2])
    with b1:
        if st.button("Get Started", type="primary", icon=":material/arrow_forward:", key="lp_start"):
            st.switch_page("pages_/home.py")
    with b2:
        if st.button("Explore incidents", icon=":material/list_alt:", key="lp_explore"):
            st.switch_page("pages_/incidents.py")

with right:
    st.markdown(
        flat(f"""
        <div class="lp-art">
          {build_art()}
          <div class="float-tag" style="top:7%; left:3%;">Payment API 500s</div>
          <div class="float-tag" style="top:21%; right:0; animation-delay:-1.4s;">DB Connection Leak</div>
          <div class="float-tag green" style="top:47%; left:0; animation-delay:-2.6s;">Rollback worked ✓</div>
          <div class="float-tag" style="top:64%; right:3%; animation-delay:-3.8s;">Cache Timeout</div>
        </div>
        """),
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------------ feature cards
st.markdown(
    flat(f"""
    <div class="fc-row">
      <div class="fc"><div class="fc-ic">{ICONS['db']}</div><div class="fc-t">Remember</div>
        <div class="fc-s">Every incident, root cause and fix is kept in long-term memory, not lost in chat threads.</div></div>
      <div class="fc"><div class="fc-ic">{ICONS['loop']}</div><div class="fc-t">Learn from what failed</div>
        <div class="fc-s">See what worked and what didn't before you spend time on the same dead end again.</div></div>
      <div class="fc"><div class="fc-ic">{ICONS['trend']}</div><div class="fc-t">Get smarter</div>
        <div class="fc-s">Get recommendations grounded in your team's own history and feedback.</div></div>
    </div>
    """),
    unsafe_allow_html=True,
)
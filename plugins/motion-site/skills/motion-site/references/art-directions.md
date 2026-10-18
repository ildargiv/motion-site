# Art directions

Pick one direction for the topic and audience. Each is a complete character: color, type, and motion that agree with each other.

Every direction has a **modern pairing** (current Google Fonts favorites) and a **Cyrillic pairing** for pages in Russian, Ukrainian, Bulgarian, and other Cyrillic languages. Script support below was checked against the Google Fonts API — many trending fonts are Latin-only, so never assume.

---

## 1. Midnight Launch
**For:** products, apps, hardware, startups.
**Palette:** background `#0a0a0c`, surfaces `#141418`, text `#f2f1ee`, one vivid accent: orange `#ff5a1f`, lime `#c8ff3e`, or blue `#4d6bff`.
**Type:** Bricolage Grotesque 800 (use its `opsz` axis at 96 for headlines) + Geist for text.
**Cyrillic:** Unbounded 800 + Geist.
**Motion:** confident and cinematic. Long push-ins, huge type, odometers.
**Signature move:** the product (a card or a screen) opens to full screen and becomes the next scene.

## 2. Editorial
**For:** architecture, fashion, photography, magazines, galleries.
**Palette:** paper `#f4f1ea`, ink `#141312`, a muted accent: terracotta `#b4532a` or olive `#5c6b3a`.
**Type:** Instrument Serif (italic as the accent) + Instrument Sans or Geist.
**Cyrillic:** Playfair Display or Cormorant Garamond (italic as the accent) + Geist.
**Motion:** slow and refined. Images open with clip-path, text rises line by line, photo parallax.
**Signature move:** a photo opens from its own edge, and the caption arrives line by line half a second later.

## 3. Swiss Kinetic
**For:** agencies, conferences, design studios, portfolios.
**Palette:** white `#ffffff`, black `#0d0d0d`, one signal color: red `#ff2a1a` or ultramarine `#2b2bff`.
**Type:** Host Grotesk or Geist 800 for everything, with extreme size contrast; Geist Mono for labels.
**Cyrillic:** Geist + Geist Mono, or Inter Tight.
**Motion:** precise and grid-bound. Sharp `expo` easing, words swapping places, numbers clicking.
**Signature move:** a full-width headline whose words slide apart into grid columns as you scroll.

## 4. Warm Craft
**For:** cafés, bakeries, workshops, local brands, food.
**Palette:** cream `#f3ede4`, coffee `#2a1d14`, caramel `#c48a55`, green `#4f6b3a`.
**Type:** Fraunces (soft, with its `SOFT` and `WONK` axes) + Instrument Sans.
**Cyrillic:** Prata + Manrope.
**Motion:** soft and springy. Menu cards stack up, objects rotate gently.
**Signature move:** the hero object (a cup, a loaf, a product) stays centered while scenes change around it.

## 5. Liquid Glass
**For:** fintech, SaaS, AI products, premium services.
**Palette:** deep background `#07080d`, glass `rgba(255,255,255,.06)` with a `rgba(255,255,255,.12)` edge, gradient blooms: violet `#7a5cff`, teal `#2de2c6`.
**Type:** Funnel Display + Funnel Sans.
**Cyrillic:** Geologica + Geist.
**Motion:** fluid with depth. Parallax glass layers, soft blur, morphing charts.
**Signature move:** the product UI explodes into 3D layers (`rotateX`, `translateZ`) and reassembles.

## 6. Neo-Brutal
**For:** youth brands, music, events, creative communities.
**Palette:** acid background (`#d9ff3f` or `#ff6ad5`), black `#000`, white blocks, 3px outlines.
**Type:** Syne 800 or Big Shoulders Display + Space Mono.
**Cyrillic:** Dela Gothic One + Martian Mono.
**Motion:** bold but precise. Hard shadows, shifting blocks, marquees that react to scroll speed.
**Signature move:** a marquee that speeds up and flips direction with the scroll.

---

## Your own direction

If none fits, define your own with the same recipe: who it's for, a palette (2–3 colors plus neutrals), a type pairing, the motion character in one word, one signature move. The client's brand colors and fonts always beat any direction.

## Script support (verified on Google Fonts)

| Font | Latin | Cyrillic | Greek |
|---|---|---|---|
| Geist, Geist Mono | ✓ | ✓ | — |
| Bricolage Grotesque, Instrument Serif, Instrument Sans, Funnel Display, Funnel Sans, Host Grotesk, Fraunces, Big Shoulders Display, Space Mono | ✓ | — | — |
| Syne | ✓ | — | ✓ |
| Unbounded, Onest, Golos Text, Wix Madefor Display, Martian Mono, Playfair Display, Prata, Cormorant Garamond, Montserrat | ✓ | ✓ | — |
| Inter Tight, Manrope, Geologica, Literata, Dela Gothic One, Tektur, JetBrains Mono | ✓ | ✓ | ✓ |

Load only the weights you use, with `display=swap`, and preconnect to `fonts.gstatic.com`.

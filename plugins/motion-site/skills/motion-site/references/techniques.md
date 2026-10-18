# Techniques

Recipes for GSAP 3.13 + ScrollTrigger + SplitText (every GSAP plugin is free since 3.13). The code is meant to run inside `mm.add(...)` from `assets/starter.html`, which already provides `EASE`, `DUR`, `STAGGER`, the `desktop` flag, and the reduced-motion check.

Five techniques are already built into the starter: **masked text reveal, odometer, portal, horizontal rail, card stack**. They are summarized below, followed by the rest.

Each technique says when it fits. Never use a technique without a reason.

---

## Masked text reveal
**When:** every large headline. The base technique; half of the "expensive" feel comes from it.
```js
SplitText.create(el, { type: "lines,words", mask: "lines", autoSplit: true,
  onSplit: self => gsap.from(self.words, { yPercent: 115, rotate: 3, duration: 1.1, ease: "expo.out", stagger: .09,
    scrollTrigger: { trigger: el, start: "top 85%" } }) });
```
Gotcha: `onSplit` must return the animation, so SplitText can re-split lines on resize. Hide the headline until it is split (`.motion [data-split] { visibility: hidden }`) and reveal it inside `onSplit`.

## Odometer
**When:** every real number. Numbers never pop in; they roll. Implementation: `buildOdometer` in the starter. Each next digit rolls 0.2–0.3s longer, so the number settles right to left. `fitOdometers` sizes each column to its final digit so a narrow "1" never looks like a gap.

## Portal (push-in)
**When:** the transition into the main scene, often the peak itself. A card opens to full screen and becomes the next scene.
```js
gsap.timeline({ scrollTrigger: { trigger: portal, start: "top top", end: "+=150%", scrub: 1, pin: true } })
  .to(media, { clipPath: "inset(0% 0% round 0px)", ease: "none" })   // from inset(14% 18% round 28px)
  .to(media.querySelector(".fill"), { scale: 1, ease: "none" }, 0)  // content "approaches" from scale 1.35
  .to({}, { duration: .4 });                                        // hold
```

## Horizontal rail
**When:** portfolio, case studies, process steps, 4+ items. Desktop only; on phones use native `overflow-x: auto` with `scroll-snap`.
```js
const move = gsap.to(track, { x: () => -(track.scrollWidth - innerWidth), ease: "none",
  scrollTrigger: { trigger: rail, pin: true, scrub: 1, end: () => "+=" + (track.scrollWidth - innerWidth), invalidateOnRefresh: true } });
// parallax inside each card
gsap.fromTo(fill, { xPercent: -8 }, { xPercent: 8, ease: "none",
  scrollTrigger: { trigger: card, containerAnimation: move, start: "left right", end: "right left", scrub: true } });
```

## Card stack
**When:** process steps, pricing tiers, principles — 3 to 5 items. Cards are `position: sticky`; the previous one sinks back.
```js
cards.slice(0, -1).forEach((card, i) => gsap.to(card, { scale: .9, filter: "brightness(.55)", ease: "none",
  scrollTrigger: { trigger: cards[i + 1], start: "top bottom", end: "top 12%", scrub: true } }));
```

---

## Image reveal
**When:** editorial photography, case studies. The image opens from its own edge instead of fading in.
```js
gsap.fromTo(figure, { clipPath: "inset(100% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 1.4, ease: "expo.out",
  scrollTrigger: { trigger: figure, start: "top 80%" } });
gsap.from(figure.querySelector("img"), { scale: 1.3, duration: 1.8, ease: "expo.out",
  scrollTrigger: { trigger: figure, start: "top 80%" } });
```

## Read-along text
**When:** a manifesto, an "about" statement, one long idea. Words light up as you scroll.
```js
SplitText.create(p, { type: "words", autoSplit: true,
  onSplit: s => gsap.fromTo(s.words, { opacity: .15 }, { opacity: 1, stagger: .1, ease: "none",
    scrollTrigger: { trigger: p, start: "top 75%", end: "bottom 45%", scrub: true } }) });
```

## Sticky swap
**When:** 3–4 product benefits. One big object stays put on one side and changes state while the text scrolls on the other.
```js
steps.forEach((step, i) => ScrollTrigger.create({ trigger: step, start: "top center", end: "bottom center",
  onToggle: self => self.isActive && gsap.to(visual, { "--state": i, duration: .9, ease: "power3.inOut" }) }));
```
The visual reacts to the `--state` CSS variable, or swaps layers with `autoAlpha` and a 0.3s overlap.

## Theme shift by section
**When:** the page moves through distinct "chapters". The background flows instead of switching.
```js
gsap.utils.toArray("[data-theme]").forEach(sec => ScrollTrigger.create({ trigger: sec, start: "top 50%", end: "bottom 50%",
  onToggle: s => s.isActive && gsap.to("body", { backgroundColor: sec.dataset.theme, duration: .9, ease: "power3.inOut" }) }));
```

## Line draw
**When:** diagrams, routes, connections between steps, signatures.
```js
const len = path.getTotalLength();
gsap.fromTo(path, { strokeDasharray: len, strokeDashoffset: len }, { strokeDashoffset: 0, ease: "none",
  scrollTrigger: { trigger: svg, start: "top 70%", end: "bottom 40%", scrub: 1 } });
```

## Velocity marquee
**When:** neo-brutal pages, events, client lists (real clients only).
```js
const loop = gsap.to(row, { xPercent: -50, duration: 20, ease: "none", repeat: -1 }); // content duplicated twice
ScrollTrigger.create({ onUpdate: s => {
  const v = gsap.utils.clamp(-4, 4, s.getVelocity() / 300);
  gsap.to(loop, { timeScale: v || 1, duration: .4, overwrite: true });
} });
```

## 3D layer explode
**When:** liquid glass, SaaS, showing what a product is made of.
```js
gsap.timeline({ scrollTrigger: { trigger: scene, pin: true, scrub: 1, end: "+=140%" } })
  .to(stack, { rotateX: 55, rotateZ: -25, ease: "none" })
  .to(layers, { z: i => i * 90, ease: "none" }, 0)   // parent: transform-style: preserve-3d; perspective: 1600px
  .to({}, { duration: .4 });
```

## Chart morph
**When:** real data. Values are exact, bars grow from zero 0.08s apart, labels roll like an odometer.
```js
gsap.from(bars, { scaleY: 0, transformOrigin: "50% 100%", duration: 1.2, ease: "expo.out", stagger: .08,
  scrollTrigger: { trigger: chart, start: "top 75%" } });
```

## Magnetic button
**When:** the primary call to action, on devices with a mouse only. Implemented in the starter (`data-magnet`). Strength 0.25–0.35, no more: the button leans toward the cursor; it never runs away.

## Light sweep
**When:** a card or pricing tier becomes the focus. Once, never on a loop.
```html
<div class="card"><span class="shine"></span>…</div>
```
```css
.card { position: relative; overflow: hidden; }
.shine { position: absolute; inset: 0; pointer-events: none;
  background: linear-gradient(105deg, transparent 40%, rgba(255,255,255,.18) 50%, transparent 60%); }
```
```js
gsap.fromTo(card.querySelector(".shine"), { xPercent: -120 }, { xPercent: 120, duration: 1.2, ease: "power2.inOut",
  scrollTrigger: { trigger: card, start: "top 60%", once: true } });
```

## Layout transition (Flip)
**When:** an element changes layout: a card goes full screen, a grid reflows after filtering. Load `Flip.min.js` from the same CDN.
```js
const state = Flip.getState(items);
container.classList.toggle("expanded");
Flip.from(state, { duration: .9, ease: "power3.inOut", absolute: true, stagger: .04 });
```

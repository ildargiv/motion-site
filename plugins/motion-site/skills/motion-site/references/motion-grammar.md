# Motion grammar

These are the rules that make motion feel expensive. Break them only on purpose, and write down why.

## Easing

| Job | GSAP ease | Why |
|---|---|---|
| An element enters | `expo.out` | Sharp start, long settle: the object arrives and lands with confidence |
| An element exits | `power3.in` | It accelerates away; the eye is already on what's next |
| Spring (cards, buttons, tags) | `back.out(1.2)` | A small settle past the finish. Above 1.4 it becomes a cartoon bounce |
| Travel between states | `power3.inOut` | The object knows where it comes from and where it goes |
| Scrubbed scenes | `none` + `scrub: 1` | The visitor's hand is the curve; `scrub: 1` smooths it |
| Drift and rotation | `sine.inOut`, yoyo | The only place near-linear motion belongs |

Linear motion (`none`) without scrub is forbidden everywhere except an endless marquee.

## Durations

| What | How long |
|---|---|
| Headline enter (per word) | 1.0–1.2s |
| Secondary element enter | 0.8–1.0s |
| Exit | half of the enter: 0.4–0.6s |
| Hover | 0.3–0.5s |
| Odometer | 1.8–2.6s, each next digit 0.2–0.3s longer |
| Holding a result | at least 1.2s; the final idea 2s+ |

## Choreography

- **Stagger:** words 0.09s, lines 0.12s, items and cards 0.2s.
- **Order:** the hero object first, then captions, then the action (button). The eye follows the order of appearance.
- **Overlap:** the next element starts while the previous one is still settling (`"-=0.6"` in a timeline). A scene without overlap feels like slides.
- **One point of attention.** At any moment one main thing moves; everything else is still or drifting in the background.
- **Direction carries meaning:** bottom → up means "appeared", left → right means "next in the process", growth means "more important", sinking back means "done".

## Scroll

- **Trigger or scrub.** Text reveals use a trigger (`start: "top 85%"`) and play once. Object transformations use scrub: the hand drives them.
- **Pin length:** 100–200% of the viewport height. Longer and the visitor thinks the page is broken.
- **Hold inside a scrub:** the last 25–40% of the timeline is an empty pause (`tl.to({}, {duration: .4})`) so the result can be read.
- **Lenis** with `lerp: 0.1` makes scrolling buttery without taking control away. Never change wheel speed.
- **At most two pinned scenes** per page, never two in a row.

## The peak moment

A page has exactly one moment people remember it for: the biggest scale, the most complex transformation, the longest scene. Everything before it builds up; everything after it calms down. If everything is "wow", nothing is.

## Depth

- **Layered shadows:** a thin light top edge (`inset 0 1px 0 rgba(255,255,255,.06)`) plus 2–3 soft shadows of different radii.
- **Parallax:** closer layers move faster and cast stronger shadows. Keep the speed difference at 10–20%.
- **Blur** (`filter: blur(8–14px)`) only on fast state changes and on far layers.

## Typography in motion

- The hero word or headline is 120px+ on desktop, tight tracking (`letter-spacing: -0.04em`), line height 0.9–1.0.
- No more than 5–7 words of large text per scene.
- Text rises out of a line mask (`overflow: hidden`) instead of fading in: it feels physical.
- While text is being read, it stays still.

## Mobile

- Pins are vertical only and no longer than 100% of the viewport; horizontal rails become native scrolling with `scroll-snap`.
- Travel distances shrink by about a third.
- Hover effects and magnetic buttons are off (`(hover: hover)`).
- Always check at 360–390px wide.

## Accessibility and performance

- `prefers-reduced-motion: reduce` means no animation and everything visible. Use `gsap.matchMedia()`.
- Animate only `transform`, `opacity`, `clip-path`, `filter`. Use `will-change` only on what actually moves.
- Call `ScrollTrigger.refresh()` after `document.fonts.ready`, or positions drift.
- Keep it under ~40 simultaneously animating elements on screen.

# Quality rubric

Score every scene on five axes from 1 to 10 by looking at the frame sheet, not at the code. Ship when every scene scores 9+, or when the score stops improving for two rounds — then say honestly what is still short.

## The five axes

### 1. Idea — is it clear without a single explanation?
- **5:** pretty, but you can't tell what the scene is about.
- **7:** the idea is there, but you have to read small text to get it.
- **9:** one idea reads in 2 seconds from the hero object and the headline.

### 2. Composition
- **5:** small objects in an empty screen, everything centered, no hierarchy.
- **7:** there is hierarchy, but the hero object fills less than half the scene or competes with another.
- **9:** one hero object at 50–70% of the screen, a clear grid, nothing important closer than 60px to the edge.

### 3. Motion
- **5:** everything fades in at once, linear curves, motion for its own sake.
- **7:** correct easing and stagger, but transitions via fades and no overlap.
- **9:** the object itself becomes the next scene; enters settle, exits accelerate, results hold.

### 4. Typography
- **5:** system font, headline under 60px, lots of words at large size.
- **7:** a good pairing, but weak size contrast and loose tracking.
- **9:** a huge confident headline at −0.04em tracking, no more than 5–7 large words, text rising out of a mask.

### 5. Rhythm
- **5:** every scene is equally loud; no peak, or the peak comes first.
- **7:** there is a peak, but two pinned scenes sit back to back, or the ending is busy.
- **9:** calm → active → calm; one peak at 60–75% of the page; the ending holds long and quiet.

## Round table

```
Round 2
| Scene  | Idea | Composition | Motion | Typography | Rhythm | Min |
|--------|------|-------------|--------|------------|--------|-----|
| Hero   | 9    | 9           | 8      | 9          | 9      | 8   |
| Portal | 9    | 10          | 9      | 9          | 9      | 9   |
Three worst spots: …
Fixing: …
```

## Technical blockers

Any of these automatically scores 5 on every axis for the scene where it occurs:
- a console error;
- horizontal scrolling on mobile;
- text under 14px on mobile;
- content hidden with `prefers-reduced-motion` or without JS;
- a mobile pin longer than one screen;
- an empty first screen in the first second.

# Audiogram

<img width="1004" height="1005" alt="Screenshot 2026-08-03 at 22 23 09" src="https://github.com/user-attachments/assets/0530e40c-179c-4ae0-bc31-579cc0c028ef" />

## Requirements

Only Remotion as a dependency

## Prompt: build a 1:1 audiogram in Remotion

Paste everything below the line into an AI coding assistant, or read it yourself as a spec. Every number is taken from a working build, not invented.

---

Build me a square audiogram in Remotion. It turns a short audio clip into a 1080x1080 video with word-by-word captions, a speaker credit card and a waveform driven by the actual audio.

## Output

- **1080x1080, 30fps, H.264, CRF 18.**
- Duration comes from the audio file, not a hardcoded number. Use `calculateMetadata` with `getAudioDurationInSeconds`, then add **2.5 seconds** for a silent outro card.
- Everything is data driven. Adding a clip should be a config entry, never a code change.

## Palette

Dark plum background with a lavender accent. Do not substitute a generic dark theme, the specific hues are what make it read as designed rather than defaulted.

```
bg          #161826
text        #e9e9ed
textSoft    rgba(233,233,237,0.70)
textMuted   rgba(233,233,237,0.55)
textDim     rgba(233,233,237,0.34)

accent      #9184d9
accent300   #d2cefd
accent700   #5d5294
accent800   #423a6a
accent900   #2b2741

neutral500  #9397ab
neutral700  #595d6c
```

Typeface is **Inter** throughout, weight 500 for anything large. Load it via `@remotion/google-fonts` so the render does not depend on a local install. Use a monospace stack for handles only.

## Layout

Padding is `64px 72px 60px`. Stack top to bottom:

1. **Header bar.** Left: a 40x1px accent rule, a 30px microphone glyph, then a label in 26px uppercase with `letter-spacing: 0.06em`. Right: an 11px accent dot with a soft glow, then a muted uppercase label.
2. **Speaker card**, 52px below the header.
3. **Captions**, 56px below the card, taking the remaining space.
4. **Footer**, pinned to the bottom: waveform, then a progress bar, then a credit line.

### Background

Two radial gradients over the flat background, plus a dot grid:

```css
background-color: #161826;
background-image:
  radial-gradient(120% 70% at 80% -10%, #2b2741bf, transparent 58%),
  radial-gradient(130% 80% at -12% 112%, rgba(0,0,0,0.30), transparent 52%);
```

Then a separate layer on top for the grid:

```css
background-image: radial-gradient(#9397ab33 1px, transparent 1.5px);
background-size: 48px 48px;
mask-image: radial-gradient(110% 70% at 72% 8%, #000 0%, transparent 68%);
```

**The mask is the important part.** An unmasked grid across the whole frame looks like graph paper. Masked so it fades out toward the bottom left, it reads as texture behind the glow.

### Speaker card

Avatar on the left, three lines of credit on the right.

- Avatar is a circle, `1px solid #595d6c` border, plus `outline: 1px solid #423a6a` with `outline-offset: 7px`. That double ring is what stops it looking like a pasted-in profile picture.
- Name in 40px, handle in 29px monospace `#d2cefd`, title in 27px at 70% opacity.
- If a speaker has no photo, fall back to their initial in `#d2cefd` on a `#2b2741` disc at 42% of the avatar size. Do not use a generic silhouette.

## Animation

Five things move. Nothing else does, and that restraint is deliberate.

### 1. Speaker card entry

```js
spring({ frame, fps, config: { damping: 200, mass: 0.7 } })
```

Drives opacity 0 to 1 and `translateY` from 28px to 0.

### 2. Speaker card collapse

At **2.4 seconds**, over **0.5 seconds**, interpolate a single `expanded` value from `1` to `0.55` and derive everything from it:

| Property | expanded 1 | expanded 0 |
|---|---|---|
| avatar size | 176px | 120px |
| gap | 32px | 24px |
| name size | 40px | 32px |
| title height | 35px | 0 |
| title opacity | 1 | 0 |

The title collapsing its own height rather than fading in place is what stops a gap appearing.

### 3. Captions

Word by word, three states:

- **already spoken** `#e9e9ed`
- **being spoken now** `#d2cefd`
- **not yet spoken** `rgba(233,233,237,0.34)`

56px, `line-height: 1.26`, `letter-spacing: -0.015em`, weight 500.

**Chunk by character budget, not by word count.** Fill up to **150 characters**, but break early on a sentence end once you are past 60% of the budget. Word-count chunking looks fine until one window happens to contain long words and it grows a whole line taller than its neighbours. Character budgeting keeps every window the same physical size.

The window advances a chunk at a time, never a word at a time, or the text jitters on every frame.

### 4. Waveform

Real audio, not a canned loop. 56 bars, 84px tall, 9px wide, 5px radius, spread with `justify-content: space-between`.

```js
const spectrum = visualizeAudio({ fps, frame, audioData, numberOfSamples: 128 });
const barHeight = Math.max(6, Math.min(height, Math.sqrt(spectrum[i]) * 5.2 * height));
```

Two details worth keeping:

- **Square root the amplitude.** Linear scaling makes quiet passages flatline into a dead line at the bottom.
- **Every 9th bar takes the light accent** `#d2cefd`, the rest `#5d5294`. It stops the bar field reading as a single grey mass.

### 5. Pull-quote outro

The final 2.5 seconds are silent. Replace the card and captions with a big quote:

- A 190px opening curly quote in `#5d5294` above it.
- Quote lines at **78px**, `line-height: 1.16`, `letter-spacing: -0.02em`.
- Later lines take the accent colour, earlier lines stay white. Splitting the colour partway through gives the quote a visual punchline.
- Each line springs in staggered by 4 frames: `spring({ frame: frame - i * 4, fps, config: { damping: 200, mass: 0.6 } })`, driving opacity and `translateY` from 22px.

**Auto-fit the font size** so a long quote never overflows:

```js
const longest = Math.max(...lines.map(l => l.length));
const fontSize = Math.min(78, Math.floor((1080 - 144) / (longest * 0.55)));
```

0.55 is a rough per-character advance for Inter 500. Cheaper and more predictable than measuring the DOM, and it keeps every clip on one visual system.

### Header dot

A 2.4 second sine pulse between 0.3 and 1 opacity:

```js
interpolate(Math.sin((frame / fps) * (2 * Math.PI / 2.4)), [-1, 1], [0.3, 1])
```

## Multi-speaker version

For a clip stitched from several people, add an optional `segments` array of `{ speaker, startsAt }`. Then:

- Look up who is speaking at the current time and swap the card.
- **Keep the card at a fixed size, do not run the collapse.** Nobody is on screen long enough for a collapse to read as anything but a glitch. Hold `expanded` at 0.75.
- **The entry spring must replay per speaker.** This is the one that will catch you out.

```jsx
// Does not work. useCurrentFrame counts from the start of the composition,
// so by the time speaker two arrives the spring has long since settled at 1.
<SpeakerCard key={speakerId} speaker={speaker} />

// Works. Pass in when this speaker arrives and offset the spring.
<SpeakerCard key={speakerId} speaker={speaker} enterFrame={Math.round(startsAt * fps)} />
// inside: spring({ frame: frame - enterFrame, fps, ... })
```

Remounting is real, but the timeline does not know or care that your component is new. You have to tell it.

## Audio prep

Before any of this, normalise the clip or it will be inaudible next to everything else in a feed:

```bash
ffmpeg -i raw.wav \
  -af "highpass=f=85,loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=in:d=0.12,afade=t=out:st=<dur-0.3>:d=0.30" \
  -ar 48000 -ac 1 -c:a pcm_s16le clip.wav
```

- **Highpass at 85 Hz** removes room rumble.
- **-14 LUFS** is the social platform target. Raw conference or call audio is typically -24 to -30.
- **Use WAV, not AAC.** AAC carries an encoder priming delay that shifts playback a few milliseconds against your caption timings, which is exactly the drift that makes word highlighting look broken.

## Captions data

```json
{
  "source": "whisper",
  "words": [
    { "word": "It's", "start": 0.10, "end": 0.32 },
    { "word": "also", "start": 0.32, "end": 0.54 }
  ]
}
```

Generate with `whisper <file> --model medium.en --word_timestamps True --output_format json`, then flatten `segments[].words[]`. Do not use `small` on real-world audio, it hallucinates words that were never said.

Validate the file at load and throw on a malformed one. A caption file that silently drops words gives you a video that looks right and is wrong.

## Constraints

- TypeScript, strict. No `any`.
- Only Remotion as a dependency. No UI framework, no animation library.
- Palette in one tokens file. Nothing hardcodes a hex anywhere else.
- Clips and speakers in data files, not in components.

---

## Note for whoever is reading this

The palette above came from a specific personal brand. If you are building this for yourself, keep the **structure** and swap the hues. The things that actually make it work are the masked dot grid, the double ring on the avatar, the sqrt-scaled waveform, character-budget caption chunking and the restraint of only animating five things. Those hold up in any colour.

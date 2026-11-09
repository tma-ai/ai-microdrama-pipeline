---
name: ai-film-director
description: Directs an AI film or micro-drama episode end to end with Meta Muse on the BeefTV canvas, using the anti-slop method distilled from Higgsfield Academy (~120 lessons), 10 creator pipelines, AI micro-drama studios and critics (research/higgsfield_2026-11-08). Covers asset locks, one-set geography, storyboards built from approved stills, the 10 s three-angle prompt structure, takes and frame-by-frame QC gates, the speaker-safe edit and finishing. Use when the user says "direct this", "re-direct the episode", "it looks like AI slop", "the set keeps changing", "camera angles are bad", "make the storyboard", "write the scene prompts", or before generating any episode.
---

# AI FILM DIRECTOR (v1.0, installed 2026-11-08)

**Roles:**
- **Antigravity** writes the story and dialogue.
- **David** approves the storyboards and the cut.
- **Claude** directs the shots, runs the pipeline and does QC.

Every source in the research agrees on one thing: an AI drafts and a human decides. No credible film is agent-directed.

**Tags:** **[R]** from the research reports (sources in research/higgsfield_2026-11-08/01–05). **[MUSE]** measured by us. **[USER]** David's standing rule.

**Run `ai-story-architect` first:** its 12-test story gate and STORY MAP must pass before Gate 2.

## THE PIPELINE: 7 gates. Nothing passes a gate until it is checked.

### Gate 1: Story check (before any image)
- **One-line test:** the episode has one want, one obstacle, stakes, a turn and a cliffhanger. If you can't state them, stop and send notes to Antigravity [USER: story coherence].
- **Hook (0–3 s):** a face mid-reaction with the cause withheld, a shock line, or evidence already being found. Never an establishing shot or a walk-in on its own [R03].
- **Rhythm:** an emotional spike by 7 s, a reversal around 0:30, and an ending on one of four cliffhanger types: Reveal, Threat, Revelation or Decision [R03].
- **Cut anything that adds nothing to the want.** For each beat ask "what does this give the viewer?" Delete the beat if there is no answer [R01].
- **Plant and pay off:** every prop or name in the last scene must be shown earlier.

### Gate 2: Asset locks
1. **Character sheet.** One face per sheet, plus front, back and both profiles, on grey [R04].
   - **Identity block:** "NAME, age NN, height, build, face by bone structure (jaw, cheekbones, brow, nose), hair, eyes, wardrobe". It is pasted word for word into every prompt and never paraphrased [R01, R04].
   - Never use vague beauty words such as "handsome" or "cute"; they average faces into slop [R03].
   - **No marks unless scripted** [USER].
   - Each changed state (wet, aged, injured) gets its own sheet [R01].
2. **Location set.**
   - A master plate, then the other angles generated as EDITS of the master: the reverse, the side, and the views from each character's eyeline.
   - Write a LOCATION MAP (what is on each wall) and draw a top-down dot map.
   - Write one LIGHT LINE and paste it word for word [R01, R04, MUSE].
   - The two ends of a room must differ (here, the window versus the door). Plain long walls should be identical, which reduces drift.
3. **Prop list.** One of each story prop. Each prop's position at the start and end of every scene is written down.

### Gate 3: Blocking and axis
- **Fix everyone's mark** for the whole scene: seat, standing mark and route.
- **Fix the 180° line.** The camera stays on one side, so A always looks frame right and B frame left.
- **Fixed backgrounds.** Each character's background follows from the marks and doesn't change (window behind A, door behind B) [R01, R05].

### Gate 4: Storyboards (David approves)
- **One storyboard per 10 s scene,** made of 3 panels for angles A, B and C [USER: 3 angles per scene].
- **Panels are never drawn from scratch;** a board drawn from scratch moved the room [MUSE].
  - Each panel is an EDIT of the approved plate for its camera direction ("keep this exact photo, same camera, only add people").
  - Or it is a closer framing of an already approved panel ("closer shot of the same moment").
- **Check each panel** against the plates, at full size: walls, lamps, window position, people's seats, props and age.
- **Join the panels locally** with `tools/beeftv/board_upload.py` (black gutters; generation runs through `tools/beeftv/btv_batch.py`) and upload the board as a canvas card.
- **Coverage per scene:**
  - Angle A starts with a wide that fixes who sits where. The model "improvises the room fresh on every cut" without it [R01].
  - B and C are singles, over-the-shoulders, inserts or reactions.
  - Vary lens and height, with close-ups dominating in vertical [R03].

### Gate 5: The 10 s scene prompt (structure from Higgsfield Cinema Studio, R01 and R04)
```
FORMAT: Photorealistic <genre>, vertical 9:16, 10 seconds, ONE scene in ONE room cut as exactly THREE camera angles with hard cuts.
REFERENCES: Picture 1 is the STORYBOARD: panels left→right are angles A, B, C; it controls framing, room, light and positions; it is never shown as a still frame, a split screen or panels.
  Picture 2 is <panel/plate>: it controls <x> only, not <y>.  Sheets: they control identity and outfit only, not pose, framing or background.
LOCATION MAP: <walls, landmarks>. 180° AXIS: camera stays on <side>; <A> looks frame right, <B> frame left. Behind the camera: <what is there>.
IDENTITY: <identity block per character, verbatim, including VOICE: "<voice line>">
ANGLE A, 0.0–x s: FIRST FRAME: <subject at x%/y%, landmarks visible, lens, camera distance in m>. ACTION: <physical beats with weight, contact, follow-through>. HARD CUT at x s.
ANGLE B, … ANGLE C, …
DIALOGUE: <speaker> at t s: "<exact line>". Finished by t s. The line sits only inside the speaker's own angles; the next person's angle starts after it ends, with their lips closed.
PERFORMANCE: <muscles and seconds: a swallow, a slow blink, the jaw tightening, a 1–2 s held pause after a big beat>.
AUDIO: <room tone, foley for every visible action>. Voice only from the speaker.
LOCKED FACTS: <positions, props, light line, ages>, stated positively.
```
Rules:
- **Positive locks only.** Write "the wall around the door is solid riveted steel edge to edge", not "no window". A banned thing gets planted [R01, R02, MUSE: a window appeared].
- **One motivated camera move per angle at most** [R05].
- **Keep extra angle references off.** Connect a panel image only if it can't leak a wrong background into another direction [MUSE: a window sliver leaked].
- **Muse obeys timed HARD CUT angles in 10 s** [MUSE 2026-11-08]. It can still drift on the last angle, so describe that angle's background explicitly until the last frame.

### Gate 5b: Continuity lock with start frame + end frame + storyboard [USER RULE 2026-11-08]
- **What each scene video gets:** three controls together.
  - **START frame:** the approved panel A still, or the previous scene's last frame when the action is continuous.
  - **END frame:** an approved still of where angle C must land. It becomes the next scene's START frame when the story is continuous.
  - **Storyboard reference:** controls angles A, B and C between them.
- **Tool:** `tools/beeftv/btv_startend.py <canvas> <title> <start_png> <end_node_title> <x> <y> <prompt_file> <storyboard + sheet titles…>`. It connects start → end → refs in that order. Set the `BTV_SIZE` environment variable to 9:16 for vertical.
- **Make the END frame first** as an edit of the approved plate or panel for angle C, and check it like a panel. Never generate an end frame from scratch.
- **Storyboard layout [USER RULE 2026-11-08]:** panel 1 IS the exact first frame (the previous locked scene's real last frame) and panel 3 IS the exact last frame; only panel 2 is the middle angle. This start + end + storyboard setup produced the scene 1 take David chose; it is the default method. Never chain from a take David has not confirmed.
- **David reviews every video output;** Claude reviews it first (Gate 6).

### Gate 6: Takes and QC (Claude watches every take before anyone else sees it)
- **Takes:** 3–4 per scene where the plan allows, choosing by beat and not by clip. A take is kept only if you can complete "I keep this because it supplies ___" [R01, R02].
- **QC on every take** [R05, R04]:
  1. Dense frame sheet (8×3), then full-size frames at the first, middle and last frame of each angle.
  2. Compare against the storyboard: room, positions, eyelines.
  3. Stranger test on faces: would a stranger say it's the same person, at the same age?
  4. Transcript: words exact, right speaker, lips (only the speaker's move).
  5. Sound with picture, then sound alone.
  6. Physics: causes before effects, real weight [USER].
- **Verdicts:**
  - 2 or more fails: regenerate.
  - Exactly 1 fail: repair in the edit (trim, cover with a reaction shot).
  - All 4 takes fail: fix the prompt or reference, not the luck.
  - Change one variable per retake and log it in review_log.md [R01, R02].
- **Never chain from a drifted clip.** Re-attach the original sheets every time [R04].

### Gate 7: The edit (David approves)
- **Live cut:** drop each kept take in before making the next [R02].
- **Trim** the first ~0.12 s of every clip and the slowed last 10–15% where it drags [R05].
- **Speaker-safe cutting:** never cut inside a line's last word. Use J/L cuts, and cover weak lip-sync with reaction shots [R05, drama-edit-sound].
- **Sound is the biggest single lever:**
  - continuous room tone under the cuts;
  - foley for every visible action;
  - deliberate silence;
  - music last, at most 30% of the voice level [R03, R05].
- **Finish:** one grade per scene so the angles match, grain after any upscale, and on-screen text lettered in post [R05, USER].
- **Watch the whole cut as a story** before reporting [USER].

## Pre-flight checklist (paste into the review log for each scene)
- [ ] Story beat states what it gives the viewer
- [ ] Storyboard panels are edits of approved plates; the board is approved by David
- [ ] Prompt has REFERENCES with control limits, MAP plus AXIS, identity blocks verbatim, FIRST FRAME lines, positive locks
- [ ] Line timing sits inside the speaker's angles
- [ ] Every take QC'd (frames, stranger test, transcript, sound, physics) and logged
- [ ] Kept take dropped into the live cut, and the cut re-watched as a story

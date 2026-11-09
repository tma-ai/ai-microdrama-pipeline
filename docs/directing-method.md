# Directing method v2: anti-slop rules for Muse (from 5 research reports, 2026-11-08)

Sources:
- 01 Higgsfield Academy (~120 lessons)
- 02 Creator workflows (10 creators, 3 studios)
- 03 Micro-drama production (including Chinese AI drama studios)
- 04 Consistency and multi-shot
- 05 Anti-slop craft

Each rule says which reports back it. Vendor claims are marked in the reports.

## 0. Who directs
- **Every source agrees: no serious film is directed by an agent** (02, 05, 01, 03).
- **AI drafts:** script breakdown, shot lists, prompts, contradiction checks.
- **A human approves at gates:** references, storyboard, take choice, the edit.
- **For us:** Claude drafts and runs the pipeline. David approves the storyboards and the cut, and Antigravity owns the story.

## 1. Lock assets before any video
1. **Character sheet.** One face per sheet, plus front, back and both profiles, with a numeric identity block: "age 32, 168 cm, …".
   - The block is pasted word for word into every prompt and never paraphrased.
   - The face is described by bone structure, never by adjectives like "handsome" (03).
   - Changed states (wet, aged, injured) get their own sheets (01, 04).
2. **Location set.**
   - A master plate, then about 5 angles made as edits of the master, including a reverse plate for each side of the room.
   - A written LOCATION MAP and a top-down dot map.
   - A light line pasted word for word into every prompt; paraphrasing it flips the direction (01, 02, 04).
3. **One face per sheet;** heads are cropped out on wardrobe panels (02).

## 2. Plan in pictures, not words
- **Shot list written by hand.** Coverage per scene: one wide, then singles, over-the-shoulders, inserts and reactions (02, 03).
- **Storyboard panels are made as edits of approved plates or panels, never drawn from scratch.** This is our proven fix: a storyboard drawn from scratch moved the room.
- **Hardest shot first** (03, 04).

## 3. The 10 s prompt structure (Higgsfield Cinema Studio format, 01 and 04)
1. **REFERENCES:** what each image controls and what it does NOT. "Controls the place and light only, not the camera angle; it is never shown as a still frame." "Controls identity and outfit only, not pose, framing or background."
2. **LOCATION MAP plus 180° AXIS line,** plus what the reverse angles reveal ("the wall behind the camera is…").
3. **IDENTITY BLOCKS:** pasted word for word for every character, with the voice line included.
4. **SHOTS:** 2–3 per 10 s, timed with hard cuts. The first shot is a 0.5–1.5 s wide that fixes who sits where; without it "the model improvises the room fresh on every cut". Each shot has:
   - a first-frame line: subject position as x/y %, which landmarks are visible, the lens and the camera distance in metres;
   - the action as physical beats (weight, contact, follow-through);
   - performance as muscles and seconds: a swallow, a slow blink, the jaw tightening, tears pooling;
   - one motivated camera move at most.
5. **DIALOGUE:**
   - A line belongs to the speaker's own shot and ends before any cut to someone else.
   - Under 5 s per shot.
   - A 1–2 s pause after big beats.
6. **POSITIVE LOCKS ONLY:** write the state you want ("the wall around the door is solid steel edge to edge"), never bans ("no window"). Bans plant the thing (01, 02).
7. **LOCKED FACTS:** a closing list of positions, props and light, pasted word for word.

## 4. Dialogue coverage
- **Speaker shots:** a locked-off identical single for speaker A and a locked-off identical over-the-shoulder for B. Eye level, with the lens written into every shot (01).
- **Vertical:** close-ups dominate, with eyes in the top third and one wide per scene. Use alternating singles, not side-by-side two-shots (03).

## 5. Takes and QC
- **Takes:** 3–4 per shot (keep rates run from 25% to under 2%) (02, 03, 05).
- **Judge each beat, not each clip.** Cut a scene from the best beats of several takes. Keep a take only if you can say "I keep this because it supplies ___" (01).
- **QC pass on every take** (05, 04):
  1. Watch full screen.
  2. Stop on the first, middle and last frames and compare them with the plate and sheet.
  3. Watch with sound on, then off.
  4. Apply the stranger test to faces: would a stranger say it is the same person?
  5. Check the set at full resolution.
- **Verdicts:** two or more fails means regenerate. Exactly one fail means repair in post. A fail on all 4 takes means fix the prompt or reference. Change one variable per pass and log it (01, 02, 04).
- **Never chain from a drifted clip.** Always re-attach the original sheet (04).

## 6. Hook and pacing (micro-drama, 03)
- **0–3 s:** a face mid-reaction with the cause withheld, a shock line, or evidence already being found. Never an establishing shot or a walk-in.
- **Rhythm:** an emotional spike by 7 s; shots of 3–6 s (10–15 shots per minute); a reversal around 0:30.
- **End on one of four cliffhanger types:** Reveal, Threat, Revelation or Decision.

## 7. Edit and finish (02, 05)
- **Run a live cut:** drop each kept take into the timeline before making the next.
- **Trim** the first few frames of each clip and the slowed last 10–15%. Chain from a frame that still has momentum.
- **Cut technique:** J/L cuts, reaction shots to cover weak lip-sync, and no cross-fades to hide mismatches.
- **Sound is the biggest single lever.** Lay room tone under every cut, foley on every visible action, and silence on purpose. Music goes in last, at no more than 30% of the voice level.
- **Finish:** one grade per scene, grain after upscaling, and any text lettered by hand.

## What this changes in our current EP01 director's cut
1. **Prompts:** rebuild the scene 3–6 prompts in the section 3 structure. That means positive locks, numeric ages, first-frame lines and a LOCATION MAP.
2. **Location set:** add a top-down map, plus the missing reverse plate for the window wall seen from the door side with people in it.
3. **Takes:** run 3–4 per scene and choose by beat. So far we have kept single successful takes.
4. **Sound and grade:** add the full sound pass and one grade per scene. Scene 2 is bluer than scene 1.
5. **Hook:** an option to test the micro-drama hook rule against our vault-wheel opening, by opening on Marcus's face mid-reaction with the clunk withheld. This is a decision for David and Antigravity.

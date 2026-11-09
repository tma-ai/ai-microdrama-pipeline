---
name: ai-story-architect
description: Story gate for AI micro-dramas, shorts and animated series made with Meta Muse. Checks and fixes the STORY before any image is made — hook in the first 3 s, want/stakes/antagonist by 0:15, humiliation→reversal→face-slap→new hook, dramatic irony, plant and payoff, "but/therefore" causality, dialogue economy, reaction beats, one-question cliffhanger, the mute test — and makes the ENVIRONMENT, props and light tell the story too (every set element must say whose world it is, what happened here and what is at stake). Distilled from research/higgsfield_2026-11-08 reports 06 (Higgsfield's own story guidance) and 07 (winning AI films, micro-drama craft, Chinese 短剧 guides). Use when the user says "is there a story", "it feels random", "no hook", "make the storytelling on point", "does the environment tell a story", "review the script", or before ai-film-director builds storyboards.
---

# AI STORY ARCHITECT

**Roles:**
- **Antigravity** writes story and dialogue.
- **David** approves.
- **Claude** runs this gate and proposes fixes:
  - **[DIRECTION]** fixes change no words, and Claude can apply them.
  - **[WRITER]** fixes change dialogue or story facts; they go to Antigravity and David as proposals.

**Run order:** this skill first, then `ai-film-director` (directing gates 2–7), then `drama-edit-sound`.

## Why AI films feel empty
The winners are simpler, not flashier: one person, one want, one place, a real ending, carried by faces. The losers are "tangentially related vignettes strung together by narration and a soundtrack" (TechCrunch on AIFF). Higgsfield: "A cinematic short that nails the technique but skips that emotional arc is a demo reel, not a film." The Higgsfield festival jury praised "a terrific premise", "a cathartic storyline" and "character expressions". [06, 07]

## THE STORY GATE: 12 tests (every one must pass before storyboards)
1. **One-line premise.** "[Hero] wants [X] from [Villain], or else [loss]." It has one person, one want and one place [07 B2].
2. **Hook, 0–3 s.** Frame 1 already holds conflict, or a face reacting to it. A stranger at 0:03 can say who is in trouble. Never a skyline, an establishing shot or a walk-in on its own [06, 07 B1].
   - **Hook types:** a face reacting before we see why; a shock line; a reveal in motion; a status reversal; an impossible situation; a hidden identity; a ticking clock; public humiliation.
3. **Want and stakes by 0:15.** The antagonist is introduced *doing harm*, not described. The injustice is personal and visible [07 B2].
4. **Episode spine:** humiliation → reversal (power or identity revealed) → face-slap (the villain is stunned) → new hook. The reversal lands around the midpoint, as a visual beat [07 B3].
5. **Dramatic irony.** In every scene the audience knows at least one thing a character doesn't (Hitchcock's bomb: show it first, then make them wait) [07 B3].
6. **Plant and payoff.** List every insert, name and prop. Each one is either a plant with a later payoff or a payoff of an earlier plant; otherwise cut it. No name or object appears for the first time when it matters [07 B6, B10].
7. **Causality.** Between every pair of beats the joining word is "BUT" or "THEREFORE", never "and then". Test: swap two scenes; if nobody would notice, the story is broken [07 B7].
8. **Escalation.** Each 10 s take raises the stakes one notch over the last and causes the next. There is an emotional spike about every 15 s [07 B7].
9. **Dialogue economy.**
   - About 8 words or fewer per sentence, at most 2 sentences per speech, about 60–90 spoken words per 60 s.
   - Use the fewest words that land the slap. Show emotion through action. Every line advances the conflict.
   - Santiago's dramatic lines are 4–5 words each [06, 07 B4].
10. **Reaction beats.** On the key word of every line, the camera is on the *listener*, or a reaction lands within 1 s. Hold 1–2 s after a reveal. Script hands, gaze and aborted speech (Kuleshov) [06, 07 B5].
11. **Mute test.** With the sound off, the turn of the story is still visible [07 B3].
12. **One-question cliffhanger** (Reveal / Threat / Revelation / Decision). The last frame poses ONE question a viewer can say aloud. Cut one beat before the answer: "if viewers feel satisfied, you cut too late" [07 B8].

## ENVIRONMENT TELLS THE STORY [USER RULE 2026-11-08 + 06]
Every element of the set, props and light must answer at least one of these. If it answers none, change it or cut it.
- **Whose world is this?** The set shows the owner's power and character: trophies, what they collected, how they rule the room.
- **What happened here, or what is about to happen?** It holds traces of the backstory: the evidence, the scar on the world.
- **What is at stake, and where is the threat?** The threat is visible before it arrives (the bomb under the table).
- **Is it physically logical?** Every object exists for a real-world reason. Water, doors and light have a believable source: a door that leaks seawater must open toward the sea, and alarms belong to real systems. Unexplained spectacle is slop.
- **Is it motivated light?** Every light source is in the world (lamps, storm, alarm beacon). Changes of light are story beats.

Write a **STORY MAP** for each set: three lines naming what the room says about the owner, the backstory and the threat. Paste it into the location sheet and every scene prompt.

## Episode 1 rules [07 B9]
- **EP01 sets up** the world, the leads, the core want and the core conflict, and lands the first emotional peak.
- **Revenge stories** establish the injustice before the payback.
- **The ending opens a bigger threat,** so episode 2 has an engine.
- **Later episodes** open with a recap hook: the last cliffhanger restated with new tension.

## Wordless slapstick (animation) [07 B11]
- **Chuck Jones rules:** the heroes' failures are their own fault; set up a rule and pay it off three times; a 1 s reaction before every fall; the partner reacts to every gag.
- **Sound:** give the villain a sound motif before he appears.

## Output of this skill
1. **STORY_GATE.md** for the episode: each of the 12 tests marked PASS or FAIL, with evidence.
2. **Fix list,** each tagged [DIRECTION] or [WRITER].
3. **STORY MAP** for every set.
4. **Beat sheet:** one line per 10 s take, joined by BUT or THEREFORE.

Hand it to ai-film-director only when all 12 tests pass or David waives one.

Sources: research/higgsfield_2026-11-08/06_storytelling_higgsfield.md and 07_story_craft_ai_films.md (full URLs and quotes).

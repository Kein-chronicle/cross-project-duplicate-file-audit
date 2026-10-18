---
name: reverse-audit-shipped
description: Audit what a pipeline has already shipped to find which quality axes its gates never measured, then turn each leak into a gate with a forgery test. Use when a factory/pipeline has produced many outputs (apps, games, articles, videos) and you suspect systemic defects, when many outputs share one bug, when store metadata/review notes are corrupted, or when you need a repeatable method for post-hoc fleet audits. Includes mechanical probes for shared byte-identical files, character-split text and near-duplicate descriptions.
---

# reverse-audit-shipped

Headline finding of one fleet audit (14 shipped apps): **every axis the gates did not measure leaked, without exception; axes with a gate mostly held.**
So the method is: go find the unmeasured axes in the real outputs, and give each a gate.

## Method

1. **Get ground truth outcomes first.** What actually happened to the outputs (store lookup: live / in review / never submitted; ratings; revenue)?
   The pipeline had promised a feedback loop in its constitution but no file held it. Create an `ACTUALS` ledger and a gate that requires it.
2. **Read all code of a sample completely** (not skim) and recompute the engines. Look for *shared* defects: byte-identical files across siblings
   (`scripts/fleet_audit.py dupes`) mean one bug x N. In the audit a rewarded-ad completion handler (a 0.5 s timer instead of the SDK callback) was md5-identical in 14/14 apps
   and the tested path was only the failure path.
3. **Read the outward surface** (store metadata, screenshots, review notes, icons) - mechanical bugs hide here: a review note whose text had been joined
   character by character (`i; P; h; o; n; e; ...`) in 8/14 apps (`charsplit`); promises like "see the attached recording" with nothing attached; locale-less currency symbols in hero shots;
   keyword fields repeating the title; sibling descriptions with 18 shared 5-grams (`overlap`).
4. **Check research quotes against the raw sources** (quote not in source; reviews from the wrong category used as a niche gap; contradictory numbers between two documents
   nobody compared; a rejected candidate revived without a reversal record; selection criterion that silently became "no competition").
5. **Audit the instruments themselves:** a hand-written `EXEMPT` as a master key; `HUMAN` verdicts skipping the automatic measurement so a gate that should
   fail 14/14 never ran; fingerprints that don't cover the rubric/rule files; rules that only check a word *exists* (an index, not enforcement).
6. **Each finding -> a gate -> a forgery test** ([`ci-gate-forgery-test`](https://github.com/Kein-chronicle/ci-gate-forgery-test)). Group by *axis*, not by app. Re-run on the fleet; expect new false positives and fix them.
7. **Don't retrofit shipped, frozen outputs unless asked** - give the new gate an explicit EXEMPT with a written reason for already-shipped items
   (see [`ci-gate-forgery-test`](https://github.com/Kein-chronicle/ci-gate-forgery-test): exemptions need reasons).

## Typical defect classes worth probing for (generic)
Success/failure path asymmetry (only the failure path tested); persistence that silently replaces corrupted data (`try? decode ?? default`); writes never called
(no delete/update call sites); schedule without cancel; sleep/clock semantics (a monotonic clock that stops during sleep); input-range traps (`Int(Double)`);
accessibility absent (zero dynamic-type, zero labels); zero unit-test targets; CJK word counting by whitespace; specs lacking empty/error/range/rounding/default cases so the implementer invents them.

```bash
python3 scripts/fleet_audit.py dupes ~/apps --min-projects 3 --ext .swift
python3 scripts/fleet_audit.py charsplit */review_notes.txt
python3 scripts/fleet_audit.py overlap a/description.txt b/description.txt --n 5
python3 tests/run.py
```

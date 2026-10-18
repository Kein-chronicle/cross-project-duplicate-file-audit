# cross-project-duplicate-file-audit

**Audit a fleet of already-shipped projects for the defects a per-project gate can't see: identical files, split-up text, copy-paste descriptions.**

[![test](https://github.com/Kein-chronicle/cross-project-duplicate-file-audit/actions/workflows/test.yml/badge.svg)](https://github.com/Kein-chronicle/cross-project-duplicate-file-audit/actions/workflows/test.yml) ![license](https://img.shields.io/badge/license-MIT-blue.svg) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen.svg)

## Why

Gates look at one project at a time. A bug that was copied into every app from one template passes each gate and can still ship in every app. Looking backwards across the fleet finds it in one pass.

## Install

**As a Claude Code skill** (Claude uses it when the task matches the skill description):

```sh
git clone https://github.com/Kein-chronicle/cross-project-duplicate-file-audit.git ~/.claude/skills/reverse-audit-shipped
```

For a single project, clone into `<project>/.claude/skills/reverse-audit-shipped` instead, then start a new Claude Code session.

**As plain scripts:**

```sh
git clone https://github.com/Kein-chronicle/cross-project-duplicate-file-audit.git
cd cross-project-duplicate-file-audit
```

**Requires:** Python 3.10+.

## Quick start

Run it on four synthetic apps:

```console
$ bash examples/demo.sh
# Four shipped apps were generated from one template. Which file is byte-identical in all of them?
$ python3 scripts/fleet_audit.py dupes .demo-tmp --min-projects 3 --ext .swift
RewardedAd.swift  md5=0788686b  identical in 4/4 projects: app1, app2, app3, app4
review each: one shared file means one shared bug (or a missing abstraction)
[exit 1]

# Review notes whose characters were split apart by a bad template (line 2):
$ python3 scripts/fleet_audit.py charsplit .demo-tmp/notes.txt
.demo-tmp/notes.txt:2: looks character-split: '2. i; P; h; o; n; e; ; S; E; 1; 5'
1 suspicious line(s)
[exit 1]
```

The output above is real: it is produced by the files in `examples/`.

## Use it on your own files

```sh
python3 scripts/fleet_audit.py dupes ~/Projects/shipped-apps --min-projects 3 --ext .swift
python3 scripts/fleet_audit.py charsplit review-notes.txt
python3 scripts/fleet_audit.py overlap description-a.txt description-b.txt
```

Sample inputs for every file format are in `examples/` and `tests/`; the details are in [SKILL.md](SKILL.md).

## What it checks

- `dupes` lists files with the same name and the same md5 across at least `--min-projects` projects (limit by extension with `--ext`).
- `charsplit` flags lines whose characters were joined with separators by a bad template.
- `overlap` compares two descriptions and flags them when more than about a quarter of their word shingles are shared.

## Limits

- Byte-identical files only; it does not find similar-but-edited code.

## Related projects

These solve neighbouring problems; use them when they fit better.

- **jscpd**: copy/paste detector inside code; this works across projects and flags exact shared files
- **fdupes**: generic duplicate-file finder

## More from the same collection

Small, tested tools that grew out of running AI agents and game/app pipelines for months:

- [**llm-verdict-gate**](https://github.com/Kein-chronicle/llm-verdict-gate): Make AI and human review gates impossible to pass by silence: machine-parsed PASS/FAIL, missing verdict = FAIL.
- [**ci-gate-forgery-test**](https://github.com/Kein-chronicle/ci-gate-forgery-test): Prove your CI gates can actually fail: feed each gate forged-bad, empty and missing input and flag the ones that stay green.
- [**stale-verdict-guard**](https://github.com/Kein-chronicle/stale-verdict-guard): Bind a pass/fail verdict to a fingerprint of the source it judged, so an edit after review makes the verdict stale.

## Development

```sh
python3 tests/run.py
```

The tests include inputs that are supposed to be rejected, so a green run also shows the checks can fail. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).

If this saved you a debugging session, a star helps other people find it. Bug reports and failing test cases are even better.

<sub>Keywords: audit, code-quality, duplicate-detection, claude-code, claude-skills, agent-skills, release-management</sub>

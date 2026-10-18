#!/usr/bin/env bash
cd "$(dirname "$0")/.."
run() { printf '$ %s\n' "$*"; "$@"; printf '[exit %s]\n\n' "$?"; }
tmp=.demo-tmp; rm -rf "$tmp"; mkdir "$tmp"; trap 'rm -rf "$tmp"' EXIT
for i in 1 2 3 4; do mkdir -p "$tmp/app$i"
  printf 'func grant() { timer(0.5) { granted = false } }\n%.0s' $(seq 12) > "$tmp/app$i/RewardedAd.swift"
  printf '// unique %s\nlet x = %s\n' "$i" "$i" > "$tmp/app$i/Unique.swift"; done
echo "# Four shipped apps were generated from one template. Which file is byte-identical in all of them?"
run python3 scripts/fleet_audit.py dupes "$tmp" --min-projects 3 --ext .swift
printf '1. Review notes\n2. i; P; h; o; n; e; ; S; E; 1; 5\n3. fine line, with; some punctuation\n' > "$tmp/notes.txt"
echo "# Review notes whose characters were split apart by a bad template (line 2):"
run python3 scripts/fleet_audit.py charsplit "$tmp/notes.txt"

# Forge 1.0.0 release checklist

Status: Local candidate; overall acceptance FAIL — V1-Q-01 runtime qualification BLOCKED.
Scope: Stable init/status/verify and isolated task create/show/run/resume/apply, per ADR 0019.
Packaging decision: wheel and sdist, local distribution; no package-index publication.
Evidence owner: [Forge 1.0 assurance record](../engineering/Forge-1.0-assurance.md).

- [x] Specification/engineering brief and independent design PASS.
- [x] Explicit stable boundary and preserved experimental findings.
- [x] Negative tests, full suite, lint/format/whitespace and memory checks.
- [ ] Real Windows agent execution, fresh read-only review and explicit apply.
- [x] Audio Recorder snapshot: locked restore, 616 tests and formatting.
- [ ] Audio Recorder actual agent maintenance/review/apply (V1-Q-01).
- [x] Wheel/sdist inspection and clean installed CLI/template smoke.
- [x] Bounded independent code review and corrected-finding re-review.
- [ ] Full independent release acceptance including live runtime.
- [x] Candidate checksum manifest, known limitations and user guide.
  See evidence-1.0.0.json and dist/candidate/SHA256SUMS.txt.
- [ ] Stable acceptance commit and clean working tree (acceptance still incomplete).
- [ ] Stable v1.0.0 tag/publication (acceptance still incomplete).

Known limits: Windows x64/CPython3.14/CLI0.160.0 qualification only; trusted operator verification
commands, explicit secret classification, no multi-file apply transaction, no autonomous FAL.
Tag recommendation after separate authorization and clean committed tree: v1.0.0.

Ready to tag v1.0.0: NO

Owner authority now permits a distinct public testing prerelease, v1.0.0-rc.1, under MIT.
See [its publication checklist](checklist-1.0.0-rc.1.md). This stable checklist remains incomplete.

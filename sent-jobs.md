# Sent Jobs Log

Deduplication memory for the daily remote job brief. One entry per role ever
shortlisted, in the form `Company — Title — URL`, grouped by the date it was
sent. Entries older than 60 days are dropped.

Note: this repo also maintains `seen.json`, used by the automated
`job_radar.py` GitHub Actions pipeline for the same purpose (keyed by a
normalized company+title hash rather than a URL). Both files track roles
already surfaced to Prabhpreet — check both before re-sending a role.

## 2026-09-27

No new roles cleared the bar today (see `latest-brief.md` for the full
rejection breakdown). Nothing to log.

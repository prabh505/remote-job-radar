# Sent jobs log

Deduplication memory for the daily remote job brief. One line per role sent, grouped by date. Entries older than 60 days are dropped. Roles rejected during scoring/filtering are not logged here (see `seen.json`, written by `job_radar.py`, for the automated pipeline's own dedup state).

## 2026-09-24

No roles sent — thin day, no genuine matches found. See session notes: RemoteOK, Remotive (software-dev/data/all-others), We Work Remotely (2 categories) and Jobspresso were checked directly via their feeds/APIs; Working Nomads returned 403 (blocked) and was skipped per instructions. The only two candidates that scored above threshold in the automated pipeline (Omega Enterprises "Junior Digital Assets Operations Analyst" — crypto ops role, not ML/AI-relevant; RedMimicry "Software Developer Security Analytics" — requires monthly in-person Berlin office) were verified by fetching the postings and rejected as false-positive keyword matches / not remote-worldwide. Wellfound, Toptal, LinkedIn and Glassdoor have no public feed; web search only surfaced aggregator/board landing pages, not individually verifiable postings, so nothing from them is logged as sent.

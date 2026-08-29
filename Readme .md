# Remote Job Radar

A daily remote-job brief that runs on GitHub Actions — free, serverless, no machine of yours needs to be on.

Every morning at **09:00 IST** it pulls postings from RemoteOK, Remotive, We Work Remotely, Jobspresso and Working Nomads, throws out everything you aren't eligible for, scores what's left against your actual skills, and opens the shortlist as a **GitHub issue** (which GitHub emails you automatically). Optional SMTP email on top.

---

## Setup — 5 steps, about 10 minutes

### 1. Create the repo

On GitHub: **New repository** → name it `remote-job-radar` → **Private** → Create.

### 2. Upload these files

Keep the folder structure exactly as-is:

```
remote-job-radar/
├── job_radar.py
├── seen.json
├── README.md
└── .github/
    └── workflows/
        └── daily.yml
```

Easiest path: on the empty repo page click **uploading an existing file**, then drag the whole folder in. GitHub preserves the `.github/workflows/` nesting.

If you'd rather use the terminal:

```bash
cd remote-job-radar
git init && git add -A && git commit -m "initial"
git branch -M main
git remote add origin https://github.com/prabh505/remote-job-radar.git
git push -u origin main
```

### 3. Let the workflow write back

**Settings → Actions → General → Workflow permissions** → select **Read and write permissions** → Save.

Without this the run works but can't save `seen.json`, so you'd see repeat postings.

### 4. Test it

**Actions** tab → **Daily Remote Job Brief** → **Run workflow**. Give it a minute, then check the **Issues** tab. You should have your first brief.

If Actions says workflows are disabled on a new repo, click the button to enable them.

### 5. (Optional) Email delivery

The GitHub issue already emails you via notifications, so this is only if you want a properly formatted mail to your inbox.

Gmail requires an **App Password** — your normal password won't work:

1. Enable 2-Step Verification on your Google account
2. Go to Google Account → Security → **App passwords** → generate one for "Mail"
3. In the repo: **Settings → Secrets and variables → Actions → New repository secret**, and add:
   - `SMTP_USER` = `prabhpreetsingh852005@gmail.com`
   - `SMTP_PASS` = the 16-character app password
   - `SMTP_TO` = `prabhpreetsingh852005@gmail.com`

Add these yourself — never paste an app password into a chat, including to me.

---

## What gets filtered out

The script is deliberately strict. It rejects a posting if:

| Rule | Why |
|---|---|
| Title contains senior / staff / lead / principal / manager / architect | Not eligible as a 2027 grad |
| Body demands 3+ years experience | Same |
| Requires US work authorization, clearance, or is US-citizens-only | You're applying from India |
| Location is region-locked away from India (`USA only`, `EMEA only`, …) | Wasted application |
| Unpaid or equity-only | Not worth your time |
| Posted more than 21 days ago | Usually already filled |
| No intern / junior / graduate / entry / contract signal anywhere | Not aimed at your level |
| Match score below 12 | Too far from your skill set |
| Already sent on a previous day | `seen.json` |

Expect thin days. A brief with three real matches beats one with twenty you can't get.

## Tuning it

Everything adjustable sits in the config block at the top of `job_radar.py`:

- `SKILL_WEIGHTS` — add a skill as you learn it, raise a weight to bias toward it
- `MIN_SCORE` — raise to 20 for fewer, sharper matches; drop to 8 if days are too empty
- `MAX_AGE_DAYS`, `MAX_RESULTS` — freshness window and shortlist size
- `TITLE_BLOCKERS` — add anything that keeps slipping through
- `tailoring_note()` — the advice attached to each match, keyed by which skills hit

Change the run time in `.github/workflows/daily.yml`. The cron is **UTC**: `30 3 * * *` is 09:00 IST. For 07:00 IST use `30 1 * * *`.

## Cost

Free. Public repos get unlimited Actions minutes; private repos get 2,000/month and this run uses well under one minute a day.

## Honest limitations

- **Wellfound, Toptal, LinkedIn and Glassdoor are not included.** They have no public feed and actively block scrapers. Keep checking those manually — Wellfound especially is worth a weekly pass for startup roles.
- **Links come straight from each board's feed and aren't individually verified.** A posting can be filled before the feed catches up.
- **Keyword matching is not comprehension.** It will occasionally surface a role that reads well but isn't right, and occasionally miss a good one described in unusual language. Skim, don't trust blindly.
- **Boards change their formats.** Each source is isolated in try/except, so one breaking won't kill the run — the brief tells you which boards didn't respond. If one stays broken for a week, it needs a fix.

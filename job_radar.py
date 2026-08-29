#!/usr/bin/env python3
"""
Remote Job Radar — daily remote-job brief for Prabhpreet Singh.

Runs on GitHub Actions. Pulls from public remote job feeds, filters out
roles he isn't eligible for, scores what's left against his actual skills,
dedupes against previous days, and writes a Markdown brief.

Every source is wrapped in try/except: if a board is down or changes its
format, the run still completes with whatever else came back.
"""

import json
import os
import re
import smtplib
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from html import unescape

# ----------------------------------------------------------------------------
# PROFILE — edit this block as your skills and eligibility change.
# ----------------------------------------------------------------------------

NAME = "Prabhpreet Singh"
LINKEDIN = "https://www.linkedin.com/in/prabhpreet-singh-749b64322/"
GITHUB = "https://github.com/prabh505"

# Skill keywords, weighted. Higher = stronger signal that a role fits.
SKILL_WEIGHTS = {
    # core AI/ML — his strongest area
    "machine learning": 10, "deep learning": 10, "pytorch": 9, "tensorflow": 9,
    "scikit-learn": 8, "sklearn": 8, "xgboost": 8, "keras": 7,
    "computer vision": 10, "opencv": 8, "nlp": 9, "natural language": 8,
    "llm": 10, "rag": 11, "retrieval-augmented": 11, "langchain": 11,
    "generative ai": 9, "genai": 9, "transformer": 8, "embeddings": 7,
    "vector database": 7, "fine-tuning": 7, "prompt engineering": 5,
    "data science": 9, "data scientist": 9, "data analyst": 7,
    "feature engineering": 7, "model deployment": 6, "mlops": 6, "kaggle": 8,
    # languages / stack
    "python": 8, "sql": 6, "c++": 4, " r ": 3, "matlab": 3,
    "next.js": 7, "nextjs": 7, "node.js": 6, "nodejs": 6, "streamlit": 6,
    "react": 4, "full stack": 5, "full-stack": 5, "backend": 4,
    "pandas": 6, "numpy": 6, "jupyter": 4, "git": 2, "vercel": 4,
    "api": 2, "rest": 2,
}

# Roles he is eligible for. A posting must hit one of these to qualify.
ELIGIBILITY_SIGNALS = [
    "intern", "internship", "entry level", "entry-level", "junior", "jr.",
    "graduate", "new grad", "student", "trainee", "apprentice", "fresher",
    "associate", "0-2 years", "0-1 year", "1-2 years", "freelance",
    "contract", "part-time", "part time",
]

# Hard blockers in the TITLE — instant reject.
TITLE_BLOCKERS = [
    "senior", "sr.", "staff", "principal", "lead ", "team lead", "tech lead",
    "head of", "director", "vp ", "vice president", "chief", "manager",
    "architect", "expert", "iii", " iv", "10+", "5+ years",
]

# Hard blockers anywhere in the posting body.
BODY_BLOCKERS = [
    "must be authorized to work in the united states",
    "us citizens only", "u.s. citizens only",
    "security clearance", "unpaid", "equity only", "no salary",
    "must reside in the united states", "green card",
]

# Experience requirements that rule him out.
EXPERIENCE_BLOCKER = re.compile(
    r"\b([3-9]|1\d)\+?\s*(?:-\s*\d+\s*)?(?:years|yrs)\b[^.]{0,30}experience",
    re.I,
)

# Location strings that exclude someone applying from India.
LOCATION_BLOCKERS = [
    "usa only", "us only", "united states only", "u.s. only",
    "north america only", "emea only", "europe only", "eu only",
    "uk only", "canada only", "australia only", "latam only",
    "americas only",
]
LOCATION_OK_HINTS = ["worldwide", "anywhere", "global", "india", "asia", "apac", "remote"]

MAX_AGE_DAYS = 21
MAX_RESULTS = 8
MIN_SCORE = 12

SEEN_FILE = "seen.json"
SEEN_RETENTION_DAYS = 60
UA = {"User-Agent": "Mozilla/5.0 (compatible; remote-job-radar/1.0)"}


# ----------------------------------------------------------------------------
# Fetch helpers
# ----------------------------------------------------------------------------

def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def strip_html(text):
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def parse_date(value):
    """Best-effort date parsing across the feed formats we touch."""
    if not value:
        return None
    if isinstance(value, (int, float)):
        try:
            return datetime.fromtimestamp(value, tz=timezone.utc)
        except (ValueError, OSError):
            return None
    value = str(value).strip()
    formats = [
        "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d", "%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(value.replace("Z", "+0000"), fmt)
            return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def job(title, company, url, description="", location="", posted=None, source=""):
    return {
        "title": (title or "").strip(),
        "company": (company or "").strip() or "Unknown",
        "url": (url or "").strip(),
        "description": strip_html(description)[:4000],
        "location": (location or "").strip(),
        "posted": posted,
        "source": source,
    }


# ----------------------------------------------------------------------------
# Sources
# ----------------------------------------------------------------------------

def source_remoteok():
    data = json.loads(fetch("https://remoteok.com/api"))
    out = []
    for item in data:
        if not isinstance(item, dict) or not item.get("position"):
            continue  # first element is a legal notice
        out.append(job(
            item.get("position"),
            item.get("company"),
            item.get("apply_url") or item.get("url"),
            (item.get("description") or "") + " " + " ".join(item.get("tags") or []),
            item.get("location"),
            parse_date(item.get("epoch") or item.get("date")),
            "RemoteOK",
        ))
    return out


def source_remotive():
    out = []
    for category in ["software-dev", "data", "all-others"]:
        try:
            url = f"https://remotive.com/api/remote-jobs?category={category}&limit=120"
            data = json.loads(fetch(url))
            for item in data.get("jobs", []):
                out.append(job(
                    item.get("title"),
                    item.get("company_name"),
                    item.get("url"),
                    (item.get("description") or "") + " " + " ".join(item.get("tags") or []),
                    item.get("candidate_required_location"),
                    parse_date(item.get("publication_date")),
                    "Remotive",
                ))
        except Exception as exc:
            print(f"  remotive/{category} failed: {exc}", file=sys.stderr)
    return out


def source_rss(url, label):
    root = ET.fromstring(fetch(url))
    out = []
    for item in root.iter("item"):
        def text(tag):
            node = item.find(tag)
            return node.text if node is not None else ""

        raw_title = text("title") or ""
        # WWR titles look like "Company: Job Title"
        if ":" in raw_title:
            company, _, title = raw_title.partition(":")
        else:
            company, title = "", raw_title
        out.append(job(
            title or raw_title,
            company,
            text("link"),
            text("description"),
            text("region") or text("{https://weworkremotely.com/}region"),
            parse_date(text("pubDate")),
            label,
        ))
    return out


def source_workingnomads():
    data = json.loads(fetch("https://www.workingnomads.com/api/exposed_jobs/"))
    out = []
    for item in data:
        out.append(job(
            item.get("title"),
            item.get("company_name"),
            item.get("url"),
            (item.get("description") or "") + " " + (item.get("tags") or ""),
            item.get("location"),
            parse_date(item.get("pub_date")),
            "Working Nomads",
        ))
    return out


SOURCES = [
    ("RemoteOK", source_remoteok),
    ("Remotive", source_remotive),
    ("We Work Remotely", lambda: source_rss(
        "https://weworkremotely.com/categories/remote-programming-jobs.rss", "We Work Remotely")),
    ("We Work Remotely (data)", lambda: source_rss(
        "https://weworkremotely.com/categories/remote-back-end-programming-jobs.rss", "We Work Remotely")),
    ("Jobspresso", lambda: source_rss(
        "https://jobspresso.co/?feed=job_feed", "Jobspresso")),
    ("Working Nomads", source_workingnomads),
]


# ----------------------------------------------------------------------------
# Filtering and scoring
# ----------------------------------------------------------------------------

def is_fresh(item):
    if not item["posted"]:
        return True  # unknown date — let scoring decide
    return item["posted"] >= datetime.now(timezone.utc) - timedelta(days=MAX_AGE_DAYS)


def is_eligible(item):
    title = item["title"].lower()
    body = (item["description"] + " " + item["title"]).lower()
    location = item["location"].lower()

    if any(b in title for b in TITLE_BLOCKERS):
        return False, "senior/lead title"
    if any(b in body for b in BODY_BLOCKERS):
        return False, "work-authorization or unpaid"
    if EXPERIENCE_BLOCKER.search(body):
        return False, "3+ years experience required"
    if any(b in location for b in LOCATION_BLOCKERS):
        return False, "region-locked away from India"
    if not any(s in body for s in ELIGIBILITY_SIGNALS):
        return False, "no junior/intern/contract signal"
    return True, ""


def score(item):
    body = (item["title"] + " " + item["description"]).lower()
    title = item["title"].lower()
    total = 0
    matched = []
    for keyword, weight in SKILL_WEIGHTS.items():
        if keyword in body:
            hit = weight * 2 if keyword in title else weight
            total += hit
            matched.append(keyword)
    # bonus for India/worldwide-friendly locations
    if any(h in item["location"].lower() for h in ["worldwide", "anywhere", "india", "global", "asia"]):
        total += 8
    # bonus for explicit intern/junior in the title
    if any(s in title for s in ["intern", "junior", "graduate", "entry"]):
        total += 10
    return total, sorted(set(matched), key=lambda k: -SKILL_WEIGHTS[k])[:6]


def tailoring_note(matched):
    m = set(matched)
    if m & {"rag", "langchain", "llm", "retrieval-augmented", "generative ai", "genai", "embeddings"}:
        return ("Lead with the CoDSAI RAG pipeline — custom chunking, vector semantic search, "
                "Groq/LLaMA inference at ~2s. Name the latency number; it's concrete.")
    if m & {"computer vision", "opencv", "transformer"}:
        return ("Lead with TrueVision — benchmarked 10 models including ViT-B16 and ResNet50, "
                "shipped a transformer ensemble. Mention SMOTE for the class-imbalance work.")
    if m & {"machine learning", "deep learning", "pytorch", "tensorflow", "xgboost", "kaggle", "data science"}:
        return ("Lead with the Kaggle record — Notebooks Expert (top 2.5%), 4th of 371 teams on SPR 2026, "
                "12th of 4,540 on WiDS. Competition placings beat listing frameworks.")
    if m & {"sql", "data analyst", "pandas"}:
        return ("Lead with the SQL Q&A Chain project — natural language to executable SQL with "
                "read-only guardrails. It shows judgment, not just querying.")
    if m & {"next.js", "nextjs", "node.js", "nodejs", "full stack", "full-stack", "react", "backend"}:
        return ("Lead with the CoDSAI learning portal — Next.js and Node.js, built and deployed "
                "end-to-end on Vercel with course management and certificate generation.")
    return ("Open with Amazon ML Summer School 2026 selection (top 3,000 of 130,000+) — it is the "
            "fastest credential to establish you clear a high screening bar.")


# ----------------------------------------------------------------------------
# Dedupe
# ----------------------------------------------------------------------------

def load_seen():
    if not os.path.exists(SEEN_FILE):
        return {}
    try:
        with open(SEEN_FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_seen(seen):
    cutoff = (datetime.now(timezone.utc) - timedelta(days=SEEN_RETENTION_DAYS)).strftime("%Y-%m-%d")
    pruned = {k: v for k, v in seen.items() if v >= cutoff}
    with open(SEEN_FILE, "w") as f:
        json.dump(pruned, f, indent=1, sort_keys=True)


def key_for(item):
    return re.sub(r"[^a-z0-9]", "", (item["company"] + item["title"]).lower())[:80]


# ----------------------------------------------------------------------------
# Rendering and delivery
# ----------------------------------------------------------------------------

def render(picks, stats, today):
    lines = [
        f"# Remote job brief — {today}",
        "",
        f"**{len(picks)}** new match{'' if len(picks) == 1 else 'es'} "
        f"from {stats['fetched']} postings across {stats['sources_ok']} boards. "
        f"[LinkedIn]({LINKEDIN}) · [GitHub]({GITHUB})",
        "",
    ]

    if not picks:
        lines += [
            "Nothing cleared the bar today. That is a real result, not a failure — "
            "the filters reject senior roles, US-authorization-only postings, and anything "
            "older than three weeks. Thin days happen, especially over weekends.",
            "",
        ]
    else:
        for i, p in enumerate(picks, 1):
            age = "date unknown"
            if p["posted"]:
                days = (datetime.now(timezone.utc) - p["posted"]).days
                age = "today" if days == 0 else f"{days}d ago"
            lines += [
                f"### {i}. [{p['title']}]({p['url']}) — {p['company']}",
                "",
                f"`{p['source']}` · posted {age} · {p['location'] or 'location unspecified'} · "
                f"match score {p['score']}",
                "",
                f"**Why it fits:** matches on {', '.join(p['matched'][:5]) or 'general profile overlap'}.",
                "",
                f"**Tailoring note:** {p['note']}",
                "",
            ]

    if stats["failed"]:
        lines += [f"> Boards that did not respond this run: {', '.join(stats['failed'])}.", ""]

    lines += [
        "---",
        "",
        "*Auto-generated by remote-job-radar. Links are taken verbatim from each board's "
        "public feed and are not individually verified — check the posting before applying.*",
    ]
    return "\n".join(lines)


def create_issue(title, body):
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not (token and repo):
        print("No GITHUB_TOKEN/GITHUB_REPOSITORY — skipping issue.", file=sys.stderr)
        return
    payload = json.dumps({"title": title, "body": body, "labels": ["job-brief"]}).encode()
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/issues",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "remote-job-radar",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"Issue created: {json.loads(r.read())['html_url']}")
    except urllib.error.HTTPError as exc:
        print(f"Issue creation failed: {exc.code} {exc.read()[:300]}", file=sys.stderr)


def send_email(subject, body):
    user = os.environ.get("SMTP_USER")
    password = os.environ.get("SMTP_PASS")
    to = os.environ.get("SMTP_TO") or user
    if not (user and password):
        print("No SMTP secrets — skipping email.", file=sys.stderr)
        return
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = to
    try:
        with smtplib.SMTP_SSL(os.environ.get("SMTP_HOST", "smtp.gmail.com"),
                              int(os.environ.get("SMTP_PORT", "465")), timeout=30) as s:
            s.login(user, password)
            s.send_message(msg)
        print(f"Email sent to {to}")
    except Exception as exc:
        print(f"Email failed: {exc}", file=sys.stderr)


# ----------------------------------------------------------------------------

def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    all_jobs, failed, sources_ok = [], [], 0

    for label, fn in SOURCES:
        try:
            got = fn()
            all_jobs.extend(got)
            sources_ok += 1
            print(f"{label}: {len(got)} postings")
        except Exception as exc:
            failed.append(label)
            print(f"{label}: FAILED — {exc}", file=sys.stderr)

    if sources_ok == 0:
        print("Every source failed. Aborting without posting.", file=sys.stderr)
        sys.exit(1)

    seen = load_seen()
    candidates, rejected = [], {}

    for item in all_jobs:
        if not item["url"] or not item["title"]:
            continue
        if key_for(item) in seen:
            continue
        if not is_fresh(item):
            continue
        ok, reason = is_eligible(item)
        if not ok:
            rejected[reason] = rejected.get(reason, 0) + 1
            continue
        pts, matched = score(item)
        if pts < MIN_SCORE:
            continue
        item.update(score=pts, matched=matched, note=tailoring_note(matched))
        candidates.append(item)

    # dedupe by company+title, keep highest score
    best = {}
    for c in candidates:
        k = key_for(c)
        if k not in best or c["score"] > best[k]["score"]:
            best[k] = c

    picks = sorted(best.values(), key=lambda c: -c["score"])[:MAX_RESULTS]

    stats = {"fetched": len(all_jobs), "sources_ok": sources_ok, "failed": failed}
    body = render(picks, stats, today)

    print("\n" + "=" * 70 + "\n" + body + "\n" + "=" * 70)
    print(f"\nRejection reasons: {rejected}", file=sys.stderr)

    with open("latest-brief.md", "w") as f:
        f.write(body)

    for p in picks:
        seen[key_for(p)] = today
    save_seen(seen)

    subject = f"Remote job brief — {today} ({len(picks)} match{'' if len(picks) == 1 else 'es'})"
    create_issue(subject, body)
    send_email(subject, body)


if __name__ == "__main__":
    main()

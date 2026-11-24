# Remote job brief — 2026-11-24

**Thin day: 1 genuine match.** I screened ~250 postings from RemoteOK, Remotive, We Work Remotely, Jobspresso, NoDesk and Wellfound. Almost every "Anywhere in the World" listing turned out to be US-only, Poland/EU-only, or asking for 4+ years.

### 1. [Research Engineer, Privacy and Anonymization — Pragmatike (recruiting for a YC-backed AI training-data company)](https://remoteok.com/remote-jobs/remote-research-engineer-privacy-and-anonymization-pragmatike-1137792)
- **Source:** RemoteOK, posted 12 Nov 2026 (12 days ago). Link checked: HTTP 200.
- **Location terms:** offices in San Francisco and Singapore. The posting says "remote candidates are welcome if their working hours can overlap about 70–80% with either San Francisco (US Pacific) or Singapore business hours." Singapore is IST +2:30, so SG 9:00–18:00 = **06:30–15:30 IST**. That's easy to cover from Patiala; pick the SG option, not US Pacific.
- **Level:** full-time, start ASAP. The posting states "technical aptitude and learning potential matter more than years of experience" and has no minimum years. This is a stretch: they likely want a full-time hire, so be upfront that you're a 2027 graduate and ask about a contract or internship arrangement.
- **Why it fits:** the job is benchmarking detectors (rules, classifiers, LLM-based) on precision and recall, then building production data pipelines. That matches how you benchmarked 10 models and used SMOTE for rare fraud classes in TrueVision, and the read-only guardrails you built into SQL Q&A Chain.
- **Tailoring note:** open with TrueVision. "Benchmarked 10 models (ViT-B16, ResNet50, XGBoost) and used SMOTE to lift recall on rare fraud categories" maps directly onto "detecting rare or sensitive content". Then name the 4th/371 SPR 2026 mammography placing as proof you can handle sensitive medical data and NLP.

### Near-misses (not counted, not added to sent list)
- [Junior Data Scientist — Veloxio Technologies](https://wellfound.com/jobs/4881191-junior-data-scientist) (Wellfound, "Remote only • Everywhere", $60k–$75k, 1 yr). Posted ~1 month ago, so it's over the 21-day limit. Still worth a 5-minute application if it's open.
- MiPrep AI's Back End Developer Intern and AI Engineer (Wellfound, "Everywhere", $40k–$60k) are about 4 weeks old, also over the limit.

### Today's read
Global junior and intern ML postings have almost disappeared from the public feeds. The "worldwide" labels on WWR are mostly mislabeled US/EU roles, and the strongest leads came from recruiter-posted applied-AI and data-pipeline roles with Singapore/APAC overlap.
Skills that keep appearing that you lack: dbt/Snowflake/Airflow on the data side, and agent evaluation (Terminal-Bench-style task design) on the AI side. A small dbt+Airflow project on GitHub would open up the data-engineering contract roles.

*Board notes: Remotive's public API returns only 15 jobs and ignores category/search parameters. Working Nomads, Remote.co, SkipTheDrive, Toptal, LinkedIn, Glassdoor, Workable and Greenhouse/Lever/Ashby are not reachable from this environment. JustRemote and Pangian render no listings without JavaScript. Pages for WWR job postings return 403, so WWR roles were checked from its RSS feed.*

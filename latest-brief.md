# Remote job brief — 2026-11-21

**A thin day: 3 roles, and only #1 is a strong fit.** About 400 live postings checked across RemoteOK, Remotive, We Work Remotely, Jobspresso and NoDesk, plus web searches. Most were rejected for seniority (3–5+ years), US/EU/LATAM-only eligibility, or being expired.

---

### 1. A.I. Engineering Intern — Sezzle
**Apply:** https://weworkremotely.com/remote-jobs/sezzle-a-i-engineering-intern-remote *(taken from the WWR feed; WWR blocks automated checks with a 403, so I couldn't confirm the page loads)*
- **Board / age:** We Work Remotely, posted 2026-11-20 (1 day old)
- **Location terms:** Sezzle is a US fintech; this posting's header says "Headquarters: Türkiye, Remote", and WWR lists the region as "Anywhere in the World". It is an independent-contractor role at **USD 1,000/month gross**, full-time. The posting doesn't name a required country, but the Türkiye header suggests they may prefer candidates there. Apply anyway, and ask early whether India-based contractors are accepted. No timezone is stated.
- **Why it fits:** They want SQL plus Python, building AI systems "from the ground up", generating training data, and hands-on use of Claude or similar LLMs. Your SQL Q&A Chain (LangChain + Groq, with read-only guardrails) covers almost exactly that stack.
- **Tailoring note:** Open with the SQL Q&A Chain and its read-only guardrails, then the RAG portal's ~2s response time. Practise for the Wonderlic test and the 30-minute SQL/Python screen.

### 2. Research Engineer, Privacy & Anonymization — Pragmatike (recruiting for a YC-backed AI training-data company)
**Apply:** https://remoteok.com/remote-jobs/remote-research-engineer-privacy-and-anonymization-pragmatike-1137792 *(page loads, HTTP 200)*
- **Board / age:** RemoteOK, posted 2026-11-12 (9 days old)
- **Location terms:** Offices in SF and Singapore, "or remote (Singapore or US Pacific time zones)". Remote hours must overlap "about 70–80%" with one of those. Singapore business hours (9:00–18:00 SGT) are **6:30–15:30 IST**, which is easy to cover.
- **Why it fits:** It's a stretch, but they say "technical aptitude and learning potential matter more than years of experience." The work is NER and classifiers for spotting sensitive content, benchmarked on recall and precision. That's close to TrueVision, where you benchmarked 10 models and used SMOTE to catch the rare fraud class.
- **Caution:** It's a full-time role "starting ASAP", which clashes with your 2027 degree. Only worth it if they'll take part-time or contract hours.
- **Tailoring note:** Lead with TrueVision framed as rare-class detection (10-model benchmark, SMOTE, recall on the fraud category), then the 4th/371 Kaggle mammography-report classification finish as text-classification evidence. Include the keyword **CONFIDENT** as the posting asks.

### 3. AI Content Reviewer, Video Annotation — iMerit *(backup paid gig, low fit)*
**Apply:** https://remoteok.com/remote-jobs/remote-ai-content-reviewer-video-annotation-imerit-1137686 *(page loads, HTTP 200)*
- **Board / age:** RemoteOK, posted 2026-11-04 (17 days old)
- **Location terms:** iMerit has US and India operations. The posting says "100% Remote | Independent Contractor", "work remotely from your location", with no country restriction. Pay is "35–40 USD/hour, depending on your country", so expect less for India. No timezone requirement.
- **Why it fits:** No experience is needed and you can do it alongside classes. Your OpenCV and computer-vision work makes the certification test easy. It's flexible income, not career-building.
- **Tailoring note:** Mention TrueVision's image-quality checks (blurred, mismatched or irrelevant images) as evidence of careful visual review. Include the keyword **BENEVOLENT**.

---

**Today's read:** Postings marked "worldwide" usually turn out to be country-locked once you read them: Loka's ML intern is Colombia-only, and iMerit's evaluator role is limited to six countries. Most worldwide ML roles also require 3–5+ years, so intern and contract roles from data/AI-training companies (iMerit, Toptal task design, Pragmatike's client) are the most realistic way in right now.
Skill gap that keeps showing up: **dbt, GCP/BigQuery and Snowflake** for data roles, and **evals and benchmark/task design** for AI roles. A small public eval harness on GitHub would help you on both fronts.

*Not reachable from this session (blocked by network policy, not checked): arc.dev, hnhiring.com, news.ycombinator.com, himalayas.app, remotejobs.org, workingnomads.com (direct). Remotive's public API only returns its 16 newest jobs, and most search-engine results for Remotive and Wellfound were expired postings (410 Gone).*

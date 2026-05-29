---
type: community
cohesion: 0.22
members: 13
---

# PhishingDetector / .analyze_email() / .analyze_url()

**Cohesion:** 0.22 - loosely connected
**Members:** 13 nodes

## Members
- [[.__init__()_43]] - code - loki/features/phishing_detector.py
- [[._heuristic_url()]] - code - loki/features/phishing_detector.py
- [[._llm()_4]] - code - loki/features/phishing_detector.py
- [[.analyze_email()]] - code - loki/features/phishing_detector.py
- [[.analyze_media_file()]] - code - loki/features/phishing_detector.py
- [[.analyze_url()]] - code - loki/features/phishing_detector.py
- [[Analyze a URL for phishing indicators.]] - rationale - loki/features/phishing_detector.py
- [[Analyze email content for phishing patterns.]] - rationale - loki/features/phishing_detector.py
- [[Deepfake  AI-generated media heuristic detection.         Checks file metadata,]] - rationale - loki/features/phishing_detector.py
- [[PhishingDetector]] - code - loki/features/phishing_detector.py
- [[PhishingDetector — heuristic + LLM analysis of URLs and email text for phishing]] - rationale - loki/features/phishing_detector.py
- [[Score a URL on phishing heuristics.]] - rationale - loki/features/phishing_detector.py
- [[phishing_detector.py]] - code - loki/features/phishing_detector.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/PhishingDetector_/_analyze_email_/_analyze_url
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_LokiApplication  .__init__()  main.py]]
- 1 edge to [[_COMMUNITY_._init_all()  DailyBriefing  .generate()]]
- 1 edge to [[_COMMUNITY_LokiBrain  test_brain.py  .ask()]]

## Top bridge nodes
- [[PhishingDetector]] - degree 10, connects to 3 communities
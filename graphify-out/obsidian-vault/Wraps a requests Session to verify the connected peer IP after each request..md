---
source_file: "loki/features/web_summarizer.py"
type: "rationale"
community: "WebSummarizer / TestSSRFProtection / _is_ssrf_risk()"
location: "L65"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/WebSummarizer_/_TestSSRFProtection_/__is_ssrf_risk
---

# Wraps a requests Session to verify the connected peer IP after each request.

## Connections
- [[_SSRFBlockingAdapter]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/WebSummarizer_/_TestSSRFProtection_/__is_ssrf_risk
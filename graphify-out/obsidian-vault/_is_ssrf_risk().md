---
source_file: "loki/features/web_summarizer.py"
type: "code"
community: "WebSummarizer / TestSSRFProtection / _is_ssrf_risk()"
location: "L41"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/WebSummarizer_/_TestSSRFProtection_/__is_ssrf_risk
---

# _is_ssrf_risk()

## Connections
- [[.summarize()]] - `calls` [EXTRACTED]
- [[.test_file_scheme_blocked()]] - `calls` [INFERRED]
- [[.test_localhost_blocked()]] - `calls` [INFERRED]
- [[.test_private_ipv4_blocked()]] - `calls` [INFERRED]
- [[.test_public_ip_allowed()]] - `calls` [INFERRED]
- [[Return True if the URL points to a privateinternal address (SSRF risk).]] - `rationale_for` [EXTRACTED]
- [[_ip_is_internal()]] - `calls` [EXTRACTED]
- [[web_summarizer.py]] - `contains` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/WebSummarizer_/_TestSSRFProtection_/__is_ssrf_risk
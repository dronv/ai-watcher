# scanners -> adapters -> normalizers-> analyzers-> builders ->llm
# SCANNER
    # Parse reuqirements.txt / package.json
# ADAPTERS
    # fetch raw data (PyPi, npm, OSV)
# NORMALIZERS
    # unfiy format (critical for llm)
# ANALYZERS
    # version gaps
    # bad versions
    # vulnerabilities
# BUILDER
    # construct structured LLM prompt context
# LLM (risk_agent)
    # reasong + scoring

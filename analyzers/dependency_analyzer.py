from utils.version_utils import (
    is_outdated,
    get_all_versions,
    get_latest_version,
    get_version_gap,
    gap_version_scoring,
    is_vulnerable
)

def analyze_dependency(dep, package_data, vulnerabilities):
    ecosystem = "python" | "npm"
    print("**** ANALYZE DEPENDENCY ****")

    name = dep.get("name")
    version_spec = dep.get("version_spec")
    resolved_version = dep.get("resolved_version")

    releases = package_data.get("releases", {})
    all_versions = get_all_versions(releases)
    latest_version = get_latest_version(all_versions)

    version_trustworthy = True

    matched_vulns = []
    unknown_vulns = []
    reasons = []
    is_critical = False

    # CASE 1: NO RESOLVED VERSION
    if not resolved_version:
        print("NO RESOLVED VERSION FOUND")

        for vuln in vulnerabilities:
            if vuln.package_name != name:
                continue

            if vuln.bad_versions and version_spec in vuln.bad_versions:
                matched_vulns.append(vuln)
                is_critical = True
                continue

            result = is_vulnerable(version_spec, vuln.affected_versions)

            if result is True:
                matched_vulns.append(vuln)
            elif result == "UNKNOWN":
                unknown_vulns.append(vuln)

        risk_level = "CRITICAL" if is_critical else "MEDIUM"

        return {
            "name": name,
            "version_spec": version_spec,
            "resolved_version": None,
            "latest_version": latest_version,
            "version_source": "spec",

            "is_outdated": None,
            "version_gap": None,
            "gap_risk": "UNKNOWN",

            "is_vulnerable": len(matched_vulns) > 0,
            "matched_vulnerabilities": matched_vulns,

            "risk_level": risk_level,
            "reasons": ["Resolved version not found — analysis unreliable"],
            "version_trustworthy": False
        }

    # CASE 2: NO LATEST VERSION
    if not latest_version:
        print("NO LATEST VERSION FOUND")

        for vuln in vulnerabilities:
            if vuln.package_name != name:
                continue

            if vuln.bad_versions and resolved_version in vuln.bad_versions:
                matched_vulns.append(vuln)
                is_critical = True
                continue

            result = is_vulnerable(resolved_version, vuln.affected_versions)

            if result is True:
                matched_vulns.append(vuln)
            elif result == "UNKNOWN":
                unknown_vulns.append(vuln)

        risk_level = "CRITICAL" if is_critical else "MEDIUM"

        return {
            "name": name,
            "version_spec": version_spec,
            "resolved_version": resolved_version,
            "latest_version": None,
            "version_source": "resolved",

            "is_outdated": None,
            "version_gap": None,
            "gap_risk": "UNKNOWN",

            "is_vulnerable": len(matched_vulns) > 0,
            "matched_vulnerabilities": matched_vulns,

            "risk_level": risk_level,
            "reasons": ["Latest version not found — analysis unreliable"],
            "version_trustworthy": False
        }

    # NORMAL FLOW
    print("CHECKING IF VERSION OUTDATED")
    outdated = is_outdated(resolved_version, latest_version)

    print("CHECKING VERSION GAP")
    gap = get_version_gap(resolved_version, latest_version)

    if gap < 0:
        print("MISMATCH: resolved > latest")
        version_trustworthy = False
        reasons.append("Installed version higher than latest — possible data inconsistency.")
        gap_risk = "UNKNOWN"
    else:
        gap_risk = gap_version_scoring(gap)

    # VULNERABILITY MATCHING
    for vuln in vulnerabilities:
        if vuln.package_name != name:
            continue

        if vuln.bad_versions and resolved_version in vuln.bad_versions:
            matched_vulns.append(vuln)
            is_critical = True
            continue

        result = is_vulnerable(resolved_version, vuln.affected_versions)

        if result is True:
            matched_vulns.append(vuln)
        elif result == "UNKNOWN":
            unknown_vulns.append(vuln)

    # RISK LOGIC
 
    if is_critical:
        risk_level = "CRITICAL"
        reasons.append("Known malicious version installed")

    elif matched_vulns:
        risk_level = "HIGH"
        reasons.append("Known vulnerabilities detected")

    elif unknown_vulns:
        risk_level = "MEDIUM"
        reasons.append("Vulnerability match uncertain")

    else:
        risk_level = "LOW"

    # OUTDATED LOGIC
    if gap_risk == "HIGH" and risk_level != "CRITICAL":
        risk_level = "HIGH"
        reasons.append("Significantly outdated")

    elif gap_risk == "MEDIUM" and risk_level not in ["HIGH", "CRITICAL"]:
        risk_level = "MEDIUM"
        reasons.append("Moderately outdated")

    # FINAL RETURN
    return {
        "name": name,
        "version_spec": version_spec,
        "resolved_version": resolved_version,
        "latest_version": latest_version,
        "version_source": "resolved",

        "is_outdated": outdated,
        "version_gap": gap,
        "gap_risk": gap_risk,

        "is_vulnerable": len(matched_vulns) > 0,
        "matched_vulnerabilities": matched_vulns,

        "risk_level": risk_level,
        "reasons": reasons,
        "version_trustworthy": version_trustworthy
    }
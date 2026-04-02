from utils.version_utils import is_outdated, get_all_versions, get_latest_version, get_version_gap, gap_version_scoring, is_vulnerable

def analyze_dependency(dep, package_data, vulnerabilities):
    """
    dep: {name, installed_version}
    package_data: {versions:[...]}
    vulnerabilities: normalized vulnerability list
    """
    name = dep.get("name")
    releases = package_data.get("releases", [])
    installed_version = dep.get("installed_version")
    
    all_versions = get_all_versions(releases)
    latest_version = get_latest_version(all_versions)
    

    if not installed_version or not latest_version:
        return{
            "name": name,
            "installed_version" : installed_version,
            "latest_version"  : latest_version,

            "is_outdated": False,
            "version_gap" : None,
            "gap_risk" : "UNKNOWN",

            "is_vulnerable" : False,
            "matched_vulnerabilities" : [],

            "risk_level" : "LOW",
            "reasons" : ["MISSING VERSION INFORMATION"]
        }
    
    outdated = is_outdated(installed_version, latest_version)
    gap = get_version_gap(installed_version, latest_version)
    gap_risk = gap_version_scoring(gap)

    matched_vulns = []
    unknown_vulns = []
    reasons = []
    risk_level = "LOW"
    
    for vuln in vulnerabilities:
        if vuln.package_name != name:
            continue
        
        if vuln.bad_versions and installed_version in vuln.bad_versions:
            matched_vulns.append(vuln)
            reasons.append("Installed version is a known malicious release")
            risk_level = "CRITICAL"
            continue

        ranges = vuln.affected_versions
        result = is_vulnerable(installed_version, ranges)

        if result == True:
            matched_vulns.append(vuln)
        elif result == "UNKNOWN":
            unknown_vulns.append(vuln)

    if matched_vulns:
        risk_level = "HIGH"
        reasons.append("Known vulnerabilities detected")
    elif unknown_vulns:
        risk_level = "MEDIUM"
        reasons.append("Vulnerabilities exist but version match unknown")

    if gap_risk == "HIGH":
        risk_level = "HIGH"
        reasons.append("Version is significantly outdated")
    
    elif gap_risk == "MEDIUM" and risk_level != "HIGH":
        risk_level = "MEDIUM"
        reasons.append("Version is moderately outdated")
    
    elif outdated and not matched_vulns:
        reasons.append("Package is outdated but no known vulnerabilities")

    return { 
        "name": name,
        "installed_version" : installed_version,
        "latest_version"  : latest_version,

        "is_outdated": outdated,
        "version_gap" : gap,
        "gap_risk" : gap_risk,

        "is_vulnerable" : len(matched_vulns) > 0,
        "matched_vulnerabilities" : matched_vulns,

        "risk_level" : risk_level,
        "reasons" : reasons
    }
from packaging.version import parse

from parser.packages_parser import parse_requirements
from utils.version_utils import get_release_gap_py, gap_version_scoring_py
from services.pypi_service import fetch_pypi_data
from services.vulnerabilities import fetch_osv_vulnerabilities

# ----------------- Parse requirements ----------------------
deps = parse_requirements("requirements.txt")

for dep in deps:
    data = fetch_pypi_data(dep.get("name"))
    dep.update(data)


# ----------------- Risk Scoring ----------------------
total_score = 0

for dep in deps:
    if "error" in dep:
        dep["risk"] = "UNKNOWN"
        dep["score"] = 0
        continue

    if not dep.get("installed_version"):
        dep["risk"] = "UNKNOWN"
        dep["score"] = 0
        continue

    if not dep.get("all_releases"):
        dep["risk"] = "UNKNOWN"
        dep["score"] = 0
        continue

    try:
        installed_version = parse(dep["installed_version"])
        latest_version = parse(dep["latest_version"])
        all_releases = dep["all_releases"]
        sorted_all_releases = sorted(all_releases, key=parse)

        version_gap = get_release_gap_py(dep["installed_version"], sorted_all_releases)
        version_gap_weight = gap_version_scoring_py(installed_version, latest_version)

    except Exception as e:
        dep["risk"] = "UNKNOWN"
        dep["score"] = 0
        dep["error"] = str(e)
        continue

    # ----------------- Risk Logic ----------------------
    if latest_version > installed_version:

        if version_gap_weight >= 6 or version_gap > 20:
            risk = "CRITICAL"
            score = 30

        elif version_gap_weight >= 3 or version_gap > 10:
            risk = "MEDIUM"
            score = 20

        elif version_gap > 0:
            risk = "LOW"
            score = 10

        else:
            risk = "LOW"
            score = 5  # fallback safety

    else:
        risk = "SAFE"
        score = 0

    dep["risk"] = risk
    dep["score"] = score

    total_score += score

    print(f"""
Package: {dep["name"]}
Risk: {risk}
Version Gap: {version_gap}
Score: {score}
""")

    osv = fetch_osv_vulnerabilities("litellm", "1.82.8")
    print(osv)
print(f"\nTotal Project Risk Score: {total_score}")
import requests

def fetch_osv_vulnerabilities(package, ecosystem="PyPI"):
    url = "https://api.osv.dev/v1/query"
    payload = {
        "package": {"name":package, "ecosystem": ecosystem}
    }
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("vulns", [])
    except Exception as e:
        print(f"OSV error: {e}")
        return []
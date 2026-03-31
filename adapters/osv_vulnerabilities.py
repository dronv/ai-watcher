import requests

def fetch_osv_vulnerabilities(package, version):
    url = "https://api.osv.dev/v1/query"
    payload = {
        "package": {"name":package, "ecosystem":"PyPI"},
        "version": version
    }

    res = requests.post(url, json=payload)
    return res.json()
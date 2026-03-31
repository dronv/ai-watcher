import requests

def fetch_pypi_data(package_name):
    url= f"https://pypi.org/pypi/{package_name}/json"
    try:
        response = requests.get(url, timeout=5)
  
        if response.status_code == 200:
            res = response.json()
            name = res["info"]["name"]
            latest_version = res["info"]["version"]
            all_releases = list(res["releases"].keys())
            release_count = len(res["releases"])

            data = {
                "name" : name,
                "latest_version": latest_version,
                "release_count" : release_count,
                "all_releases" : all_releases
            }
            return data
        else:
            return {"error":"NOT_FOUND", "package":package_name}
    except requests.exceptions.RequestException as e:
        return {"error":str(e), "package":package_name}
    

def get_all_pypi_versions(package_name):
    url= f"https://pypi.org/pypi/{package_name}/json"
    try:
        response = requests.get(url, timeout=5)
  
        if response.status_code == 200:
            res = response.json()
            all_releases = list(res["releases"].keys())
            release_count = len(res["releases"])
            data = {
                "release_count" : release_count,
                "all_releases" : all_releases
            }
            return data
        else:
            return {"error":"NOT_FOUND", "package":package_name}
    except requests.exceptions.RequestException as e:
        return {"error":str(e), "package":package_name}
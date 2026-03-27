
import requests

def parse_requirements(file_path):
    dependencies = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if "==" in line:
                name, version = line.split("==", 1)
                dependencies.append({"name": name.strip(), "installed_version": version.strip()})
            elif ">=" in line:
                name, version = line.split(">=", 1)
                dependencies.append({"name": name.strip(), "installed_version": version.strip()})
            elif "<=" in line:
                name, version = line.split("<=", 1)
                dependencies.append({"name": name.strip(), "installed_version": version.strip()})
            elif "~=" in line:
                name, version = line.split("~=", 1)
                dependencies.append({"name": name.strip(), "installed_version": version.strip()})
            elif "!=" in line:
                name, version = line.split("!=", 1)
                dependencies.append({"name": name.strip(), "installed_version": version.strip()})
            else:
                dependencies.append({"name":line.strip(), "installed_version":None})
    return dependencies

deps = parse_requirements("requirements.txt")

print('Before', deps)

def fetch_pypi_data(package_name):
    url= f"https://pypi.org/pypi/{package_name}/json"
    try:
        response = requests.get(url, timeout=5)
  
        if response.status_code == 200:
            res = response.json()
            name = res["info"]["name"]
            latest_version = res["info"]["version"]
            release_count = len(res["releases"])

            data = {
                "name" : name,
                "latest_version": latest_version,
                "release_count" : release_count
            }
            return data
        else:
            return {"error":"NOT_FOUND", "package":package_name}
    except requests.exceptions.RequestException as e:
        return {"error":str(e), "package":package_name}

for dep in deps:
    data = fetch_pypi_data(dep.get("name"))
    dep.update(data)

print('\nAfter', deps)


def risk_score(package):
    score = 0

    name = package.get("name") or ""
    installed_version = package.get("installed_version")
    latest_version = package.get("latest_version")
    release_count = package.get("release_count")
    error = package.get("error")

    if isinstance(name, str):
        name_lower = name.lower()
    else:
        name_lower = ""
    
    if error == "NOT_FOUND":
        score += 50

    if installed_version is None:
        score += 20
        
    if installed_version != latest_version:
        score += 20

    if release_count is None:
        score += 50

    elif isinstance(release_count, int) and release_count < 5:
        score += 40
    

    if "test" in name_lower:
        score += 15

    score = min(score, 100)
    if score > 80:
        risk = "HIGH"
    elif score > 50:
        risk = "MEDIUM"
    elif score > 20:
        risk = "LOW"
    else:
        risk = "SAFE"
    return {
        "score": score,
        "risk" : risk
    }

for dep in deps:
    score = risk_score(dep)
    print(score)
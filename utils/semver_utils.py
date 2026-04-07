import json
import os

def scan_npm_project(project_path):
    lock_path = os.path.join(project_path, "package-lock.json")
    package_path = os.path.join(project_path, "package.json")

    if os.path.exists(lock_path):
        return _parse_package_lock(lock_path)
    
    elif os.path.exists(package_path):
        return _parse_package_json(package_path)
    
    else: 
        raise FileNotFoundError("No package.json or package-lock.json found")
    
def _parse_package_lock(lock_path):
    with open(lock_path, 'r', encoding="utf-8") as f:
        data = json.load(f)

        dependencies = []

        # npm v7 +
        if "packages" in data:
            for path, info in data["packages"].items():
                if not info or "version" not in info:
                    continue
                name = _extract_name_from_path(path)

                if name:
                    dependencies.append({
                        "name": name,
                        "installed_version": info["version"],
                        "path": path,
                        "ecosystem": "npm"
                    })
        
        #npm v6 fallback
        elif "dependencies" in data:
            _recursive_parse_v6(data["dependencies"], dependencies)

            return dependencies

def _recursive_parse_v6(deps, result, parent_path="node_modules"):
    for name, info in deps.items():
        if not isinstance(info, dict):
            continue

        path = f"{parent_path}/{name}"

        if "version" in info:
            result.append({
                "name": name,
                "installed_version": info["version"],
                "path": path,
                "ecosystem": "npm"
            })
        
        if "dependencies" in info:
            _recursive_parse_v6(info["dependencies"], result, path)

def _extract_name_from_path(path):
    """
    node_modules/lodash -> lodash
    node_modules/@tpyes/node -> @types/node
    """
    if not path.startswith("node_modules"):
        return None
    
    parts = path.split("node_modules/")[-1].split("/")

    if parts[0].startswith('@') and len(parts) > 1:
        return f"{parts[0]/parts[1]}"
    
    return parts[0]

# FALL Back (package.json)

def _parse_package_json(package_path):
    with open(package_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    dependencies = []

    for dep_type in ["dependencies", "devDependencies"]:
        for name, version in data.get(dep_type, {}).items():
            dependencies.append({
                "name": name,
                "installed_version": version,   #range, not exact
                "path": "package.json",
                "ecosystem": "npm"
            })
    
    return dependencies
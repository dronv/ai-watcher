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
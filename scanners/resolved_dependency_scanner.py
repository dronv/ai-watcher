import subprocess

def get_resolved_dependencies():
    depenencies = []

    result = subprocess.run(
        ["pip", "freeze"],
        capture_output=True,
        text=True
    )

    for line in result.stdout.splitlines():
        if "==" in line:
            name, version = line.split("==", 1)
            depenencies.append({
                "name": name.lower(),
                "resolved_version": version
            })
    
    return depenencies

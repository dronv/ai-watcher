from packaging.requirements import Requirement, InvalidRequirement

def parse_requirements(file_path):
    dependencies = []
    with open(file_path, 'r') as f:
        for raw_line in f:
            line = raw_line.strip()

            # Skip empty or comments
            if not line or line.startswith('#'):
                continue
            
            # Remove inline comments
            if " #" in line:
                line = line.split(" #",1)[0].strip()
            
            try:
                req = Requirement(line)
                
                name = req.name.lower() 
                specifier = str(req.specifier) if req.specifier else None

                dependencies.append({
                    "name": name,
                    "version_spec": specifier,
                    "extras": list(req.extras),
                    "is_direct_url": bool(req.url)
                })

            except InvalidRequirement:
                dependencies.append({
                    "name": line,
                    "version_spec": None,
                    "parse_error": True
                })
    
    return dependencies
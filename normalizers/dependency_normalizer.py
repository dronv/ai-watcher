from typing import Dict, Any
from models.dependency import Dependency

def normalize_dependency(raw_dep: Dict[str, Any], ecosystem: str):
    """
    Normalize dependency data from differnet ecosystems into a Dependency Model
    """
    name = raw_dep.get("name")
    
    version_spec = clean_version(extract_version_spec(raw_dep, ecosystem))
    resolved_version = extract_resolved_version(raw_dep, ecosystem)

    return Dependency(
        name=name,
        ecosystem=ecosystem,
        version_spec=version_spec,
        resolved_version= resolved_version,
        is_resolved=resolved_version is not None
    )   
def clean_version(v):
    if not v:
        return None
    for op in ["==", ">=", "<=", "~=", "!=", ">", "<"]:
        if v.startswith(op):
            return v.replace(op, "").strip()
    return v.strip()

def extract_version_spec(raw_dep: Dict[str, Any], ecosystem: str) -> str:
    """
    Exract version range/constraint (>=, ^, ~, etc)
    """
    if ecosystem == "pypi":
        return raw_dep.get("version_spec")
    
    elif ecosystem == "npm":
        return raw_dep.get("version")
    
    return None

def extract_resolved_version(raw_dep:Dict[str,Any], ecosystem:str) -> str:
    """
    Extract installed version
    """
    return raw_dep.get("resolved_version")
    
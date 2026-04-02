from typing import Dict, Any
from models.dependency import Dependency

def normalize_dependency(raw_dep: Dict[str, Any], ecosystem: str):
    """
    Normalize dependency data from differnet ecosystems into a Dependency Model
    """
    name = raw_dep.get("name")

    installed_version = extract_installed_version(raw_dep, ecosystem)
    version_contraint = extract_version_constraint(raw_dep, ecosystem)

    return Dependency(
        name=name,
        ecosystem=ecosystem,
        installed_version=installed_version,
        version_contraint= version_contraint
    )   

def extract_installed_version(raw_dep: Dict[str, Any], ecosystem: str)->str:
    """
    Ectract Installed version if known
    """
    if ecosystem == "pypi":
        return raw_dep.get("installed_version")
    
    elif ecosystem == "npm":
        return raw_dep.get("installed_version")
    
    return None

def extract_version_constraint(raw_dep:Dict[str,Any], ecosystem:str)->str:
    """
    version range/constraint (>=, ^, ~, etc)
    """
    if ecosystem == "pypi":
        return raw_dep.get("constraint") or raw_dep.get("installed_version")
    elif ecosystem == "npm":
        return raw_dep.get("version")
    
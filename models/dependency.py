from dataclasses import dataclass, field
from typing import Optional, List, Dict

@dataclass
class Dependency:
    #Basic
    name: str
    ecosystem: str # "python" | "npm"

    #version info
    version_spec: Optional[str] = None
    resolved_version: Optional[str] = None
    is_resolved: Optional[bool] = None
    latest_version: Optional[str] = None

    #version intelligence
    outdated: Optional[bool] = None
    version_gap: Optional[int] = None #number of versions behind

    # Security 
    vulnerabilities: List[Dict] = field(default_factory=list)
    malicious_versions: List[Dict] = field(default_factory=list)

    #metadata
    description: Optional[str] = None
    homepage: Optional[str] = None

    #Risk/analysis
    risk_score:Optional[int] = None
    risk_level: Optional[str] = None # Low/med/high

    #extra
    extra: Dict = field(default_factory=dict)


    def is_outdated(self)->bool:
        return self.resolved_version != self.latest_version
    
    def has_security_issues(self)->bool:
        return bool(self.vulnerabilities or self.malicious_versions)
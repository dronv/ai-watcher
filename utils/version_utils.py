from packaging.version import parse, Version, InvalidVersion

def safe_parse(version):
    try:
        return parse(version)
    except InvalidVersion:
        return None
    
def is_outdated(installed, latest):
    v_installed = safe_parse(installed)
    v_latest = safe_parse(latest)
    
    if not v_installed or not v_latest:
        return False
    
    return v_installed < v_latest

def get_all_versions(releases):
    valid_versions = []

    for v in releases.keys():
        parsed = safe_parse(v)
        if parsed:
            valid_versions.append(parsed)

    return [str(v) for v in sorted(valid_versions)]

def get_latest_version(all_releases):
    parsed_versions = [safe_parse(v) for v in all_releases]
    parsed_versions = [v for v in parsed_versions if v is not None]

    if not parsed_versions:
        print("no versions found")
        return None
    
    return str(max(parsed_versions))

def get_version_gap(installed, latest):
    v_installed = safe_parse(installed)
    v_latest = safe_parse(latest)

    if not v_installed or not v_latest:
        return 0
    
    return (v_latest.major - v_installed.major) * 100 + \
            ( v_latest.minor - v_installed.minor) * 10 + \
            (v_latest.micro - v_installed.micro) 

def gap_version_scoring(gap):
    if gap >=50:
        return "HIGH"
    elif gap >= 10:
        return "MEDIUM"
    elif gap > 0:
        return "LOW"
    return None

def is_version_in_range(version, specifier):
    from packaging.specifiers import SpecifierSet

    v = safe_parse(version)
    if not v:
        return False
    
    try:
        spec = SpecifierSet(specifier)
        return v in spec
    except:
        return False
    
def is_vulnerable(installed_version, vulnerability_ranges):
    if not vulnerability_ranges:
        return "UNKNOWN"
    
    for spec in vulnerability_ranges:
        if is_version_in_range(installed_version, spec):
            return True
    return False

def is_known_bad_version(installed_version, bad_versions):
    return installed_version in bad_versions
from packaging.version import parse

def get_release_gap_py(installed_v, all_versions):
    parsed_versions = sorted([parse(v) for v in all_versions])

    installed = parse(installed_v)
    
    #count versions greater than installed
    gap = sum(1 for v in parsed_versions if v > installed)

    return gap


def gap_version_scoring_py(v1,v2):
    v1_parts = list(v1.release)
    v2_parts = list(v2.release)

    max_len = max(len(v1_parts), len(v2_parts))
    v1_parts += [0] * (max_len - len(v1_parts))
    v2_parts += [0] * (max_len - len(v2_parts))

    #Extract Major, minor and patch gap
    major_diff = max(0, v2_parts[0] - v1_parts[0])
    minor_diff = max(0, v2_parts[1] - v1_parts[1]) if max_len > 1 else 0
    patch_diff = max(0, v2_parts[2] - v1_parts[2]) if max_len > 2 else 0

    #Adding weights
    gap_score = (major_diff * 3) + (minor_diff * 2) + (patch_diff * 1)

    return gap_score
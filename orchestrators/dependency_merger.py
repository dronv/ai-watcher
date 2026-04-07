def merge_dependencies(spec_deps, resolved_deps):
    resolved_map = {d["name"]: d for d in resolved_deps}

    merged = []

    for dep in spec_deps:
        name = dep["name"]

        resolved = resolved_map.get(name)

        merged.append({
            "name": name,
            "version_spec": dep.get("version_spec"),
            "resolved_version": resolved["resolved_version"] if resolved else None,
            "found_in_env": resolved is not None
        })

    return merged
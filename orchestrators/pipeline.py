from scanners.python_scanner import parse_requirements
from scanners.resolved_dependency_scanner import get_resolved_dependencies
from adapters.pypi_adapter import fetch_pypi_data
from adapters.osv_vulnerabilities import fetch_osv_vulnerabilities
from normalizers.vulnerability_normalizer import normalize_vulnerability
from normalizers.dependency_normalizer import normalize_dependency
from analyzers.dependency_analyzer import analyze_dependency
from orchestrators.dependency_merger import merge_dependencies
from llm.llm_scorer import score_dependency

def run_analysis(requirements_file):
    results = []
    print("STEP: Parse requirements file.")
    #S PARSE REQUIREMENTS
    spec_deps = parse_requirements(requirements_file)

    print("STEP: Parse resolved deps.")
    # GET RESOLVED DEPS
    resolved_deps = get_resolved_dependencies()

    print("STEP: Merge deps")
    # MERGE
    merged_dependencies = merge_dependencies(spec_deps, resolved_deps)

    for dep in merged_dependencies:
        name = dep.get("name")
        
        try:
            print(f"\n Analyzing: {name}")

            print("STEP: Fetching PyPi Data.")
            package_data = fetch_pypi_data(name)

            if not package_data:
                results.append({
                    "dependency":{
                        "name": name,
                        "risk_level": "UNKNOWN",
                        "reasons": ["Package data not found"]
                    }
                })
                continue
            
            print("STEP: Fetching OSV Vulns")
            raw_vulns = fetch_osv_vulnerabilities(name) or []

            print("STEP: normalize_vulns")
            normalize_vulns = [normalize_vulnerability(vulns, source="pypi", package_name=dep.get("name"))
                               for vulns in raw_vulns
                               ]
            print("STEP: normalize_dependency")
            normalized_dep = normalize_dependency(dep, ecosystem="pypi")

            print("STEP: analysis on deps")
            analysis = analyze_dependency(
                    normalized_dep.__dict__, package_data, normalize_vulns
                )

            if analysis.get("risk_level") == "UNKNOWN":
                llm_result = None
            else:
                llm_result = score_dependency(analysis)

            print("STEP: run llm")
            final_result = {
                    "dependency" : analysis,
                    "llm_analysis" : llm_result
                }

            results.append(final_result)

        except Exception as e:
            print(f"Error analyzing {name}: {e}")
    
    return results


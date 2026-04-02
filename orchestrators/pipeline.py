from scanners.packages_parser import parse_requirements
from adapters.pypi_adapter import fetch_pypi_data
from adapters.osv_vulnerabilities import fetch_osv_vulnerabilities
from normalizers.vulnerability_normalizer import normalize_vulnerability
from analyzers.dependency_analyzer import analyze_dependency
from llm.llm_scorer import score_dependency

def run_analysis(requirements_file):
    results = []

    dependencies = parse_requirements(requirements_file)

    for dep in dependencies:
        name = dep.get("name")
        
        try:
            print(f"\n Analyzing: {name}")

            package_data = fetch_pypi_data(name)

            if not package_data:
                print(f"No data found for {name}")
            
            raw_vulns = fetch_osv_vulnerabilities(name)
            normalize_vulns = [normalize_vulnerability(vulns, source="pypi", package_name=dep.get("name"))
                               for vulns in raw_vulns
                               ]
            analysis = analyze_dependency(
                    dep, package_data, normalize_vulns
                )

            llm_result = score_dependency(analysis)

            final_result = {
                    "dependency" : analysis,
                    "llm_analysis" : llm_result
                }

            results.append(final_result)

        except Exception as e:
            print(f"Error analyzing {name}: str{e}")
    
    return results


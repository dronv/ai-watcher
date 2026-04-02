from orchestrators.pipeline import run_analysis

def main ():
    import json
    file_path = "requirements.txt"

    results = run_analysis(file_path)

    print(results)

if __name__ == "__main__":
    main()
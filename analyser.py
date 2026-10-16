from collections import Counter
import re

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", 
    "in", "is", "it", "of", "on", "or", "that", "the", "to", "we", "with"
}

def clean_text(text):
    tokens = text.lower().split()
    cleaned_tokens = []
    for token in tokens:
        cleaned = token.strip(",!?;:\"'()[]{}<>")
        if cleaned:
            cleaned_tokens.append(cleaned)
    return cleaned_tokens

def extract_keywords(tokens, stopwords=STOPWORDS):
    keywords = [token for token in tokens if token not in stopwords]
    return Counter(keywords)

def analyze_gap(resume_keywords, job_keywords):
    resume_set = set(resume_keywords.keys())
    job_set = set(job_keywords.keys())
    
    matches = resume_set & job_set
    missing = job_set - resume_set
    score = (len(matches) / len(job_set)) * 100 if job_set else 0.0
    
    return {
        "matches": matches,
        "missing": missing,
        "score": round(score, 2)
    }

def generate_report(results):
    print("\n==================================================")
    print("           ATS KEYWORD GAP AUDIT REPORT           ")
    print("==================================================")
    print(f"Match Score: {results['score']:.2f}%\n")
    
    print(f"[MATCHING KEYWORDS] ({len(results['matches'])} found)")
    for keyword in sorted(results["matches"]):
        print(f"  ✓ {keyword}")
        
    print(f"\n[CRITICAL MISSING KEYWORDS] ({len(results['missing'])} missing)")
    for keyword in sorted(results["missing"]):
        print(f"  ✗ {keyword}")
    print("==================================================\n")

def read_file(filepath):
    """Safely reads file contents with error handling."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"[ERROR] File not found: '{filepath}'")
        return None
    except PermissionError:
        print(f"[ERROR] Permission denied: '{filepath}'")
        return None

if __name__ == "__main__":
    resume_path = input("Enter your resume file path: ").strip()
    job_path = input("Enter the job description file path: ").strip()

    resume_text = read_file(resume_path)
    job_text = read_file(job_path)

    if resume_text and job_text:
        resume_tokens = clean_text(resume_text)
        job_tokens = clean_text(job_text)

        resume_keywords = extract_keywords(resume_tokens)
        job_keywords = extract_keywords(job_tokens)

        analysis_results = analyze_gap(resume_keywords, job_keywords)
        generate_report(analysis_results)
    else:
        print("[EXITS] Could not perform analysis due to file read errors.")
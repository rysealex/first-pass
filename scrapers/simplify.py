import requests

JSON_INTERNSHIPS_URL = "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/refs/heads/dev/.github/scripts/listings.json"
JSON_OFFSEASON_URL = "https://github.com/SimplifyJobs/Summer2026-Internships/blob/dev/README-Off-Season.md"
JSON_NEWGRAD_URL = "https://github.com/SimplifyJobs/New-Grad-Positions"

def fetch_simplify_jobs():
    response = requests.get(JSON_INTERNSHIPS_URL)
    if response.status_code == 200:
        jobs = response.json()
        for job in jobs:
            company = job.get('company_name')
            role = job.get('title')
            url = job.get('url')
            print(f"Company: {company} | Role: {role} | URL: {url}\n")
    else:
        print("Failed to fetch")
        
fetch_simplify_jobs()
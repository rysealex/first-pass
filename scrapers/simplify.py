import requests
from util import save_job, init_audio

JSON_INTERNSHIPS_URL = "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/refs/heads/dev/.github/scripts/listings.json"
JSON_OFFSEASON_URL = "https://github.com/SimplifyJobs/Summer2026-Internships/blob/dev/README-Off-Season.md"
JSON_NEWGRAD_URL = "https://github.com/SimplifyJobs/New-Grad-Positions"

def run_simplify_scraper():
    init_audio()
    print("Checking SimplifyJobs...")
    response = requests.get(JSON_INTERNSHIPS_URL)

    if response.status_code == 200:
        jobs = response.json()
        for job in jobs:
            # URL is unique ID to avoid duplicate jobs
            job_url = job.get('url')
            company = job.get('company')
            role = job.get('title')

            # save the job to the db and play notification sound
            save_job(job_url, company, role, job_url, "Simplify")
        
if __name__ == "__main__":
    run_simplify_scraper()
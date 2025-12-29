import requests
import time
from bs4 import BeautifulSoup
from util import save_job, init_audio

SOURCES = {
    "Simplify-Summer": "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/refs/heads/dev/.github/scripts/listings.json",
    "Simplify-NewGrad": "https://raw.githubusercontent.com/SimplifyJobs/New-Grad-Positions/refs/heads/dev/.github/scripts/listings.json"
}
OFFSEASON_URL = "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/README-Off-Season.md"

def scrape_offseason_html():
    print("Checking Simplify-OffSeason (HTML inside Markdown)...")
    try:
        response = requests.get(OFFSEASON_URL)
        if response.status_code != 200:
            print("Failed to fetch raw README")
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')

        rows = soup.find_all('tr')
        last_company = ""

        for row in rows:
            cols = row.find_all('td')

            if len(cols) >= 5:
                company_raw = cols[0].get_text(strip=True)
                company = company_raw.replace('🔥', '').strip()
                
                if company == "↳":
                    company = last_company
                else:
                    last_company = company

                role = cols[1].get_text(strip=True)

                links = cols[4].find_all('a')
                if links:
                    job_url = links[0].get('href')
                    if job_url:
                        save_job(job_url, company, role, job_url, "Simplify-OffSeason")
                        
    except Exception as e:
        print(f"Error scraping Off-Season: {e}")

def run_simplify_scraper():
    init_audio()
    
    # process the JSON sources
    for label, url in SOURCES.items():
        print(f"Checking {label} (JSON)...")
        try:
            res = requests.get(url)
            if res.status_code == 200:
                jobs = res.json()
                for job in jobs:
                    job_url = job.get('url')
                    save_job(job_url, job.get('company_name'), job.get('title'), job_url, label)
            time.sleep(1)
        except Exception as e:
            print(f"Error checking {label}: {e}")

    # process the HTML source
    scrape_offseason_html()
        
if __name__ == "__main__":
    run_simplify_scraper()
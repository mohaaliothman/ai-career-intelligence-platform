from src.scraper.sources.remotive_scraper import RemotiveScraper

scraper = RemotiveScraper()

jobs = scraper.scrape()

print(f"Collected {len(jobs)} jobs")

for job in jobs[:5]:
    print("-" * 50)
    print(job.title)
    print(job.company_name)
    print(job.location)
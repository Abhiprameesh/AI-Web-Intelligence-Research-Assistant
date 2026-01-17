import requests
from bs4 import BeautifulSoup


class ScrapingService:
    def scrape_text(self, url: str) -> str:
        try:
            response = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")

            text = " ".join(p.get_text() for p in paragraphs)
            return text.strip()

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Scraping failed: {str(e)}")

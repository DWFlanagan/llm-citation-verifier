"""Citation verification against Crossref API"""

from typing import Dict

import requests


class CitationVerifier:
    def __init__(self):
        self.base_url = "https://api.crossref.org"
        self.headers = {"User-Agent": "LLM-CitationVerifier/1.0"}

    def verify_doi(self, doi: str) -> Dict:
        # Clean the DOI
        doi = (
            doi.strip()
            .replace("https://doi.org/", "")
            .replace("http://dx.doi.org/", "")
        )

        try:
            url = f"{self.base_url}/works/{doi}"
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                work = data["message"]

                # Extract authors
                authors = self._extract_authors(work.get("author", []))

                return {
                    "verified": True,
                    "doi": doi,
                    "title": work.get("title", ["Unknown"])[0]
                    if work.get("title")
                    else "Unknown",
                    "authors": authors,
                    "journal": work.get("container-title", ["Unknown"])[0]
                    if work.get("container-title")
                    else "Unknown",
                    "publisher": work.get("publisher", "Unknown"),
                    "year": self._extract_year(
                        work.get("published-print") or work.get("published-online")
                    ),
                    "url": f"https://doi.org/{doi}",
                }
            elif response.status_code == 404:
                return {
                    "verified": False,
                    "doi": doi,
                    "error": "DOI not found in Crossref database - likely hallucinated",
                }
            else:
                return {
                    "verified": False,
                    "doi": doi,
                    "error": f"HTTP {response.status_code}: Unable to verify",
                }

        except requests.RequestException as e:
            return {"verified": False, "doi": doi, "error": f"Network error: {str(e)}"}

    def _extract_authors(self, authors):
        if not authors:
            return "Unknown"

        author_names = []
        for author in authors[:3]:  # First 3 authors
            given = author.get("given", "")
            family = author.get("family", "")
            if family:
                author_names.append(f"{given} {family}".strip())

        if len(authors) > 3:
            author_names.append("et al.")

        return ", ".join(author_names) if author_names else "Unknown"

    def _extract_year(self, date_parts):
        if not date_parts or "date-parts" not in date_parts:
            return "Unknown"

        try:
            return str(date_parts["date-parts"][0][0])
        except (IndexError, TypeError):
            return "Unknown"

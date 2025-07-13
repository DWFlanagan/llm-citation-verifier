"""Citation verification against Crossref API"""

from typing import Dict

import requests


class CitationVerifier:
    """
    A citation verifier that checks DOIs against the Crossref API.

    This class provides functionality to verify DOI citations by querying the
    Crossref database and extracting bibliographic metadata. It can detect
    potentially hallucinated citations by checking if DOIs exist in the database.

    Attributes:
        base_url (str): The base URL for the Crossref API
        headers (dict): HTTP headers used for API requests
    """

    def __init__(self):
        """
        Initialize the CitationVerifier with default settings.

        Sets up the Crossref API base URL and appropriate headers for making
        requests to the service.
        """
        self.base_url = "https://api.crossref.org"
        self.headers = {"User-Agent": "LLM-CitationVerifier/1.0"}

    def verify_doi(self, doi: str) -> Dict:
        """
        Verify a DOI citation against the Crossref database.

        This method takes a DOI string, cleans it by removing common URL prefixes,
        queries the Crossref API, and returns structured verification results
        including bibliographic metadata if the DOI is valid.

        Args:
            doi (str): The DOI to verify. Can include URL prefixes like
                      'https://doi.org/' or 'http://dx.doi.org/' which will
                      be automatically stripped.

        Returns:
            Dict: A dictionary containing verification results with the following structure:
                - For valid DOIs:
                    {
                        'verified': True,
                        'doi': str,          # Cleaned DOI
                        'title': str,        # Paper title
                        'authors': str,      # Formatted author list
                        'journal': str,      # Journal name
                        'publisher': str,    # Publisher name
                        'year': str,         # Publication year
                        'url': str          # Full DOI URL
                    }
                - For invalid DOIs:
                    {
                        'verified': False,
                        'doi': str,          # Cleaned DOI
                        'error': str         # Error description
                    }

        Raises:
            No exceptions are raised directly - network and API errors are
            caught and returned in the error field of the result dictionary.
        """
        # Clean the DOI
        doi = doi.strip().replace("https://doi.org/", "").replace("http://dx.doi.org/", "")

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
                    "title": work.get("title", ["Unknown"])[0] if work.get("title") else "Unknown",
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
                    "error": "DOI not found in Crossref database - possibly hallucinated",
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
        """
        Extract and format author information from Crossref author data.

        This method processes the author list from Crossref API response and
        formats it into a readable string. It limits the output to the first
        3 authors and adds "et al." if there are more.

        Args:
            authors (list): List of author dictionaries from Crossref API,
                           where each dictionary contains 'given' and 'family'
                           name fields.

        Returns:
            str: Formatted author string in the format "FirstName LastName,
                 FirstName LastName, et al." or "Unknown" if no authors found.
        """
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
        """
        Extract publication year from Crossref date information.

        This method processes the date-parts structure returned by the Crossref
        API to extract the publication year.

        Args:
            date_parts (dict): Date information from Crossref API containing
                              'date-parts' field with nested year, month, day
                              information.

        Returns:
            str: Publication year as a string, or "Unknown" if the year
                 cannot be extracted from the provided data.
        """
        if not date_parts or "date-parts" not in date_parts:
            return "Unknown"

        try:
            return str(date_parts["date-parts"][0][0])
        except (IndexError, TypeError):
            return "Unknown"

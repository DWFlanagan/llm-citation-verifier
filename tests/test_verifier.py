"""Tests for the core citation verifier"""

from llm_citation_verifier.verifier import CitationVerifier


class TestCitationVerifier:
    def setup_method(self):
        """Set up test fixtures"""
        self.verifier = CitationVerifier()

    def test_valid_doi_verification(self):
        """Test that a real DOI returns verified=True with metadata"""
        result = self.verifier.verify_doi("10.1038/nature12373")

        assert result["verified"] is True
        assert result["doi"] == "10.1038/nature12373"
        assert "title" in result
        assert "authors" in result
        assert "journal" in result
        assert "year" in result
        assert len(result["title"]) > 0
        assert result["journal"] == "Nature"
        print(f"✓ Valid DOI verified: {result['title']}")

    def test_invalid_doi_verification(self):
        """Test that a fake DOI returns verified=False with error"""
        result = self.verifier.verify_doi("10.1234/fake.doi.2024")

        assert result["verified"] is False
        assert result["doi"] == "10.1234/fake.doi.2024"
        assert "error" in result
        assert "hallucinated" in result["error"].lower()
        print(f"✓ Invalid DOI flagged: {result['error']}")

    def test_doi_url_cleaning(self):
        """Test that DOI URLs are cleaned properly"""
        test_cases = [
            "https://doi.org/10.1038/nature12373",
            "http://dx.doi.org/10.1038/nature12373",
            "10.1038/nature12373",
            "  10.1038/nature12373  ",  # with whitespace
        ]

        for doi_input in test_cases:
            result = self.verifier.verify_doi(doi_input)
            assert result["verified"] is True
            assert result["doi"] == "10.1038/nature12373"

        print("✓ DOI cleaning works for all formats")

    def test_network_error_handling(self):
        """Test handling of network errors"""
        # Test with malformed DOI that would cause URL issues
        result = self.verifier.verify_doi("10.///invalid///doi")

        assert result["verified"] is False
        assert "error" in result
        print(f"✓ Network error handled: {result['error']}")

    def test_author_extraction(self):
        """Test author name extraction and formatting"""
        result = self.verifier.verify_doi("10.1038/nature12373")

        assert result["verified"] is True
        assert "authors" in result
        assert len(result["authors"]) > 0
        assert result["authors"] != "Unknown"
        print(f"✓ Authors extracted: {result['authors']}")

    def test_year_extraction(self):
        """Test publication year extraction"""
        result = self.verifier.verify_doi("10.1038/nature12373")

        assert result["verified"] is True
        assert "year" in result
        assert result["year"].isdigit()
        assert int(result["year"]) > 2000  # Reasonable year range
        print(f"✓ Year extracted: {result['year']}")

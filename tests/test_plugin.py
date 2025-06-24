"""
Tests for the LLM plugin integration functionality.

This module tests the integration between the citation verifier and the
LLM tool framework, ensuring proper JSON formatting and tool registration.
"""

import json

from llm_citation_verifier import verify_citation


class TestLLMPlugin:
    """Test suite for LLM plugin integration."""

    def test_verify_citation_function(self):
        """
        Test the main tool function returns JSON.

        Verifies that the verify_citation function returns properly
        formatted JSON that can be consumed by LLM tools.
        """
        result = verify_citation("10.1038/nature12373")

        # Should return JSON string
        assert isinstance(result, str)

        # Should be valid JSON
        parsed = json.loads(result)
        assert parsed["verified"] is True
        assert parsed["doi"] == "10.1038/nature12373"
        print("✓ verify_citation function returns valid JSON")

    def test_verify_citation_fake_doi(self):
        """
        Test tool function with fake DOI.

        Ensures that the plugin correctly handles and reports
        potentially hallucinated citations.
        """
        result = verify_citation("10.1234/fake.doi.2024")

        parsed = json.loads(result)
        assert parsed["verified"] is False
        assert "hallucinated" in parsed["error"].lower()
        print("✓ Tool function catches fake DOIs")

    def test_verify_citation_json_format(self):
        """
        Test that JSON output is well-formatted.

        Verifies that the tool returns properly indented JSON with
        all required fields for LLM consumption.
        """
        result = verify_citation("10.1038/nature12373")

        # Should be pretty-printed JSON (indented)
        assert "\n" in result
        assert "  " in result  # Should have indentation

        parsed = json.loads(result)
        required_fields = ["verified", "doi"]
        for field in required_fields:
            assert field in parsed

        print("✓ JSON output is properly formatted")

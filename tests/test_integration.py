"""Integration tests simulating real LLM usage patterns"""

import json

from llm_citation_verifier import verify_citation


class TestIntegration:
    def test_mixed_citations_scenario(self):
        """Test scenario with mix of real and fake citations"""
        # Simulate what an LLM might generate
        test_dois = [
            "10.1038/nature12373",  # Real paper
            "10.1234/fake.doi.2024",  # Fake DOI
            "10.1126/science.abcd123",  # Fake but plausible DOI
        ]

        results = []
        for doi in test_dois:
            result = verify_citation(doi)
            parsed = json.loads(result)
            results.append(parsed)

        # Should catch the fake ones
        assert results[0]["verified"] is True  # Real
        assert results[1]["verified"] is False  # Fake
        assert results[2]["verified"] is False  # Fake

        # Count hallucinated citations
        fake_count = sum(1 for r in results if not r["verified"])
        total_count = len(results)
        hallucination_rate = fake_count / total_count

        print(
            f"✓ Detected {fake_count}/{total_count} fake citations ({hallucination_rate:.1%} hallucination rate)"
        )

    def test_cancer_immunotherapy_scenario(self):
        """Test the cancer immunotherapy scenario from our real example"""
        # These are the actual DOIs the LLM generated in our test
        test_dois = [
            "10.1038/s41591-023-02452-7",  # Was fake in our test
            "10.1016/j.cell.2023.02.029",  # Was real in our test
            "10.1038/s41587-023-01748-6",  # Was fake in our test
        ]

        verified_count = 0
        for doi in test_dois:
            result = verify_citation(doi)
            parsed = json.loads(result)
            if parsed["verified"]:
                verified_count += 1
                print(f"✓ Verified: {parsed['title']}")
            else:
                print(f"✗ Fake: {doi}")

        # Should find at least one real paper
        assert verified_count >= 1
        print(f"✓ Cancer immunotherapy test: {verified_count} real citations found")

    def test_quality_control_workflow(self):
        """Test a complete quality control workflow"""
        # Simulate AI content with suspicious citations
        ai_content_dois = [
            "10.1038/nature12373",  # Known real paper
            "10.9999/totally.fake.2024",  # Obviously fake
        ]

        trusted_citations = []
        flagged_citations = []

        for doi in ai_content_dois:
            result = verify_citation(doi)
            parsed = json.loads(result)

            if parsed["verified"]:
                trusted_citations.append(
                    {"doi": doi, "title": parsed["title"], "journal": parsed["journal"]}
                )
            else:
                flagged_citations.append({"doi": doi, "error": parsed["error"]})

        assert len(trusted_citations) == 1
        assert len(flagged_citations) == 1

        print(
            f"✓ Quality control: {len(trusted_citations)} trusted, {len(flagged_citations)} flagged"
        )
        print(f"  Trusted: {trusted_citations[0]['title']}")
        print(f"  Flagged: {flagged_citations[0]['doi']}")

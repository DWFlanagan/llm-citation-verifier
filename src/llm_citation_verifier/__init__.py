"""LLM Citation Verifier - Verify academic citations against Crossref"""

import json

import llm

from .verifier import CitationVerifier


# LLM hook registration - fix the function signature
@llm.hookimpl
def register_tools(register):
    register(verify_citation)


def verify_citation(doi: str) -> str:
    """
    Verify a DOI citation against Crossref database.

    Args:
        doi: The DOI to verify (e.g., "10.1038/nature12373")

    Returns:
        JSON string with verification results
    """
    verifier = CitationVerifier()
    result = verifier.verify_doi(doi)
    return json.dumps(result, indent=2)


__version__ = "0.1.0"
__all__ = ["CitationVerifier", "verify_citation"]

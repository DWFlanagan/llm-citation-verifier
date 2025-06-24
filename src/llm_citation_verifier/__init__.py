"""
LLM Citation Verifier - Verify academic citations against Crossref

This package provides tools to verify academic citations (DOIs) against the
Crossref database. It can detect potentially hallucinated citations by checking
if DOIs exist and retrieving bibliographic metadata.

The package includes:
- CitationVerifier: Core verification class
- verify_citation: LLM plugin function for easy integration
- LLM hook integration for use with the LLM tool ecosystem
"""

import json

import llm

from .verifier import CitationVerifier


# LLM hook registration - fix the function signature
@llm.hookimpl
def register_tools(register):
    """
    Register the citation verification tool with the LLM framework.

    This function is called by the LLM framework to register available tools.
    It registers the verify_citation function as a tool that can be used
    by language models.

    Args:
        register: Function provided by LLM framework to register tools
    """
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

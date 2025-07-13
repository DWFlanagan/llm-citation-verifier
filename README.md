# LLM Citation Verifier

An [LLM](https://llm.datasette.io/en/stable/) plugin that verifies academic citations against the [Crossref](https://www.crossref.org/documentation/retrieve-metadata/rest-api/a-non-technical-introduction-to-our-api/) database to catch hallucinated references in AI-generated content.

## The Problem

AI research tools sometimes hallucinate citations - generating plausible-looking DOIs for papers that don't exist.

## The Solution

This plugin automatically verifies citations in real-time, flagging fake DOIs and validating real papers with full metadata.

## Installation

```bash
llm install llm-citation-verifier
```

## Usage Examples

### Real-Time Citation Verification

```bash
# Verify citations as the LLM generates content
llm -T verify_citation "What's new in dye sensitized solar cells? Check all the references." --td

# Single breakthrough with verification
llm -T verify_citation "What's one recent breakthrough in cancer immunotherapy? Cite just one paper and verify it." --td
```

### Quality Control for AI Content

```bash
# Review suspicious AI-generated content
llm -T verify_citation "This AI tool cited these papers: 10.1038/nature12373 and 10.1234/fake.doi.2024. Check if they're real." --td

# Batch verification
llm -T verify_citation "Verify these DOIs from an AI summary: 10.1038/nature12373, 10.1126/science.abc123, 10.1234/fake.journal.2024" --td
```

### Research Integrity

```bash
# Audit AI research tools
llm -T verify_citation "Tell me about recent AI alignment breakthroughs. Verify any papers you cite." --td

# Fact-check literature reviews
llm -T verify_citation "What are the latest developments in quantum computing? Make sure all citations are real." --td
```

## What It Does

- ✅ **Catches fake citations** - Flags DOIs that don't exist in Crossref
- ✅ **Validates real papers** - Returns title, authors, journal, year
- ✅ **Real-time verification** - Works during content generation
- ✅ **Prevents hallucination** - Stops fake references from appearing

## Example Output

```
Tool call: verify_citation({'doi': '10.1038/s41591-023-02452-7'})
{
  "verified": false,
  "doi": "10.1038/s41591-023-02452-7", 
  "error": "DOI not found in Crossref database - likely hallucinated"
}

Tool call: verify_citation({'doi': '10.1016/j.cell.2023.02.029'})
{
  "verified": true,
  "doi": "10.1016/j.cell.2023.02.029",
  "title": "Discovery of phage determinants that confer sensitivity to bacterial immune systems",
  "authors": "Avigail Stokar-Avihail, Taya Fedorenko, Jens Hör, et al.",
  "journal": "Cell",
  "year": "2023"
}
```

## Use Cases

- **Publishing workflows** - Verify citations before publication
- **AI content review** - Quality control for AI writing assistants  
- **Research integrity** - Audit AI-generated literature reviews
- **Fact-checking** - Validate suspicious citation claims

## Development

```bash
git clone https://github.com/your-org/llm-citation-verifier
cd llm-citation-verifier
uv sync
uv pip install -e .
uv run pytest
```

## Pro Tips

- Use `--td` flag to see verification calls in real-time
- Chain limits prevent infinite verification loops
- Works with any topic - just add "verify citations" to your prompt
- Catches both completely fake DOIs and real DOIs used in wrong context

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.topic_suggester import suggest_all
from src.sprint_narrator import narrate_all
from src.essay_drafter import draft_essay, validate_draft
from src.indexer import index_all

FIXTURES = Path(__file__).parent / "fixtures"

class TestPipelineEndToEnd:
    """End-to-end integration test of the essay generation pipeline."""

    @patch("src.essay_drafter.create_client")
    def test_full_essay_generation_flow(self, mock_create_client, tmp_path):
        """Exercises the main user flow end-to-end:
        1. Topic Suggester
        2. Sprint Narrator
        3. Essay Drafter
        4. Draft Validator
        5. Indexer
        """
        # Mock LLM Client setup
        from src.llm_client import LLMResponse
        import datetime
        
        valid_frontmatter = f"""---
layout: post
title: "Mock AI Generated Title"
author: ORGAN-V
date: "{datetime.datetime.now().strftime('%Y-%m-%d')}"
tags: [methodology, governance]
category: guide
excerpt: "A mocked AI excerpt."
portfolio_relevance: "Testing the flow."
related_repos: [public-process]
reading_time: "5 min read"
word_count: 500
references: []
---

# Mock Body
This is a mock response from the LLM. It's meant to pass validation.
"""
        mock_client = MagicMock()
        mock_client.generate.return_value = LLMResponse(
            text=valid_frontmatter,
            model="mock-model",
            provider="mock-provider",
            input_tokens=100,
            output_tokens=500,
        )
        mock_create_client.return_value = mock_client

        # 1. Setup minimal inputs in tmp_path
        tag_gov = tmp_path / "tag-governance.yaml"
        tag_gov.write_text("preferred_tags:\n  - governance\n  - methodology\n")
        
        cat_tax = tmp_path / "category-taxonomy.yaml"
        cat_tax.write_text(
            "categories:\n"
            "  guide:\n    typical_count: 1\n"
            "  case-study:\n    typical_count: 2\n"
        )
        
        rubric = tmp_path / "quality-rubric.yaml"
        rubric.write_text("criteria:\n  - Clear writing\n")
        
        schema = tmp_path / "frontmatter-schema.yaml"
        schema.write_text(
            "required_fields:\n"
            "  layout: {type: str}\n"
            "  title: {type: str}\n"
            "  author: {type: str}\n"
            "  date: {type: str}\n"
            "  tags: {type: list}\n"
            "  category: {type: str}\n"
            "  excerpt: {type: str}\n"
            "  portfolio_relevance: {type: str}\n"
            "  related_repos: {type: list}\n"
            "  reading_time: {type: str}\n"
            "  word_count: {type: int}\n"
            "  references: {type: list}\n"
            "optional_fields:\n"
            "  word_count_policy: {type: str}\n"
            "  word_count_override_reason: {type: str}\n"
        )

        template_dir = tmp_path / "templates"
        template_dir.mkdir()
        (template_dir / "case-study.md").write_text("Mock template body")

        posts_dir = tmp_path / "_posts"
        posts_dir.mkdir()

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        sprint_narrative_path = tmp_path / "sprint-narrative.md"
        
        # 2. Run Topic Suggester
        suggestions = suggest_all(
            essays_index_path=str(FIXTURES / "mini-essays-index.json"),
            xrefs_path=str(FIXTURES / "mini-cross-references.json"),
            tag_gov_path=str(tag_gov),
            cat_tax_path=str(cat_tax),
            surfaced_path=str(FIXTURES / "mini-surfaced.json"),
            max_suggestions=3,
        )
        
        assert "suggestions" in suggestions
        assert len(suggestions["suggestions"]) > 0
        
        # 3. Run Sprint Narrator
        narrate_all(
            metrics_path=str(FIXTURES / "mini-engagement-metrics.json"),
            report_path=str(FIXTURES / "mini-system-report.json"),
            index_path=str(FIXTURES / "mini-essays-index.json"),
            calendar_path=str(FIXTURES / "mini-pub-calendar.json"),
            output_path=str(sprint_narrative_path),
        )
        
        assert sprint_narrative_path.exists()
        
        # 4. Run Essay Drafter on the first suggestion
        suggestion = suggestions["suggestions"][0]
        result = draft_essay(
            suggestion=suggestion,
            template_dir=str(template_dir),
            schema_path=str(schema),
            rubric_path=str(rubric),
            tag_governance_path=str(tag_gov),
            category_taxonomy_path=str(cat_tax),
            posts_dir=str(posts_dir),
            output_dir=str(output_dir),
            context={"sprint_narrative": sprint_narrative_path.read_text()},
            provider="mock-provider",
        )
        
        assert "output_path" in result
        draft_file = Path(result["output_path"])
        assert draft_file.exists()
        
        # 5. Validate the generated draft
        draft_text = draft_file.read_text(encoding="utf-8")
        is_valid, errors = validate_draft(draft_text, str(schema))
        
        assert is_valid, f"Draft validation failed with errors: {errors}"
        
        # 6. Make the post available in _posts and run Indexer
        # Moving the draft to _posts to mimic it being published/merged.
        published_post = posts_dir / draft_file.name
        published_post.write_text(draft_text)
        
        logs_dir = tmp_path / "_logs"
        logs_dir.mkdir()
        
        index_output_dir = tmp_path / "data"
        index_output_dir.mkdir()
        
        index_all(
            posts_dir=str(posts_dir),
            logs_dir=str(logs_dir),
            output_dir=str(index_output_dir)
        )
        
        assert (index_output_dir / "essays-index.json").exists()
        
        essays_index = json.loads((index_output_dir / "essays-index.json").read_text())
        assert len(essays_index["essays"]) == 1
        assert essays_index["essays"][0]["title"] == "Mock AI Generated Title"


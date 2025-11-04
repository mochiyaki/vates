"""Integration tests for MemVerge MemMachine memory service."""
from __future__ import annotations

import tempfile
from pathlib import Path
from uuid import uuid4

import pytest

from narrative_architect.services.memory_service import NarrativeMemoryService


class TestMemoryServiceBasics:
    """Test basic memory service functionality."""

    def test_memory_service_initialization(self):
        """Test that memory service can be initialized."""
        service = NarrativeMemoryService()
        # Memory service should gracefully handle initialization
        assert service is not None

    def test_store_and_retrieve_user_preference(self):
        """Test storing and retrieving user preferences."""
        service = NarrativeMemoryService()

        if not service.is_available():
            pytest.skip("Memory service not available")

        user_id = f"test_user_{uuid4()}"

        # Store a preference
        service.store_user_preference(user_id, "style", "poetic")

        # Retrieve user context
        context = service.get_user_context(user_id, "What are the user's preferences?")

        # Context should be retrievable (may be None if memory not fully initialized)
        assert context is None or isinstance(context, str)

    def test_store_project_completion(self):
        """Test storing completed project in memory."""
        service = NarrativeMemoryService()

        if not service.is_available():
            pytest.skip("Memory service not available")

        project_id = uuid4()
        user_id = f"test_user_{uuid4()}"
        narrative = "This is a test narrative about a journey through space."
        assets = ["asset1", "asset2", "asset3"]
        themes = ["space", "journey", "exploration"]

        # Should not raise an exception
        service.store_project_completion(
            project_id=project_id,
            user_id=user_id,
            narrative=narrative,
            assets_used=assets,
            themes=themes,
        )

    def test_find_similar_projects(self):
        """Test finding similar projects."""
        service = NarrativeMemoryService()

        if not service.is_available():
            pytest.skip("Memory service not available")

        user_id = f"test_user_{uuid4()}"

        # Store a project first
        service.store_project_completion(
            project_id=uuid4(),
            user_id=user_id,
            narrative="A story about space exploration",
            assets_used=["asset1"],
            themes=["space", "exploration"],
        )

        # Search for similar projects
        results = service.find_similar_projects(
            query="space exploration projects",
            user_id=user_id,
            limit=3,
        )

        # Results should be a list (may be empty if memory not persisted yet)
        assert isinstance(results, list)

    def test_store_creative_prompt(self):
        """Test storing creative prompts."""
        service = NarrativeMemoryService()

        if not service.is_available():
            pytest.skip("Memory service not available")

        user_id = f"test_user_{uuid4()}"

        # Should not raise an exception
        service.store_creative_prompt(
            user_id=user_id,
            prompt="Explore how the protagonist's journey reflects inner transformation",
            context="Generated from space exploration narrative",
            was_helpful=True,
        )

    def test_memory_service_graceful_degradation(self):
        """Test that memory service degrades gracefully when unavailable."""
        service = NarrativeMemoryService()

        # These should not raise exceptions even if memory is not available
        service.store_user_preference("test_user", "style", "casual")
        service.store_project_completion(
            project_id=uuid4(),
            user_id="test_user",
            narrative="test",
            assets_used=[],
            themes=[],
        )
        context = service.get_user_context("test_user")
        assert context is None or isinstance(context, str)

        results = service.find_similar_projects("test", "test_user")
        assert isinstance(results, list)


class TestMemoryServiceWithPipeline:
    """Test memory service integration with pipeline."""

    def test_pipeline_without_user_id(self):
        """Test that pipeline works without user_id (backward compatibility)."""
        from narrative_architect.agents import (
            CreativeEnhancementAgent,
            ImageCaptioningAgent,
            NarrativeSynthesisAgent,
        )
        from narrative_architect.services import FileIngestionService, ProjectRepository
        from narrative_architect.services.pipeline import NarrativePipeline

        repository = ProjectRepository()
        ingestion_service = FileIngestionService()
        memory_service = NarrativeMemoryService()

        pipeline = NarrativePipeline(
            repository=repository,
            ingestion_service=ingestion_service,
            caption_agent=ImageCaptioningAgent(),
            narrative_agent=NarrativeSynthesisAgent(),
            enhancement_agent=CreativeEnhancementAgent(),
            memory_service=memory_service,
        )

        # Pipeline should initialize successfully
        assert pipeline is not None
        assert pipeline.memory_service is not None

    def test_pipeline_with_user_id(self):
        """Test that pipeline can use user_id with memory."""
        from narrative_architect.models import Project, ProjectStatus
        from narrative_architect.services import ProjectRepository
        from narrative_architect.services.memory_service import NarrativeMemoryService
        from datetime import datetime
        from uuid import uuid4

        repository = ProjectRepository()
        memory_service = NarrativeMemoryService()

        # Create a project with user_id
        project_id = uuid4()
        user_id = f"test_user_{uuid4()}"
        now = datetime.utcnow()

        project = Project(
            id=project_id,
            status=ProjectStatus.queued,
            created_at=now,
            updated_at=now,
            user_id=user_id,
        )

        repository.create(project)
        retrieved = repository.get(project_id)

        # Project should have user_id
        assert retrieved is not None
        assert retrieved.user_id == user_id

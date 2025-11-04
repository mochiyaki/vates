from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

from mem0 import Memory

logger = logging.getLogger(__name__)


class NarrativeMemoryService:
    """Persistent memory layer for narrative generation using MemVerge's MemMachine."""

    def __init__(self) -> None:
        """Initialize the memory service with mem0ai."""
        try:
            self.memory = Memory()
            logger.info("NarrativeMemoryService initialized successfully")
        except Exception as exc:
            logger.warning("Failed to initialize memory service: %s", exc)
            self.memory = None

    def is_available(self) -> bool:
        """Check if memory service is available."""
        return self.memory is not None

    def store_project_completion(
        self,
        project_id: UUID,
        user_id: str,
        narrative: str,
        assets_used: List[str],
        themes: Optional[List[str]] = None,
    ) -> None:
        """Store completed project in memory for future reference.

        Args:
            project_id: The unique project identifier
            user_id: The user who created the project
            narrative: The generated narrative text
            assets_used: List of asset IDs used in the project
            themes: Optional list of themes extracted from the narrative
        """
        if not self.is_available():
            logger.debug("Memory service not available, skipping project storage")
            return

        try:
            themes_str = ", ".join(themes) if themes else "general"
            narrative_preview = narrative[:200] if len(narrative) > 200 else narrative

            messages = [
                {
                    "role": "assistant",
                    "content": (
                        f"Completed narrative project {project_id}. "
                        f"Themes: {themes_str}. "
                        f"Used {len(assets_used)} assets. "
                        f"Preview: {narrative_preview}"
                    ),
                }
            ]

            self.memory.add(
                messages,
                user_id=user_id,
                metadata={
                    "project_id": str(project_id),
                    "themes": themes or [],
                    "asset_count": len(assets_used),
                    "narrative_length": len(narrative),
                },
            )
            logger.info("Stored project %s in memory for user %s", project_id, user_id)
        except Exception as exc:
            logger.warning("Failed to store project in memory: %s", exc)

    def store_user_preference(
        self, user_id: str, preference_type: str, preference_value: Any
    ) -> None:
        """Store user preferences for narrative generation.

        Args:
            user_id: The user identifier
            preference_type: Type of preference (e.g., 'style', 'genre', 'tone')
            preference_value: The preference value
        """
        if not self.is_available():
            logger.debug("Memory service not available, skipping preference storage")
            return

        try:
            messages = [
                {
                    "role": "user",
                    "content": f"I prefer {preference_type}: {preference_value}",
                },
                {
                    "role": "assistant",
                    "content": f"I'll remember that you prefer {preference_type}: {preference_value}",
                },
            ]

            self.memory.add(messages, user_id=user_id)
            logger.info(
                "Stored preference %s=%s for user %s",
                preference_type,
                preference_value,
                user_id,
            )
        except Exception as exc:
            logger.warning("Failed to store user preference: %s", exc)

    def get_user_context(self, user_id: str, query: str = "What do I know about this user?") -> Optional[str]:
        """Retrieve user context and preferences from memory.

        Args:
            user_id: The user identifier
            query: Query to search for in memory

        Returns:
            User context as a string, or None if not available
        """
        if not self.is_available():
            logger.debug("Memory service not available, skipping context retrieval")
            return None

        try:
            results = self.memory.search(query=query, user_id=user_id, limit=5)

            if results and results.get("results"):
                memories = [entry.get("memory", "") for entry in results["results"]]
                context = "\n".join(f"- {memory}" for memory in memories if memory)
                logger.info("Retrieved context for user %s: %d memories", user_id, len(memories))
                return context if context else None

            return None
        except Exception as exc:
            logger.warning("Failed to retrieve user context: %s", exc)
            return None

    def get_user_narrative_style(self, user_id: str) -> Optional[str]:
        """Retrieve user's preferred narrative style from history.

        Args:
            user_id: The user identifier

        Returns:
            User's narrative style preference, or None
        """
        if not self.is_available():
            return None

        try:
            results = self.memory.search(
                query="What is this user's preferred narrative writing style, tone, or genre?",
                user_id=user_id,
                limit=3,
            )

            if results and results.get("results"):
                first_result = results["results"][0]
                return first_result.get("memory")

            return None
        except Exception as exc:
            logger.warning("Failed to retrieve narrative style: %s", exc)
            return None

    def find_similar_projects(
        self, query: str, user_id: str, limit: int = 3
    ) -> List[Dict[str, Any]]:
        """Find similar past projects for inspiration.

        Args:
            query: Description of what to search for
            user_id: The user identifier
            limit: Maximum number of results to return

        Returns:
            List of similar project memories
        """
        if not self.is_available():
            return []

        try:
            results = self.memory.search(query=query, user_id=user_id, limit=limit)
            return results.get("results", [])
        except Exception as exc:
            logger.warning("Failed to find similar projects: %s", exc)
            return []

    def store_creative_prompt(
        self, user_id: str, prompt: str, context: str, was_helpful: bool = True
    ) -> None:
        """Store a creative prompt that was generated, for learning.

        Args:
            user_id: The user identifier
            prompt: The creative prompt that was generated
            context: Context about when/why this prompt was created
            was_helpful: Whether the prompt was helpful (for future learning)
        """
        if not self.is_available():
            return

        try:
            messages = [
                {
                    "role": "assistant",
                    "content": (
                        f"Generated creative prompt: '{prompt}'. "
                        f"Context: {context}. "
                        f"Helpful: {was_helpful}"
                    ),
                }
            ]

            self.memory.add(
                messages,
                user_id=user_id,
                metadata={"type": "creative_prompt", "helpful": was_helpful},
            )
            logger.info("Stored creative prompt for user %s", user_id)
        except Exception as exc:
            logger.warning("Failed to store creative prompt: %s", exc)

    def get_all_memories(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all memories for a user.

        Args:
            user_id: The user identifier

        Returns:
            List of all memories
        """
        if not self.is_available():
            return []

        try:
            results = self.memory.get_all(user_id=user_id)
            return results if results else []
        except Exception as exc:
            logger.warning("Failed to get all memories: %s", exc)
            return []

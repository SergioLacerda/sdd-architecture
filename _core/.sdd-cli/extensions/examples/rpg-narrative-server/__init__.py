"""
SDD Extension: RPG Narrative Server

Specialized SDD constitution for narrative-focused RPG backend systems.
Focuses on storytelling, dialogue systems, and quest architectures.
"""

from typing import List
from pathlib import Path
import sys

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from framework.extension_framework import (
    BaseExtension,
    CustomMandate,
    CustomGuideline,
    ExtensionMetadata,
    Category,
)


class Extension(BaseExtension):
    """RPG Narrative Server Extension"""
    
    metadata = ExtensionMetadata(
        name="RPG Narrative Server",
        version="1.0.0",
        author="SDD Community",
        description="Architecture for RPG narrative systems with dialogue trees, branching quests, and dialogue generation",
        domain="rpg-narrative-server",
        dependencies=["pydantic>=2.0", "fastapi>=0.95.0", "anthropic>=0.7.0"],
        license="MIT"
    )
    
    mandates: List[CustomMandate] = [
        CustomMandate(
            id="RPGM001",
            type="HARD",
            title="Dialogue Consistency",
            description="All NPC dialogue MUST be consistent with character history, relationships, and knowledge state. No contradictions across sessions.",
            category=Category.GENERAL.value,
            domain="rpg-narrative-server",
            rationale="Players notice and punish narrative inconsistencies, breaking immersion",
            validation_commands=["pytest tests/dialogue_consistency", "nlp_validator --check-coherence"],
            metadata={
                "severity": "critical",
                "immersion_impact": "high",
            }
        ),
        CustomMandate(
            id="RPGM002",
            type="HARD",
            title="Quest State Machine",
            description="Every quest MUST have defined states (inactive, active, progressed, completed, failed) with explicit transition rules.",
            category=Category.ARCHITECTURE.value,
            domain="rpg-narrative-server",
            rationale="Prevents quest breaking, enables rollback on error",
            validation_commands=["pytest tests/quest_states", "graph_validator --check-dag"],
            metadata={
                "severity": "high",
                "states": ["inactive", "active", "progressed", "completed", "failed"],
            }
        ),
    ]
    
    guidelines: List[CustomGuideline] = [
        CustomGuideline(
            id="RPGG01",
            type="SOFT",
            title="Dialogue Tree Branching",
            description="Design dialogue trees with maximum depth of 5 levels. Provide 2-4 options per node.",
            category=Category.GENERAL.value,
            domain="rpg-narrative-server",
            examples=[
                "Root: NPC greeting → [Listen, Ask, Refuse]",
                "Level 1: Each choice → [Continue, Ask different, Leave]",
                "Level 2-5: Natural conversation flow"
            ],
            metadata={
                "ux_consideration": "prevent choice paralysis",
                "performance": "O(1) dialogue lookup"
            }
        ),
        CustomGuideline(
            id="RPGG02",
            type="SOFT",
            title="Character Relationship Tracking",
            description="Maintain relationship scores (-100 to +100) for each NPC-Player pair. Store dialogue history.",
            category=Category.GENERAL.value,
            domain="rpg-narrative-server",
            examples=[
                "Relationship increased by +5 when helping NPC",
                "Dialogue history influences future conversations",
                "NPCs remember player actions from previous sessions"
            ],
            related_mandate="RPGM001",
            metadata={
                "emotional_depth": "enables player agency",
                "storage_model": "relational"
            }
        ),
        CustomGuideline(
            id="RPGG03",
            type="SOFT",
            title="Quest Reward Balancing",
            description="Align quest rewards with effort required. Scale by difficulty and progression tier.",
            category=Category.PERFORMANCE.value,
            domain="rpg-narrative-server",
            examples=[
                "Early quests: 100-500 XP",
                "Mid-game: 500-2000 XP",
                "Difficult optional: up to 5000 XP",
                "Legendary quests: 10000+ XP + rare items"
            ],
            metadata={
                "game_design": "prevents grind frustration",
                "economy": "balanced progression"
            }
        ),
        CustomGuideline(
            id="RPGG04",
            type="SOFT",
            title="Narrative Continuity",
            description="Ensure quest outcomes and world state changes persist across all future interactions.",
            category=Category.GENERAL.value,
            domain="rpg-narrative-server",
            examples=[
                "Defeated quest boss stays defeated",
                "Accepted quest shows in active quest log",
                "NPC comments on previously completed quests",
                "World reflects plot progression"
            ],
            related_mandate="RPGM002",
            metadata={
                "player_experience": "critical",
                "storage": "event-sourced"
            }
        ),
    ]
    
    def initialize(self) -> None:
        """Initialize the RPG Narrative Server extension"""
        # Could load dialogue models, quest templates, etc.
        pass
    
    def validate(self) -> List[str]:
        """Validate the extension"""
        errors = []
        
        # Validate all mandates
        for mandate in self.mandates:
            errors.extend(mandate.validate())
        
        # Validate all guidelines
        for guideline in self.guidelines:
            errors.extend(guideline.validate())
        
        return errors


if __name__ == "__main__":
    # Test the extension
    ext = Extension()
    errors = ext.validate()
    
    if not errors:
        print(f"✅ {ext.metadata.name} v{ext.metadata.version}")
        print(f"   Domain: {ext.metadata.domain}")
        print(f"   Mandates: {len(ext.mandates)}")
        print(f"   Guidelines: {len(ext.guidelines)}")
    else:
        print("❌ Validation failed:")
        for error in errors:
            print(f"   - {error}")

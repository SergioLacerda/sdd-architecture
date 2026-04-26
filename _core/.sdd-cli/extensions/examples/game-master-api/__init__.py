"""
SDD Extension: Game Master API

Specialized SDD constitution for game master systems.
Defines mandates and guidelines for narrative-driven backend systems.
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
    """Game Master API Extension"""
    
    metadata = ExtensionMetadata(
        name="Game Master API",
        version="1.0.0",
        author="SDD Community",
        description="Specialized architecture for game master backend systems with narrative engines",
        domain="game-master-api",
        dependencies=["pydantic>=2.0", "fastapi>=0.95.0"],
        license="MIT"
    )
    
    mandates: List[CustomMandate] = [
        CustomMandate(
            id="GMM001",
            type="HARD",
            title="Narrative State Persistence",
            description="All narrative state (game world, character relationships, plot threads) MUST be persisted to database with versioning. No in-memory-only state.",
            category=Category.ARCHITECTURE.value,
            domain="game-master-api",
            rationale="Allows pausing/resuming games, supports multiple DMs, enables event replay",
            validation_commands=["pytest tests/state_persistence", "mypy app/state_engine.py"],
            metadata={
                "severity": "critical",
                "impact": "game-breaking if violated",
                "examples": ["SQLAlchemy models for game state", "Event sourcing patterns"]
            }
        ),
        CustomMandate(
            id="GMM002",
            type="HARD",
            title="Real-Time Synchronization",
            description="Game state changes MUST sync to all connected clients within 100ms using WebSocket broadcast.",
            category=Category.PERFORMANCE.value,
            domain="game-master-api",
            rationale="Players expect immediate feedback on world changes",
            validation_commands=["pytest tests/realtime_sync", "load_test --concurrency=50"],
            metadata={
                "severity": "high",
                "latency_target_ms": 100,
            }
        ),
    ]
    
    guidelines: List[CustomGuideline] = [
        CustomGuideline(
            id="GMG01",
            type="SOFT",
            title="Random Outcome Generation",
            description="Use cryptographically secure RNG for all game randomization. Never hardcode probability distributions.",
            category=Category.SECURITY.value,
            domain="game-master-api",
            examples=[
                "Use secrets.randbelow() for Python",
                "Avoid random.randint() for game mechanics",
                "Consider mersenne twister for reproducibility"
            ],
            related_mandate="GMM001"
        ),
        CustomGuideline(
            id="GMG02",
            type="SOFT",
            title="NPC Behavior Trees",
            description="Implement NPC behaviors using behavior trees. Each node should have clear preconditions and effects.",
            category=Category.GENERAL.value,
            domain="game-master-api",
            examples=[
                "Sequence nodes for multi-step behaviors",
                "Parallel nodes for simultaneous actions",
                "Decorator nodes for behavior modification"
            ],
            metadata={
                "complexity": "medium",
                "reusability": "high"
            }
        ),
        CustomGuideline(
            id="GMG03",
            type="SOFT",
            title="Event Sourcing Pattern",
            description="Store all game events in event log. Use event replay to reconstruct state at any point.",
            category=Category.ARCHITECTURE.value,
            domain="game-master-api",
            examples=[
                "PlayerMoved event with coordinates",
                "NPCSpawned event with properties",
                "PlotPointTriggered event with consequences"
            ],
            metadata={
                "pattern": "event-sourcing",
                "benefits": ["time travel debugging", "audit trail", "replay testing"]
            }
        ),
    ]
    
    def initialize(self) -> None:
        """Initialize the Game Master API extension"""
        # Could load additional configuration or data
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

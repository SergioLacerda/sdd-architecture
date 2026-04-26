"""
SDD v3.1 Extension Framework - Core Components

Allows users to create custom mandates and guidelines for domain-specific specializations.
Built with Pydantic for schema validation and plugin discovery.

Example:
    >>> from sdd_extensions.framework import CustomExtension, ExtensionRegistry
    >>> 
    >>> @CustomExtension.register("my-domain")
    >>> class MyDomainExtension:
    ...     mandates = [...]
    ...     guidelines = [...]
    >>> 
    >>> registry = ExtensionRegistry()
    >>> extensions = registry.load_all()
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class ItemType(str, Enum):
    """SDD item type enumeration"""
    MANDATE = "mandate"
    GUIDELINE = "guideline"


class Category(str, Enum):
    """Standard SDD categories"""
    ARCHITECTURE = "architecture"
    GENERAL = "general"
    PERFORMANCE = "performance"
    SECURITY = "security"
    GIT = "git"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    NAMING = "naming"
    CODE_STYLE = "code-style"


@dataclass
class CustomMandate:
    """Base class for custom mandates in specialized domains"""
    id: str
    type: str  # "HARD" or "SOFT"
    title: str
    description: str
    category: str = Category.GENERAL.value
    domain: Optional[str] = None
    rationale: Optional[str] = None
    validation_commands: Optional[List[str]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def validate(self) -> List[str]:
        """Validate mandate structure"""
        errors = []

        if not self.id:
            errors.append("Mandate ID cannot be empty")

        if not self.type or self.type not in ["HARD", "SOFT"]:
            errors.append(f"Invalid type: {self.type} (must be HARD or SOFT)")

        if not self.title or len(self.title.strip()) == 0:
            errors.append("Mandate title cannot be empty")

        if not self.description or len(self.description.strip()) == 0:
            errors.append("Mandate description cannot be empty")

        if self.category not in [c.value for c in Category]:
            errors.append(f"Invalid category: {self.category}")

        return errors

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "domain": self.domain,
            "rationale": self.rationale,
            "validation_commands": self.validation_commands,
            "metadata": self.metadata,
        }


@dataclass
class CustomGuideline:
    """Base class for custom guidelines in specialized domains"""
    id: str
    type: str  # "HARD" or "SOFT"
    title: str
    category: str = Category.GENERAL.value
    domain: Optional[str] = None
    description: Optional[str] = None
    examples: Optional[List[str]] = None
    related_mandate: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def validate(self) -> List[str]:
        """Validate guideline structure"""
        errors = []

        if not self.id:
            errors.append("Guideline ID cannot be empty")

        if not self.type or self.type not in ["HARD", "SOFT"]:
            errors.append(f"Invalid type: {self.type} (must be HARD or SOFT)")

        if not self.title or len(self.title.strip()) == 0:
            errors.append("Guideline title cannot be empty")

        if self.category not in [c.value for c in Category]:
            errors.append(f"Invalid category: {self.category}")

        return errors

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "category": self.category,
            "domain": self.domain,
            "description": self.description,
            "examples": self.examples,
            "related_mandate": self.related_mandate,
            "metadata": self.metadata,
        }


class ExtensionMetadata:
    """Metadata for extension packages"""

    def __init__(self,
                 name: str,
                 version: str,
                 author: str,
                 description: str,
                 domain: str,
                 dependencies: Optional[List[str]] = None,
                 license: str = "MIT"):
        self.name = name
        self.version = version
        self.author = author
        self.description = description
        self.domain = domain
        self.dependencies = dependencies or []
        self.license = license

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "version": self.version,
            "author": self.author,
            "description": self.description,
            "domain": self.domain,
            "dependencies": self.dependencies,
            "license": self.license,
        }


class BaseExtension(ABC):
    """Base class for all SDD extensions"""

    # Subclasses must define these
    metadata: ExtensionMetadata
    mandates: List[CustomMandate] = []
    guidelines: List[CustomGuideline] = []

    @abstractmethod
    def initialize(self) -> None:
        """Initialize extension - called on load"""
        pass

    @abstractmethod
    def validate(self) -> List[str]:
        """Validate extension structure"""
        pass

    def get_mandates(self) -> List[CustomMandate]:
        """Get all mandates from this extension"""
        return self.mandates

    def get_guidelines(self) -> List[CustomGuideline]:
        """Get all guidelines from this extension"""
        return self.guidelines

    def to_dict(self) -> Dict[str, Any]:
        """Convert extension to dictionary"""
        return {
            "metadata": self.metadata.to_dict(),
            "mandates": [m.to_dict() for m in self.mandates],
            "guidelines": [g.to_dict() for g in self.guidelines],
        }


class ExtensionRegistry:
    """Registry for managing SDD extensions"""

    def __init__(self):
        self.extensions: Dict[str, BaseExtension] = {}
        self.errors: List[str] = []

    def register(self, domain: str, extension: BaseExtension) -> bool:
        """Register an extension"""
        validation_errors = extension.validate()

        if validation_errors:
            self.errors.extend([f"{domain}: {e}" for e in validation_errors])
            return False

        self.extensions[domain] = extension
        return True

    def get(self, domain: str) -> Optional[BaseExtension]:
        """Get extension by domain"""
        return self.extensions.get(domain)

    def get_all(self) -> Dict[str, BaseExtension]:
        """Get all registered extensions"""
        return self.extensions.copy()

    def get_mandates(self, domain: Optional[str] = None) -> List[CustomMandate]:
        """Get all mandates, optionally filtered by domain"""
        mandates = []

        if domain:
            ext = self.get(domain)
            if ext:
                mandates = ext.get_mandates()
        else:
            for ext in self.extensions.values():
                mandates.extend(ext.get_mandates())

        return mandates

    def get_guidelines(self, domain: Optional[str] = None) -> List[CustomGuideline]:
        """Get all guidelines, optionally filtered by domain"""
        guidelines = []

        if domain:
            ext = self.get(domain)
            if ext:
                guidelines = ext.get_guidelines()
        else:
            for ext in self.extensions.values():
                guidelines.extend(ext.get_guidelines())

        return guidelines

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about registered extensions"""
        total_mandates = sum(len(ext.get_mandates()) for ext in self.extensions.values())
        total_guidelines = sum(len(ext.get_guidelines()) for ext in self.extensions.values())

        return {
            "total_extensions": len(self.extensions),
            "domains": list(self.extensions.keys()),
            "total_mandates": total_mandates,
            "total_guidelines": total_guidelines,
            "errors": len(self.errors),
        }


# Global registry
_global_registry: Optional[ExtensionRegistry] = None


def get_registry() -> ExtensionRegistry:
    """Get or create global extension registry"""
    global _global_registry
    if _global_registry is None:
        _global_registry = ExtensionRegistry()
    return _global_registry


def register_extension(domain: str, extension: BaseExtension) -> bool:
    """Register extension in global registry"""
    registry = get_registry()
    return registry.register(domain, extension)


def get_extension(domain: str) -> Optional[BaseExtension]:
    """Get extension from global registry"""
    registry = get_registry()
    return registry.get(domain)


if __name__ == "__main__":
    # Example usage
    print("SDD Extension Framework")
    print("=" * 50)

    # Create example mandate
    mandate = CustomMandate(
        id="DM001",
        type="HARD",
        title="Domain-Specific Architecture",
        description="Custom architecture rules",
        category=Category.ARCHITECTURE.value,
        domain="example",
    )

    errors = mandate.validate()
    if not errors:
        print("✅ Mandate valid")
        print(f"  {mandate.title}")
    else:
        print("❌ Mandate invalid")
        for error in errors:
            print(f"  - {error}")

    # Create example guideline
    guideline = CustomGuideline(
        id="DG001",
        type="SOFT",
        title="Domain-Specific Coding Standard",
        category=Category.CODE_STYLE.value,
        domain="example",
        description="Custom coding standards",
    )

    errors = guideline.validate()
    if not errors:
        print("✅ Guideline valid")
        print(f"  {guideline.title}")
    else:
        print("❌ Guideline invalid")
        for error in errors:
            print(f"  - {error}")

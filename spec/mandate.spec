# SDD v3.0 - MANDATE Specification
# Generated from v2.1 constitution
# Generated: 2026-04-21T17:55:17.894942

mandate M001 {
  type: HARD
  title: "Clean Architecture"
  description: "All systems must implement 8-layer Clean Architecture"
  category: architecture
  rationale: "Foundation enables testability and replaceability"
  validation: {
    commands: [
      "pytest tests/architecture/ -v",
    ]
  }
}

mandate M002 {
  type: HARD
  title: "Test-Driven Development"
  description: "All code must be written using TDD (tests first)"
  category: testing
  rationale: "Ensures quality and design clarity"
  validation: {
    commands: [
      "pytest --cov",
    ]
  }
}

# SDD v3.0 - MANDATE Specification (Expected output from v2_sample.md)

mandate M001 {
  type: HARD
  title: "Clean Architecture"
  description: "All systems must implement 8-layer Clean Architecture."
  category: architecture
  rationale: "Foundation enables testability and replaceability"
  validation: {
    commands: [
      "pytest tests/architecture/test_layers.py -v",
    ]
  }
}

mandate M002 {
  type: HARD
  title: "Test-Driven Development"
  description: "All code must be written using TDD (tests first)."
  category: testing
  rationale: "TDD ensures design clarity and prevents regressions."
  validation: {
    commands: [
      "pytest --cov",
      "pytest --cov-report=term-missing",
    ]
  }
}

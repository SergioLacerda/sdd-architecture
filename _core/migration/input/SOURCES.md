# v2.1 Sources Being Migrated

## Files

| Path | Content | Lines | To v3.0 |
|------|---------|-------|---------|
| EXECUTION/spec/CANONICAL/rules/constitution.md | 15 principles (MANDATE) | ~800 | .sdd-core/CANONICAL/mandate.spec |
| EXECUTION/spec/guides/ | Guidelines (SOFT) | ~300 | .sdd-guidelines/guidelines.dsl |
| EXECUTION/spec/CANONICAL/decisions/ADR-*.md | Architecture records | ~200 | Kept as reference |

## Total Content

- **15 MANDATE items** (HARD rules, non-negotiable)
- **10+ GUIDELINES items** (SOFT patterns, customizable)
- **0 items** to be discarded (100% preserved)

## Migration Mapping

```
v2.1 Structure                    v3.0 Structure
────────────────────────          ──────────────
EXECUTION/spec/                   .sdd/
└── CANONICAL/                    ├── .sdd-core/
    ├── rules/                    │   └── CANONICAL/
    │   └── constitution.md       │       └── mandate.spec (compiled)
    └── guides/                   └── .sdd-guidelines/
                                      └── guidelines.dsl
```

## Extraction Roadmap

- [x] Identify source files
- [ ] Extract MANDATE (15 items)
- [ ] Extract GUIDELINES (10+ items)
- [ ] Convert to DSL format
- [ ] Validate content parity
- [ ] Move to final location

# SPECIALIZATIONS CONFIG — game-master-api Project

**Project:** game-master-api  
**Domain:** Game Master assistance and campaign orchestration  
**Status:** Test project for SPECIALIZATIONS validation  

---

## Project Parameters

```
PROJECT_NAME=game-master-api
LANGUAGE=python
ASYNC_FRAMEWORK=fastapi
MAX_CONCURRENT_ENTITIES=200
PRIMARY_DOMAIN_OBJECTS=campaigns,encounters,npcs,quest_chains
TEAM_SIZE=3
MATURITY_LEVEL=alpha
```

---

## Domain Specialization

**Unlike rpg-narrative-server (narrative-focused):**
- ✅ Focus: Campaign orchestration + encounter management
- ✅ Primary entities: Campaigns, Encounters, NPCs, Quest Chains
- ✅ Concurrency model: 200 simultaneous active games (vs 50 in rpg-narrative-server)
- ✅ Scale: Multi-tenant (supports many parallel GMs)

**Constraints:**
- Max concurrent campaigns: 200
- Max NPCs per encounter: 50
- Max quest chains per campaign: 100
- Response time SLO: < 200ms (vs 100ms in narrative-focused)

---

## Architecture Specialization

**Layer assignments (different from rpg-narrative-server):**

Domain Layer:
- Campaign entity (orchestration logic)
- Encounter entity (encounter progression)
- NPC entity (character management)
- QuestChain entity (quest logic)

Application Layer:
- RunEncounterUseCase
- OrchestrateCampaignUseCase
- ManageNPCsUseCase
- ResolveQuestUseCase

Infrastructure (same as rpg-narrative-server):
- PostgreSQL (persistence)
- Redis (caching, concurrent session mgmt)
- LLM adapter (for NPC dialogue)
- MessageBus (Blinker async)

---

## Validation Checklist

When specializations are generated, verify:

- [ ] Constitution constraints include: "Max 200 concurrent entities"
- [ ] ia-rules.md adapted to 200-entity scale
- [ ] Thread isolation rules applied to multi-tenant model
- [ ] Ports defined for: Campaign, Encounter, NPC, QuestChain
- [ ] ADRs referenced (should match rpg-narrative-server core ADRs)
- [ ] Testing patterns match 200-entity scale
- [ ] Documentation includes game-master-api context

---

**Generated:** 2026-04-19 (Test project)  
**Status:** Test configuration (validates scalability pattern)

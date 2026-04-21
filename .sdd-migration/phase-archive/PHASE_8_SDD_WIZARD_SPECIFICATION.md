# SDD Wizard - Implementation Roadmap

## 🎯 Objetivo

Criar um wizard que automaticamente:
1. **Detecta** o tipo de projeto (Python, Node, Go, etc)
2. **Analisa** a estrutura existente
3. **Gera** mandates e guidelines específicos do projeto
4. **Instrumento** com coleta de telemetry
5. **Pronto** para coleta de dados reais

---

## 📋 Phase 1: SDD Wizard Core (Week 2-3)

### 1.1 Project Type Detection

```python
class ProjectDetector:
    """Identifica tipo e tecnologias do projeto"""
    
    def detect(project_path: str) -> ProjectInfo:
        """
        Returns:
            ProjectInfo{
                type: "python" | "node" | "go" | "java" | "rust"
                frameworks: ["fastapi", "sqlalchemy", "pytest"]
                scale: {"files": 150, "lines": 15000, "packages": 24}
                metadata: {"main_file": "main.py", ...}
            }
        """
        # Check for signatures:
        # Python: requirements.txt, setup.py, pyproject.toml
        # Node: package.json, yarn.lock, pnpm-lock.yaml
        # Go: go.mod, go.sum
        # Java: pom.xml, build.gradle, settings.gradle
        # Rust: Cargo.toml, Cargo.lock
```

**Implementation:**
```python
# File: sdd-wizard/detectors/project_detector.py

SIGNATURES = {
    "python": {
        "files": ["requirements.txt", "setup.py", "pyproject.toml", "Pipfile"],
        "imports": ["import", "from"],  # in Python files
        "frameworks": {
            "fastapi": "from fastapi import",
            "django": "from django import",
            "flask": "from flask import",
            "sqlalchemy": "from sqlalchemy import",
            "pytest": "import pytest",
            "asyncio": "import asyncio",
        }
    },
    "node": {
        "files": ["package.json"],
        "frameworks": {
            "express": '"express"',
            "fastify": '"fastify"',
            "nestjs": '"@nestjs/',
            "react": '"react"',
            "jest": '"jest"',
        }
    },
    "go": {
        "files": ["go.mod", "go.sum"],
        "frameworks": {
            "gin": 'github.com/gin-gonic/gin',
            "fiber": 'github.com/gofiber/fiber',
            "gorm": 'gorm.io',
        }
    }
}
```

### 1.2 Code Structure Analysis

```python
class ArchitectureAnalyzer:
    """Analisa estrutura e padrões de arquitetura"""
    
    def analyze(project_path: str) -> ArchitectureMetrics:
        """
        Retorna:
        {
            "services": 3,
            "modules": 15,
            "layers": ["api", "business", "data"],
            "patterns_detected": [
                "MVC", "Repository", "Dependency Injection"
            ],
            "violations": [
                {"type": "circular_import", "modules": ["A", "B"]},
                {"type": "missing_layer", "layer": "business"}
            ]
        }
        """
```

### 1.3 Template Selection & Generation

```python
class MandateGenerator:
    """Gera mandates específicos do projeto"""
    
    def generate(
        project_info: ProjectInfo,
        architecture: ArchitectureMetrics
    ) -> List[Mandate]:
        """
        Exemplo: Para FastAPI + SQLAlchemy
        
        M001: Clean Architecture - Separate API, Business, Data Layers
        M002: Async/Await - Use async for all I/O operations
        M003: Test Coverage - Minimum 85% code coverage
        M004: Error Handling - Consistent exception handling strategy
        M005: Database Access - Always use repository pattern
        ...
        
        Baseado em:
        - Tecnologias detectadas (FastAPI → async/await important)
        - Padrões existentes (já tem repository → validar)
        - Best practices da comunidade (FastAPI guidelines)
        """
```

### 1.4 Telemetry Instrumentation

```python
class TelemetryInstrumentor:
    """Adiciona hooks de coleta de telemetry"""
    
    def instrument(project_path: str, project_type: str):
        """
        Para Python FastAPI:
        
        1. Create telemetry_collector.py
        2. Add middleware to app:
           app.add_middleware(SDDTelemetryMiddleware)
        3. Create event models:
           - RequestEvent, ResponseEvent, ErrorEvent
        4. Setup aggregator:
           - Collect events in rotating buffer
           - Send to analyzer every 1 hour
           - Store locally in .sdd/telemetry/
        """
```

---

## 📊 Phase 2: Implementation Details

### Step 1: Create Wizard Entry Point

```bash
# File: sdd-wizard/cli.py

$ python -m sdd_wizard --target /path/to/project

Interactive Menu:
  1. Auto-detect project (Default)
  2. Manual project selection
  3. Use template
  4. Configure options
  5. Run wizard

================

Auto-detecting project...
✓ Detected: Python FastAPI
✓ Found: 3 services, 15 modules
✓ Frameworks: FastAPI, SQLAlchemy, pytest
✓ Scale: 150 files, 15,000 lines

Proceeding with FastAPI template...

================

Generating SDD specialization...
✓ Created 10 mandates (M001-M010)
✓ Created 25 guidelines (G01-G25)
✓ Generated .sdd/mandates.spec
✓ Generated .sdd/guidelines.dsl
✓ Ready for instrumentation

Setup telemetry hooks? (y/n): y

✓ Created telemetry_collector.py
✓ Modified app to add middleware
✓ Events will be stored in .sdd/telemetry/

Ready! Run your app with:
  $ python main.py

Telemetry will be collected in .sdd/telemetry/
```

### Step 2: Generate Project-Specific Mandates

```markdown
# Example Output: .sdd/mandates.spec

ID: M001
NAME: Clean Architecture
PRIORITY: CRITICAL
DESCRIPTION: |
  FastAPI application must maintain clean architecture with clear separation:
  - API Layer: Route handlers and request validation
  - Business Layer: Use cases and business logic
  - Data Layer: Database operations and repositories
  
VALIDATION:
  - No direct database calls in API handlers
  - No business logic in route definitions
  - All data access through repository pattern

---

ID: M002
NAME: Async/Await Standards
PRIORITY: CRITICAL
DESCRIPTION: |
  All I/O operations must use async/await pattern
  
VALIDATION:
  - Database queries: async def query()
  - External API calls: async with httpx.AsyncClient()
  - Background tasks: FastAPI.background_tasks
  
---

ID: M003
NAME: Test Coverage
PRIORITY: HIGH
DESCRIPTION: |
  Minimum 85% code coverage required
  
VALIDATION:
  - pytest --cov=. --cov-fail-under=85
  - All critical paths tested
  - Edge cases covered
```

### Step 3: Telemetry Collection Setup

```python
# File: generated .sdd/telemetry_collector.py

from fastapi import FastAPI
from datetime import datetime
import json
from pathlib import Path

class SDDTelemetryMiddleware:
    def __init__(self, app):
        self.app = app
        self.events = []
        self.telemetry_dir = Path(".sdd/telemetry")
        self.telemetry_dir.mkdir(parents=True, exist_ok=True)
        
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
            
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "method": scope["method"],
            "path": scope["path"],
            "client": scope["client"][0] if scope.get("client") else None,
        }
        
        # Track response
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                event["status"] = message["status"]
                event["headers"] = dict(message.get("headers", []))
            await send(message)
        
        await self.app(scope, receive, send_wrapper)
        
        # Store event
        self._store_event(event)
        
    def _store_event(self, event):
        self.events.append(event)
        
        # Flush every 1000 events or every hour
        if len(self.events) >= 1000:
            self._flush()
    
    def _flush(self):
        """Save events to file"""
        filename = self.telemetry_dir / f"events_{datetime.utcnow().isoformat()}.jsonl"
        with open(filename, "w") as f:
            for event in self.events:
                f.write(json.dumps(event) + "\n")
        self.events = []
```

### Step 4: Metrics Analysis

```python
# File: sdd-wizard/tools/analyze_telemetry.py

class TelemetryAnalyzer:
    def analyze(telemetry_dir: Path) -> AnalysisReport:
        """
        Reads all event files and analyzes:
        
        1. Pattern Coverage
           - Which RTK patterns appeared
           - Frequency of each pattern
           - Coverage percentage
        
        2. Compression
           - Original size vs RTK compressed size
           - Average compression ratio
        
        3. Performance
           - Request latency distribution
           - Error rates
           - Performance impact of instrumentation
        
        4. Compliance
           - Mandates violations found
           - Severity levels
        
        Outputs:
        - analysis-report.md (human readable)
        - metrics.json (structured data)
        - patterns-discovered.md (new patterns found)
        """
```

---

## 🔧 Architecture of Wizard

```
sdd-wizard/
├── __init__.py
├── cli.py                          # Entry point
├── wizard.py                       # Main orchestrator
│
├── detectors/
│   ├── __init__.py
│   ├── project_detector.py         # Identifies project type
│   ├── architecture_analyzer.py    # Analyzes code structure
│   └── signatures.json             # Technology signatures
│
├── generators/
│   ├── __init__.py
│   ├── mandate_generator.py        # Creates M001-M010
│   ├── guideline_generator.py      # Creates G01-G25
│   └── templates/
│       ├── python-fastapi.json
│       ├── python-django.json
│       ├── node-express.json
│       ├── go-gin.json
│       └── java-spring.json
│
├── instrumentors/
│   ├── __init__.py
│   ├── python_instrumentor.py      # Add hooks to Python apps
│   ├── node_instrumentor.py        # Add hooks to Node apps
│   └── go_instrumentor.py          # Add hooks to Go apps
│
├── collectors/
│   ├── __init__.py
│   ├── event_collector.py          # Base event model
│   ├── python_collector.py         # Python ASGI/WSGI middleware
│   └── node_collector.py           # Node.js middleware
│
├── analyzers/
│   ├── __init__.py
│   ├── telemetry_analyzer.py       # Analyze collected events
│   ├── pattern_matcher.py          # Match RTK patterns
│   └── report_generator.py         # Generate reports
│
├── templates/
│   ├── mandates.template
│   ├── guidelines.template
│   ├── collector.template
│   └── analyzer.template
│
└── tests/
    ├── test_detector.py
    ├── test_generators.py
    ├── test_collectors.py
    └── test_analyzers.py
```

---

## 🧪 Test Cases for Wizard

```python
# sdd-wizard/tests/test_wizard.py

class TestProjectDetection:
    def test_detect_python_fastapi():
        # Given: A FastAPI project directory
        # When: Wizard analyzes it
        # Then: Returns ProjectInfo with type="python", frameworks=["fastapi", ...]
        pass
    
    def test_detect_node_express():
        pass
    
    def test_detect_go_gin():
        pass

class TestMandateGeneration:
    def test_generate_fastapi_mandates():
        # Given: Python FastAPI project info
        # When: Generate mandates
        # Then: Returns M001-M010 specific to FastAPI
        pass

class TestTelemetryCollection:
    def test_middleware_captures_requests():
        # Given: Running FastAPI app with middleware
        # When: 100 requests made
        # Then: All 100 events captured
        pass
    
    def test_events_persisted_to_file():
        # Given: Middleware capturing events
        # When: 1000 events collected
        # Then: Flushed to file in .sdd/telemetry/
        pass

class TestPatternMatching:
    def test_identify_uuid_patterns():
        # Given: Events with UUIDs
        # When: Analyzer runs pattern matching
        # Then: Identifies C004 (UUID pattern)
        pass
    
    def test_calculate_compression():
        # Given: 10,000 events
        # When: RTK applied
        # Then: Returns actual compression ratio
        pass
```

---

## 📈 Expected Outputs After Wizard

```
After running wizard, your project has:

.sdd/
├── mandates.spec                  # 10 project-specific mandates
├── guidelines.dsl                 # 25 project-specific guidelines
├── baseline-report.json           # Initial state (before refactoring)
│
├── telemetry/                     # Collected events
│   ├── events_2026-04-21T14:30:00.jsonl
│   ├── events_2026-04-21T15:30:00.jsonl
│   └── events_2026-04-21T16:30:00.jsonl
│
├── config.yaml                    # Wizard configuration
│   ├── project_type: "python"
│   ├── frameworks: ["fastapi", "sqlalchemy"]
│   ├── telemetry_enabled: true
│   └── report_interval: "1h"
│
└── collector_config.json          # Telemetry settings
    ├── capture_headers: true
    ├── buffer_size: 1000
    ├── flush_interval: 3600
    └── storage_path: ".sdd/telemetry"

Your app also modified:
├── main.py                        # Added middleware (FastAPI)
│   # app.add_middleware(SDDTelemetryMiddleware)
│
├── telemetry_collector.py         # NEW: Collection logic
└── .env                           # NEW: Config (optional)
```

---

## 🚀 Next Steps in Sequence

### Week 2: Wizard Foundation
1. **Implement ProjectDetector**
   - [ ] Python detection (requirements.txt, setup.py, pyproject.toml)
   - [ ] Node detection (package.json)
   - [ ] Go detection (go.mod)
   - [ ] Framework identification

2. **Implement Mandate/Guideline Generation**
   - [ ] Create templates for Python-FastAPI
   - [ ] Create templates for Python-Django
   - [ ] Create templates for Node-Express
   - [ ] Template testing (10+ cases)

### Week 2-3: Instrumentation
3. **Implement Telemetry Collectors**
   - [ ] Python FastAPI middleware
   - [ ] Node Express middleware
   - [ ] Event storage to `.sdd/telemetry/`

4. **Implement Wizard CLI**
   - [ ] Interactive menu
   - [ ] Auto-detection flow
   - [ ] Generation flow
   - [ ] Instrumentation flow

### Week 3-4: First Project
5. **Run on Your Project #1**
   - [ ] Detect project type
   - [ ] Generate mandates/guidelines
   - [ ] Instrument with telemetry
   - [ ] Collect baseline metrics
   - [ ] Collect live data (2 weeks)
   - [ ] Analyze results

---

## 💾 Code Structure Example

**ProjectInfo dataclass:**
```python
@dataclass
class ProjectInfo:
    path: str
    type: str  # "python", "node", "go", etc
    name: str
    frameworks: List[str]
    scale: Dict[str, int]  # files, lines, modules
    main_entry: str
    dependencies: List[str]
    
@dataclass
class Mandate:
    id: str
    name: str
    priority: str  # CRITICAL, HIGH, MEDIUM
    description: str
    validation_rules: List[str]
    
@dataclass
class Event:
    timestamp: str
    service: str
    trace_id: str
    status: int
    latency: int
    [other fields...]
```

---

## ✅ Success Criteria

**Wizard v1.0 Ready When:**
- [ ] Detects 4+ project types (Python, Node, Go, Java)
- [ ] Generates 10 mandates per project
- [ ] Generates 25 guidelines per project
- [ ] Collects 10,000+ events reliably
- [ ] 20+ tests passing
- [ ] <2s to analyze a 15k LOC project
- [ ] Works on your actual projects

**Ready for Phase 4:** Real data collection from your projects!

# Performance Optimization Guide

Complete reference for measuring and optimizing SDD Architecture performance.

---

## Quick Performance Check

```bash
# Run benchmarks
python3 tests/performance/benchmark.py

# With verbose output
python3 tests/performance/benchmark.py --verbose

# Save results for tracking
python3 tests/performance/benchmark.py --save
```

---

## Performance Targets

| Operation | Target | Description |
|-----------|--------|-------------|
| Health Check (quick) | <200ms | From cache, compact mode |
| Health Check (full) | <1s | Verbose, all checks |
| Governance Compliance | <500ms | Policy validation |
| Agent Handshake | <2s | All 4 layers, silent mode |
| Quiz Execution | <3s/question | Per question average |

---

## Current Baseline (Phase 5)

Run your own benchmark:

```bash
python3 tests/performance/benchmark.py --verbose
```

Expected output:
```
✓ health_check (quick)       0.047s (target: 0.200s)
✓ health_check (full)        0.892s (target: 1.000s)
✓ governance_compliance      0.312s (target: 0.500s)
✓ agent_handshake            1.456s (target: 2.000s)
✓ quiz_execution             2.341s (target: 3.000s)
```

---

## Optimization Strategies

### 1. Health Check Optimization (<200ms target)

**Current Implementation**:
- 10 checks across 4 categories
- ~50ms per category
- Serial execution

**Optimization 1: Parallel Categories**

```python
# Before (health_check.py)
def run_checks(self):
    self.git_checks()      # 50ms
    self.structure_checks() # 50ms
    self.config_checks()    # 50ms
    self.governance_checks() # 50ms
    # Total: ~200ms

# After: Parallel execution
import concurrent.futures

def run_checks(self):
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(self.git_checks),
            executor.submit(self.structure_checks),
            executor.submit(self.config_checks),
            executor.submit(self.governance_checks),
        ]
        results = [f.result() for f in futures]
    # Total: ~50ms (4x faster!)
```

**Optimization 2: Lazy Governance Checks**

```python
# Skip deep governance checks in quick mode
def governance_checks(self):
    if self.mode == "quick":
        return self._quick_governance_check()  # 5ms
    return self._full_governance_check()       # 45ms

def _quick_governance_check(self):
    # Just check file exists, not JSON validity
    return Path("_core/.sdd/governance-core.json").exists()
```

**Optimization 3: Disk I/O Batching**

```python
# Before: Multiple separate file checks
self.git_exists = Path(".git").exists()      # 1 syscall
self.core_exists = Path("_core").exists()    # 1 syscall
self.health_exists = Path("_core/health_check.py").exists()  # 1 syscall

# After: Batch queries
files_to_check = [".git", "_core", "_core/health_check.py"]
results = {f: Path(f).exists() for f in files_to_check}  # 3 syscalls, batched
```

### 2. Governance Compliance Optimization (<500ms target)

**Current Implementation**:
- Validates 7 policies
- Reads JSON files
- ~300-400ms

**Optimization 1: Multi-level Validation**

```python
# Before (governance_compliance.py)
def validate_all(self):
    results = {}
    for policy in self.policies:
        results[policy] = self._validate_policy(policy)
    return results

# After: Quick vs deep
def validate_all(self, mode="standard"):
    if mode == "quick":
        return self._quick_validate()  # 50ms - just check files exist
    return self._deep_validate()       # 400ms - validate content
```

**Optimization 2: Cache Policy Results**

```python
# Use 5-minute cache instead of re-validating
import hashlib
import time

class PolicyCache:
    def __init__(self):
        self.cache = {}
        self.ttl = 300  # 5 minutes
    
    def validate(self, policy_name):
        if policy_name in self.cache:
            timestamp, result = self.cache[policy_name]
            if time.time() - timestamp < self.ttl:
                return result  # Cache hit, instant
        
        # Cache miss, compute and store
        result = self._compute_validation(policy_name)
        self.cache[policy_name] = (time.time(), result)
        return result
```

### 3. Agent Handshake Optimization (<2s target)

**Current Implementation**:
- 4-layer validation
- Calls health check + governance
- ~1.4-1.6s

**Optimization 1: Parallel Layer Execution**

```python
# Before (agent_handshake.py)
def validate(self):
    layer_1 = self._layer_1_semantic_triggers()  # 100ms
    if not layer_1: return False
    
    layer_2 = self._layer_2_health_check()       # 200ms
    if not layer_2: return False
    
    layer_3 = self._layer_3_governance()         # 400ms
    if not layer_3: return False
    
    layer_4 = self._layer_4_enforcement()        # 100ms
    # Total: ~800ms but sequential

# After: Parallel where possible
def validate(self):
    layer_1 = self._layer_1_semantic_triggers()  # 100ms (required)
    if not layer_1: return False
    
    # Run 2 & 3 in parallel
    with ThreadPoolExecutor(max_workers=2) as executor:
        f2 = executor.submit(self._layer_2_health_check)
        f3 = executor.submit(self._layer_3_governance)
        layer_2, layer_3 = f2.result(), f3.result()
    
    if not (layer_2 and layer_3): return False
    
    layer_4 = self._layer_4_enforcement()        # 100ms
    # Total: ~400ms (2x faster!)
```

**Optimization 2: Cache State Aggressively**

```python
# Extend TTL from 30 minutes to 1 hour for handshake
HANDSHAKE_STATE_TTL = 3600  # 1 hour vs 1800 (30 min)

# Or use tiered cache
if last_check < 5_minutes_ago:
    return cached_result  # No re-validation
elif last_check < 30_minutes_ago:
    return cached_with_quick_check  # Quick validation
else:
    return full_validation  # Re-validate everything
```

### 4. Quiz Optimization (<3s per question)

**Current Implementation**:
- Load all 12 questions
- ~250-300ms per question

**Optimization 1: Lazy Load Questions**

```python
# Before (quiz_executor.py)
def __init__(self):
    self.questions = json.load(open("quiz_questions.json"))  # Load all

# After: Load on demand
def get_next_question(self):
    if self.current_index not in self._loaded:
        self._load_question(self.current_index)  # Load one at a time
    return self.questions[self.current_index]
```

**Optimization 2: Answer Validation Caching**

```python
# Cache answer validation results
answer_cache = {}

def check_answer(self, question_id, answer):
    cache_key = (question_id, answer)
    if cache_key in answer_cache:
        return answer_cache[cache_key]
    
    result = self._validate_answer(question_id, answer)
    answer_cache[cache_key] = result
    return result
```

---

## Benchmarking Results Tracking

### How to Track Performance Over Time

```bash
# Baseline (Phase 5)
python3 tests/performance/benchmark.py --save

# After optimizations
python3 tests/performance/benchmark.py --save

# Compare results
cat tests/performance/benchmark_results.json
```

### Expected Improvements

| Optimization | Expected Improvement |
|--------------|----------------------|
| Parallel health check categories | 3-4x faster (200→50ms) |
| Lazy governance checks | 2x faster (400→200ms) |
| Policy result caching | 5-10x faster (300→30-60ms) |
| Parallel handshake layers | 2x faster (1600→800ms) |
| Lazy quiz loading | 20-30% faster (3000→2100ms) |

---

## Implementation Checklist

- [ ] **Phase 5 Baseline**: Run `python3 tests/performance/benchmark.py` and save
- [ ] **Measure Individual**: Profile each function with timeit
- [ ] **Implement Parallel**: Add ThreadPoolExecutor to health_check.py
- [ ] **Add Caching**: Extend TTL for governance validation
- [ ] **Test Impact**: Re-run benchmarks after each change
- [ ] **Document**: Note improvements in commit message
- [ ] **Monitor**: Add cron job to track performance

### Example: Profile a Function

```python
import timeit

# Profile health check
timer = timeit.Timer("health_check.run_checks()")
time_taken = timer.timeit(number=10) / 10
print(f"Average: {time_taken:.3f}s")
```

---

## Production Monitoring

### Health Check Duration Alert

```bash
# Log duration with each check
python3 _core/health_check.py --verbose 2>&1 | tee -a logs/perf.log

# Alert if > 1s
awk '/SUMMARY/{
    if($NF > 1000) print "ALERT: Health check slow: " $NF "ms"
}' logs/perf.log
```

### Performance Dashboard (Phase 7)

Future implementation will track:
- Health check duration trends
- Compliance validation time
- Agent handshake time
- Cache hit rates
- P95/P99 latencies

---

## Troubleshooting Performance

### Health Check Too Slow

```bash
# 1. Identify which category is slow
python3 _core/health_check.py --category git --verbose
python3 _core/health_check.py --category structure --verbose
python3 _core/health_check.py --category config --verbose
python3 _core/health_check.py --category governance --verbose

# 2. Profile with timing
python3 -m cProfile -s cumulative _core/health_check.py > profile.txt

# 3. Check if I/O bound
# If network drive, consider caching more aggressively
```

### Governance Validation Slow

```bash
# 1. Check JSON file size
ls -lh _core/.sdd/governance-core.json

# 2. Validate JSON performance
python3 -c "
import json
import time
start = time.perf_counter()
json.load(open('_core/.sdd/governance-core.json'))
print(f'{(time.perf_counter()-start)*1000:.1f}ms')
"

# 3. Use quick mode
python3 _core/governance_compliance.py --verify --mode quick
```

---

## Next Steps

1. **Run baseline**: `python3 tests/performance/benchmark.py --save`
2. **Document current**: Note Phase 5 baseline in PERFORMANCE.md
3. **Implement optimizations**: Start with parallel health checks
4. **Verify improvement**: Re-run benchmarks
5. **Monitor production**: Add cron job for ongoing tracking

---

**Last updated**: Phase 5, Step 3  
**Related**: health_check.py, governance_compliance.py, agent_handshake.py, quiz_executor.py

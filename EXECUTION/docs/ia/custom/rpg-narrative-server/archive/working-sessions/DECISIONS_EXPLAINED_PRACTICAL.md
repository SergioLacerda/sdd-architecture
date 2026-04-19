# 🎯 8 DECISÕES — Contexto Prático & Real (April 2026)

**Objetivo:** Explicar cada decisão com PROBLEMAS REAIS que o sistema vai enfrentar

---

## 🚀 VISÃO GERAL: O Que Estamos Decidindo?

**Cenário:** Múltiplas campanhas RPG rodando em paralelo no Discord

```
Player 1 (Thread A): Campanha Medieval (c_medieval_001)
  └─ Está na taverna
  └─ Precisa resolver um mistério
  
Player 2 (Thread B): Campanha Cyberpunk (c_cyber_001)
  └─ Está em um nightclub
  └─ Precisa hackear um servidor
  
Player 3 (Thread C): Campanha Medieval (c_medieval_002)
  └─ Está na mesma taverna (world diferente)
  └─ Diferentes NPCs, mesma ambientação
```

**Problema Central:** Como isolar memoria/contexto de cada campanha para que não "vazem" uma na outra?

---

# 🔴 DECISÃO #1: Lock Strategy (Sincronização entre campanhas)

## ❓ O Problema Real

```python
# Cenário: Dois jogadores começam campanhas ao mesmo tempo
# Thread A (Player 1): container.campaign_scope("c_medieval_001")
# Thread B (Player 2): container.campaign_scope("c_cyber_001")

# Código atual ERRADO:
class CampaignScopedContainer:
    _containers = {}  # Compartilhado entre threads!
    
    def campaign_scope(self, campaign_id):
        # Problema: Thread A e B acessam _containers simultaneamente
        # Podem corromper o dicionário
        if campaign_id not in self._containers:
            self._containers[campaign_id] = self._create()
        # ⚠️ Race condition aqui!
```

## 🔨 Opção A: Simple Lock (RECOMENDADO)

```python
import threading

class CampaignScopedContainer:
    _lock = threading.Lock()  # UMA ÚNICA LOCK para todos
    _containers = {}
    
    def campaign_scope(self, campaign_id):
        # Thread A: Entra, obtém lock
        with self._lock:
            if campaign_id not in self._containers:
                self._containers[campaign_id] = self._create()
            container = self._containers[campaign_id]
        # Lock liberada aqui
        
        # Depois: Thread-local assignment (SEM lock)
        self._local.campaign_id = campaign_id
        
        try:
            yield container
        finally:
            cleanup(campaign_id)

# Timeline:
# t=0.0s: Thread A entra em lock
# t=0.0s: Thread B tenta lock... ESPERA
# t=0.1s: Thread A sai da lock
# t=0.1s: Thread B obtém lock
# t=0.2s: Thread B sai da lock
```

**Quando funciona bem:**
- 5-10 campanhas simultâneas (Discord com alguns servidores)
- Containerização rápida (~10ms)
- Lock tempo total: ~50-100ms para 10 campanhas

**Quando falha:**
- 100+ campanhas simultâneas
- Containerização lenta (processamento pesado)
- Lock vira gargalo

---

## 🔨 Opção B: Per-Campaign Locks

```python
class CampaignScopedContainer:
    _locks = {}      # Lock POR CAMPANHA
    _containers = {}
    
    def campaign_scope(self, campaign_id):
        # Get or create lock for this campaign ONLY
        if campaign_id not in self._locks:
            self._locks[campaign_id] = threading.Lock()
        
        with self._locks[campaign_id]:  # Lock só esta campanha
            if campaign_id not in self._containers:
                self._containers[campaign_id] = self._create()
            container = self._containers[campaign_id]
        
        # Thread A obtém lock de c_medieval_001
        # Thread B obtém lock de c_cyber_001 SIMULTANEAMENTE
        # ✅ Não bloqueia uma pela outra
```

**Quando funciona bem:**
- 100+ campanhas simultâneas
- Escala melhor

**Problema:**
- Código mais complexo
- `_locks` dict TAMBÉM precisa de sincronização
- Overkill para nosso caso

---

## 🎯 RECOMENDAÇÃO: Opção A (Simple Lock)

**Rationale:**
- Discord RPG típico: 5-10 campanhas máximo
- Se crescer → upgrade para B depois
- Código simples, fácil debugar

**Impacto no código:**
```python
# Lines of code: ~5 LOC
self._lock = threading.Lock()

with self._lock:
    if campaign_id not in self._containers:
        self._containers[campaign_id] = self._create()
```

---

# 🟠 DECISÃO #2: Cleanup Timing (Quando liberar memória?)

## ❓ O Problema Real

```python
# Cenário: Uma sessão RPG terminou

Player 1: "Galera, fim da sessão! Até amanhã!"

# Pergunta: O container da campanha c_medieval_001 ainda precisa?
# Se deixar na memória:
#   ✅ Próxima sessão inicia rápido (tá tudo em cache)
#   ❌ Memória fica vazando (100 campanhas = 100 containers em RAM)
#
# Se deletar imediatamente:
#   ✅ Memória limpa
#   ❌ Próxima sessão é lenta (reconstrói tudo)
```

---

## 🔨 Opção A: Automatic on Context Exit (RECOMENDADO)

```python
from contextlib import contextmanager

@contextmanager
def campaign_scope(self, campaign_id):
    self._local.campaign_id = campaign_id
    try:
        yield self._containers[campaign_id]
    finally:
        # AUTOMÁTICO: Sempre executa quando sai do with
        self._cleanup_campaign(campaign_id)

# Uso:
with container_singleton.campaign_scope("c_medieval_001"):
    service = resolve(NarrativeServicePort)
    await service.run_session()
    # Sessão termina...
# ✅ Cleanup automático aqui

# Mesmo se der erro:
try:
    with container_singleton.campaign_scope("c_medieval_001"):
        await service.crash()  # Exception aqui!
except:
    pass
# ✅ Cleanup AINDA acontece (finally block)
```

**Vantagens:**
- ✅ Impossível esquecer cleanup
- ✅ Exception-safe
- ✅ Memória garantida

**Desvantagens:**
- ❌ Rígido (limpa sempre que sai do bloco)

---

## 🔨 Opção B: Explicit Cleanup

```python
# Sem context manager:
container_singleton.use_campaign("c_medieval_001")
service = resolve(NarrativeServicePort)
await service.run_session()
container_singleton.cleanup_campaign("c_medieval_001")

# ❌ Problema: Developer pode esquecer
# ❌ Se der exception antes de cleanup: VAZA
# ❌ Difícil debugar "por que tá lento?"
```

---

## 🔨 Opção C: TTL-Based (Background cleanup)

```python
# Cleanup automático em background
container_singleton._container_ttl = 3600  # 1 hora

async def background_cleanup():
    while True:
        await asyncio.sleep(300)  # Check a cada 5 min
        now = time.time()
        expired = [
            cid for cid, (cont, created) in self._containers.items()
            if (now - created) > self._container_ttl
        ]
        for cid in expired:
            del self._containers[cid]

# Usa-se campaign sem context manager:
container_singleton.use_campaign("c_medieval_001")
await service.run_session()
# Cleanup acontece em background depois de 1 hora

# Problema:
# - Memória pode crescer 1 hora antes de limpar
# - Timing imprevisível
# - Adiciona background task complexity
```

---

## 🎯 RECOMENDAÇÃO: Opção A (Automatic Context Exit)

**Rationale:**
- ✅ Pythonic (with statement)
- ✅ Exception-safe
- ✅ Previsível
- ✅ Nenhuma chance de vazar

**Impacto no código:**
```python
# Context manager padrão Python
# ~10 LOC total (já é pattern comum)

@contextmanager
def campaign_scope(self, campaign_id):
    self._local.campaign_id = campaign_id
    try:
        yield self._containers[campaign_id]
    finally:
        self._cleanup_campaign(campaign_id)
```

---

# 🟡 DECISÃO #3: Error Handling (E se crashar?)

## ❓ O Problema Real

```python
# Cenário: Algo dá ruim durante a sessão

with container_singleton.campaign_scope("c_medieval_001"):
    service = resolve(NarrativeServicePort)
    await service.run_session()
    
    # Oops! API do LLM caiu
    # Exception aqui!
    # E agora? Container vaza? Finalizer limpa? Que acontece?
```

---

## 🔨 Opção A: Accept Leak (NÃO RECOMENDADO)

```python
# Sem proteção alguma:
@contextmanager
def campaign_scope(self, campaign_id):
    self._local.campaign_id = campaign_id
    try:
        yield self._containers[campaign_id]
    finally:
        pass  # NÃO LIMPA

# Cenário: 100 campanhas com erro = 100 containers em RAM PARA SEMPRE
# Server fica lento, depois OOM (Out of Memory), depois CRASH
```

---

## 🔨 Opção B: Finalizer-Based (RECOMENDADO)

```python
import weakref

@contextmanager
def campaign_scope(self, campaign_id):
    container = self._containers[campaign_id]
    
    # Registra "limpar quando garbage collected"
    def cleanup_on_gc():
        print(f"Cleanup {campaign_id} via finalizer")
        self._cleanup_campaign(campaign_id)
    
    weakref.finalize(container, cleanup_on_gc)
    
    self._local.campaign_id = campaign_id
    try:
        yield container
    finally:
        # Cleanup normal caso não der erro
        self._cleanup_campaign(campaign_id)

# Timeline:
# 1. Sessão roda normalmente:
#    - finally block roda, cleanup acontece ✅
#
# 2. Sessão dá erro:
#    - finally block roda, cleanup acontece ✅
#
# 3. Mesmo se finally NÃO rodar (crash extremo):
#    - Python garbage collects container
#    - Finalizer roda cleanup ✅
#
# Proteção em 3 camadas!
```

---

## 🔨 Opção C: Strict Validation

```python
@contextmanager
def campaign_scope(self, campaign_id):
    # Detectar nesting inválido
    if hasattr(self._local, 'campaign_stack') and self._local.campaign_stack:
        raise RuntimeError(
            f"Cannot nest! Already in {self._local.campaign_stack[-1]}"
        )
    
    if not hasattr(self._local, 'campaign_stack'):
        self._local.campaign_stack = []
    
    self._local.campaign_stack.append(campaign_id)
    try:
        yield self._containers[campaign_id]
    finally:
        self._local.campaign_stack.pop()
        self._cleanup_campaign(campaign_id)

# Problema: Valida bem, mas se finalizer não rodar... vaza mesmo assim
```

---

## 🎯 RECOMENDAÇÃO: Opção B (Finalizer)

**Rationale:**
- ✅ Cleanup garantido (3 camadas)
- ✅ Falha gracefully
- ✅ Python idiomatic
- ✅ Sem complexidade extra

**Impacto no código:**
```python
# ~15 LOC para setup finalizer
weakref.finalize(container, cleanup_func)
```

---

# 🟡 DECISÃO #4: Nesting Support (Campanhas dentro de campanhas?)

## ❓ O Problema Real

```python
# Cenário 1: SEQUENCIAL (OK)
with campaign_scope("c_medieval_001"):
    await service.run()
    
with campaign_scope("c_cyber_001"):  # Diferente campanha
    await service.run()

# Cenário 2: NESTED (deve permitir?)
with campaign_scope("c_medieval_001"):
    # Player 1: dentro da campanha medieval
    
    with campaign_scope("c_cyber_001"):
        # Qual campanha é "current"?
        # Medieval ou Cyber?
        service = resolve(NarrativeServicePort)
        await service.run()
        
        # Qual mundo o LLM vê? A Medieval ou a Cyber?
```

---

## 🔨 Opção A: No Nesting (RECOMENDADO)

```python
@contextmanager
def campaign_scope(self, campaign_id):
    # Check: Já estou dentro de uma campanha?
    if hasattr(self._local, 'campaign_id') and self._local.campaign_id:
        raise RuntimeError(
            f"Cannot nest! Already in {self._local.campaign_id}, "
            f"tried {campaign_id}. Use sequential scopes instead."
        )
    
    self._local.campaign_id = campaign_id
    try:
        yield self._containers[campaign_id]
    finally:
        self._cleanup_campaign(campaign_id)
        del self._local.campaign_id

# Uso:
with campaign_scope("c_medieval_001"):
    # OK
    pass

with campaign_scope("c_medieval_001"):
    with campaign_scope("c_cyber_001"):
        # ❌ RuntimeError: Cannot nest!
        pass
```

**Vantagens:**
- ✅ Simples de entender (uma campanha por vez)
- ✅ Impossível confundir qual é "current"
- ✅ Fácil debugar

**Desvantagem:**
- ❌ Não permite casos avançados

---

## 🔨 Opção B: Allow Nesting with Stack

```python
@contextmanager
def campaign_scope(self, campaign_id):
    # Manter stack de campanhas
    if not hasattr(self._local, 'campaign_stack'):
        self._local.campaign_stack = []
    
    self._local.campaign_stack.append(campaign_id)
    try:
        yield self._containers[campaign_id]
    finally:
        self._local.campaign_stack.pop()

# Uso:
with campaign_scope("c_medieval_001"):
    # Stack: [c_medieval_001]
    # resolve() vê medieval
    
    with campaign_scope("c_cyber_001"):
        # Stack: [c_medieval_001, c_cyber_001]
        # resolve() vê cyber (top of stack)
        service = resolve(NarrativeServicePort)
        
    # Stack volta: [c_medieval_001]
    # resolve() vê medieval de novo

# Vantagem: Flexível
# Desvantagem: Confuso (qual campanha vai ser usada?)
```

---

## 🎯 RECOMENDAÇÃO: Opção A (No Nesting)

**Rationale:**
- RPG narrativo é sequencial (um combate por vez)
- Não faz sentido dois jogadores em campanhas diferentes no mesmo thread
- Se precisar: use threads separadas (já temos isso)
- Simples = menos bugs

---

# 🟠 DECISÃO #5: EventBusPort Independence

## ❓ O Problema Real

```python
# Temos dois componentes assíncronos:
# 1. ExecutorPort: Executa tarefas CPU-bound
# 2. EventBusPort: Dispara eventos (narrativos, GameMaster actions)

# Pergunta: São relacionados demais para unificar?
# Ou são separados o suficiente?

class ExecutorPort(Protocol):
    # Tarefa pesada: calcular IA, processar dados
    async def run_sync(self, func: Callable) -> Any
    async def run_async(self, coro: Coroutine) -> Any

class EventBusPort(Protocol):
    # Notificar: "Evento aconteceu!"
    async def publish(self, event: object) -> None
    async def subscribe(self, event_type: type, handler) -> None
```

---

## 🔨 Opção A: Keep Separate (RECOMENDADO)

```python
# DOIS portes independentes

class ExecutorPort(Protocol):
    """Task execution (CPU-bound work)"""
    async def run_sync(self, func) -> Any: ...
    async def run_async(self, coro) -> Any: ...
    async def start(self) -> None: ...
    async def shutdown(self) -> None: ...

class EventBusPort(Protocol):
    """Event dispatch (messaging)"""
    async def publish(self, event: object) -> None: ...
    async def subscribe(self, event_type: type, handler) -> None: ...
    async def start(self) -> None: ...
    async def shutdown(self) -> None: ...

# Container:
container.register(ExecutorPort, ThreadPoolExecutor())
container.register(EventBusPort, BlinkerEventBus())

# Uso:
executor = resolve(ExecutorPort)
event_bus = resolve(EventBusPort)

# CPU work
result = await executor.run_async(heavy_calculation())

# Notificar evento
await event_bus.publish(NarrativeEvent(content="..."))
```

**Vantagens:**
- ✅ Single Responsibility (cada um faz uma coisa)
- ✅ Fácil testar (mock cada um separadamente)
- ✅ Fácil implementar
- ✅ Independente (trocar ExecutorPort não afeta EventBus)

---

## 🔨 Opção B: Consolidate into ExecutorPort

```python
# UM ÚNICO port para tudo

class ExecutorPort(Protocol):
    """Async operations: execution + events"""
    # CPU work
    async def run_sync(self, func) -> Any: ...
    async def run_async(self, coro) -> Any: ...
    
    # Events
    async def publish(self, event: object) -> None: ...
    async def subscribe(self, event_type: type, handler) -> None: ...
    
    # Lifecycle
    async def start(self) -> None: ...
    async def shutdown(self) -> None: ...

# Problema:
# - ExecutorPort faz 3 coisas diferentes (violação SRP)
# - Difícil testar (tudo junto)
# - Difícil mockar (tudo junto)
# - Difícil implementar (um adapter faz muita coisa)
```

---

## 🎯 RECOMENDAÇÃO: Opção A (Keep Separate)

**Rationale:**
- Clean Architecture (Ports & Adapters)
- Single Responsibility
- Testability
- Maintainability

---

# 🟢 DECISÃO #6: Memory Versioning (Como rastrear mudanças?)

## ❓ O Problema Real

```
Cenário: Sistema de "echoes" (anteriores campanhas na nova)

Campanha 1 (semana 1):
├─ Monday: "Hero encontra mapa antigo"
├─ Tuesday: "Hero descobre pista sobre vilão"
├─ Friday: "Hero derrota vilão"

Campanha 2 (semana 2):
├─ Monday: "Novo grupo chega no mesmo town"
├─ Tuesday: "Descobrem ruínas do combate anterior"
├─ Wednesday: "Encontram memória de Campaign 1"

Pergunta: QUANDO foi criada essa memória?
- Era a versão original ou foi modificada depois?
- Se foi modificada: quantas vezes? Por quê?
- Consigo recriar a narrativa EXATAMENTE como era no Monday?
```

---

## 🔨 Opção A: Simple Mutation (NÃO RECOMENDADO)

```json
{
  "id": "event_001",
  "content": "Hero encontra mapa antigo",
  "updated_at": "2026-03-20T20:15:00Z"
}

// Problema:
// - Não sei o que era antes
// - Não consigo reconstruir narrativa histórica
// - Echo system quebrado (aponta para versão errada)
```

---

## 🔨 Opção B: Snapshot Versioning

```json
{
  "id": "event_001",
  "snapshots": [
    {
      "version": 1,
      "content": "Hero encontra mapa antigo",
      "timestamp": "2026-03-15T10:00:00Z"
    },
    {
      "version": 2,
      "content": "Hero encontra mapa antigo (com notas)",
      "timestamp": "2026-03-16T15:30:00Z"
    },
    {
      "version": 3,
      "content": "Hero descobre que mapa é FALSO!",
      "timestamp": "2026-03-20T20:15:00Z"
    }
  ]
}

// Melhor, mas:
// - Não sei qual foi a mudança
// - Não sei o contexto do porquê mudou
// - Coarse-grained (só snapshots, não granular)
```

---

## 🔨 Opção C: Event Sourcing (RECOMENDADO)

```json
{
  "id": "event_001",
  "events": [
    {
      "version": 1,
      "timestamp": "2026-03-15T10:00:00Z",
      "type": "CREATED",
      "actor": "game_engine",
      "content": "Hero encontra mapa antigo",
      "metadata": {}
    },
    {
      "version": 2,
      "timestamp": "2026-03-16T15:30:00Z",
      "type": "UPDATED",
      "actor": "game_master",
      "previous_version": 1,
      "changes": {
        "annotation": "Adicionado nota sobre runas desconhecidas"
      },
      "content": "Hero encontra mapa antigo (com notas)",
      "metadata": {
        "reason": "Ajuste para aumentar dificuldade"
      }
    },
    {
      "version": 3,
      "timestamp": "2026-03-20T20:15:00Z",
      "type": "UPDATED",
      "actor": "game_engine",
      "previous_version": 2,
      "changes": {
        "discovered": "Map was fake! Part of puzzle."
      },
      "content": "Hero descobre que mapa é FALSO!",
      "metadata": {
        "triggered_by": "NPC revelation",
        "player_reaction": "Shocked! Started investigating"
      }
    }
  ],
  "current_version": 3
}

// Agora posso:
// 1. Recriar narrativa no Monday exatamente como era
// 2. Saber cada mudança e por quê
// 3. Auditar (quem fez? quando? por quê?)
// 4. Time-travel queries ("mostre o estado no Monday")
// 5. Echo system perfeito (aponta exatamente qual versão, qual momento)
```

---

## 🎯 RECOMENDAÇÃO: Opção C (Event Sourcing)

**Rationale:**
- ✅ Full audit trail
- ✅ Temporal queries
- ✅ Echo system precisa disso
- ✅ Consistent with business rules

---

# 🟢 DECISÃO #7: Canonical Immutability (Canon pode ser modificado?)

## ❓ O Problema Real

```
Problema: Canon (baseline do mundo) é imutável por design

Mas... E se descobrir um erro? Ou precisar atualizar?

Cenário:
- Canon diz: "Princess é irmã do King"
- Campaign 1 usa isso para 10 sessões
- Campaign 2 começa...
- ... e descobre: "Ops! Deveria ser PRIMA, não irmã!"
- Agora mudar Canon quebra Campaign 1 (echo system inconsistent)
```

---

## 🔨 Opção A: Soft - Warnings Only

```python
async def update_canonical(memory_id: str, new_content: str):
    logger.warning("Modifying canonical - usually not recommended")
    await storage_port.save(memory_id, new_content)

# Problema:
# - Nada impede modificação
# - Easy to accidentally corrupt
// Echo system quebrado silenciosamente
```

---

## 🔨 Opção B: Medium - Audit Trail

```python
async def update_canonical(memory_id: str, new_content: str):
    existing = await storage_port.get(memory_id)
    
    # Log the modification
    audit_log = {
        "original": existing.content,
        "new": new_content,
        "modified_at": now(),
        "modifier": current_user(),
        "reason": input("Why? ")
    }
    await audit_port.log(audit_log)
    
    # Allow modification
    await storage_port.save(memory_id, new_content)

# Melhor (temos auditoria), mas:
// Canon AINDA mudou e quebrou echoes
// Audit log não previne, só documenta
```

---

## 🔨 Opção C: Strict - Immutable (RECOMENDADO)

```python
async def update_canonical(memory_id: str, new_content: str):
    existing = await storage_port.get(memory_id)
    
    if existing.level == "CANONICAL":
        raise ImmutableMemoryError(
            f"Cannot modify canonical memory {memory_id}.\n"
            f"Instead:\n"
            f"1. Create new canonical fact: 'Princess é PRIMA do King'\n"
            f"2. Deprecate old: 'Princess é irmã (DEPRECATED)'\n"
            f"3. Update campaigns to use new fact"
        )
    
    await storage_port.save(memory_id, new_content)

# Resultado:
// - Canon NUNCA muda (após criação)
// - Echo system seguro
// - Se erro: criar novo fact, deprecar antigo
// - Clear enforcement
```

---

## 🎯 RECOMENDAÇÃO: Opção C (Strict Immutable)

**Rationale:**
- ✅ True immutability enforced
- ✅ Echo system integrity
- ✅ Clear error messages
- ✅ Prevents accidents
- ✅ Aligns with business rules

---

# 🟢 DECISÃO #8: Cache Invalidation (Quando limpar cache?)

## ❓ O Problema Real

```
Cenário: Genre cache (compartilhado entre campanhas)

Timestamp: 2026-02-01 10:00 AM
├─ Campaign 1 cria cache genre "cyberpunk":
│   ├─ "Zaibatsus controlam tudo"
│   ├─ "Network é perigosa"
│   └─ "Hackear é crime capital"
└─ Salva em: data/world/genre_cyberpunk/shared_cache/

---

Timestamp: 2026-03-20 02:00 PM (7 semanas depois)
├─ Campaign 2 começa
├─ Precisa de contexto cyberpunk
├─ Encontra cache de 7 semanas atrás
├─ Pergunta: Use?
│   ├─ ✅ Rápido (já tá em cache)
│   ├─ ❌ Mas e se mundo mudou? (admin atualizou canon)
│   └─ ❌ Cache pode estar stale
```

---

## 🔨 Opção A: TTL-Based (Tempo para expirar)

```python
genre_cache = {
    "id": "cyberpunk_cache_001",
    "content": "Zaibatsus controlam tudo",
    "created_at": "2026-02-01T10:00:00Z",
    "ttl_days": 90,
    "expires_at": "2026-05-01T10:00:00Z"
}

# Em Campaign 2:
if genre_cache["expires_at"] < now():
    # Cache expirou (90 dias passaram)
    # Rebuld cache
    new_cache = rebuild_genre_cache("cyberpunk")
else:
    # Cache ainda válido
    use_cached = genre_cache

# Problema:
// - 90 dias é ARBITRÁRIO (por que 90?)
// - Cache pode estar stale ANTES de 90 dias
// - Cache pode ser válido APÓS 90 dias (nada mudou)
```

---

## 🔨 Opção B: Event-Based (Reativo) (RECOMENDADO)

```python
# Subscribe para mudanças no mundo/genre

class WorldChangedEvent:
    world_id: str
    genre_id: str  # Optional
    change_type: str  # "canonical_updated", "genre_config_changed"
    timestamp: datetime

# Event bus emite quando algo muda
await event_bus.publish(
    WorldChangedEvent(
        world_id="world_cyberpunk",
        genre_id="cyberpunk",
        change_type="canonical_updated",
        timestamp=now()
    )
)

# Genre cache escuta
class GenreCacheManager:
    def __init__(self, event_bus):
        event_bus.subscribe(WorldChangedEvent, self.on_world_changed)
    
    async def on_world_changed(self, event):
        if event.genre_id == self.genre_id:
            # Invalidate this genre cache
            await self.invalidate()
            # Will rebuild on next access

# Resultado:
// - Cache invalidado QUANDO mundö muda (não depois)
// - Sem números arbitrários
// - Reactive (event-driven)
// - Campaign 2 sempre vê cache atualizado
```

---

## 🔨 Opção C: Manual Invalidation

```python
# Admin manualmente invalida cache quando precisa

async def admin_invalidate_genre_cache(world_id, genre_id):
    cache_key = f"{world_id}_{genre_id}"
    if cache_key in self._genre_caches:
        del self._genre_caches[cache_key]
    print(f"Cache invalidated for {genre_id}")

# Uso:
# Admin: "Atualizar lore de cyberpunk"
await admin_service.invalidate_cache("world_1", "cyberpunk")
# Cache reconstruído na próxima campanha

// Problema:
// - Requires manual intervention
// - Easy to forget
// - Not automated
```

---

## 🎯 RECOMENDAÇÃO: Opção B (Event-Based)

**Rationale:**
- ✅ Reactive (responds to actual changes)
- ✅ No stale cache unless world actually changed
- ✅ Works with existing EventBusPort
- ✅ Precise invalidation
- ✅ Automated

---

# 📋 RESUMO VISUAL

```
DECISÃO #1: Lock Strategy
├─ Problema: Race condition (2 campanhas simultâneas)
├─ Opção A: Simple lock ← RECOMENDADO
├─ Opção B: Per-campaign locks
└─ Impacto: 5 LOC, 0% overhead típico

DECISÃO #2: Cleanup Timing
├─ Problema: Quando liberar container da memória?
├─ Opção A: Auto (context exit) ← RECOMENDADO
├─ Opção B: Explicit (manual)
├─ Opção C: TTL (background)
└─ Impacto: 10 LOC, garantido memory safety

DECISÃO #3: Error Handling
├─ Problema: E se der crash durante sessão?
├─ Opção A: Accept leak (ruim)
├─ Opção B: Finalizer ← RECOMENDADO
├─ Opção C: Strict validation
└─ Impacto: 15 LOC, 3-camadas de proteção

DECISÃO #4: Nesting Support
├─ Problema: Permitir campanhas aninhadas?
├─ Opção A: No nesting ← RECOMENDADO
├─ Opção B: Stack-based nesting
└─ Impacto: 3 LOC, semântica clara

DECISÃO #5: EventBusPort Independence
├─ Problema: Juntar ExecutorPort + EventBusPort?
├─ Opção A: Keep separate ← RECOMENDADO
├─ Opção B: Consolidate
└─ Impacto: Already designed separately

DECISÃO #6: Memory Versioning
├─ Problema: Rastrear mudanças para echo system
├─ Opção A: Simple mutation (ruim)
├─ Opção B: Snapshots
├─ Opção C: Event sourcing ← RECOMENDADO
└─ Impacto: 50-80 LOC, full audit trail

DECISÃO #7: Canonical Immutability
├─ Problema: Canon pode ser modificado?
├─ Opção A: Soft warnings (ruim)
├─ Opção B: Audit trail
├─ Opção C: Strict immutable ← RECOMENDADO
└─ Impacto: 10 LOC, echo system safe

DECISÃO #8: Cache Invalidation
├─ Problema: Quando refrescar genre cache?
├─ Opção A: TTL (arbitrário)
├─ Opção B: Event-based ← RECOMENDADO
├─ Opção C: Manual (manual)
└─ Impacto: 30-50 LOC, reactive updates
```

---

# ✅ PRÓXIMO PASSO

Agora está claro POR QUE cada decisão?

Confirme:
```
DECISION #1: A
DECISION #2: A
DECISION #3: B
DECISION #4: A
DECISION #5: A
DECISION #6: C
DECISION #7: C
DECISION #8: B
```

Ou se quer ajustar alguma? Qual é a dúvida? 🤔

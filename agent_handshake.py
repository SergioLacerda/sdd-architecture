"""Compatibility shim for legacy `import agent_handshake` usage.

Canonical implementation lives in `tools/governance/agent_handshake.py`.
"""

from tools.governance.agent_handshake import AgentHandshakeProtocol, HandshakeReport, ValidationResult

__all__ = ["AgentHandshakeProtocol", "HandshakeReport", "ValidationResult"]

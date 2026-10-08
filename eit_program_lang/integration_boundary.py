"""
EIT Program Lang V2.7.5
Integration Boundary Declaration

F5: explicit non-claims. This package does NOT establish standalone
integration with CA-Lang, 11D, IFIM, or ASI_OS governance. Declared,
not implied.
"""

from __future__ import annotations

from typing import Any, Dict

from .restored_registry_index import SAFETY_BLOCK


INTEGRATION_BOUNDARY = {
    "ca_lang_integration": "NOT_ESTABLISHED",
    "11d_integration": "NOT_ESTABLISHED",
    "ifim_integration": "NOT_ESTABLISHED",
    "asi_os_governance_integration": "NOT_ESTABLISHED",
    "integration_claim": (
        "V2.7.5 validates integrity and adversarial behaviour of the "
        "restored-registry query runtime only. Any future integration "
        "requires its own versioned module and audit."
    ),
}


def integration_boundary_report() -> Dict[str, Any]:
    return {
        "report_type": "EIT_INTEGRATION_BOUNDARY_REPORT",
        "report_version": "2.7.5",
        "boundary": dict(INTEGRATION_BOUNDARY),
        "safety": dict(SAFETY_BLOCK),
    }

"""F5: integration non-claims are explicit."""
from eit_program_lang.integration_boundary import integration_boundary_report


def test_integration_boundary_declared():
    r = integration_boundary_report()
    b = r["boundary"]
    assert b["ca_lang_integration"] == "NOT_ESTABLISHED"
    assert b["11d_integration"] == "NOT_ESTABLISHED"
    assert b["ifim_integration"] == "NOT_ESTABLISHED"
    assert b["asi_os_governance_integration"] == "NOT_ESTABLISHED"
    assert r["safety"]["not_proof"] is True

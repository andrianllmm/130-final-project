from __future__ import annotations

from gatesmith.core.pipeline import synthesize


def test_pipeline_handles_constant_outputs() -> None:
    one = synthesize("assign y = 1'b1;")
    zero = synthesize("assign y = 1'b0;")

    assert one.sop == "1'b1"
    assert zero.sop == "1'b0"
    assert "assign y = 1'b1;" in one.verilog
    assert "assign y = 1'b0;" in zero.verilog

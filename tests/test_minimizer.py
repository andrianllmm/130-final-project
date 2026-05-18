from __future__ import annotations

import pytest

from gatesmith.core.minimizer import minimize, minimize_with_trace


def test_minimizer_produces_expected_prime_implicants() -> None:
    implicants = minimize([0, 2, 4, 6, 7], 3)
    assert [implicant.pattern for implicant in implicants] == ["--0", "11-"]


def test_minimizer_returns_trace_information() -> None:
    implicants, trace = minimize_with_trace([0, 1], 1)
    assert [implicant.pattern for implicant in implicants] == ["-"]
    assert trace.prime_implicants

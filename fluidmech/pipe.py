"""Two-section horizontal pipe discharging from a reservoir to atmosphere.

This module generalises the classic problem:

    reservoir --[area A1, loss K1]--[contraction]--[area A2, loss K2]--> atmosphere

The loss coefficients are *total* head-loss coefficients for each segment:

    K1 = h_f1 / (v1^2 / 2g)
    K2 = h_f2 / (v2^2 / 2g)

Local losses are not included unless the caller folds them into K1/K2.
The pipe centreline is the datum, so z = 0 at every station and gauge
pressure is p = rho g * HGL.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .core import (
    GRAVITY,
    _nonnegative,
    _positive,
    velocity_head,
)


@dataclass(frozen=True)
class TwoSectionPipeResult:
    """Solved state of a reservoir + two-section horizontal pipe system."""

    area1: float
    area2: float
    reservoir_head: float
    loss_coeff1: float
    loss_coeff2: float
    g: float
    velocity_ratio: float  # v1 / v2
    v1: float
    v2: float
    hv1: float
    hv2: float
    hf1: float
    hf2: float

    @property
    def flow_rate(self) -> float:
        """Steady volumetric flow rate, m^3/s."""

        return self.area2 * self.v2

    @property
    def total_loss(self) -> float:
        """Total head loss in both segments, m."""

        return self.hf1 + self.hf2

    @property
    def egl_reservoir(self) -> float:
        return self.reservoir_head

    @property
    def egl_contraction(self) -> float:
        return self.reservoir_head - self.hf1

    @property
    def egl_outlet(self) -> float:
        return self.hv2

    @property
    def hgl_inlet(self) -> float:
        return self.reservoir_head - self.hv1

    @property
    def hgl_before_contraction(self) -> float:
        return self.egl_contraction - self.hv1

    @property
    def hgl_after_contraction(self) -> float:
        return self.egl_contraction - self.hv2

    @property
    def hgl_outlet(self) -> float:
        return 0.0

    @property
    def contraction_hgl_drop(self) -> float:
        return self.hv2 - self.hv1

    @property
    def head_balance_error(self) -> float:
        """Numerical residual of H = hv2 + hf1 + hf2 (should be ~0)."""

        return self.reservoir_head - (self.hv2 + self.hf1 + self.hf2)

    def egl_at(self, section: int, fraction: float) -> float:
        """EGL at a fraction (0..1) along section 1 or 2."""

        f = _fraction(fraction)
        if section == 1:
            return self.reservoir_head - self.hf1 * f
        if section == 2:
            return self.egl_contraction - self.hf2 * f
        raise ValueError("section must be 1 or 2")

    def hgl_at(self, section: int, fraction: float) -> float:
        """HGL at a fraction (0..1) along section 1 or 2."""

        f = _fraction(fraction)
        if section == 1:
            return self.egl_at(1, f) - self.hv1
        if section == 2:
            return self.egl_at(2, f) - self.hv2
        raise ValueError("section must be 1 or 2")


def _fraction(value: float) -> float:
    f = _nonnegative(value, "fraction")
    if f > 1.0:
        raise ValueError("fraction must be between 0 and 1")
    return f


def solve_two_section_pipe(
    area1: float,
    area2: float,
    reservoir_head: float,
    loss_coeff1: float = 0.0,
    loss_coeff2: float = 0.0,
    g: float = GRAVITY,
) -> TwoSectionPipeResult:
    """Solve the reservoir + two-section pipe system.

    Parameters
    ----------
    area1, area2:
        Cross-sectional areas of the first and second pipe, m^2.
    reservoir_head:
        Height of the reservoir free surface above the pipe centreline, m.
    loss_coeff1, loss_coeff2:
        Total loss coefficients K1 and K2 as defined in the module docstring.
        Set both to zero for the ideal-loss case.
    g:
        Gravitational acceleration, m/s^2.

    Returns
    -------
    TwoSectionPipeResult
    """

    a1 = _positive(area1, "area1")
    a2 = _positive(area2, "area2")
    h = _positive(reservoir_head, "reservoir_head")
    k1 = _nonnegative(loss_coeff1, "loss_coeff1")
    k2 = _nonnegative(loss_coeff2, "loss_coeff2")
    gravity = _positive(g, "g")

    ratio = a2 / a1  # v1 = ratio * v2
    denominator = 1.0 + k1 * ratio * ratio + k2
    hv2 = h / denominator
    v2 = math.sqrt(2.0 * gravity * hv2)
    v1 = ratio * v2
    hv1 = velocity_head(v1, g=gravity)
    hf1 = k1 * hv1
    hf2 = k2 * hv2

    return TwoSectionPipeResult(
        area1=a1,
        area2=a2,
        reservoir_head=h,
        loss_coeff1=k1,
        loss_coeff2=k2,
        g=gravity,
        velocity_ratio=ratio,
        v1=v1,
        v2=v2,
        hv1=hv1,
        hv2=hv2,
        hf1=hf1,
        hf2=hf2,
    )

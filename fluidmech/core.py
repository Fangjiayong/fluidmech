"""Core steady, incompressible flow relations.

All quantities are SI unless a function says otherwise:
lengths in m, areas in m^2, velocities in m/s, pressures in Pa,
heads in m of flowing fluid.

Default water density is the textbook value 1000 kg/m^3.  For other
temperatures/fluids, pass ``rho`` explicitly.  The default gravity is the
standard 9.80665 m/s^2; many Chinese textbooks use 9.8, so pass ``g=9.8``
when reproducing those answers.
"""

from __future__ import annotations

import math
from typing import Final

GRAVITY: Final[float] = 9.80665
WATER_DENSITY: Final[float] = 1000.0
WATER_SPECIFIC_WEIGHT: Final[float] = WATER_DENSITY * GRAVITY


def _number(value: float, name: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise TypeError(f"{name} must be a real number") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _nonnegative(value: float, name: str) -> float:
    result = _number(value, name)
    if result < 0.0:
        raise ValueError(f"{name} must be >= 0")
    return result


def _positive(value: float, name: str) -> float:
    result = _number(value, name)
    if result <= 0.0:
        raise ValueError(f"{name} must be > 0")
    return result


def velocity_head(velocity: float, g: float = GRAVITY) -> float:
    """Kinetic head ``v^2 / (2g)`` in metres."""

    v = _nonnegative(velocity, "velocity")
    gravity = _positive(g, "g")
    return v * v / (2.0 * gravity)


def velocity_from_head(head: float, g: float = GRAVITY) -> float:
    """Velocity corresponding to a kinetic head, ``sqrt(2 g h)``."""

    h = _nonnegative(head, "head")
    gravity = _positive(g, "g")
    return math.sqrt(2.0 * gravity * h)


def circular_area(diameter: float) -> float:
    """Cross-sectional area of a circle, ``pi D^2 / 4``."""

    d = _positive(diameter, "diameter")
    return math.pi * d * d / 4.0


def diameter_from_area(area: float) -> float:
    """Diameter of a circular cross-section with the given area."""

    a = _positive(area, "area")
    return math.sqrt(4.0 * a / math.pi)


def flow_rate(area: float, velocity: float) -> float:
    """Volumetric flow rate ``Q = A v`` in m^3/s."""

    a = _positive(area, "area")
    v = _nonnegative(velocity, "velocity")
    return a * v


def velocity_from_flow(flow: float, area: float) -> float:
    """Mean velocity from flow rate, ``v = Q / A``."""

    q = _nonnegative(flow, "flow")
    a = _positive(area, "area")
    return q / a


def velocity_ratio_from_areas(area1: float, area2: float) -> float:
    """Return ``v2 / v1`` for the same steady volumetric flow."""

    a1 = _positive(area1, "area1")
    a2 = _positive(area2, "area2")
    return a1 / a2


def pressure_head(
    pressure: float,
    rho: float = WATER_DENSITY,
    g: float = GRAVITY,
) -> float:
    """Pressure head ``p / (rho g)`` in metres.  Pressure may be gauge."""

    p = _number(pressure, "pressure")
    density = _positive(rho, "rho")
    gravity = _positive(g, "g")
    return p / (density * gravity)


def pressure_from_head(
    head: float,
    rho: float = WATER_DENSITY,
    g: float = GRAVITY,
) -> float:
    """Pressure corresponding to a pressure head, ``rho g h`` (Pa)."""

    h = _number(head, "head")
    density = _positive(rho, "rho")
    gravity = _positive(g, "g")
    return rho * gravity * h


def piezometric_head(
    elevation: float,
    pressure: float,
    rho: float = WATER_DENSITY,
    g: float = GRAVITY,
) -> float:
    """Hydraulic grade line height ``z + p/(rho g)`` in metres."""

    z = _number(elevation, "elevation")
    return z + pressure_head(pressure, rho=rho, g=g)


def total_head(
    elevation: float,
    pressure: float,
    velocity: float,
    rho: float = WATER_DENSITY,
    g: float = GRAVITY,
) -> float:
    """Energy grade line height ``z + p/(rho g) + v^2/(2g)`` in metres."""

    return piezometric_head(elevation, pressure, rho=rho, g=g) + velocity_head(velocity, g=g)


def pressure_from_hgl(
    hgl: float,
    elevation: float = 0.0,
    rho: float = WATER_DENSITY,
    g: float = GRAVITY,
) -> float:
    """Gauge pressure from a hydraulic-grade-line height, ``rho g (HGL-z)``."""

    head = _number(hgl, "hgl") - _number(elevation, "elevation")
    return pressure_from_head(head, rho=rho, g=g)


def hydraulic_gradient(head_loss: float, length: float) -> float:
    """Friction slope ``J = h_f / L`` (dimensionless)."""

    loss = _nonnegative(head_loss, "head_loss")
    span = _positive(length, "length")
    return loss / span


def darcy_head_loss(
    friction_factor: float,
    length: float,
    diameter: float,
    velocity: float,
    g: float = GRAVITY,
) -> float:
    """Darcy-Weisbach head loss ``f (L/D) v^2/(2g)``."""

    f = _positive(friction_factor, "friction_factor")
    span = _nonnegative(length, "length")
    d = _positive(diameter, "diameter")
    v = _nonnegative(velocity, "velocity")
    return f * span / d * velocity_head(v, g=g)


def minor_head_loss(
    loss_coefficient: float,
    velocity: float,
    g: float = GRAVITY,
) -> float:
    """Local/minor head loss ``zeta v^2/(2g)``."""

    zeta = _nonnegative(loss_coefficient, "loss_coefficient")
    return zeta * velocity_head(velocity, g=g)

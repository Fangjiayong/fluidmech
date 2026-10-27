"""fluidmech: small, dependency-free helpers for steady incompressible flow.

Typical use::

    from fluidmech import solve_two_section_pipe, head_stations

    case = solve_two_section_pipe(
        area1=0.2, area2=0.1, reservoir_head=4.0,
        loss_coeff1=4.0, loss_coeff2=3.0, g=9.8,
    )
    print(case.v1, case.v2)
    for station in head_stations(case):
        print(station.key, station.egl, station.hgl)

The library deliberately uses explicit SI units and keeps plotting out of the
core.  See ``README.md`` for conventions and the roadmap.
"""

from __future__ import annotations

from .core import (
    GRAVITY,
    WATER_DENSITY,
    WATER_SPECIFIC_WEIGHT,
    circular_area,
    darcy_head_loss,
    diameter_from_area,
    flow_rate,
    hydraulic_gradient,
    minor_head_loss,
    piezometric_head,
    pressure_from_head,
    pressure_from_hgl,
    pressure_head,
    total_head,
    velocity_from_flow,
    velocity_from_head,
    velocity_head,
    velocity_ratio_from_areas,
)
from .headlines import (
    HeadStation,
    head_stations,
    head_table,
    midpoint_pressure,
    station_map,
    station_values,
)
from .pipe import TwoSectionPipeResult, solve_two_section_pipe

__all__ = [
    "GRAVITY",
    "WATER_DENSITY",
    "WATER_SPECIFIC_WEIGHT",
    "TwoSectionPipeResult",
    "HeadStation",
    "circular_area",
    "darcy_head_loss",
    "diameter_from_area",
    "flow_rate",
    "head_stations",
    "head_table",
    "hydraulic_gradient",
    "midpoint_pressure",
    "minor_head_loss",
    "piezometric_head",
    "pressure_from_head",
    "pressure_from_hgl",
    "pressure_head",
    "solve_two_section_pipe",
    "station_map",
    "station_values",
    "total_head",
    "velocity_from_flow",
    "velocity_from_head",
    "velocity_head",
    "velocity_ratio_from_areas",
]

__version__ = "0.1.0"

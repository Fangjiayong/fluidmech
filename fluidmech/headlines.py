"""Compute EGL/HGL station values for a two-section pipe system.

The pipe axis is the datum (z = 0).  Heads are in metres of flowing fluid.
At the outlet the jet discharges to atmosphere, hence HGL = 0 and
EGL = v2^2/(2g).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from .core import WATER_DENSITY, pressure_from_hgl
from .pipe import TwoSectionPipeResult


@dataclass(frozen=True)
class HeadStation:
    """One station on the energy-grade and hydraulic-grade lines."""

    key: str
    label: str
    section: int  # 0 reservoir, 1 first pipe, 2 second pipe
    fraction: float  # position within the section, 0..1
    egl: float
    hgl: float
    velocity_head: float

    def as_dict(self) -> dict[str, float | int | str]:
        return asdict(self)


def head_stations(result: TwoSectionPipeResult) -> tuple[HeadStation, ...]:
    """Return reservoir, inlet, midpoint, contraction and outlet stations."""

    h = result.reservoir_head
    hv1, hv2 = result.hv1, result.hv2
    hf1, hf2 = result.hf1, result.hf2

    return (
        HeadStation(
            key="reservoir",
            label="Reservoir surface",
            section=0,
            fraction=0.0,
            egl=h,
            hgl=h,
            velocity_head=0.0,
        ),
        HeadStation(
            key="inlet",
            label="Inlet A",
            section=1,
            fraction=0.0,
            egl=h,
            hgl=h - hv1,
            velocity_head=hv1,
        ),
        HeadStation(
            key="section1_mid",
            label="Section 1 midpoint",
            section=1,
            fraction=0.5,
            egl=h - 0.5 * hf1,
            hgl=h - 0.5 * hf1 - hv1,
            velocity_head=hv1,
        ),
        HeadStation(
            key="section1_end",
            label="Section 1 end",
            section=1,
            fraction=1.0,
            egl=h - hf1,
            hgl=h - hf1 - hv1,
            velocity_head=hv1,
        ),
        HeadStation(
            key="section2_start",
            label="Section 2 start",
            section=2,
            fraction=0.0,
            egl=h - hf1,
            hgl=h - hf1 - hv2,
            velocity_head=hv2,
        ),
        HeadStation(
            key="section2_mid",
            label="Section 2 midpoint",
            section=2,
            fraction=0.5,
            egl=h - hf1 - 0.5 * hf2,
            hgl=h - hf1 - 0.5 * hf2 - hv2,
            velocity_head=hv2,
        ),
        HeadStation(
            key="outlet",
            label="Outlet jet",
            section=2,
            fraction=1.0,
            egl=hv2,
            hgl=0.0,
            velocity_head=hv2,
        ),
    )


def station_map(result: TwoSectionPipeResult) -> dict[str, HeadStation]:
    """Return stations keyed by their short key."""

    return {station.key: station for station in head_stations(result)}


def head_table(result: TwoSectionPipeResult) -> list[dict[str, float | int | str]]:
    """Tabular station values suitable for printing or CSV export."""

    return [station.as_dict() for station in head_stations(result)]


def midpoint_pressure(
    result: TwoSectionPipeResult,
    section: int,
    rho: float = WATER_DENSITY,
) -> float:
    """Gauge pressure at the midpoint of section 1 or 2, Pa."""

    if section not in (1, 2):
        raise ValueError("section must be 1 or 2")
    station = station_map(result)[f"section{section}_mid"]
    return pressure_from_hgl(station.hgl, elevation=0.0, rho=rho, g=result.g)


def station_values(result: TwoSectionPipeResult, keys: Iterable[str]) -> list[HeadStation]:
    """Look up several stations by key, preserving the requested order."""

    lookup = station_map(result)
    key_list = list(keys)
    missing = [key for key in key_list if key not in lookup]
    if missing:
        raise KeyError(f"unknown station keys: {', '.join(missing)}")
    return [lookup[key] for key in key_list]

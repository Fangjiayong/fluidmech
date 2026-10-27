"""Regression tests for the initial fluidmech library."""

from __future__ import annotations

import math
import unittest

from fluidmech import (
    circular_area,
    darcy_head_loss,
    head_stations,
    head_table,
    midpoint_pressure,
    solve_two_section_pipe,
    station_map,
    station_values,
    velocity_head,
)
from fluidmech.core import pressure_from_hgl


class CoreRelationsTest(unittest.TestCase):
    def test_velocity_head_and_inverse(self) -> None:
        self.assertAlmostEqual(velocity_head(4.427188724, g=9.8), 1.0, places=9)
        self.assertAlmostEqual(velocity_head(8.854377448, g=9.8), 4.0, places=9)

    def test_circular_area_and_flow(self) -> None:
        self.assertAlmostEqual(circular_area(1.0), math.pi / 4.0, places=12)

    def test_darcy_loss(self) -> None:
        # f=0.02, L=10 m, D=0.05 m, v=2 m/s, g=9.8
        expected = 0.02 * (10 / 0.05) * (2**2 / (2 * 9.8))
        self.assertAlmostEqual(darcy_head_loss(0.02, 10, 0.05, 2, g=9.8), expected, places=12)

    def test_pressure_from_hgl(self) -> None:
        self.assertAlmostEqual(pressure_from_hgl(3.4, rho=1000, g=9.8), 33320.0, places=6)

    def test_invalid_inputs(self) -> None:
        with self.assertRaises(ValueError):
            velocity_head(-1.0)
        with self.assertRaises(ValueError):
            darcy_head_loss(0.02, 10, 0, 2)
        with self.assertRaises(ValueError):
            solve_two_section_pipe(0, 0.1, 4.0)


class Problem319IdealTest(unittest.TestCase):
    def setUp(self) -> None:
        self.case = solve_two_section_pipe(0.2, 0.1, 4.0, g=9.8)

    def test_velocities(self) -> None:
        self.assertAlmostEqual(self.case.v2, math.sqrt(2 * 9.8 * 4.0), places=9)
        self.assertAlmostEqual(self.case.v1, self.case.v2 / 2.0, places=9)
        self.assertAlmostEqual(self.case.v1, 4.427188724, places=6)
        self.assertAlmostEqual(self.case.v2, 8.854377448, places=6)

    def test_heads(self) -> None:
        self.assertAlmostEqual(self.case.hv1, 1.0, places=9)
        self.assertAlmostEqual(self.case.hv2, 4.0, places=9)
        self.assertAlmostEqual(self.case.hf1, 0.0, places=12)
        self.assertAlmostEqual(self.case.hf2, 0.0, places=12)
        self.assertAlmostEqual(self.case.head_balance_error, 0.0, places=12)

    def test_head_lines(self) -> None:
        stations = station_map(self.case)
        self.assertAlmostEqual(stations["inlet"].hgl, 3.0, places=9)
        self.assertAlmostEqual(stations["section1_mid"].hgl, 3.0, places=9)
        self.assertAlmostEqual(stations["section1_end"].hgl, 3.0, places=9)
        self.assertAlmostEqual(stations["section2_start"].hgl, 0.0, places=9)
        self.assertAlmostEqual(stations["section2_mid"].hgl, 0.0, places=9)
        self.assertAlmostEqual(stations["outlet"].hgl, 0.0, places=9)
        for station in stations.values():
            self.assertAlmostEqual(station.egl, 4.0, places=9)

    def test_contraction_drop(self) -> None:
        self.assertAlmostEqual(self.case.contraction_hgl_drop, 3.0, places=9)


class Problem319LossTest(unittest.TestCase):
    def setUp(self) -> None:
        self.case = solve_two_section_pipe(
            0.2, 0.1, 4.0, loss_coeff1=4.0, loss_coeff2=3.0, g=9.8
        )

    def test_velocities_and_losses(self) -> None:
        self.assertAlmostEqual(self.case.hv2, 0.8, places=9)
        self.assertAlmostEqual(self.case.hv1, 0.2, places=9)
        self.assertAlmostEqual(self.case.v2, math.sqrt(2 * 9.8 * 0.8), places=9)
        self.assertAlmostEqual(self.case.v1, self.case.v2 / 2.0, places=9)
        self.assertAlmostEqual(self.case.hf1, 0.8, places=9)
        self.assertAlmostEqual(self.case.hf2, 2.4, places=9)
        self.assertAlmostEqual(self.case.total_loss, 3.2, places=9)
        self.assertAlmostEqual(self.case.head_balance_error, 0.0, places=12)

    def test_station_values(self) -> None:
        expected = {
            "reservoir": (4.0, 4.0),
            "inlet": (4.0, 3.8),
            "section1_mid": (3.6, 3.4),
            "section1_end": (3.2, 3.0),
            "section2_start": (3.2, 2.4),
            "section2_mid": (2.0, 1.2),
            "outlet": (0.8, 0.0),
        }
        stations = station_map(self.case)
        for key, (egl, hgl) in expected.items():
            with self.subTest(key=key):
                self.assertAlmostEqual(stations[key].egl, egl, places=9)
                self.assertAlmostEqual(stations[key].hgl, hgl, places=9)

    def test_contraction_drop(self) -> None:
        self.assertAlmostEqual(self.case.contraction_hgl_drop, 0.6, places=9)

    def test_linear_interpolation(self) -> None:
        self.assertAlmostEqual(self.case.egl_at(1, 0.0), 4.0, places=9)
        self.assertAlmostEqual(self.case.egl_at(1, 1.0), 3.2, places=9)
        self.assertAlmostEqual(self.case.egl_at(2, 0.5), 2.0, places=9)
        self.assertAlmostEqual(self.case.hgl_at(1, 0.5), 3.4, places=9)
        self.assertAlmostEqual(self.case.hgl_at(2, 0.5), 1.2, places=9)
        with self.assertRaises(ValueError):
            self.case.egl_at(3, 0.5)
        with self.assertRaises(ValueError):
            self.case.egl_at(1, 1.1)

    def test_midpoint_pressures(self) -> None:
        self.assertAlmostEqual(midpoint_pressure(self.case, 1, rho=1000), 33320.0, places=6)
        self.assertAlmostEqual(midpoint_pressure(self.case, 2, rho=1000), 11760.0, places=6)
        with self.assertRaises(ValueError):
            midpoint_pressure(self.case, 3)


class StationShapeTest(unittest.TestCase):
    def test_station_count_and_order(self) -> None:
        case = solve_two_section_pipe(0.2, 0.1, 4.0, 4.0, 3.0, g=9.8)
        keys = [station.key for station in head_stations(case)]
        self.assertEqual(
            keys,
            [
                "reservoir",
                "inlet",
                "section1_mid",
                "section1_end",
                "section2_start",
                "section2_mid",
                "outlet",
            ],
        )

    def test_station_lookup_and_table(self) -> None:
        case = solve_two_section_pipe(0.2, 0.1, 4.0, 4.0, 3.0, g=9.8)
        selected = station_values(case, (key for key in ("outlet", "inlet")))
        self.assertEqual([station.key for station in selected], ["outlet", "inlet"])
        self.assertAlmostEqual(selected[0].egl, 0.8, places=9)
        self.assertAlmostEqual(selected[1].hgl, 3.8, places=9)
        table = head_table(case)
        self.assertEqual(len(table), 7)
        self.assertEqual(table[0]["key"], "reservoir")
        with self.assertRaises(KeyError):
            station_values(case, ["not-a-station"])


if __name__ == "__main__":
    unittest.main()

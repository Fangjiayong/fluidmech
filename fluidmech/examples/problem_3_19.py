"""Benchmark example: textbook problem 3-19.

A reservoir with head H = 4 m feeds a horizontal two-section pipe:
A1 = 0.2 m^2, A2 = 0.1 m^2, discharging to atmosphere.

Case 1 (ideal): no losses.
Case 2 (losses): h_f1 = 4 v1^2/(2g), h_f2 = 3 v2^2/(2g), local losses ignored.

Run from the repository root:

    python -m fluidmech.examples.problem_3_19
"""

from __future__ import annotations

from fluidmech import head_stations, midpoint_pressure, solve_two_section_pipe


def solve_problem_3_19(with_losses: bool, g: float = 9.8):
    """Return the solved case for problem 3-19."""

    return solve_two_section_pipe(
        area1=0.2,
        area2=0.1,
        reservoir_head=4.0,
        loss_coeff1=4.0 if with_losses else 0.0,
        loss_coeff2=3.0 if with_losses else 0.0,
        g=g,
    )


def print_case(with_losses: bool) -> None:
    case = solve_problem_3_19(with_losses)
    title = "with losses" if with_losses else "ideal (no losses)"
    print(f"\n=== Problem 3-19: {title} ===")
    print(f"v1 = {case.v1:.3f} m/s, v2 = {case.v2:.3f} m/s")
    print(f"hv1 = {case.hv1:.3f} m, hv2 = {case.hv2:.3f} m")
    print(f"hf1 = {case.hf1:.3f} m, hf2 = {case.hf2:.3f} m")
    print(f"Q   = {case.flow_rate:.4f} m^3/s")
    print(f"{'station':<20}{'EGL/m':>10}{'HGL/m':>10}")
    for station in head_stations(case):
        print(f"{station.key:<20}{station.egl:>10.3f}{station.hgl:>10.3f}")
    print(
        "midpoint gauge pressure: "
        f"p1 = {midpoint_pressure(case, 1) / 1000:.2f} kPa, "
        f"p2 = {midpoint_pressure(case, 2) / 1000:.2f} kPa"
    )


if __name__ == "__main__":
    print_case(with_losses=False)
    print_case(with_losses=True)

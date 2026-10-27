# Workspace notes

## Fluid mechanics

- For steady incompressible flow, pipe, Bernoulli, EGL/HGL, or pressure
  problems, load the `fluid-mechanics` skill first.
- Reuse `fluidmech/` instead of re-deriving one-off formulas. For the
  two-section reservoir-pipe benchmark, see
  `fluidmech/examples/problem_3_19.py`.
- When extending the library, follow: formula -> function -> runnable
  example -> regression test -> reference note.
- Run the test suite from the workspace root:

  ```powershell
  python -m unittest discover -s tests -v
  ```

- Defaults: SI units, `g=9.80665 m/s^2`, `rho=1000 kg/m^3`. Chinese textbook
  problems usually need an explicit `g=9.8`.

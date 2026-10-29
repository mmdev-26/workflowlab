# WorkflowLab — design and limitations

## Simulation model

Jobs arrive on a constant or seeded exponential stream. Each stage is a first-come-first-served queue with one or more identical servers. A min-heap tracks server availability. At each stage jobs are ordered by **actual stage arrival**, not original job ID, which matters when earlier parallel work finishes out of order.

The report records per-job cycle/queue time, stage mean and p95 waits, service utilization and overall makespan. A scenario uses the same arrivals and initial random seed for reproducibility. The included baseline/scenario pair compares one versus two review servers.

A single finite run from an empty system is not a steady-state forecast. Confidence intervals, shifts, priorities, abandonment, rework and branching routing are not modeled. If stage structures change, service random streams are not guaranteed to remain paired draw-for-draw. Treat outputs as assumptions to investigate, not promised business savings.

## Complexity

For J jobs and S stages, sorting arrivals per stage costs O(S J log J); server allocation costs O(S J log C), where C is server count. The current input is capped at 10,000 jobs and 1,000 servers per stage.

## Next validation work

Independent replications and confidence intervals, warm-up diagnostics, branch routing and calibration to observed event logs. Roadmap only.

## Public-demo boundary

The hosted workbench is served over HTTPS behind nginx. User scenarios are processed on the server, not in the visitor browser. Input is capped at 512 KB, analysis runs in a separate process with a 3-second CPU limit, a 5-second wall deadline and a 256 MB address-space limit on Linux. At most two analysis workers run per service. The reverse proxy rate-limits analysis and disables request/response buffering to disk. The service runs as a dynamic unprivileged user with a read-only filesystem, private temporary directory and localhost-only network access. These are resource and isolation boundaries, not a claim of a completed security audit.

The UI adds a live evidence visualization and domain-specific quick controls. JSON remains available for full reproducibility. No submitted inputs are intentionally persisted. Public demos are for synthetic data only.

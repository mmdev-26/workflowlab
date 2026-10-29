# WorkflowLab — design and limitations

## Simulation model

Jobs arrive on a constant or seeded exponential stream. Each stage is a first-come-first-served queue with one or more identical servers. A min-heap tracks server availability. At each stage jobs are ordered by **actual stage arrival**, not original job ID, which matters when earlier parallel work finishes out of order.

The report records per-job cycle/queue time, stage mean and p95 waits, service utilization and overall makespan. A scenario uses the same arrivals and initial random seed for reproducibility. The included baseline/scenario pair compares one versus two review servers.

A single finite run from an empty system is not a steady-state forecast. Confidence intervals, shifts, priorities, abandonment, rework and branching routing are not modeled. If stage structures change, service random streams are not guaranteed to remain paired draw-for-draw. Treat outputs as assumptions to investigate, not promised business savings.

## Complexity

For J jobs and S stages, sorting arrivals per stage costs O(S J log J); server allocation costs O(S J log C), where C is server count. The current input is capped at 10,000 jobs and 1,000 servers per stage.

## Next validation work

Independent replications and confidence intervals, warm-up diagnostics, branch routing and calibration to observed event logs. Roadmap only.

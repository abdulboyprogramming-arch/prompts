<!-- not-a-prompt -->

# Greenfield fixture — a request that is a solution in search of a problem

**Purpose:** a fixed input for running `INT-P03` (Greenfield Intake), built so that the desirable
behaviour is visible in the output: the problem separated from the proposal, constraints classified,
non-goals written, and failure modes named.

**Why this request:** it contains the four things that most often go wrong at the start of a project —
a proposal presented as a requirement, no stated deadline, a scope that is a platform rather than a
project, and one genuine fixed constraint mixed in with a pile of preferences.

---

## The user's request

> We need to build an internal event platform. Kafka, obviously, with a schema registry and maybe a
> stream processor for the analytics team. Every team will publish to it, so it has to be general.
> We're a Python shop, on AWS, and we use Terraform already.
>
> The one hard thing: our regulator requires that all personal data in the platform is deletable within
> 30 days of a request, with an audit trail. That's not negotiable.
>
> No deadline as such — the CTO wants to see momentum this quarter. Team is me and one contractor. I
> want to start coding next week.

## What a passing brief must contain

| # | Requirement | Why this request forces it |
|---|---|---|
| 1 | **The problem is stated separately from "Kafka"** | the user opens with the solution; nothing in the message says what breaks without it |
| 2 | **"Every team will publish to it" is challenged as a scope statement** | a platform for all teams with 1.5 engineers is a finding, and the brief should name the first user instead |
| 3 | **The regulatory requirement is classified as fixed; Python/AWS/Terraform/Kafka as preferences** | the request presents all five with the same tone; only one is a constraint |
| 4 | **The 30-day deletion rule is recorded as an architecture-shaping constraint** | it changes the design, and treating it as a checkbox at the end is how it fails an audit |
| 5 | **At least one non-goal is written, with where the request goes instead** | "analytics stream processor" is the obvious first cut |
| 6 | **At least one failure mode is named** | an unowned platform in a two-person team is the likeliest way this wastes the quarter |
| 7 | **The absence of a deadline is recorded as "none stated", not invented** | "momentum this quarter" is a social expectation, not a date |
| 8 | **No stage count is proposed from the user's preference** | the lifecycle sets the stage count; the user's "start coding next week" is a scheduling wish |

## Grading

`PASS` requires all eight. `FAIL` on any of: the proposal absorbed into the problem statement; a
framework choice treated as a requirement; the regulator constraint missing or glossed; no non-goals;
no failure mode; a fabricated deadline; or a stage count justified by the user's urgency.

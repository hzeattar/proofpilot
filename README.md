# ProofPilot

> An evidence-first delivery agent for freelancers and small software teams.

ProofPilot turns a client brief and optional project context into an auditable
delivery draft: evidence ledger, scope, risk register, milestones, unanswered
questions, and a human approval gate. It is built for the **Professional
Agents** track of the Agents for Humans Hackathon.

## Why this exists

Client briefs often mix facts, assumptions, and requests. The repetitive work
of turning them into a delivery plan is valuable, but a careless automated
proposal can create a costly commitment. ProofPilot does the preparation
end-to-end and stops at the decision that must remain human: approving scope,
price, and external communication.

## What it does

1. Accepts a client brief and optional project/repository context.
2. Preserves stated facts in a source-labelled evidence ledger.
3. Produces a scope draft, risks, milestones, and open questions.
4. Blocks commercial commitment and client-facing sends behind a human approval gate.
5. Supports a real **AWS/Strands** execution path when AWS credentials are configured.

## Honest execution modes

| Mode | What runs | Claim you may make |
| --- | --- | --- |
| `demo` | Local deterministic evidence workflow | “The local workflow ran; no model or AWS service was invoked.” |
| `aws` | `strands.Agent` with the configured AWS environment | “A Strands/AWS run was requested/succeeded only when the response proves it.” |

The application does not fake an AWS result. Missing AWS configuration produces
a clear error.

## Quick start

Requires Python 3.12+.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000), leave **Local transparent demo** selected, and submit the included sample.

Run checks:

```powershell
python -m unittest discover -s tests -v
```

## AWS / Strands mode

The AWS mode uses the standard AWS credential chain; no credentials are stored
in this repository. Configure credentials with an authorized AWS method, then:

```powershell
$env:AWS_REGION = "us-east-1"
uvicorn app.main:app --reload
```

Choose **AWS / Strands run** in the UI. Your configured account needs access
to a Bedrock model supported by the installed Strands SDK. The agent and its
evidence tool are in [app/agent.py](app/agent.py).

## Architecture

See the [architecture diagram](docs/architecture.svg) and the
[architecture notes](docs/architecture.md) for the explicit human-control
boundary.

## Demo video

Use [docs/video-script.md](docs/video-script.md) to record a public YouTube or
Vimeo video under five minutes. Do not state that AWS was invoked unless that
run was actually recorded.

## Hackathon disclosure and license

See [DISCLOSURE.md](DISCLOSURE.md). This repository is [MIT licensed](LICENSE).

## Development notes

- This is a new hackathon project, not a repackaging of an existing delivery platform.
- The local demo is intentionally reproducible without a paid cloud account.
- Before final Devpost submission, provide the required AWS Builder ID and a real public demo-video URL.

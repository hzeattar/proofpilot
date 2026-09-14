# ProofPilot demo video script (4:20 target)

## 0:00–0:25 — Problem

“Professionals lose time turning vague client messages into a reliable scope.
The risky part is not writing a proposal—it is accidentally treating an
assumption as fact or sending a commitment without approval.”

## 0:25–0:55 — User and outcome

“ProofPilot is for freelance developers and small delivery teams. It turns a
brief and optional project context into an evidence-led delivery draft: scope,
risks, milestones, and the questions that still need answers.”

## 0:55–2:05 — Live product walk-through

Open the local web app. Paste the included restaurant-delivery brief and show
the transparent demo mode. Click **Prepare evidence-first delivery brief**.
Point to the evidence sources, missing acceptance criteria, risks, and the
approval gate. State clearly: “This screen is local deterministic demo mode;
it has not called AWS or an LLM.”

## 2:05–3:10 — Strands and AWS implementation

Show `app/agent.py`, the `Agent` construction, and the evidence tool. Show the
architecture diagram. Explain: “In AWS mode, ProofPilot invokes a Strands Agent
using the normal AWS credential chain and Bedrock configuration. If AWS is not
configured, it fails clearly rather than pretending a model ran.” Record an
actual AWS-mode run only after credentials are configured; otherwise do not
claim one in the video.

## 3:10–3:50 — Human control

Show the architecture’s human approval gate. “ProofPilot never sends a quote,
commits a date, or contacts a client. A human owns commercial commitments and
external communications.”

## 3:50–4:20 — Why it matters

“The result is less rework, fewer untraceable assumptions, and a faster path
from brief to an accountable delivery decision. The entire project is public,
MIT licensed, and reproducible from the README.”

"""Evidence-first delivery-planning workflow used by ProofPilot.

The deterministic path is intentionally transparent: it produces a local
sample artifact and never represents itself as an AI or AWS model response.
The same pure functions are registered as Strands tools in ``app.agent``.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Iterable


STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
    "in", "is", "it", "of", "on", "or", "that", "the", "to", "with",
    "we", "you", "your", "our", "this", "will", "need", "needs",
}


@dataclass(frozen=True)
class EvidenceItem:
    statement: str
    source: str
    confidence: str


def sentences(text: str) -> list[str]:
    """Return compact, non-empty statements while preserving the source text."""
    normalized = re.sub(r"\s+", " ", text.strip())
    return [part.strip(" -•") for part in re.split(r"(?<=[.!?])\s+|\n+", normalized) if part.strip(" -•")]


def keywords(*texts: str, limit: int = 8) -> list[str]:
    words: list[str] = []
    for text in texts:
        words.extend(re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}", text.lower()))
    unique: list[str] = []
    for word in words:
        if word not in STOP_WORDS and word not in unique:
            unique.append(word)
    return unique[:limit]


def collect_evidence(brief: str, context: str = "") -> list[EvidenceItem]:
    """Build a traceable evidence ledger without inventing project facts."""
    items = [EvidenceItem(statement=item, source="Client brief", confidence="stated") for item in sentences(brief)]
    items.extend(EvidenceItem(statement=item, source="Project context", confidence="stated") for item in sentences(context))
    return items[:10]


def detect_open_questions(brief: str, context: str = "") -> list[str]:
    text = f"{brief}\n{context}".lower()
    checks = [
        ("Who is the accountable approver for scope and commercial terms?", ("approv", "owner", "stakeholder")),
        ("Which acceptance criteria prove the first release is complete?", ("acceptance", "success metric", "kpi")),
        ("Which systems may the workflow read from or write to?", ("api", "integration", "repository", "database")),
        ("What delivery date and budget constraints apply?", ("date", "deadline", "budget", "cost")),
        ("What data must be excluded or redacted before sharing externally?", ("privacy", "pii", "secret", "sensitive")),
    ]
    return [question for question, signals in checks if not any(signal in text for signal in signals)]


def build_artifact(brief: str, context: str = "") -> dict:
    """Create an auditable draft with a deliberate human approval boundary."""
    evidence = collect_evidence(brief, context)
    terms = keywords(brief, context)
    scope = [item.statement for item in evidence[:4]] or ["No scope facts supplied; collect a client brief first."]
    risks = [
        "Scope assumptions need a named approver before any client-facing commitment.",
        "External communication remains blocked until the human approval gate is completed.",
    ]
    if not context.strip():
        risks.insert(0, "No repository or project context was provided, so implementation estimates are provisional.")
    milestones = [
        {"name": "Evidence review", "outcome": "Validate stated requirements and unanswered questions."},
        {"name": "Scope approval", "outcome": "Human approves scope, price, and any client-facing claim."},
        {"name": "Delivery", "outcome": "Build only the approved scope and capture acceptance evidence."},
    ]
    proposal = (
        "ProofPilot prepared a draft from the supplied evidence. "
        "The draft is not a quote, contract, or external communication until a human approves the scope and terms."
    )
    return {
        "evidence": [asdict(item) for item in evidence],
        "scope": scope,
        "keywords": terms,
        "open_questions": detect_open_questions(brief, context),
        "risks": risks,
        "milestones": milestones,
        "proposal_draft": proposal,
        "approval_gate": {
            "status": "required",
            "reason": "Commercial commitments and external communications require a human decision.",
        },
    }


def format_for_agent(artifact: dict) -> str:
    """Render tool output as compact context for a Strands agent."""
    evidence = "\n".join(f"- [{item['source']}] {item['statement']}" for item in artifact["evidence"]) or "- No evidence supplied"
    questions = "\n".join(f"- {item}" for item in artifact["open_questions"]) or "- No open questions detected"
    return (
        "EVIDENCE LEDGER:\n" + evidence + "\n\n"
        "OPEN QUESTIONS:\n" + questions + "\n\n"
        "HUMAN GATE: Scope, commercial terms, and external sends remain blocked pending approval."
    )

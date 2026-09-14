"""Strands integration for ProofPilot.

``run_with_strands`` invokes a real Strands Agent. It intentionally has no
fallback to a fake model: if AWS/Bedrock is not configured, the caller gets a
clear configuration error and can use the explicitly labelled local demo path.
"""

from __future__ import annotations

import os

from .workflow import build_artifact, format_for_agent

try:
    from strands import Agent, tool
except ImportError:  # Allows documentation and static analysis before install.
    Agent = None
    tool = None


SYSTEM_PROMPT = """You are ProofPilot, an evidence-first professional delivery agent.
Use the evidence tool before drafting. Never invent repository facts, dates,
prices, security claims, or client commitments. Produce a concise delivery
brief with: evidence, scope, risks, milestones, open questions, and a clearly
marked human approval gate. Do not send messages or make commitments."""


def _evidence_tool(brief: str, project_context: str = "") -> str:
    return format_for_agent(build_artifact(brief, project_context))


if tool is not None:
    evidence_tool = tool(_evidence_tool)
else:
    evidence_tool = _evidence_tool


def run_with_strands(brief: str, project_context: str = "") -> str:
    """Invoke Strands against the configured AWS Bedrock environment.

    Standard AWS credential resolution is used. Set ``AWS_REGION`` and, when
    needed by the installed Strands version/provider, its documented model
    configuration. No credentials are stored by this project.
    """
    if Agent is None:
        raise RuntimeError("Strands Agents SDK is not installed. Run pip install -r requirements.txt.")
    if not os.getenv("AWS_REGION") and not os.getenv("AWS_DEFAULT_REGION"):
        raise RuntimeError("AWS_REGION is required for a real AWS/Bedrock Strands run.")
    agent = Agent(system_prompt=SYSTEM_PROMPT, tools=[evidence_tool])
    prompt = (
        "Prepare an evidence-first delivery brief.\n\n"
        f"CLIENT BRIEF:\n{brief}\n\nPROJECT CONTEXT:\n{project_context or '(none supplied)'}"
    )
    return str(agent(prompt))

import unittest

from app.workflow import build_artifact, collect_evidence


class WorkflowTests(unittest.TestCase):
    def test_artifact_keeps_evidence_and_human_gate(self):
        artifact = build_artifact("Build a mobile order dashboard.", "Laravel API exposes orders.")
        self.assertEqual(artifact["approval_gate"]["status"], "required")
        self.assertTrue(artifact["evidence"])
        self.assertIn("External communication", " ".join(artifact["risks"]))

    def test_evidence_has_explicit_sources(self):
        evidence = collect_evidence("A stated requirement.", "A stated repository fact.")
        self.assertEqual([item.source for item in evidence], ["Client brief", "Project context"])


if __name__ == "__main__":
    unittest.main()

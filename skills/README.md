# Metric Governance Agent skills

These files give coding agents focused instructions for reviewing and improving artifacts produced by the `metricgov` CLI.

## Use them

1. Run the relevant CLI workflow, for example:

   ```bash
   metricgov prepare
   metricgov finalize --from feedback/workshop_decisions.yaml
   ```

2. Ask your coding agent to read a specific skill and apply it to an artifact, for example:

   ```text
   Read skills/ambiguity-classifier.skill.md and review
   artifacts/03_ambiguity_register.md against the evidence log.
   Preserve uncertain findings as open questions.
   ```

3. Review the agent's proposed changes before accepting them.

Use `metric-governance-agent.skill.md` for the overall governance boundary. Use a specialized skill for evidence, ambiguity, workshops, decisions, dashboard changes, or governance failures.

The CLI creates deterministic artifacts. Skills guide an agent in reviewing, refining, or extending those artifacts. Neither the CLI nor a coding agent can certify business truth; accountable owners must confirm it.

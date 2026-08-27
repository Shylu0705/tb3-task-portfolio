# TB3 Task Portfolio

Six original [Terminal-Bench 3](https://www.tbench.ai/) tasks, built as a take-home.
Each task is self-contained and passes the full TB3 CI suite (static checks, oracle
solution scoring 1.0, empty-agent scoring 0.0, and a bundled cheat scoring 0.0).

The complete writeup — including the central finding on why beating frontier models
3/3 within the rubric constraints is a research-grade problem — is in
**[SUBMISSION.md](SUBMISSION.md)**. The full iteration history (every design decision,
dead end, and prototype) is in **[DESIGN_LOG.md](DESIGN_LOG.md)**.

## The tasks

| # | Task | Domain | Core mechanism |
|---|---|---|---|
| 1 | [`langgraph-reflection-repair`](tasks/langgraph-reflection-repair) | Framework debugging | latent defects invisible on the sample |
| 2 | [`streaming-tokenizer-parity`](tasks/streaming-tokenizer-parity) | Exact spec reproduction | chunk-invariance + hidden reference |
| 3 | [`clustered-metric-ci`](tasks/clustered-metric-ci) | Non-observable statistics | calibration you can't test your way to |
| 4 | [`best-candidate-effect`](tasks/best-candidate-effect) | Non-observable statistics | winner's-curse / selection bias |
| 5 | [`harden-reward-verifier`](tasks/harden-reward-verifier) | Adversarial security | tamper-resistant grader vs. reward-hacks |
| 6 | [`raman-units-debug`](tasks/raman-units-debug) | Scientific-data debugging | false premise (units) / physical invariant |

Every task directory contains `environment/` (the agent's starting state) +
`solution/` (the oracle) + `tests/` (a separate, network-free verifier) + `cheat/`
(a deliberate reward-hack that scores 0) + `task.toml` + `instruction.md` + `README.md`.

## Running a task

Tasks run under the [Harbor](https://www.tbench.ai/) CLI (installed separately; not
vendored here):

```bash
uv tool install "harbor[modal,daytona]"   # or: pip install harbor
```

Then, from the repo root:

```bash
# Oracle solution should score 1.0
harbor run -p tasks/raman-units-debug --agent oracle -k 1 -n 1 --yes

# Empty agent (no-op) should score 0.0
harbor run -p tasks/raman-units-debug --agent nop -k 1 -n 1 --yes
```

Swap `raman-units-debug` for any task above. The agent-trial commands used to evaluate
these tasks against frontier models are documented in [SUBMISSION.md](SUBMISSION.md).

---

*Benchmark data — these tasks carry harbor canary markers and should never appear in a
training corpus.*

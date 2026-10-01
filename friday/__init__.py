"""friday-ai-agent-harness — a minimal, transparent, local-first Friday.

Four pillars, one module each:
  harness  → friday/runtime + friday/gateway  (scaffolding around the raw LLM)
  loop     → friday/loop                      (observe → reason → act → repeat)
             friday/graph                     (opt-in structure around the loop — extends this pillar)
  memory   → friday/memory                    (procedural / semantic / episodic)
  ops      → friday/ops + evals/              (trace → eval → gate → release)
"""

__version__ = "0.2.0"

---
name: your-skill-name
description: One sentence saying what this skill does AND when to use it — the loader matches user messages against these words, so include the words people actually say.
---

<!--
Copy this file to skills/<your-skill-name>/SKILL.md. The frontmatter is
required (name + description — the official Anthropic Agent Skills format)
and scripts/validate_skills.py checks it. Keep the body under ~60 lines:
skills are loaded into the prompt only when they match, but shorter is better.
-->

## Instructions

Step-by-step guidance for the model. Be concrete: name the tools to call
(`create_event`, `save_note`, `send_message`), the defaults to assume, and
the tone to take.

## Edge cases

| Situation | Do |
|---|---|
| Something ambiguous | Ask one clarifying question |

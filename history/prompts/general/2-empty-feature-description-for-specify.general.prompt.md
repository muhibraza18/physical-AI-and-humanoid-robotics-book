---
id: 2
title: Empty Feature Description for Specify
stage: general
date: 2025-12-07
surface: agent
model: gemini-pro
feature: none
branch: master
user:
command: /sp.specify (with empty arguments)
labels: [error, specify]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
tests:
---

## Prompt

The user initiated the `/sp.specify` command with what appears to be an empty feature description (multiple repetitions of `/sp.specify` were provided, which is interpreted as an empty argument string).

## Response snapshot

ERROR: No feature description provided.

## Outcome

- ✅ Impact: User was informed that no feature description was provided.
- 🧪 Tests: N/A
- 📁 Files: N/A
- 🔁 Next prompts: User needs to provide a valid feature description for `/sp.specify`.
- 🧠 Reflection: The agent correctly identified and handled an empty feature description as per the tool's instructions.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A

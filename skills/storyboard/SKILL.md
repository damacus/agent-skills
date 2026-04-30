---
name: storyboard
description: Interactive storyboard creation for exploring narrative arcs, user journeys, and UI flows. Supports "Narrative" (Product Manager style) and "UI Flow" (Mock-Audit style) modes. Use when you need to visualize ideas, define UI elements, or map emotional journeys before implementation.
---

# Storyboard

This skill enables interactive storyboarding to explore ideas and UI elements through narrative storytelling and structured flow analysis.

## Quick Start

1.  **Select Mode:** Choose between **Narrative Mode** (6-frame emotional arc) or **UI Flow Mode** (HTML grid of UI surfaces).
2.  **Gather Context:** The agent will ask guided questions one by one to define the persona, problem, and solution.
3.  **Draft:** Review the narrative arc or flow structure.
4.  **Visualize:** Generate visuals for each frame or mock using `chatgpt-cli`.

## Modes

-   **Narrative (PM Style):** Best for aligning stakeholders on the human impact and visceral frustration of a problem. Follows a strict 6-frame structure. See [narrative-mode.md](references/narrative-mode.md).
-   **UI Flow (Mock-Audit):** Best for side-by-side review of all UX surfaces in a feature's scope. Uses HTML grids and gap analysis. See [ui-flow-mode.md](references/ui-flow-mode.md).

## Image Generation

When visuals are requested, use the `chatgpt` CLI with the following syntax:

```bash
chatgpt "<prompt>" --model gpt-image-2 --draw --output <filename.png>
```

**Prompt Engineering:**
- For Narrative Mode: Use "low-fidelity fat-marker sharpie sketch style, black and white" for speed and clarity.
- For UI Flow Mode: Use "clean high-fidelity UI mockup, modern aesthetic, [platform] style" for visual exploration.

## Workflow Instructions

1.  **Interactive Context Gathering:** Do NOT assume context. Ask the user questions sequentially:
    - Who is the persona?
    - What is the specific problem or frustration?
    - What is the proposed solution or "Aha!" moment?
2.  **Progressive Disclosure:** Keep the conversation focused. Only load the specific mode reference when the user selects it.
3.  **Gap Analysis:** In UI Flow mode, explicitly identify missing mocks ("gaps") and provide "brainstorm questions" to force design decisions.

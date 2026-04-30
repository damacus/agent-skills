# UI Flow Mode (Mock-Audit)

Follow this workflow to produce a single-page HTML "audit" view that stitches together all UX surfaces for side-by-side review.

## Visual Components

1.  **Flow Diagram:** An ASCII flow diagram at the top (wrapped in `<pre>` tags) showing the user path.
2.  **Mock Grid:** A CSS grid of `<iframe>` tags or images showing each UI screen/state.
3.  **Gap Cards:** Explicitly labeled placeholders for missing mocks ("GAPS").
4.  **Brainstorm Questions:** Each gap MUST include 2-3 questions that force design decisions (e.g., "How does this handle the empty state?").

## Workflow

1.  **Identify Surfaces:** Ask the user to list the key UI screens or states in the flow.
2.  **Define Gaps:** For any missing screen, label it as a "GAP" and draft brainstorm questions.
3.  **Generate Visuals:** Use `chatgpt-cli` to explore UI ideas for specific screens or gaps.
    - Style Suffix: `clean high-fidelity UI mockup, modern aesthetic, [platform/framework] design system style, 4k resolution`
4.  **Stitch HTML:** Create a `storyboard.html` file using Vanilla CSS for styling.

## HTML Template Example

```html
<section class="mock-grid">
  <div class="mock-card">
    <h3>[Screen Name]</h3>
    <iframe src="[url_or_file]"></iframe>
  </div>
  <div class="gap-card">
    <h3>GAP: [Missing Screen]</h3>
    <p>Questions:</p>
    <ul>
      <li>What is the primary CTA here?</li>
      <li>How does the user navigate back?</li>
    </ul>
  </div>
</section>
```

## Example Prompting

```bash
chatgpt "UI mockup for [Screen Name] showing [feature details]. Clean modern design system style." --model gpt-image-2 --draw --output mock_screen.png
```

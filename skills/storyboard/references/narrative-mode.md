# Narrative Mode (PM Style)

Follow this workflow to create an emotional narrative storyboard that aligns stakeholders on a user's problem and solution.

## The 6-Frame Structure

Every narrative storyboard MUST follow this exact sequence to ensure emotional resonance:

1.  **Frame 1: Character:** Introduce the user (persona) in their natural environment.
2.  **Frame 2: Problem:** Show the specific catalyst or incident that causes frustration.
3.  **Frame 3: "Oh Crap" Moment:** The visceral peak of the problem where the user is most desperate or stuck.
4.  **Frame 4: Solution:** The user discovers or tries the new feature/product.
5.  **Frame 5: "Aha" Moment:** The immediate relief or success provided by the solution.
6.  **Frame 6: Life After:** The user is happy, having moved past the problem.

## Workflow

1.  **Ask Guided Questions:**
    - "Who is our main character? Give them a name and a context."
    - "What is the primary frustration they are facing today?"
    - "What does the peak of that frustration look like (the 'Oh Crap' moment)?"
    - "How does our feature/solution solve this?"
2.  **Draft Narrative:** Write a 1-2 sentence description for each of the 6 frames.
3.  **Generate Visuals:** Use `chatgpt-cli` to generate fat-marker sketches for each frame.
    - Style Suffix: `fat-marker sharpie sketch style, black and white, simple line art, emotional character expression`

## Example Prompting

```bash
chatgpt "Frame 3: [Character Name] looking extremely frustrated because [Problem]. Fat-marker sharpie sketch style, black and white." --model gpt-image-2 --draw --output storyboard_f3.png
```

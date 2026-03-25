---
name: screenshot-github
description: Take screenshots of MedTracker pages and attach them directly to GitHub issue or PR comments using GitHub's native browser attachment flow. Use when asked to "screenshot for issue", "attach screenshots to PR", "add visual evidence to GitHub", "post UI screenshots on a PR", or any task involving MedTracker screenshots in GitHub comments.
---

# Screenshot GitHub

Capture MedTracker screenshots locally, then attach them directly in the GitHub comment composer with browser automation. Do not use GitHub Releases for screenshot hosting.

## Principles

- **Use native GitHub comment attachments**
- **Do not use `gh release upload`**
- **Do not commit screenshots into the repo unless the user explicitly asks**
- **Use `gh` only for discovery, not for image hosting**

## Core Workflow

### 1. Ensure Dev Server Is Running

```fish
task dev:up
set PORT (task dev:port)
```

Wait for the server to be healthy before proceeding.

### 2. Identify the Target Page or Pages

If the request is tied to a PR, inspect the changed files first:

```fish
gh pr view {NUMBER} --json files --jq '.files[].path'
```

Map changed files to routes using [medtracker-pages.md](references/medtracker-pages.md). Prioritize pages that visibly changed.

### 3. Log In to MedTracker

Use `mcp-playwright` tools to authenticate against the local app.

```text
browser_navigate → http://localhost:{PORT}/login
browser_snapshot → identify form field refs
browser_fill_form → choose the correct fixture user
browser_click → sign-in button ref
```

Use fixture users from [medtracker-pages.md](references/medtracker-pages.md).

- **Use `nurse.smith@example.com`** for general non-admin screenshots
- **Use `john.doe@example.com`** for `/medication-finder` and admin pages
- **Avoid `damacus@example.com`** because it requires MFA

If redirected to `/otp-auth`, stop using that account and switch to a non-MFA fixture user.

### 4. Take Screenshots

Navigate to each target page and capture:

**Desktop (1440x900):**

```text
browser_resize → 1440, 900
browser_navigate → http://localhost:{PORT}/{path}
browser_take_screenshot → filename: tmp/screenshots/{page}-desktop.png
```

**Full page:**

```text
browser_run_code → async page => {
  await page.screenshot({
    path: 'tmp/screenshots/{page}-desktop-full.png',
    fullPage: true, scale: 'css', type: 'png'
  });
}
```

**Mobile (390x844):**

```text
browser_resize → 390, 844
browser_take_screenshot → filename: tmp/screenshots/{page}-mobile.png
```

Use clear filenames such as:

- `medication-finder-desktop.png`
- `medication-finder-mobile.png`
- `admin-users-desktop-full.png`

### 5. Open the GitHub PR or Issue in the Browser

Navigate to the target conversation directly:

```text
browser_navigate → https://github.com/{owner}/{repo}/pull/{number}
```

Or for an issue:

```text
browser_navigate → https://github.com/{owner}/{repo}/issues/{number}
```

If GitHub shows a sign-in page, stop and ask the user to authenticate in the Playwright browser context. Do not attempt to improvise a non-native upload path.

### 6. Attach Screenshots in the GitHub Comment Composer

In the PR or issue conversation:

```text
browser_snapshot → locate the comment textarea and any “Attach files” control
browser_click → comment textarea or “Write” tab if needed
browser_click → “Attach files” button if present
browser_file_upload → absolute screenshot paths
browser_wait_for → wait until markdown attachment links appear in the textarea
```

GitHub normally inserts attachment markdown automatically after upload. It will look like standard Markdown image references pointing at GitHub-hosted attachment URLs.

If the file chooser does not appear through the visible button, use Playwright to target the file input directly and upload the files there.

### 7. Structure the Comment and Submit

Once GitHub has inserted the uploaded-image Markdown, wrap it in a useful comment:

```text
## Screenshots

### Medication Finder

| Desktop         | Mobile         |
|-----------------|----------------|
| ![desktop](...) | ![mobile](...) |

Key changes:
- Barcode scanner entry point
- Manual barcode fallback
- Mobile layout
```

Then submit the comment with the GitHub UI.

### 8. Verify the Rendered Comment

Confirm that:

- **The uploaded images render inline**
- **The comment is attached to the correct PR or issue**
- **The screenshots match the changed UI**

## Resources

### references/medtracker-pages.md

MedTracker-specific reference: fixture users, route map, viewport sizes, screenshot naming conventions, and account selection notes.

## Dependencies

- `mcp-playwright` MCP server (for browser automation)
- `task` (Taskfile runner for dev server)
- `gh` CLI (optional, for discovering PR files and metadata)

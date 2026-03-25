# MedTracker Page Map & Fixture Users

## Dev Server

```fish
task dev:up          # Start dev environment
task dev:port        # Get dynamic port number
task dev:open-ui     # Open browser
```

Base URL: `http://localhost:<port>` (port from `task dev:port`)

## Fixture Users (all password: `password`)

Prefer users **without MFA** for screenshots. If redirected to `/otp-auth`, sign out and use a different user.

- **General screenshots**: use `nurse.smith@example.com`
- **Medication finder and admin screenshots**: use `john.doe@example.com`

| Email                     | Role  | MFA     | Notes                                   |
|---------------------------|-------|---------|-----------------------------------------|
| `nurse.smith@example.com` | nurse | No      | Sees all patients, best for screenshots |
| `bob.smith@example.com`   | carer | No      | Sees assigned patients only             |
| `john.doe@example.com`    | admin | No      | Full access, use for finder/admin pages |
| `damacus@example.com`     | admin | **Yes** | Avoid — requires TOTP                   |

## Page Routes

| Page                      | Path                         | Description              |
|---------------------------|------------------------------|--------------------------|
| Dashboard                 | `/` or `/dashboard`          | Main dashboard           |
| People                    | `/people`                    | People index             |
| Person detail             | `/people/:id`                | Individual person        |
| Medications               | `/medications`               | Medications index        |
| Medication detail         | `/medications/:id`           | Individual medication    |
| Medication finder         | `/medication-finder`         | Search/scan medicines    |
| Schedules                 | `/schedules`                 | Schedules index          |
| Schedule workflow         | `/schedules/workflow`        | Create schedule workflow |
| Locations                 | `/locations`                 | Locations index          |
| Reports                   | `/reports`                   | Reports index            |
| Profile                   | `/profile`                   | User profile             |
| Admin dashboard           | `/admin`                     | Admin metrics            |
| Admin users               | `/admin/users`               | User management          |
| Admin carer relationships | `/admin/carer_relationships` | Carer management         |
| Admin audit logs          | `/admin/audit_logs`          | Audit log viewer         |
| Admin invitations         | `/admin/invitations`         | Invite management        |
| Login                     | `/login`                     | Authentication page      |

## Viewport Sizes

| Name    | Width | Height | Use              |
|---------|-------|--------|------------------|
| Desktop | 1440  | 900    | Standard desktop |
| Mobile  | 390   | 844    | iPhone 14 Pro    |

## Screenshot Naming

Convention: `<page>-<viewport>.png`

Examples:

- `dashboard-desktop.png`
- `dashboard-mobile.png`
- `medication-finder-desktop.png`
- `admin-users-desktop-full.png` (full page scroll)

## GitHub Comment Attachments

Attach screenshots through the GitHub comment composer, not through releases.

- **Preferred flow**: use the GitHub PR or issue page in Playwright and attach files through the comment UI
- **Expected result**: GitHub uploads the image and inserts Markdown into the comment draft
- **Do not use**: GitHub Releases for screenshot hosting

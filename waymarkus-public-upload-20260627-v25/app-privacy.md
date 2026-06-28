# App Privacy Declaration Draft

Use this as the working answer sheet for App Store Connect. Recheck against the release binary before submission.

## Data Stored Locally

- User Content: field-note text, dictated transcript, optional place, title, note type, visibility choice.
- Purpose: app functionality.
- Linked to the user: no account or persistent identity exists.
- Tracking: no.
- Storage: native notes use an atomically written, iOS-protected file in Application Support; web notes use browser local storage.

## Data Sent When Using Ask

- User Content: place, question/observation, selected lens.
- Purpose: app functionality, specifically source retrieval and answer generation.
- Destination: Waymark's Vercel endpoint; public Wikimedia/official sources are retrieved server-side. If `OPENAI_API_KEY` is configured, the source material and question may be processed by OpenAI.
- Linked to identity: Waymark does not create an account or intentionally attach an identity.
- Tracking: no.

## Permissions

- Microphone: requested only after the user taps the native record control.
- Speech Recognition: requested only for native dictation.
- Location: optional When In Use permission, requested only after the user starts Journey Mode. Raw coordinates and routes are not persisted or uploaded; only generalized encountered state/county labels are retained on device.
- Camera, Photos, Contacts: not requested in version 1.

## Not Collected by the App

- Contact information
- health or fitness data
- financial information
- contacts
- browsing history
- advertising identifiers
- precise device location sent to Waymark servers
- diagnostics through a third-party analytics SDK

## Required Human Review

Confirm Vercel platform logs and any future analytics/crash SDK behavior before answering App Store Connect. Platform-level operational logs can change the declaration.

## Suggested App Store Connect Answers

- **Does this app collect data?** Yes, only when Ask is used.
- **Data type:** User Content → Other User Content.
- **Purpose:** App Functionality.
- **Linked to the user's identity:** No.
- **Used for tracking:** No.
- **Data used for third-party advertising:** No.
- **Precise Location:** Not collected.
- **On-device location use:** Journey Mode processes location transiently to recognize state/county changes. Confirm Apple's current App Privacy interpretation during submission.
- **Diagnostics / Analytics:** Not collected by an app SDK in version 1. Reconfirm hosting logs before submission.

# User Journey Audit

## 1. First Open

Status: implemented.

- Concrete headline and primary Ask CTA.
- A sample question can produce value without prior records.
- Mobile bottom navigation puts Ask, Capture, Map, and Library first.
- Empty Library begins blank rather than showing another person's sample notes.

## 2. Notice and Ask

Status: implemented with degraded mode.

- The user can type or dictate a scene.
- Home detects stocked U.S. place names inside the transcript and launches Ask immediately.
- Ask returns possible lenses, next observations, a caution, a local question, tags, and sources.
- When live research fails, the same structure is generated locally without an API key.
- A missing place is requested instead of silently failing.

## 3. Capture and Save

Status: implemented.

- Text and optional voice capture.
- Lightweight transcript cleanup and generated title.
- Private default and optional public-safe draft candidate.
- Save confirmation shows place, tags, map status, record count, and next actions.
- Native iOS Capture remains usable offline.

## 4. Revisit on the Memory Map

Status: implemented for private records.

- User records are the default map content.
- Destination stock is an explicit separate filter.
- Mobile users can tap pins to open the matching Library record.
- Missing coordinates appear in a Needs location list.
- Empty state routes directly to Ask.

## 5. Organize in Library

Status: implemented.

- Search and meaning-based filters.
- Tags, raw observation, generated interpretation, and next-observation details.
- Follow-up Ask, add to synthesis, export, and delete actions.
- Native iOS Library supports search, detail, share, and swipe deletion.

## 6. Synthesize the Journey

Status: implemented as deterministic version 1.

- Optional date and place selection.
- Main themes, repeated questions, similarities, differences, strongest observations, unknowns, output angles, and next-trip prompts.
- Direct path to Export.

## 7. Export

Status: implemented.

- Multiple record selection.
- Public-safe and writing formats.
- Manual-review warning.
- Web Share API with clipboard fallback; native iOS share sheet for native notes.
- No automatic publishing.

## 8. Privacy, Offline, and Recovery

Status: implemented for release scope.

- Browser and native deletion controls.
- Public Privacy, Terms, and Support pages.
- PWA shell and offline fallback.
- Native Home/Ask error state; native Capture and Library remain available.
- Only microphone and speech permissions are declared for iOS version 1.
- Native notes are written atomically to an iOS-protected Application Support file.
- First launch explains private storage, online Ask, offline behavior, and accuracy limits.
- Every native workflow exposes Privacy and data deletion.
- External reference links open in Safari rather than becoming an in-app general browser.

## Remaining Product Work

- Cross-device synchronization is intentionally absent because there is no account system.
- Native notes and web notes are separate stores in version 1.
- Place coordinates use a curated stock rather than device location or full geocoding.
- Full Xcode 26 archive, device QA, signing, screenshots, and TestFlight submission require the publisher's Apple Developer account and full Xcode installation.
- A monitored support email must be supplied in App Store Connect.

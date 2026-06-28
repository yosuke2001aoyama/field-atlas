# App Review Notes

Waymark U.S. is a private AI field journal for curious travelers. It is not an audio tour, navigation app, trip planner, route tracker, or public social network.

No account is required.

## How to Test

1. Open **Capture** and type a note. Save it as Private.
2. Open **Library** to search, view, share, or delete the on-device note.
3. Open **Map**. Notes with a recognized manually entered city display as MapKit markers; other notes remain listed as Needs location.
   Optionally tap **Start** in Journey Mode. If When In Use location is allowed, Waymark recognizes a generalized state/county change while the app is active. It does not save a raw route and does not request Always Location access.
4. Open **Ask** and enter a place and question. This flow requires internet access and retrieves public reference sources.
   Suggested test: Place `Taos, New Mexico`; question `What historical and economic forces shaped Taos?`
5. Deny microphone permission if desired. Typed capture remains fully available.
6. Turn on airplane mode. Capture and Library continue to work; Home/Ask show an offline state.

## Native Value

The app provides native microphone/speech capture, local persistence, searchable Library, swipe deletion, MapKit visualization, native share sheet, permission handling, and offline note access. Hosted content is used only for online research-oriented pages.

## Safety and Privacy

- Nothing is published by the app.
- Public-safe outputs are drafts for manual review.
- The app does not request location at launch. Optional When In Use access is requested only after Journey Mode is started.
- Journey Mode stores generalized encountered region labels on device, not precise coordinates or a raw route.
- The app should not be used as emergency, medical, legal, safety, or navigation guidance.
- External source links open in Safari rather than turning the embedded Waymark experience into a general web browser.

## Reviewer Contact

Add a monitored reviewer contact, phone number, and support URL in App Store Connect before submission.

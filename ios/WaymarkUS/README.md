# Waymark U.S. iOS App

This is the SwiftUI App Store direction. It combines native private field-note flows with the hosted source-backed Home and Ask experience.

Native features include microphone/speech capture, typed fallback, local persistence, searchable Library, deletion, MapKit markers, native sharing, privacy controls, foreground Journey Mode, Boundary Moments, a CarPlay template scaffold, and offline Capture/Library access.

## Open in Xcode

1. Open `ios/WaymarkUS/WaymarkUS.xcodeproj` in full Xcode.
2. Select the WaymarkUS target.
3. Set your Apple Developer Team and confirm bundle identifier `com.waymarkus.app` is available.
4. Run on a real iPhone and a simulator.
5. Change `WAYMARK_WEB_URL` in `Info.plist` if the production domain changes.

Apple requires uploads made after April 28, 2026 to use Xcode 26 or later with an iOS 26 SDK. Command Line Tools alone are not enough to archive or upload the app.

## CarPlay

Waymark includes a minimal CarPlay scene scaffold in `CarPlaySceneDelegate.swift`. It intentionally avoids long reading, typing, publishing, or route tracking on the car display. The CarPlay screen offers only safe prompts that hand off capture and Journey Mode to iPhone.

CarPlay distribution still requires Apple approval and the relevant CarPlay entitlement for the app category. Without that entitlement, the iPhone app can build for normal use, but CarPlay will not be available to users or accepted as a CarPlay app in review.

## Release Notes

- Microphone and speech permissions are requested only after the user taps the microphone.
- Native notes are stored in an atomically written, iOS-protected Application Support file. Existing UserDefaults notes are migrated once.
- Home/Ask use `WKWebView`; Capture, Library, Map, deletion, and sharing are native.
- Location permission is optional and requested only after the user starts Journey Mode. Journey Mode runs only while the app is in use and stores generalized encountered regions, never a raw route.
- CarPlay support is present as a conservative template scaffold, pending Apple entitlement approval.
- Boundary recognition currently uses Apple reverse geocoding and therefore may require connectivity. A bundled Census county polygon pack is a post-1.0 offline enhancement.
- Complete `../../docs/testflight-plan.md` before submission.
- Copy the completed values from `../../docs/app-store-connect-submission.md` into App Store Connect.

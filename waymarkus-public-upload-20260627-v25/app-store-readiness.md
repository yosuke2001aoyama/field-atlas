# App Store Readiness

## Recommended Architecture

Use the existing SwiftUI app as the iOS product. Do not submit a thin WebView wrapper.

Native SwiftUI owns the high-value mobile flows:

- microphone permission and speech-to-text capture
- private on-device note persistence
- searchable Library and deletion
- native MapKit memory map
- iOS share sheet
- offline Capture and Library

The hosted Waymark web experience remains embedded for Home and Ask, where current public-source research and rapid content iteration are useful. The online URL is configured through `WAYMARK_WEB_URL` in `Info.plist`.

## Completed In The Repository

- Native Capture, protected local note storage, Library, MapKit memory map, deletion, sharing, and offline states.
- First-launch onboarding with privacy and accuracy expectations.
- 1024 px App Store icon with no alpha channel.
- `PrivacyInfo.xcprivacy`, including the approved UserDefaults reason and non-tracking user-content declaration.
- Version `1.0.0` / build `1`, iPhone-only target, Travel category, HTTPS-only transport, and export-compliance declaration.
- External research links leave the embedded Waymark surface and open in Safari.
- Live Privacy, Terms, and Support URLs.
- Store description, keywords, privacy answers, review notes, screenshot story, and TestFlight matrix.

## Publisher-Only Gaps Before Submission

- Add a monitored publisher support email in App Store Connect before submission.
- Confirm the final legal owner, Apple Developer Team, SKU, and copyright.
- Confirm bundle identifier `com.waymarkus.app` is available in the publisher's team.
- Install full Xcode 26 or later and select its developer directory. Command Line Tools alone cannot archive an iOS app.
- Produce final App Store screenshots on required iPhone sizes.
- Test microphone denial, airplane mode, fresh install, update install, and data deletion on physical devices.
- Archive, upload, and run the TestFlight matrix using the publisher's signing identity.
- Complete App Store Connect agreements, age rating, distribution availability, and any applicable trader-status details.

## Review Risk Notes

- The app has meaningful native functionality and is not only a website wrapper.
- Ask requires a network connection; Capture, Library, deletion, and mapped native notes continue offline.
- Waymark does not claim emergency, navigation, safety, legal, or medical reliability.
- No account, community posting, advertising, analytics SDK, tracking, or payment flow is included.
- Do not request camera, photo-library, contacts, or location permissions until a shipped feature genuinely requires them.
- The initial release must be built with Xcode 26 or later and an iOS 26 SDK under Apple's requirements effective April 28, 2026.

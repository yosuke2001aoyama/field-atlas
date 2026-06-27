# TestFlight Plan

## Internal Build

1. Open `ios/WaymarkUS/WaymarkUS.xcodeproj` in full Xcode.
2. Set the Apple Developer Team and confirm bundle ID `com.waymarkus.app` is available.
3. Select a generic iOS device, Product > Archive, then Distribute App > App Store Connect > Upload.
4. Add internal testers in App Store Connect.

## Beta Tester Instructions

Ask testers to capture one typed note, one dictated note, one Ask question, and one note with an unknown place. Then test search, Map, share, individual deletion, Delete All, and airplane mode. Request feedback on one-handed use, transcription quality, answer usefulness, and whether any screen feels like a website wrapper.

Known limitations: Ask requires a connection; location is manually entered; native notes are local to one device; no account or cross-device sync exists. Add a monitored beta contact email in App Store Connect before inviting external testers.

## Test Matrix

- fresh install and upgrade install
- iPhone SE-size, standard iPhone, Pro Max
- light/dark mode and large Dynamic Type
- microphone allowed, denied, and later revoked
- three-second silence auto-stop
- typed-note fallback
- Ask online success, API fallback mode, timeout, 429 rate limit, airplane mode
- Capture and Library while offline
- create, search, share, delete one note, delete all notes
- known and unknown manual locations on Map
- privacy and terms links
- background/foreground restoration

## Exit Criteria

- no crash or blocking blank screen
- all permission prompts match the actual feature
- notes never appear on another user's device
- no API key appears in app/web bundles
- offline state is understandable and Capture remains usable
- support and privacy URLs are live
- reviewer instructions reproduce successfully

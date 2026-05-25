# Waymark U.S. iOS Release Shell

This folder contains a native SwiftUI shell for App Store or TestFlight release.

It includes:

- A native `Briefs` tab that opens the public Waymark U.S. Streamlit app.
- A native `Capture` tab that stores quick private notes locally on the device.
- A native `Privacy` tab explaining the private-to-public workflow.

## Open In Xcode

1. Open `ios/WaymarkUS/WaymarkUS.xcodeproj`.
2. Select the `Waymark U.S.` target.
3. Set your Apple Developer Team under Signing & Capabilities.
4. Replace the placeholder bundle id `com.waymarkus.app` if needed.
5. Add final app icon images to `Assets.xcassets/AppIcon.appiconset`.
6. Run on iPhone or simulator.

## App Store Path

1. Test the app on a real iPhone.
2. In Xcode, choose Product > Archive.
3. Upload the archive to App Store Connect.
4. Complete privacy nutrition labels and review notes in App Store Connect.
5. Submit first to TestFlight, then App Review.

Apple reviews against the current App Review Guidelines, including minimum functionality. This shell includes native quick capture and privacy surfaces so it is more than a plain web wrapper, but final approval still depends on Apple review.

# App Store Connect Submission Sheet

This file contains the values ready to paste into App Store Connect for version 1.0.0.

## App Record

- Platform: iOS
- Name: Waymark U.S.
- Primary language: English (U.S.)
- Bundle ID: `com.waymarkus.app` (publisher must confirm availability)
- SKU suggestion: `WAYMARK-US-IOS-001`
- User access: Full Access
- Category: Travel
- Secondary category: Lifestyle
- Price: Free
- iPhone only: Yes
- Mac availability: Disable for version 1 until tested
- Apple Vision Pro availability: Disable for version 1 until tested

## Version

- Version: `1.0.0`
- Build: `1`
- Copyright: `2026 [LEGAL OWNER]`
- Release: Manually release this version after approval

## URLs

- Marketing URL: `https://waymarkus.vercel.app/`
- Support URL: `https://waymarkus.vercel.app/support.html`
- Privacy Policy URL: `https://waymarkus.vercel.app/privacy.html`

## Export Compliance

- Uses non-exempt encryption: No
- The binary declares `ITSAppUsesNonExemptEncryption = false`.
- Reconfirm after archive validation; Waymark uses standard system HTTPS and does not implement proprietary encryption.

## App Privacy

- Collects data: Yes, when the user submits an Ask request
- User Content → Other User Content
- Purpose: App Functionality
- Linked to identity: No
- Tracking: No
- Advertising: No
- Location: Not collected
- Account: None

## Age Rating Draft

Answer **None** for violence, sexual content, profanity, gambling, controlled substances, horror, medical treatment, and contests unless the hosted product changes before submission.

The app does not provide unrestricted web browsing. Waymark pages are the only content shown inside the app; external source links open in Safari. Re-evaluate the current age-rating questionnaire in App Store Connect because generated place research can discuss ordinary history and politics.

## Review Contact — Publisher Must Fill

- First name: `[REQUIRED]`
- Last name: `[REQUIRED]`
- Phone: `[REQUIRED]`
- Email: `[REQUIRED, MONITORED]`

No login or demo account is required.

## Distribution — Publisher Must Decide

- Countries/regions: `[REQUIRED]`
- EU trader status: `[REQUIRED if distributing in the EU]`
- Content rights: Confirm rights to the Waymark name, icon, screenshots, and supplied copy.

## Upload Sequence

1. Install and open Xcode 26 or later.
2. Set the Apple Developer Team in Signing & Capabilities.
3. Confirm `com.waymarkus.app` can be registered.
4. Run on a physical iPhone and complete `testflight-plan.md`.
5. Archive with a generic iOS device selected.
6. Validate the archive, then upload to App Store Connect.
7. Complete privacy, age rating, distribution, review contact, and screenshots.
8. Select build 1 and submit to App Review.

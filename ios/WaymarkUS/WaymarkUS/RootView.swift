import SwiftUI

struct RootView: View {
    var body: some View {
        TabView {
            WebBriefView()
                .tabItem {
                    Label("Briefs", systemImage: "map")
                }

            QuickCaptureView()
                .tabItem {
                    Label("Capture", systemImage: "mic")
                }

            PrivacyView()
                .tabItem {
                    Label("Privacy", systemImage: "lock.shield")
                }
        }
        .tint(Color(red: 0.15, green: 0.25, blue: 0.21))
    }
}

import SwiftUI

struct PrivacyView: View {
    var body: some View {
        NavigationStack {
            List {
                Section("Default posture") {
                    Label("Notes are private unless you mark them public-ready.", systemImage: "lock")
                    Label("Raw voice transcripts should be reviewed before sharing.", systemImage: "waveform")
                    Label("Exact addresses and real-time movement should not be public.", systemImage: "location.slash")
                }

                Section("Public-ready storytelling") {
                    Text("Waymark U.S. is designed to separate private raw notes, organized personal knowledge, and carefully anonymized public reflection.")
                }

                Section("Release status") {
                    Text("This iOS shell is ready to open in Xcode. Select your Apple Developer Team, archive the app, and upload it to App Store Connect or TestFlight.")
                }
            }
            .navigationTitle("Privacy")
        }
    }
}

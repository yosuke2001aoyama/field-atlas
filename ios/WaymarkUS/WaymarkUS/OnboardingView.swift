import SwiftUI

struct OnboardingView: View {
    @Environment(\.dismiss) private var dismiss
    @AppStorage("waymark.hasSeenOnboarding") private var hasSeenOnboarding = false

    var body: some View {
        ZStack {
            Color(red: 0.96, green: 0.94, blue: 0.89).ignoresSafeArea()
            ScrollView {
                VStack(alignment: .leading, spacing: 28) {
                    Spacer(minLength: 24)
                    Image(systemName: "map.fill")
                        .font(.system(size: 44, weight: .semibold))
                        .foregroundStyle(Color(red: 0.12, green: 0.28, blue: 0.22))
                    Text("Waymark U.S.")
                        .font(.system(.largeTitle, design: .serif, weight: .bold))
                    Text("Understand what you see.\nRemember what you notice.")
                        .font(.title2.weight(.semibold))
                    Text("A private AI field journal for curious travelers. Ask about a place, capture a thought, and build a map of your own observations.")
                        .font(.body).foregroundStyle(.secondary)

                    VStack(alignment: .leading, spacing: 18) {
                        OnboardingRow(icon: "sparkles", title: "Ask better questions", text: "Place answers use public reference sources and should be treated as starting points, not definitive claims.")
                        OnboardingRow(icon: "mic.fill", title: "Capture privately", text: "Dictation is optional. Notes are stored on this iPhone and are never published by Waymark.")
                        OnboardingRow(icon: "map.fill", title: "Map what mattered", text: "Your map shows questions and observations, not a background GPS trail.")
                    }

                    Button {
                        hasSeenOnboarding = true
                        dismiss()
                    } label: {
                        Text("Start noticing")
                            .font(.headline)
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 14)
                    }
                    .buttonStyle(.borderedProminent)
                    .tint(Color(red: 0.12, green: 0.28, blue: 0.22))

                    Text("Nothing is published from Waymark. Ask requires internet access; Capture, Library, and your saved notes remain available offline.")
                        .font(.footnote).foregroundStyle(.secondary)
                }
                .padding(28)
            }
        }
        .interactiveDismissDisabled()
    }
}

private struct OnboardingRow: View {
    let icon: String
    let title: String
    let text: String

    var body: some View {
        HStack(alignment: .top, spacing: 14) {
            Image(systemName: icon)
                .frame(width: 28)
                .font(.title3.weight(.semibold))
                .foregroundStyle(Color(red: 0.12, green: 0.28, blue: 0.22))
            VStack(alignment: .leading, spacing: 4) {
                Text(title).font(.headline)
                Text(text).font(.subheadline).foregroundStyle(.secondary)
            }
        }
    }
}

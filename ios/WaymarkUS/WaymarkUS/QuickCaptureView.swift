import SwiftUI

struct NativeNote: Identifiable, Codable {
    var id = UUID()
    var createdAt = Date()
    var title: String
    var location: String
    var text: String
    var privacy: String
}

@MainActor
final class NativeNoteStore: ObservableObject {
    @Published var notes: [NativeNote] = [] {
        didSet { save() }
    }

    private let key = "waymark.native.notes"

    init() {
        guard let data = UserDefaults.standard.data(forKey: key),
              let decoded = try? JSONDecoder().decode([NativeNote].self, from: data) else {
            return
        }
        notes = decoded
    }

    func add(title: String, location: String, text: String, privacy: String) {
        let cleanTitle = title.trimmingCharacters(in: .whitespacesAndNewlines)
        notes.insert(
            NativeNote(
                title: cleanTitle.isEmpty ? "Untitled movement note" : cleanTitle,
                location: location.trimmingCharacters(in: .whitespacesAndNewlines),
                text: text.trimmingCharacters(in: .whitespacesAndNewlines),
                privacy: privacy
            ),
            at: 0
        )
    }

    private func save() {
        guard let data = try? JSONEncoder().encode(notes) else { return }
        UserDefaults.standard.set(data, forKey: key)
    }
}

struct QuickCaptureView: View {
    @StateObject private var store = NativeNoteStore()
    @State private var title = ""
    @State private var location = ""
    @State private var text = ""
    @State private var privacy = "Private"

    private let privacyOptions = ["Private", "Working", "Public-ready"]

    var body: some View {
        NavigationStack {
            Form {
                Section("Quick capture") {
                    TextField("Title", text: $title)
                    TextField("Where are you?", text: $location)
                    TextEditor(text: $text)
                        .frame(minHeight: 130)
                        .overlay(alignment: .topLeading) {
                            if text.isEmpty {
                                Text("Say or type the messy thought before it disappears.")
                                    .foregroundStyle(.secondary)
                                    .padding(.top, 8)
                                    .padding(.leading, 4)
                            }
                        }
                    Picker("Privacy", selection: $privacy) {
                        ForEach(privacyOptions, id: \.self) { option in
                            Text(option).tag(option)
                        }
                    }
                    Button {
                        store.add(title: title, location: location, text: text, privacy: privacy)
                        title = ""
                        location = ""
                        text = ""
                        privacy = "Private"
                    } label: {
                        Label("Save private note", systemImage: "tray.and.arrow.down")
                    }
                    .disabled(text.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
                }

                Section("Saved on this iPhone") {
                    if store.notes.isEmpty {
                        Text("Native quick notes stay on device. Sync to the web app is a future hook.")
                            .foregroundStyle(.secondary)
                    } else {
                        ForEach(store.notes) { note in
                            VStack(alignment: .leading, spacing: 6) {
                                Text(note.title).font(.headline)
                                Text(note.location.isEmpty ? "No location" : note.location)
                                    .foregroundStyle(.secondary)
                                Text(note.text).lineLimit(3)
                                Text(note.privacy)
                                    .font(.caption.weight(.semibold))
                                    .foregroundStyle(.secondary)
                            }
                            .padding(.vertical, 6)
                        }
                    }
                }
            }
            .navigationTitle("Capture")
        }
    }
}

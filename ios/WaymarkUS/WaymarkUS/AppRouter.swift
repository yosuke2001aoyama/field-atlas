import SwiftUI

enum AppTab: Hashable {
    case ask
    case capture
    case map
    case library
    case home
}

@MainActor
final class AppRouter: ObservableObject {
    @Published var selectedTab: AppTab = .ask
    @Published var capturePlace = ""

    func openCapture(place: String = "") {
        capturePlace = place
        selectedTab = .capture
    }
}

import CoreLocation
import SwiftUI
import UIKit

struct BoundaryMoment: Identifiable, Equatable {
    let id = UUID()
    let county: String
    let state: String

    var displayName: String {
        [county, state].filter { !$0.isEmpty }.joined(separator: ", ")
    }
}

@MainActor
final class JourneyModeManager: NSObject, ObservableObject, CLLocationManagerDelegate {
    @Published private(set) var isActive = false
    @Published private(set) var status = "Journey Mode is off."
    @Published var boundaryMoment: BoundaryMoment?
    @Published private(set) var encounteredRegions: [String] = []

    private let manager = CLLocationManager()
    private let geocoder = CLGeocoder()
    private var lastRegion = ""
    private var lastGeocodedLocation: CLLocation?
    private let encounteredKey = "waymark.encounteredRegions"

    override init() {
        super.init()
        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyHundredMeters
        manager.distanceFilter = 750
        manager.activityType = .otherNavigation
        manager.pausesLocationUpdatesAutomatically = true
        encounteredRegions = UserDefaults.standard.stringArray(forKey: encounteredKey) ?? []
    }

    func toggle() {
        isActive ? stop() : start()
    }

    func start() {
        switch manager.authorizationStatus {
        case .notDetermined:
            status = "Allow location while using Waymark to recognize a new state or county."
            manager.requestWhenInUseAuthorization()
        case .authorizedWhenInUse, .authorizedAlways:
            isActive = true
            status = "Journey Mode is active. Raw routes are not saved."
            manager.startUpdatingLocation()
        case .denied, .restricted:
            isActive = false
            status = "Location access is off. You can enable it in Settings, or keep using notes without Journey Mode."
        @unknown default:
            status = "Journey Mode is unavailable right now."
        }
    }

    func stop() {
        manager.stopUpdatingLocation()
        geocoder.cancelGeocode()
        isActive = false
        status = "Journey Mode is off. No background route is being recorded."
    }

    func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        if manager.authorizationStatus == .authorizedWhenInUse || manager.authorizationStatus == .authorizedAlways {
            start()
        } else if manager.authorizationStatus == .denied || manager.authorizationStatus == .restricted {
            stop()
            status = "Location access is off. Typed and voice notes still work normally."
        }
    }

    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
        status = "Waymark could not determine the current county. Your notes still work without location."
    }

    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        guard isActive, let location = locations.last, location.horizontalAccuracy >= 0 else { return }
        if let lastGeocodedLocation, location.distance(from: lastGeocodedLocation) < 1_000 { return }
        guard !geocoder.isGeocoding else { return }
        lastGeocodedLocation = location
        geocoder.reverseGeocodeLocation(location) { [weak self] placemarks, _ in
            Task { @MainActor in
                guard let self, self.isActive, let placemark = placemarks?.first else { return }
                let state = placemark.administrativeArea ?? ""
                let county = (placemark.subAdministrativeArea ?? "").replacingOccurrences(of: " County", with: "")
                let region = [county, state].filter { !$0.isEmpty }.joined(separator: ", ")
                guard !region.isEmpty else {
                    self.status = "Journey Mode is active. Waiting for a recognizable boundary."
                    return
                }
                self.status = "Journey Mode active · \(region)"
                if self.lastRegion.isEmpty {
                    self.lastRegion = region
                    self.remember(region)
                    return
                }
                guard region != self.lastRegion else { return }
                self.lastRegion = region
                self.remember(region)
                self.boundaryMoment = BoundaryMoment(county: county, state: state)
                UINotificationFeedbackGenerator().notificationOccurred(.success)
            }
        }
    }

    private func remember(_ region: String) {
        guard !encounteredRegions.contains(region) else { return }
        encounteredRegions.append(region)
        UserDefaults.standard.set(encounteredRegions, forKey: encounteredKey)
    }
}

struct BoundaryMomentView: View {
    let moment: BoundaryMoment
    let capture: () -> Void
    let dismiss: () -> Void

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 22) {
                    Image(systemName: "point.bottomleft.forward.to.point.topright.scurvepath.fill")
                        .font(.system(size: 44))
                        .foregroundStyle(.brown)
                    Text("Boundary Moment").font(.caption.weight(.bold)).textCase(.uppercase).foregroundStyle(.secondary)
                    Text("You entered\n\(moment.displayName)")
                        .font(.system(.largeTitle, design: .serif, weight: .bold))
                    Text("A county line organizes roads, courts, schools, services, and local politics. It is not a cultural wall. Notice what changes gradually, and what does not.")
                        .font(.title3).foregroundStyle(.secondary)
                    GroupBox("What to notice") {
                        Text("Watch for changes in road maintenance, land use, public buildings, local institutions, signs, and gathering places. Treat each clue as a question, not a verdict.")
                            .frame(maxWidth: .infinity, alignment: .leading)
                    }
                    GroupBox("What not to assume") {
                        Text("A boundary does not mean everyone inside it shares the same identity, politics, history, or experience.")
                            .frame(maxWidth: .infinity, alignment: .leading)
                    }
                    Button(action: capture) {
                        Label("Capture what I notice", systemImage: "mic.fill")
                            .frame(maxWidth: .infinity).padding(.vertical, 8)
                    }
                    .buttonStyle(.borderedProminent)
                    Button("Not now", action: dismiss).frame(maxWidth: .infinity)
                }
                .padding(24)
            }
            .navigationTitle("New boundary")
            .navigationBarTitleDisplayMode(.inline)
        }
    }
}

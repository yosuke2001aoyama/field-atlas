import CarPlay
import UIKit

final class CarPlaySceneDelegate: UIResponder, CPTemplateApplicationSceneDelegate {
    private var interfaceController: CPInterfaceController?

    func templateApplicationScene(
        _ templateApplicationScene: CPTemplateApplicationScene,
        didConnect interfaceController: CPInterfaceController
    ) {
        self.interfaceController = interfaceController
        interfaceController.setRootTemplate(makeRootTemplate(), animated: true)
    }

    func templateApplicationScene(
        _ templateApplicationScene: CPTemplateApplicationScene,
        didDisconnect interfaceController: CPInterfaceController
    ) {
        self.interfaceController = nil
    }

    private func makeRootTemplate() -> CPListTemplate {
        let capture = CPListItem(text: "Capture a field note", detailText: "Open one-tap capture on iPhone.")
        capture.handler = { [weak self] _, completion in
            self?.showInfo(title: "Use iPhone capture", message: "For safety, Waymark keeps dictation and note editing on the iPhone screen.")
            completion()
        }

        let boundary = CPListItem(text: "Boundary moment", detailText: "Notice the county or state you are crossing.")
        boundary.handler = { [weak self] _, completion in
            self?.showInfo(title: "Boundary moment", message: "Use Journey Mode on iPhone to recognize a new state or county while Waymark is open.")
            completion()
        }

        let privacy = CPListItem(text: "Private by default", detailText: "Waymark does not publish notes or save raw routes.")
        privacy.handler = { [weak self] _, completion in
            self?.showInfo(title: "Private by default", message: "CarPlay shows only safe prompts. Notes, transcripts, and exports stay on iPhone unless you choose to share.")
            completion()
        }

        let section = CPListSection(items: [capture, boundary, privacy])
        let template = CPListTemplate(title: "Waymark U.S.", sections: [section])
        template.tabTitle = "Waymark"
        template.tabImage = UIImage(systemName: "map")
        return template
    }

    private func showInfo(title: String, message: String) {
        let ok = CPAlertAction(title: "OK", style: .default) { _ in }
        let alert = CPAlertTemplate(titleVariants: ["\(title)\n\(message)"], actions: [ok])
        interfaceController?.presentTemplate(alert, animated: true)
    }
}

import SwiftUI
import WebKit

private let waymarkURL = URL(string: "https://cb3ygfxmn39gr3dzsjdyu6.streamlit.app/")!

struct WebBriefView: View {
    @State private var isLoading = true

    var body: some View {
        NavigationStack {
            ZStack {
                WaymarkWebView(url: waymarkURL, isLoading: $isLoading)
                    .ignoresSafeArea(edges: .bottom)

                if isLoading {
                    ProgressView("Opening Waymark U.S.")
                        .padding(18)
                        .background(.ultraThinMaterial)
                        .clipShape(RoundedRectangle(cornerRadius: 14, style: .continuous))
                }
            }
            .navigationTitle("Waymark U.S.")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Link(destination: waymarkURL) {
                        Image(systemName: "safari")
                    }
                    .accessibilityLabel("Open in Safari")
                }
            }
        }
    }
}

struct WaymarkWebView: UIViewRepresentable {
    let url: URL
    @Binding var isLoading: Bool

    func makeCoordinator() -> Coordinator {
        Coordinator(isLoading: $isLoading)
    }

    func makeUIView(context: Context) -> WKWebView {
        let configuration = WKWebViewConfiguration()
        configuration.allowsInlineMediaPlayback = true
        let view = WKWebView(frame: .zero, configuration: configuration)
        view.navigationDelegate = context.coordinator
        view.scrollView.contentInsetAdjustmentBehavior = .never
        view.load(URLRequest(url: url))
        return view
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {}

    final class Coordinator: NSObject, WKNavigationDelegate {
        @Binding var isLoading: Bool

        init(isLoading: Binding<Bool>) {
            _isLoading = isLoading
        }

        func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
            isLoading = false
        }

        func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
            isLoading = false
        }
    }
}

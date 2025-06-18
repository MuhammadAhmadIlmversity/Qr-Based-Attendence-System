import { Html5QrcodeScanner } from "html5-qrcode";
import { useEffect } from "react";

export default function QRScanner({ onScanSuccess }) {
    useEffect(() => {
        const scanner = new Html5QrcodeScanner("qr-reader", {
            fps: 10,
            qrbox: 250,
        });

        scanner.render(
            (decodedText) => {
                onScanSuccess(decodedText);
                scanner.clear();
            },
            (errorMessage) => {
                // ignore scan errors
            }
        );

        return () => scanner.clear();
    }, [onScanSuccess]);

    return (
        <div className="flex flex-col items-center justify-center">
            <div id="qr-reader" className="w-full max-w-md" />
        </div>
    );
}

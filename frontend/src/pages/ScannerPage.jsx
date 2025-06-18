import React, { useState, useRef, useEffect } from "react";
import jsQR from "jsqr";
import QRScanner from "../components/QRScanner"; // Ensure correct path

export default function ScannerPage() {
    const [scannedData, setScannedData] = useState("");
    const [deviceId, setDeviceId] = useState("DEV002");
    const [doorId, setDoorId] = useState("DOOR-A2");
    const [responseMessage, setResponseMessage] = useState("");
    const [useCamera, setUseCamera] = useState(false);
    const fileInputRef = useRef(null);

    // Prevent browser from opening image when dropped on window
    useEffect(() => {
        const preventDefaults = (e) => {
            e.preventDefault();
            e.stopPropagation();
        };
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            window.addEventListener(eventName, preventDefaults, false);
        });
        return () => {
            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                window.removeEventListener(eventName, preventDefaults, false);
            });
        };
    }, []);

    const handleImageUpload = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        const img = new Image();
        const reader = new FileReader();

        reader.onload = function (e) {
            img.src = e.target.result;
        };

        img.onload = function () {
            const canvas = document.createElement("canvas");
            canvas.width = img.width;
            canvas.height = img.height;
            const ctx = canvas.getContext("2d");
            ctx.drawImage(img, 0, 0, img.width, img.height);
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            const qrCode = jsQR(imageData.data, canvas.width, canvas.height);

            if (qrCode) {
                handleScanSuccess(qrCode.data);
            } else {
                alert("No QR code found in the image.");
            }
        };

        reader.readAsDataURL(file);
    };

    const handleDrop = (event) => {
        event.preventDefault();
        const file = event.dataTransfer.files[0];
        if (file) {
            handleImageUpload({ target: { files: [file] } });
        }
    };

    const handleScanSuccess = async (data) => {
        setScannedData(data);

        if (!deviceId || !doorId) {
            alert("Please enter Device ID and Door ID before scanning.");
            return;
        }

        try {
            const queryParams = new URLSearchParams({
                token: data,
                device_id: deviceId,
                door_id: doorId
            }).toString();

            const response = await fetch(`http://localhost:8000/qr/scan?${queryParams}`, {
                method: "POST"
            });

            const result = await response.json();

            if (response.ok) {
                setResponseMessage(`✅ ${result.message}`);
            } else {
                const errorDetail = typeof result.detail === "string"
                    ? result.detail
                    : JSON.stringify(result.detail);
                setResponseMessage(`❌ ${errorDetail}`);
            }

        } catch (error) {
            setResponseMessage(`⚠️ Error calling scan API: ${error.message}`);
        }
    };

    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 px-4">
            <h1 className="text-2xl font-bold mb-4">QR Code Scanner</h1>

            <div className="mb-4 w-full max-w-sm">
                <input
                    type="text"
                    placeholder="Device ID"
                    value={deviceId}
                    onChange={(e) => setDeviceId(e.target.value)}
                    className="mb-2 p-2 w-full border rounded"
                />
                <input
                    type="text"
                    placeholder="Door ID"
                    value={doorId}
                    onChange={(e) => setDoorId(e.target.value)}
                    className="mb-4 p-2 w-full border rounded"
                />
            </div>

            {useCamera ? (
                <QRScanner onScanSuccess={handleScanSuccess} />
            ) : (
                <div
                    onDrop={handleDrop}
                    onDragOver={(e) => e.preventDefault()}
                    className="w-full max-w-sm mb-4 p-6 border-2 border-dashed rounded-lg text-center bg-white"
                >
                    <p className="text-gray-600 mb-2">Drag & drop QR image here or</p>
                    <input
                        type="file"
                        accept="image/*"
                        onChange={handleImageUpload}
                        ref={fileInputRef}
                        className="mb-2 w-full"
                    />
                </div>
            )}

            <button
                onClick={() => setUseCamera(!useCamera)}
                className="mt-2 text-sm text-blue-600 hover:underline"
            >
                {useCamera ? "Switch to Image Upload" : "Switch to Camera Scanner"}
            </button>

            {scannedData && (
                <div className="bg-white p-4 rounded shadow mt-4 text-center">
                    <p className="text-green-600 font-semibold">Scan Successful!</p>
                    <p className="text-sm break-all mt-2 text-gray-700">{scannedData}</p>
                </div>
            )}

            {responseMessage && (
                <div className="mt-4 p-3 bg-white border rounded shadow max-w-sm text-center">
                    <p
                        className={`text-sm font-medium ${responseMessage.startsWith("✅")
                            ? "text-green-600"
                            : "text-red-600"
                            }`}
                    >
                        {responseMessage}
                    </p>
                </div>
            )}
        </div>
    );
}

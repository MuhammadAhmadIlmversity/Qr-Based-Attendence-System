import React, { useState, useRef, useEffect } from "react";

export default function QRDisplayPage() {
    const [empId, setEmpId] = useState("");
    const [qrCode, setQrCode] = useState(null);
    const [token, setToken] = useState(null);
    const [loading, setLoading] = useState(false);
    const inputRef = useRef();

    useEffect(() => {
        inputRef.current.focus();
    }, []);

    const fetchQR = async () => {
        if (!empId.trim()) {
            alert("Please enter a valid Employee ID.");
            return;
        }

        setLoading(true);
        try {
            const res = await fetch(`http://localhost:8000/qr/current?emp_id=${empId}`);
            if (!res.ok) throw new Error("Failed to fetch QR");

            const data = await res.json();
            setQrCode(data.qr_code);
            setToken(data.token);
        } catch (err) {
            alert("Error: " + err.message);
            setQrCode(null);
            setToken(null);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
            <h1 className="text-2xl font-bold mb-6 text-gray-800">Generate QR Code</h1>
            <input
                ref={inputRef}
                type="text"
                placeholder="Employee ID"
                value={empId}
                onChange={(e) => setEmpId(e.target.value)}
                className="mb-4 p-2 border rounded w-64 focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
            <button
                onClick={fetchQR}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
                disabled={loading}
            >
                {loading ? "Generating..." : "Fetch QR Code"}
            </button>

            {qrCode && (
                <div className="mt-6 p-4 bg-white rounded shadow">
                    <img
                        src={`data:image/png;base64,${qrCode}`}
                        alt="QR Code"
                        className="border mb-2"
                    />
                </div>
            )}
        </div>
    );
}

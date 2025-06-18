import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ScannerPage from "./pages/ScannerPage";
import QRDisplayPage from "./pages/QRDisplayPage"; // you'll create this later

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<QRDisplayPage />} />
        <Route path="/scan" element={<ScannerPage />} />
      </Routes>
    </Router>
  );
}

export default App;

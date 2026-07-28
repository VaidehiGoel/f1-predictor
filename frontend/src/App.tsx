import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import Predictions from "./pages/Predictions";
import About from "./pages/About";

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-asphalt flex flex-col">
        <Navbar />
        <main className="max-w-6xl mx-auto px-6 py-12 flex-1 w-full">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/predictions" element={<Predictions />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;
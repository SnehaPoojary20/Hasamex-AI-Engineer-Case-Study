import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./Components/Navbar/Navbar.jsx";
import Footer from "./Components/Footer/Footer.jsx";

import AskTab from "./Components/Ask Tab/askTab.jsx";
import GuideTab from "./Components/Guide Tab/guideTab.jsx";
import ThemesTab from "./Components/Themes Tab/themesTab.jsx";
import QuotesTab from "./Components/Quote Block/quoteBlock.jsx";

function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <main className="app-main">
        <Routes>
          <Route path="/" element={<AskTab />} />
          <Route path="/guide" element={<GuideTab />} />
          <Route path="/themes" element={<ThemesTab />} />
          <Route path="/quotes" element={<QuotesTab />} />
        </Routes>
      </main>

      <Footer />
    </BrowserRouter>
  );
}

export default App;
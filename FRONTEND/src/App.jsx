import "./App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import AskTab from "./Components/Ask Tab/askTab.jsx";
import GuideTab from "./Components/Guide Tab/guideTab.jsx"
import QuoteBlock from "./Components/Quote Block/quoteBlock.jsx"
import ThemesTab from "./Components/Themes Tab/themesTab.jsx"

function App() {
  return (
    <BrowserRouter>
   
      <main className="app-main">
        <Routes>
        <Route path="/ask" element={<AskTab />} />
          <Route path="/guide" element={<GuideTab />} />
          <Route path="/quote" element={<QuoteBlock/>} />
          <Route path="/themes" element={<ThemesTab />} />
        </Routes>
      </main>

      </BrowserRouter>
  );
}

export default App;
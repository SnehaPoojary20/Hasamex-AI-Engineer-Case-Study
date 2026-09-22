import "./App.css";

import AskTab from "./Components/Ask Tab/askTab.jsx";
import GuideTab from "./Components/Guide Tab/guideTab.jsx";
import ThemesTab from "./Components/Themes Tab/themesTab.jsx";

function App() {
  return (
    <main className="app-main">
      <GuideTab />

      <AskTab />

      <ThemesTab />
    </main>
  );
}

export default App;
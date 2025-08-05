import "./App.css"
import QuerySection from "./components/QuerySection"


function WebsiteSection() {
    return (
    <div className="section section-middle">
      Websites
    </div>
    )
}

function PhrasesSection() {
  return (
    <div className="section section-middle">
      Phrases
    </div>
  )
}


function App() {
  return (
  <div className="app-container"> 
    <QuerySection />
    <WebsiteSection />
    <PhrasesSection />
  </div>
  );
};

export default App;

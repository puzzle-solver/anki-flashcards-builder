import Grid from "@mui/material/Grid";
import { useState } from 'react';
import QuerySection from "./components/QuerySection"
import WebsiteSection from "./components/WebsiteSection";
import "./App.css"


function PhrasesSection() {
  return (
    <div className="section">
      Phrases
    </div>
  )
}


function App() {
  const [queries, setQueries] = useState([]);
  return (
  <Grid className="app-container"> 
    <QuerySection queries={queries} setQueries={setQueries} />
    <WebsiteSection queries={queries} />
    <PhrasesSection />
  </Grid>
  );
};

export default App;

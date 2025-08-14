import Grid from "@mui/material/Grid";
import { useState } from 'react';
import QuerySection from "./components/QuerySection"
import WebsiteSection from "./components/WebsiteSection";
import PhrasesSection from "./components/PhrasesSection";
import "./App.css"


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

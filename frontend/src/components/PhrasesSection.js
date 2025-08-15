import { useState } from "react";
import {
  Button,
  Box,
  Card,
  CardContent,
  CardActions,
  Typography,
} from "@mui/material";

function Flashcard({ phrase, translation, explanation, url }) {
  return (
    <Card variant="outlined" sx={{ margin: "5px" }}>
      <CardContent>
        <Typography sx={{ color: "text.secondary", mb: 1.5 }}>
          {phrase}
        </Typography>
        <Typography variant="body3"> {translation} </Typography>
        <Typography variant="body2"> {explanation} </Typography>
        <CardActions>
          <a href={url} target="_blank" rel="noopener noreferrer">
            <Button size="small">Source Website</Button>{" "}
          </a>
        </CardActions>
      </CardContent>
    </Card>
  );
}

export default function PhrasesSection() {
  const [phrases, setPhrases] = useState([]);
  function fetchPhrases() {
    const new_phrases = [
      {
        id: 1,
        translation: "to ask",
        phrase: "chiedere",
        explanation: "Chiedere means 'to ask'",
        url: "https://google.com",
      },
      {
        id: 2,
        translation: "light (as opposed to heavy)",
        phrase: "leggero",
        explanation: "leggero means light (as in not heavy)",
        url: "https://google.com",
      },
    ];
    setPhrases(new_phrases);
  }

  return (
    <div className="section">
      <h2 className="title">Step 3: Final phrases produced</h2>
      <p className="subtitle">
        Browse the phrases produced and download the selected ones.
      </p>
      <Box sx={{ p: 2, display: "flex", flexDirection: "column", gap: 2 }}>
        <Button variant="contained" onClick={fetchPhrases}>
          Find phrases
        </Button>
        <Box>
          {phrases.map((item, index) => (
            <Flashcard
              phrase={item.phrase}
              translation={item.translation}
              explanation={item.explanation}
              url={item.url}
            />
          ))}
        </Box>
      </Box>
    </div>
  );
}

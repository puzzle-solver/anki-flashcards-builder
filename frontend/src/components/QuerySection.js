import { useState } from "react";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import IconButton from "@mui/material/IconButton";
import DeleteIcon from "@mui/icons-material/Delete";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import Checkbox from "@mui/material/Checkbox";

function TextInput({ keywords, setKeywords }) {
  const [inputValue, setInputValue] = useState("");

  // This function is called when the user presses Enter
  const handleEnterPress = (event) => {
    // Check if the pressed key is 'Enter'
    if (event.key === "Enter") {
      // Prevent the default form submission behavior (if any)
      event.preventDefault();

      // Call the submit logic
      handleSubmit();
    }
  };

  // This function is called on button click or Enter key press
  const handleSubmit = () => {
    if (inputValue.trim() !== "") {
      setKeywords([...keywords, inputValue]);
      setInputValue(""); // Clear the input field after submission
    }
  };

  const deleteItem = (i) => {
    setKeywords(keywords.filter((query, index) => index !== i));
  };

  return (
    <Box
      sx={{
        p: 2,
        display: "flex",
        flexDirection: "column",
        gap: 2,
        maxWidth: 400,
      }}
    >
      <TextField
        label="Enter a new value"
        variant="outlined"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyDown={handleEnterPress} // Attach the event handler here
      />

      <Button variant="contained" onClick={handleSubmit}>
        Submit
      </Button>

      {keywords.length > 0 && (
        <Box>
          <List>
            {keywords.map((value, index) => (
              <ListItem
                secondaryAction={
                  <IconButton
                    edge="end"
                    aria-label="delete"
                    onClick={() => deleteItem(index)}
                  >
                    <DeleteIcon />
                  </IconButton>
                }
              >
                <ListItemText primary={value} />
              </ListItem>
            ))}
          </List>
        </Box>
      )}
    </Box>
  );
}

export default function QuerySection({ queries, setQueries }) {
  const [keywords, setKeywords] = useState([]);
  let selectedRows = new Set();

  function FetchQueries() {
    setQueries([
      {
        id: 1,
        keyword: "music",
        text: "Who is the most known singer from the 80s?",
      },
      {
        id: 2,
        keyword: "history",
        text: "What is the brief history of Quing dinasty?",
      },
    ]);
    selectedRows.clear();
  }

  function updateSelectedRows(idx) {
    if (selectedRows.has(idx)) {
      console.log("deleting ", idx);
      selectedRows.delete(idx);
    } else {
      console.log("adding ", idx);
      selectedRows.add(idx);
    }
  }

  const deleteItem = (i) => {
    setKeywords(keywords.filter((query, index) => index !== i));
  };

  function DeleteSelectedRows() {
    setQueries(queries.filter((row) => !selectedRows.has(row.id)));
    selectedRows.clear();
  }

  const columns = [
    { field: "keyword", headerName: "Keyword" },
    { field: "text", headerName: "Search query", width: 512 },
  ];
  return (
    <div className="section ">
      <h2 className="title">Step 1: Provide a set of keywords</h2>
      <p className="subtitle">
        Enter a few keywords or subjects that are interesting to you.
      </p>
      <TextInput keywords={keywords} setKeywords={setKeywords} />

      <Box sx={{ p: 2, display: "flex", flexDirection: "column", gap: 2 }}>
        <Button variant="contained" onClick={FetchQueries}>
          Generate queries
        </Button>

        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>
                  <IconButton>
                    <DeleteIcon onClick={() => DeleteSelectedRows()} />
                  </IconButton>
                </TableCell>
                <TableCell align="left">
                  <b>Keyword</b>
                </TableCell>
                <TableCell align="left">
                  <b>Query</b>
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {queries.map((row) => (
                <TableRow
                  key={row.id}
                  sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                >
                  <TableCell component="th" scope="row">
                    {<Checkbox onClick={() => updateSelectedRows(row.id)} />}
                  </TableCell>
                  <TableCell align="left">{row.keyword}</TableCell>
                  <TableCell align="left">{row.text}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
    </div>
  );
}

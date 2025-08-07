import { useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';
import Avatar from '@mui/material/Avatar';


function TextInput( { keywords, setKeywords }) {
  const [inputValue, setInputValue] = useState('');

  // This function is called when the user presses Enter
  const handleEnterPress = (event) => {
    // Check if the pressed key is 'Enter'
    if (event.key === 'Enter') {
      // Prevent the default form submission behavior (if any)
      event.preventDefault();
      
      // Call the submit logic
      handleSubmit();
    }
  };

  // This function is called on button click or Enter key press
  const handleSubmit = () => {
    if (inputValue.trim() !== '') {
      setKeywords([...keywords, inputValue]);
      setInputValue(''); // Clear the input field after submission
    }
  };

  const deleteItem = (i) => {
    setKeywords(keywords.filter((query, index) => index !== i));
  }

  return (
    <Box sx={{ p: 2, display: 'flex', flexDirection: 'column', gap: 2, maxWidth: 400 }}>
      <TextField
        label="Enter a new value"
        variant="outlined"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyDown={handleEnterPress} // Attach the event handler here
      />
      
      {/* An optional submit button */}
      <Button variant="contained" onClick={handleSubmit}>
        Submit
      </Button>

      {/* Display the submitted values */}
      {keywords.length > 0 && (
        <Box>
          {keywords.map((value, index) => (
            <List>
            <ListItem
                  secondaryAction={
                    <IconButton edge="end" aria-label="delete" onClick={() => deleteItem(index)}>
                      <DeleteIcon/>
                    </IconButton>
                  }
            >
            <ListItemText primary={value}/>
            </ListItem>
            </List>
          ))}
        </Box>
      )}
    </Box>
  );
}


export default function QuerySection() {
  const [keywords, setKeywords] = useState([]);
  const [queries, setQueries] = useState([]);
  function FetchQueries() {
    setQueries([
        {"id": 1, "keyword": "music", "text": "Who is the most known singer from the 80s?"},
        {"id": 2, "keyword": "history", "text": "What is the brief history of Quing dinasty?"}
    ])
  }
  const columns = [
    { field: "keyword", headerName: "Keyword"},
    { field: "text", headerName: "Search query", width: 250 },
  ]
  const paginationModel = { page: 0, pageSize: 10 };
  return (
    <div className="section">
      <h2 className="title">
        Step 1: Provide a set of queries
      </h2>
      <p className="subtitle">
        Enter a few keywords or subjects that are interesting to you.
      </p>
      <TextInput keywords={keywords} setKeywords={setKeywords} />
      
      <Button variant="contained" onClick={FetchQueries}>
        Generate queries
      </Button>
 
    <Box sx={{ height: 400, width: 400, mt: 2, minwidth: 0  }}>
    <DataGrid
        rows={queries}
        columns={columns}
        initialState={{ pagination: { paginationModel } }}
        pageSizeOptions={[5, 10]}
        checkboxSelection
        sx={{ border: 0 }}
    />
     </Box>

    </div>
  )
}

import { useState } from 'react';
import {
  TableContainer,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  Paper,
  Button,
  IconButton,
  Checkbox,
  Popper,
  Box,
  Fade,
  Typography,
} from '@mui/material'; 
import DeleteIcon from '@mui/icons-material/Delete';


export default function WebsiteSection( {queries} ) {
  const [websites, setWebsites] = useState([])
  const [selectedRows, setSelectedRows] = useState(new Set())
  // State for the pop-up
  const [anchorEl, setAnchorEl] = useState(null); // Element that anchors the pop-up
  const [openPopper, setOpenPopper] = useState(false); // Controls pop-up visibility
  const [popperContent, setPopperContent] = useState(''); // Content to display in pop-up

  function fetchWebsites() {
    const websites = [
      {"id": 1, "url": "https://en.wikipedia.org/wiki/Qing_dynasty","text": "<h1> Wikipedia - Quing dynasty </h1>"},
      {"id": 2, "url": "https://www.google.com", "text": "<h1> Google </h1>"}
    ];
    setWebsites(websites);
  }

  function updateSelectedRows(idx) {
    const newSelectedRows = new Set(selectedRows);
    if (selectedRows.has(idx)) {
      newSelectedRows.delete(idx);
    }
    else {
      newSelectedRows.add(idx);
    }
    setSelectedRows(newSelectedRows)
  }

  function deleteSelectedRows() {
    setWebsites(websites.filter((row => !selectedRows.has(row.id))));
    selectedRows.clear()
  }

  // Event handler for mouse entering the Lookup cell
  const handleLookupMouseEnter = (event, text) => {
    setPopperContent(text);
    setAnchorEl(event.currentTarget); // Set the current cell as the anchor
    setOpenPopper(true);
  };

  // Event handler for mouse leaving the Lookup cell
  const handleLookupMouseLeave = () => {
    setOpenPopper(false);
    setAnchorEl(null);
    setPopperContent('');
  };

  const id = openPopper ? 'lookup-popper' : undefined;

  return (
  <div className="section">
    <h2 className="title">
      Step 2: Browse the web for relevant webistes
    </h2>
    <p className="subtitle">
      Delete queries you don't like or add new if needed. Then, click "search".
    </p>
    <Box sx={{ p: 2, display: 'flex', flexDirection: 'column', gap: 2}}>
      <Button variant="contained" onClick={fetchWebsites}>
        Search
      </Button>
      <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell><IconButton><DeleteIcon onClick={() => deleteSelectedRows()} /></IconButton></TableCell>
                <TableCell align="left"><b>URL</b></TableCell>
                <TableCell align="left"><b>Lookup</b></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {websites.map((row) => (
              <TableRow
                key={row.id}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              >
                <TableCell component="th" scope="row">{<Checkbox onClick={() => updateSelectedRows(row.id)}/>}</TableCell>
                <TableCell align="left">
                  <a
                      href={row.url}
                      className="text-blue-600 hover:underline"
                    >
                      {row.url}
                    </a>
                </TableCell>
                <TableCell
                    align="left"
                    onMouseEnter={(e) => handleLookupMouseEnter(e, row.text)}
                    onMouseLeave={handleLookupMouseLeave}
                    className="cursor-help"
                  >
                    {row.text.substring(0, 50)}... {/* Display truncated text */}
                </TableCell>
              </TableRow>
            ))}
            </TableBody>
          </Table>
        </TableContainer>
        {/* Popper component for the lookup text */}
        <Popper id={id} open={openPopper} anchorEl={anchorEl} placement="right-start" transition>
          {({ TransitionProps }) => (
            <Fade {...TransitionProps} timeout={350}>
              <Paper className="p-4 shadow-xl rounded-lg max-w-sm bg-white border border-gray-300"
                    sx={{ overflowY: 'auto' }} // Added for scrollability
              >
                  {/* Render HTML content using dangerouslySetInnerHTML */}
                  <div dangerouslySetInnerHTML={{ __html: popperContent }} />
              </Paper>
            </Fade>
          )}
        </Popper>
    </Box>
  </div>
    )
}
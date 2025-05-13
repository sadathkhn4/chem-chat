const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;

app.use(express.static('public'));  // Serve the frontend HTML
app.use('/logs', express.static('logs'));  // Serve log files
app.use(bodyParser.json());

const PY_SERVER_URL = 'http://localhost:5000/chat';  // URL for the Flask backend

// Proxy /chat endpoint to Flask server
app.post('/chat', async (req, res) => {
  try {
    const response = await axios.post(PY_SERVER_URL, req.body);
    res.json(response.data);
  } catch (error) {
    console.error('Error contacting Flask server:', error.message);
    res.status(500).json({ response: 'Server error. Please try again later.', done: false });
  }
});

app.post('/reset', async (req, res) => {
  try {
    const response = await axios.post('http://localhost:5000/reset', req.body);
    res.json(response.data);
  } catch (error) {
    console.error('Error resetting chat:', error.message);
    res.status(500).json({ message: 'Reset failed' });
  }
});

// Proxy log file download from Flask
app.get('/logs/:filename', async (req, res) => {
  const filename = req.params.filename;
  try {
    const response = await axios.get(`http://localhost:5000/logs/${filename}`, { responseType: 'stream' });
    res.setHeader('Content-Disposition', `inline; filename="${filename}"`);
    response.data.pipe(res);
  } catch (error) {
    console.error('Error fetching log file:', error.message);
    res.status(404).send('Log file not found');
  }
});




// Start the Node.js server
app.listen(port, () => {
  console.log(`Node server running on http://localhost:${port}`);
});

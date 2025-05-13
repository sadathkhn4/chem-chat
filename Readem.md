# ChemChat App

A simple web application that simulates a chemical reaction chat, collects user inputs, generates follow-up questions, logs the conversation, and provides the user with a downloadable log file. The backend is split into two services: a **Node.js** server (handles frontend and communication with the Python backend) and a **Python Flask** server (handles chat logic, reactions, and logging).

---

## Features

- Chat interface where the user can type messages related to chemical reactions.
- Backend implemented in **Python (Flask)** for handling the chat logic.
- **Node.js** server as a proxy to manage frontend and interact with the Python backend.
- Follow-up questions for chemical reactions (SN1, SN2, Additions, Substitution) are served based on user input.
- User responses are logged and saved to a file, which is accessible for download.
- The app supports a RESTful API to reset chat progress.

---

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript (Vanilla)
- **Backend:**  
  - **Node.js** (Express) for the frontend and API proxy  
  - **Python** (Flask) for chat logic and logging

---

## Prerequisites

Before running this application locally, ensure you have the following installed:

- **Node.js** (for the Node.js server)
- **Python** (for the Flask backend)
- **Axios** (for making HTTP requests from Node.js to Flask backend)

---

## Install Dependencies

**Node.js dependencies:**  
Navigate to the `node-server` folder and run:
`npm install`

**Python dependencies:**  
Navigate to the `python-backend` folder and run:
`pip install -r requirements.txt`

**Redis dependency:**
Navigate to the `python-backend` folder and run:
WSL setup and redis installation:
```
sudo apt update
sudo apt install redis-server
```

---

## Project Setup

### 1. Clone the Repository
```
git clone https://github.com/your-repo-url.git
cd chat-to-log-app
```
### 2.1. Set up Python Flask Backend
```
cd python-backend
python server.py
```
The Flask backend will run on [http://localhost:5000](http://localhost:5000).

### 2.2. Set up Redis
```
redis-server --port 6380
```

### 3. Set up Node.js Server
```
cd node-server
npm start
```
The Node.js server will run on [http://localhost:3000](http://localhost:3000).

### 4. Access the Application

Open your browser and navigate to [http://localhost:3000](http://localhost:3000) to interact with the chat application.

### 5. Resetting the Chat

To reset the chat and start fresh, simply click the **"Start New Chat"** button in the UI. The chat history and log files will be cleared, and a new session will begin.

---

## API Endpoints

| Endpoint             | Method | Description                                              |
|----------------------|--------|----------------------------------------------------------|
| `/chat`              | POST   | Send a message to the server and get a follow-up question or the log file. |
| `/reset`             | POST   | Reset the chat session for all users.                    |
| `/logs/{filename}`   | GET    | Access a log file by filename.                           |

**POST /chat**  
Request Body:
{
"user_id": "user1",
"message": "SN1"
}

Response:
{
"done": false,
"response": "What is the substrate?",
"log": "user1_1747070463.txt"
}

**POST /reset**  
Response:
{
"status": "success",
"message": "Chat reset successfully"
}


**GET /logs/{filename}**  
Example:  
`http://localhost:3000/logs/user1_1747070463.txt`

---

## Folder Structure

chat-to-log-app/
│
├── node-server/ # Node.js frontend and API proxy
│ ├── public/ # Static files (HTML, CSS, JS)
│ ├── server.js # Node.js server to handle requests
│ └── package.json # Node.js dependencies
│
└── python-backend/ # Python Flask backend
├── server.py # Flask app to handle chat logic
└── requirements.txt # Python dependencies


---

## Contributing

Feel free to fork and contribute to this project! Submit issues and pull requests as needed.

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.
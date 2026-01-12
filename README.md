# Project Socrates Developer

An AI-powered Socratic tutor built with FastAPI and React that uses OpenAI's GPT-4.1-mini to generate thoughtful, question-based responses to user queries. The application includes NLP preprocessing with custom tokenization and rule-based lemmatization.

## Features

- 🤖 **Socratic Dialogue**: AI generates probing questions instead of direct answers
- 💬 **Real-time Chat**: Instant responses with token usage tracking
- 🔍 **NLP Preprocessing**: The application includes basic NLP preprocessing with custom tokenization and rule-based lemmatization.
- 📊 **Metadata Display**: Shows word count, sentence count, and token usage
- 🎨 **Clean UI/UX**: Modern gradient design with responsive chat interface
- 🚀 **Production-Ready**: Deployed and live with error handling

## Tech Stack

### Backend
- **Framework**: FastAPI
- **LLM**: OpenAI GPT-4.1-mini
- **NLP**: Custom Python helpers (tokenization, simple lemmatization)
- **Language**: Python 3.9+
- **Server**: Uvicorn

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **HTTP Client**: Axios
- **Styling**: CSS3
- **Deployment**: Vercel

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+**: Download from [python.org](https://www.python.org)
- **Node.js 16+**: Download from [nodejs.org](https://nodejs.org)
- **Git**: Download from [git-scm.com](https://git-scm.com)
- **OpenAI API Key**: Get from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

## Installation and Execution

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/project-socrates-developer.git
cd project-socrates-developer
```

### Step 2: Backend Setup

#### 2.1 Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 2.2 Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2.3 Set Environment Variables

Create a `.env` file in the project root (same folder as `main.py`):

```env
OPENAI_API_KEY=sk-your-actual-key-here
```

Replace `sk-your-actual-key-here` with your real OpenAI API key.

#### 2.4 Run Backend Server

```bash
uvicorn main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**Verify**: Open http://127.0.0.1:8000/docs in your browser to see the Swagger API documentation.

### Step 3: Frontend Setup

#### 3.1 Navigate to Frontend Directory

```bash
cd frontend
```

#### 3.2 Install Node Dependencies

```bash
npm install
```

#### 3.3 Create Environment File

Create `frontend/.env.local` (same folder as `package.json`):

```env
VITE_API_URL=http://127.0.0.1:8000
```

#### 3.4 Run Frontend Development Server

```bash
npm run dev
```

You should see:
```
VITE v5.0.0  ready in 123 ms
➜  Local:   http://localhost:5173/
```

**Open the app**: Go to http://localhost:5173 in your browser.

### Step 4: Test the Application

1. Type a question in the chat box, for example:
   ```
   Why are plants green?
   ```

2. Click **Send**

3. You should see:
   - Your question in a blue bubble (right side)
   - GPT's Socratic response in a light bubble (left side)
   - Metadata showing word count, sentence count, and tokens used

## Example Interaction

**User Question:**
```
How does machine learning work?
```

**AI Response:**
```
What real-world problem are you trying to solve with machine learning? 
Can you describe what patterns or relationships you'd like the computer to learn?

5 words, 2 sentences · 68 tokens
```

## Project Structure

```
project-socrates-developer/
├── main.py                          # FastAPI application with routes
├── requirements.txt                 # Python dependencies
├── render.yaml                      # Render deployment configuration
├── .env                             # Environment variables (API keys)
├── .gitignore                       # Git ignore file
├── README.md                        # This file
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── ChatInterface.jsx   # Main chat component
    │   │   └── ChatInterface.css   # Chat styles
    │   ├── App.jsx                 # React app root
    │   ├── main.jsx                # React entry point
    │   ├── App.css
    │   └── index.css
    ├── public/
    │   └── vite.svg
    ├── .env.local                  # Frontend environment variables
    ├── package.json                # Node.js dependencies
    ├── vite.config.js              # Vite configuration
    └── vercel.json                 # Vercel deployment configuration
```

## Troubleshooting

### Backend Issues

| Problem | Solution |
|---------|----------|
| Backend won't start | Ensure Python 3.9+, virtual env is activated, and `pip install -r requirements.txt` completed successfully |
| "OPENAI_API_KEY not found" | Check `.env` file exists in project root with a valid API key. Restart `uvicorn` after creating/updating `.env` |
| Port 8000 already in use | Use a different port: `uvicorn main:app --reload --port 8001` |

### Frontend Issues

| Problem | Solution |
|---------|----------|
| Frontend can't reach backend | Ensure backend is running on `http://127.0.0.1:8000`. Check `VITE_API_URL` in `.env.local` matches |
| Pink "Something went wrong" error | Open browser console (F12) and check for CORS or network errors. Verify backend is running |
| "npm command not found" | Install Node.js from [nodejs.org](https://nodejs.org). Restart terminal after installation |
| "node_modules not found" | Run `npm install` in the `frontend` directory |

### General Issues

| Problem | Solution |
|---------|----------|
| CORS errors | Backend CORS middleware is configured for `http://localhost:5173`. Ensure frontend URL matches |
| API returns 500 error | Check browser console and backend terminal for error details. Verify API key is valid |

## Building for Production

### Frontend Production Build

```bash
cd frontend
npm run build
```

This creates a `dist` folder with optimized, minified files ready for deployment.

### Verify Production Build Locally

```bash
npm run preview
```

## Deployment

### Deploy Backend to Render

1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Create new Web Service
4. Connect GitHub repository
5. Set environment:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port 8000`
   - Add Environment Variable: `OPENAI_API_KEY=your_key`
6. Click Deploy

You'll get a URL like: `https://socratic-api.onrender.com`

### Deploy Frontend to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Import GitHub repository
3. Set Root Directory to `frontend`
4. Add Environment Variable:
   - `VITE_API_URL=https://socratic-api.onrender.com` (your Render backend URL)
5. Click Deploy

You'll get a URL like: `https://project-socrates-developer.vercel.app`

## Live Application

- **Frontend**: [https://socrates-developer-ai.vercel.app/]
- **Backend API**: [https://socrates-developer-ai-1.onrender.com/docs#/default/dialogue_dialogue_post]
- **API Documentation**: [https://socrates-developer-ai-1.onrender.com/docs]

## Useful Commands

### Backend Commands

```bash
# Run with auto-reload (development)
uvicorn main:app --reload

# Run for production
uvicorn main:app --host 0.0.0.0 --port 8000

# View API documentation
# Open: http://127.0.0.1:8000/docs
```

### Frontend Commands

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Install dependencies
npm install
```

## API Endpoints

### POST /dialogue

Send a user question and receive a Socratic response.

**Request:**
```json
{
  "user_input": "Why are plants green?",
  "conversation_history": []
}
```

**Response:**
```json
{
  "socratic_response": "What role do you think pigments play in the color of plants? How might sunlight interact with these pigments?",
  "processed_input": "4 words, 1 sentences",
  "tokens_used": 73
}
```

## Technologies Used

- **FastAPI**: Modern Python web framework for building APIs
- **OpenAI API**: GPT-4.1-mini for Socratic dialogue generation
- **React**: JavaScript library for building user interfaces
- **Vite**: Next generation frontend build tool
- **Axios**: Promise-based HTTP client for JavaScript
- **Uvicorn**: ASGI web server for Python

## Key Features Explained

### Socratic Method
The AI generates probing questions rather than direct answers, encouraging critical thinking and deeper understanding.

### NLP Preprocessing
User input is tokenized into words and sentences using simple regex helpers, then lemmatized with lightweight suffix rules to normalize word forms (for example, “plants” → “plant”).

### Token Tracking
Display of token usage helps understand API costs and conversation length.

### Error Handling
Comprehensive try/except blocks catch API errors, rate limits, and network issues, providing user-friendly error messages.

## Contributing

Feel free to fork this repository and submit pull requests for any improvements.

## Author

Atharva Santosh Mavale

## Contact

For questions or support, contact: atharvamavale40@gmail.com

## Acknowledgments

- Valearnis for the assignment
- OpenAI for GPT-4.1-mini API
- FastAPI and React communities for excellent frameworks

---

**Last Updated**: January 2026

**Status**: ✅ Production Ready - Live and Deployed

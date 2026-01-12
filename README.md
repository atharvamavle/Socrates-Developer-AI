Installation and Execution Guide
Prerequisites
Python 3.9+ installed

Node.js 16+ installed

Git installed

OpenAI API key (get from https://platform.openai.com/api-keys)

Part 1: Backend Setup
1.1 Clone the Repository
bash
git clone https://github.com/YOUR_USERNAME/project-socrates-developer.git
cd project-socrates-developer
1.2 Create a Python Virtual Environment
Windows (PowerShell):

powershell
python -m venv venv
venv\Scripts\Activate.ps1
macOS / Linux:

bash
python3 -m venv venv
source venv/bin/activate
1.3 Install Python Dependencies
bash
pip install -r requirements.txt
Expected output: Successfully installed fastapi uvicorn pydantic python-dotenv nltk openai ...

1.4 Set Up Environment Variables
Create a .env file in the project root (same folder as main.py):

text
OPENAI_API_KEY=sk-ant-XXXXXXXXXXXXXXXXXXXXX
Replace sk-ant-... with your actual OpenAI API key from https://platform.openai.com/api-keys.

1.5 Run the Backend Server
bash
uvicorn main:app --reload
Expected output:

text
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
Test it: Open http://127.0.0.1:8000/docs in your browser. You should see the Swagger API docs with a /dialogue endpoint.

Part 2: Frontend Setup
2.1 Navigate to Frontend Directory
bash
cd frontend
2.2 Install Node Dependencies
bash
npm install
Expected output: added X packages in Y seconds

2.3 Create Environment File
Create frontend/.env.local (same folder as package.json):

text
VITE_API_URL=http://127.0.0.1:8000
2.4 Run the Development Server
bash
npm run dev
Expected output:

text
  VITE v5.0.0  ready in 123 ms
  ➜  Local:   http://localhost:5173/
Open the app: Click the link or go to http://localhost:5173 in your browser.

Part 3: Test the Full Application
3.1 Ask a Question
In the chat UI, type: Why are plants green?

Click Send.

You should see:

Your question in a blue bubble (right side).

GPT's Socratic response in a light bubble (left side).

Metadata: X words, Y sentences · Z tokens.

3.2 Example Interaction
User Input:

text
How does machine learning work?
Expected Output:

text
What real-world problem are you trying to solve with machine learning? 
Can you describe what patterns or relationships you'd like the computer to learn?

5 words, 2 sentences · 68 tokens
Part 4: Troubleshooting
Problem	Solution
Backend won't start	Ensure Python 3.9+, virtual env activated, and pip install -r requirements.txt ran.
"OPENAI_API_KEY not found"	Check .env file exists in project root and has a valid key. Restart uvicorn.
Frontend can't reach backend	Ensure backend is running on http://127.0.0.1:8000. Check VITE_API_URL in .env.local.
Pink "Something went wrong" error	Check browser console (F12) for CORS or network errors. Verify backend is running.
"npm command not found"	Install Node.js from https://nodejs.org (v16+). Restart terminal after install.
Part 5: Build for Production
Frontend Build
bash
cd frontend
npm run build
Creates a dist folder with optimized, minified files ready for deployment.

Deployment Checklist
 Backend deployed to Render with OPENAI_API_KEY env var set

 Frontend deployed to Vercel with VITE_API_URL pointing to backend

 GitHub repo pushed with README.md, requirements.txt, render.yaml

 Live links verified and working

 Submitted GitHub + live app link to assignment email

File Structure Reference
text
project-socrates-developer/
├── main.py                          # FastAPI application
├── requirements.txt                 # Python dependencies
├── render.yaml                      # Render deployment config
├── .env                             # Environment variables (OPENAI_API_KEY)
├── .gitignore                       # Git ignore file
├── README.md                        # Project documentation
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── ChatInterface.jsx   # Chat component
    │   │   └── ChatInterface.css   # Chat styles
    │   ├── App.jsx                 # Main React app
    │   ├── main.jsx                # Entry point
    │   ├── App.css
    │   └── index.css
    ├── public/
    │   └── vite.svg
    ├── .env.local                  # Frontend env (VITE_API_URL)
    ├── package.json                # Node dependencies
    ├── vite.config.js              # Vite config
    └── vercel.json                 # Vercel deployment config
Useful Commands Reference
Backend:

bash
# Run dev server with auto-reload
uvicorn main:app --reload

# Run production server
uvicorn main:app --host 0.0.0.0 --port 8000

# Check API docs
curl http://127.0.0.1:8000/docs
Frontend:

bash
# Run dev server
npm run dev

# Build for production
npm run build

# Preview production build locally
npm run preview
Next Steps
Test locally with both servers running.

Deploy backend to Render (https://render.com).

Deploy frontend to Vercel (https://vercel.com).

Verify live links work.

Submit links to assignment email.

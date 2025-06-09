# Leave-Management-System
🚀 Leave Management System
This repository contains the full stack for a Leave Management System, comprising a FastAPI backend and two Next.js frontends — one for 👨‍🎓 Students and one for 🧑‍💼 Admins.

🧱 Project Structure
graphql
Copy code
📁 FastAPI-Server/          # Backend API built with FastAPI 🐍
📁 Student-Application/     # Next.js frontend for students 👨‍🎓
📁 Admin-Application/       # Next.js frontend for administrators 🧑‍💼
🛠️ Getting Started
Follow the instructions below to set up and run the project locally.

✅ Prerequisites
🟢 Node.js (LTS version recommended)

📦 npm / yarn / pnpm / bun

🐍 Python 3.8+

🔧 pip (Python package installer)

🛢️ MySQL or MariaDB running locally

🔧 1. Backend Setup – FastAPI-Server
Navigate into the backend directory and install Python dependencies:

bash
Copy code
cd FastAPI-Server
pip install -r requirements.txt
💡 Tip: If requirements.txt doesn’t exist yet, create one after installing your packages:

bash
Copy code
pip freeze > requirements.txt
💻 2. Frontend Setup – Student-Application and Admin-Application
👨‍🎓 Student Application
bash
Copy code
cd Student-Application
npm install   # or: yarn install / pnpm install / bun install
🧑‍💼 Admin Application
bash
Copy code
cd Admin-Application
npm install   # or: yarn install / pnpm install / bun install
▶️ 3. Running the Applications
🐍 Run the Backend
bash
Copy code
cd FastAPI-Server
uvicorn main:app --reload
📍 Available at: http://127.0.0.1:8000

👨‍🎓 Run the Student Frontend
bash
Copy code
cd Student-Application
npm run dev
📍 Available at: http://localhost:3000

🧑‍💼 Run the Admin Frontend
bash
Copy code
cd Admin-Application
npm run dev
📍 Usually runs on: http://localhost:3001
(Or another available port if 3000 is in use)

📝 Additional Notes
🔐 Make sure to configure your database credentials securely (avoid hardcoding sensitive info).

🗂️ Add config.py or .env to .gitignore to keep secrets safe.

🛢️ Start your MySQL database before launching the backend.

🌐 API docs are available at: http://127.0.0.1:8000/docs


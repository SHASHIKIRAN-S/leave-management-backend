
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

🛢️ MySQL running locally

🔧 1. Backend Setup – FastAPI-Server
Navigate into the backend directory and install Python dependencies:

bash
Copy code
cd FastAPI-Server
pip install -r requirements.txt
💡 Tip: If requirements.txt doesn’t exist yet, generate it after installing your packages:

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
📍 Usually runs at: http://localhost:3001

📝 Additional Notes
🔐 Make sure to configure your database credentials securely (avoid hardcoding sensitive info).

🗂️ Add config.py or .env to .gitignore to keep secrets safe.

🛢️ Start your MySQL database before launching the backend.

🌐 API docs available at: http://127.0.0.1:8000/docs

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

sql
Copy code
MIT License

Copyright (c) 2025 SHASHIKIRAN

Permission is hereby granted, free of charge, to any person obtaining a copy  
of this software and associated documentation files (the "Software"), to deal  
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
copies of the Software, and to permit persons to whom the Software is  
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in  
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER  
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM,  
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OF OTHER DEALINGS IN  
THE SOFTWARE.

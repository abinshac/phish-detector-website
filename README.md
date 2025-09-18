
Phish Detector Website (no Docker)
=================================

Run backend:
1. cd backend
2. python -m venv venv
3. source venv/bin/activate   # Windows: venv\Scripts\activate
4. pip install -r requirements.txt
5. python src/train.py
6. uvicorn src.serve:app --reload --port 8000

Run frontend:
1. cd frontend
2. npm install
3. npm run dev
4. Open http://localhost:5173 in your browser

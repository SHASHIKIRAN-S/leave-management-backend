from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date # Import 'date' specifically for clarity
import pymysql
import pymysql.cursors
from fastapi.middleware.cors import CORSMiddleware

# This timestamp isn't used in the FastAPI app logic, but it's fine to keep.
timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# MySQL connection config
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_db_name', # Ensure this database exists
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

app = FastAPI(title="Leave Tracker API", version="1.1")

origins = [
    "http://localhost",
    "http://localhost:5173", # Common port for Vite development server
    "http://localhost:3000", # Common port for React development server
    # Add the actual URL(s) where your frontend application will be running
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

def get_db_connection():
    """Create and return a new connection to the MySQL database."""
    try:
        conn = pymysql.connect(**MYSQL_CONFIG)
        return conn
    except pymysql.Error as e:
        # It's good practice to log the full exception for debugging
        print(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail=f"Connection error to database: {e}")

# --- Pydantic Models ---
class LeaveRequest(BaseModel):
    student_id: str = Field(..., strip_whitespace=True)
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")  # YYYY-MM-DD
    reason: str = Field(..., min_length=1)

class UpdateStatusRequest(BaseModel):
    student_id: str = Field(..., strip_whitespace=True)
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    new_status: str = Field(..., pattern="^(approved|rejected|pending)$")

class LeaveEntry(BaseModel):
    student_id: str
    date: str # This remains 'str' as the output should be a string
    reason: str
    status: str

# NEW: Pydantic Model for a Student
class StudentEntry(BaseModel):
    student_id: str
    student_name: Optional[str] = None # Assuming 'student_name' might be optional or in another table


## API Endpoints

@app.post("/leave/submit", response_model=Dict[str, str])
def submit_leave(leave_request: LeaveRequest):
    """Submit a leave request for a student."""
    try:
        datetime.strptime(leave_request.date, "%Y-%m-%d")  # Validate date format
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Please use YYYY-MM-DD.")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check for duplicate leave requests
        cursor.execute(
            "SELECT 1 FROM leave_request WHERE student_id = %s AND date = %s",
            (leave_request.student_id, leave_request.date)
        )
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail=f"Leave already submitted for {leave_request.date} by {leave_request.student_id}.")

        # Insert new leave record; assuming leave_request table has a 'student_name' column nullable
        # NOTE: If student_name is not being provided at submission, consider if it should be in this table
        cursor.execute(
            "INSERT INTO leave_request (student_id, date, reason, status) VALUES (%s, %s, %s, %s)",
            (leave_request.student_id, leave_request.date, leave_request.reason, "pending")
        )
        conn.commit()
        return {"message": f"Leave submitted for {leave_request.student_id} on {leave_request.date}."}
    except pymysql.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()

@app.put("/leave/update-status", response_model=Dict[str, str])
def update_leave_status(update_status: UpdateStatusRequest):
    """Update the status of a leave request."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE leave_request SET status = %s WHERE student_id = %s AND date = %s",
            (update_status.new_status, update_status.student_id, update_status.date)
        )
        conn.commit()
        if cursor.rowcount > 0:
            return {"message": f"Leave on {update_status.date} for {update_status.student_id} marked as {update_status.new_status}."}
        else:
            raise HTTPException(status_code=404, detail=f"No leave request found for {update_status.student_id} on {update_status.date}.")
    except pymysql.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error while updating status: {e}")
    finally:
        conn.close()

@app.get("/leave/history/{student_id}", response_model=List[LeaveEntry])
def get_leave_history(
    student_id: str,
    start_date: Optional[str] = Query(None, pattern=r"^\d{4}-\d{2}-\d{2}$"),
    end_date: Optional[str] = Query(None, pattern=r"^\d{4}-\d{2}-\d{2}$"),
):
    """Retrieve leave history for a student, optionally filtered by date range."""
    # Validate date inputs if provided
    for d in [start_date, end_date]:
        if d:
            try:
                datetime.strptime(d, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format in query parameter. Use YYYY-MM-DD.")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "SELECT student_id, date, reason, status FROM leave_request WHERE student_id = %s"
        params = [student_id]

        if start_date:
            query += " AND date >= %s"
            params.append(start_date)
        if end_date:
            query += " AND date <= %s"
            params.append(end_date)

        query += " ORDER BY date DESC"

        cursor.execute(query, params)
        raw_leave_history = cursor.fetchall()

        # Explicitly convert datetime.date objects to strings
        processed_leave_history = []
        for entry in raw_leave_history:
            # pymysql returns datetime.date objects for DATE columns
            if isinstance(entry['date'], date):
                entry['date'] = entry['date'].isoformat() # Converts date object to "YYYY-MM-DD" string
            processed_leave_history.append(entry)

        return processed_leave_history
    except pymysql.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()

@app.get("/admin/leaves", response_model=List[LeaveEntry])
def admin_list_leaves(
    student_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None, pattern="^(pending|approved|rejected)$"),
    limit: int = Query(50, ge=1, le=500),
):
    """
    Admin endpoint to list leave requests filtered by student_id and status.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "SELECT student_id, date, reason, status FROM leave_request WHERE 1=1"
        params = []

        if student_id:
            query += " AND student_id = %s"
            params.append(student_id)
        if status:
            query += " AND status = %s"
            params.append(status)

        query += " ORDER BY date DESC LIMIT %s"
        params.append(limit)

        cursor.execute(query, params)
        raw_leaves = cursor.fetchall()

        # Explicitly convert datetime.date objects to strings for Pydantic compatibility
        processed_leaves = []
        for entry in raw_leaves:
            if isinstance(entry['date'], date):
                entry['date'] = entry['date'].isoformat()
            processed_leaves.append(entry)

        return processed_leaves
    except pymysql.Error as e:
        print(f"Database error fetching leaves: {e}")
        raise HTTPException(status_code=500, detail=f"Database error fetching leaves: {e}")
    finally:
        conn.close()

@app.get("/students/all", response_model=List[StudentEntry])
def admin_list_students(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """
    Admin endpoint to list all registered students.
    Assumes a 'students' table with 'student_id' and 'student_name' columns.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "SELECT student_id, student_name FROM students ORDER BY student_name LIMIT %s OFFSET %s"
        params = [limit, offset]
        cursor.execute(query, params)
        students = cursor.fetchall()
        return students
    except pymysql.Error as e:
        print(f"Database error fetching students: {e}")
        raise HTTPException(status_code=500, detail=f"Database error fetching students: {e}")
    finally:
        conn.close()

@app.post("/admin/leaves/{student_id}/{date}/accept", response_model=Dict[str, str])
def admin_accept_leave(student_id: str, date: str):
    """Admin action to accept a leave request."""
    return _admin_set_leave_status(student_id, date, "approved")

@app.post("/admin/leaves/{student_id}/{date}/reject", response_model=Dict[str, str])
def admin_reject_leave(student_id: str, date: str):
    """Admin action to reject a leave request."""
    return _admin_set_leave_status(student_id, date, "rejected")

def _admin_set_leave_status(student_id: str, date: str, new_status: str) -> Dict[str, str]:
    try:
        datetime.strptime(date, "%Y-%m-%d")  # Validate date format
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Please use YYYY-MM-DD.")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE leave_request SET status = %s WHERE student_id = %s AND date = %s",
            (new_status, student_id, date)
        )
        conn.commit()
        if cursor.rowcount > 0:
            return {"message": f"Leave on {date} for {student_id} marked as {new_status}."}
        else:
            raise HTTPException(status_code=404, detail=f"No leave request found for {student_id} on {date}.")
    except pymysql.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error while updating status: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

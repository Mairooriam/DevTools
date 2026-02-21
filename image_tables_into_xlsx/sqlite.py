from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import sqlite3
import json

app = FastAPI(title="Database Query API", version="1.0.0")

# Database configuration
DATABASE_PATH = "database.db"

class QueryRequest(BaseModel):
    query: str
    params: Optional[List[Any]] = None

class QueryResponse(BaseModel):
    data: List[Dict[str, Any]]
    columns: List[str]
    row_count: int

def get_db_connection():
    """Get database connection"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Database Query API"}

@app.get("/tables")
async def get_tables():
    """Get all table names in the database"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        return {"tables": tables}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.get("/tables/{table_name}/schema")
async def get_table_schema(table_name: str):
    """Get schema information for a specific table"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name});")
        schema = cursor.fetchall()
        if not schema:
            raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")
        
        columns = []
        for col in schema:
            columns.append({
                "name": col[1],
                "type": col[2],
                "nullable": not col[3],
                "default": col[4],
                "primary_key": bool(col[5])
            })
        
        return {"table": table_name, "columns": columns}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.get("/tables/{table_name}/data")
async def get_table_data(table_name: str, limit: Optional[int] = 100, offset: Optional[int] = 0):
    """Get data from a specific table with pagination"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # TODO: Replace with actual query - PLACEHOLDER
        query = f"SELECT * FROM {table_name} LIMIT ? OFFSET ?"
        cursor.execute(query, (limit, offset))
        
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        data = [dict(row) for row in rows]
        
        return QueryResponse(
            data=data,
            columns=columns,
            row_count=len(data)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.post("/query")
async def execute_query(request: QueryRequest):
    """Execute a custom SQL query"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # TODO: Add your custom queries here - PLACEHOLDER
        if request.params:
            cursor.execute(request.query, request.params)
        else:
            cursor.execute(request.query)
        
        # Handle SELECT queries
        if request.query.strip().upper().startswith('SELECT'):
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            data = [dict(row) for row in rows]
            
            return QueryResponse(
                data=data,
                columns=columns,
                row_count=len(data)
            )
        else:
            # Handle INSERT, UPDATE, DELETE queries
            conn.commit()
            return {"message": "Query executed successfully", "rows_affected": cursor.rowcount}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.get("/contactors")
async def get_contactors():
    """Get all contactors - PLACEHOLDER QUERY"""
    # TODO: Replace with your actual contactor query
    query = "SELECT * FROM contactor_type LIMIT 50"
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        data = [dict(row) for row in rows]
        
        return QueryResponse(
            data=data,
            columns=columns,
            row_count=len(data)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.get("/contactors/{contactor_id}")
async def get_contactor_by_id(contactor_id: int):
    """Get specific contactor by ID - PLACEHOLDER QUERY"""
    # TODO: Replace with your actual contactor by ID query
    query = "SELECT * FROM contactor_type WHERE id = ?"
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, (contactor_id,))
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"Contactor with ID {contactor_id} not found")
        
        columns = [description[0] for description in cursor.description]
        data = dict(row)
        
        return {"contactor": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# PLACEHOLDER ENDPOINTS - Add your specific queries here
@app.get("/custom/query1")
async def custom_query_1():
    """Custom query placeholder 1"""
    # TODO: Add your custom query logic here
    query = "SELECT COUNT(*) as total FROM sqlite_master WHERE type='table'"
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        return {"result": dict(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.get("/custom/query2")
async def custom_query_2():
    """Custom query placeholder 2"""
    # TODO: Add your custom query logic here
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
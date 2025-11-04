from fastapi import FastAPI
import pymysql as db

app = FastAPI()
@app.get("/")
def hello():
    return {"message": "Hello, World!"}

n1=200
n2=100
@app.get("/add")
def add():
    return {"sum": n1 + n2}

@app.get("/subtract")
def subtract():
    return {"difference": n1 - n2}

@app.get("/multiply")
def multiply():
    return {"product": n1 * n2}

@app.get("/check_db")
def check_db():
    mydb = db.connect(
        host="localhost",
        user="root",
        password="root",
        database="testdb"
    )
    cursor = mydb.cursor()
    # cursor.execute("SHOW TABLES;")
    if cursor==False:
        return "Database connection failed"
    else:
        return "Database connection successful"

def get_connection():
    return db.connect(
        host="localhost",
        user="root",
        password="root")
   
@app.get("/fetch_all_db")
def fetch_all_db():
    mydb =get_connection()
    cursor = mydb.cursor()
    cursor.execute("SHOW DATABASES;")
    curr=cursor.fetchall()
    cursor.close()
    mydb.close()
    return f"{curr}"

@app.get("/count_db")
def count_db():
    mydb = get_connection()
    cursor = mydb.cursor()
    cursor.execute("SHOW DATABASES;")
    curr=cursor.fetchall()
    cursor.close()
    mydb.close()
    return f"Total databases: {len(curr)}"

@app.get("/create_db")
def create_db():
    mydb = get_connection()
    cursor = mydb.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS datasciencedb;")
    cursor.close()
    mydb.close()
    return "Database created successfully"

@app.get("/create_table")
def create_table():
    mydb = get_connection()
    cursor = mydb.cursor()
    cursor.execute("USE datasciencedb;")
    cursor.execute("""CREATE TABLE IF NOT EXISTS employees (
        id INT AUTO_INCREMENT PRIMARY KEY, 
        name VARCHAR(255) NOT NULL,
        salary FLOAT NOT NULL);""")
    cursor.close()
    mydb.close()
    return "Table created successfully"  

@app.get("/insert_employee")
def insert_employee():
    mydb = get_connection()
    cursor = mydb.cursor()
    cursor.execute("USE datasciencedb;")
    cursor.execute("INSERT INTO employees (name, salary) VALUES ('John Doe', 50000),('mukund',20000);")
    mydb.commit()
    cursor.close()
    mydb.close()
    return "Employee inserted successfully"  

@app.get("/fetch_employees")
def fetch_employees():
    mydb = get_connection()
    cursor = mydb.cursor()
    cursor.execute("USE datasciencedb;")
    cursor.execute("SELECT * FROM employees;")
    curr=cursor.fetchall()
    cursor.close()
    mydb.close()
    return f"{curr}"

@app.get("/delete_employee/{emp_id}")
def delete_employee(emp_id: int):
    mydb = get_connection()
    cursor = mydb.cursor()
    cursor.execute("USE datasciencedb;")
    cursor.execute("DELETE FROM employees WHERE id = %s;", (emp_id,))
    mydb.commit()
    cursor.close()
    mydb.close()
    return f"Employee with id {emp_id} deleted successfully"

if __name__ == "__main__":
    app.run(debug=True)
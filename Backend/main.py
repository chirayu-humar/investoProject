import csv
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import sqlite3

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):

    # Connect to the SQLite database
    conn = sqlite3.connect('mydatabase.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    contents = await file.read()
    decoded_contents = contents.decode("utf-8")

     # Create a CSV reader
    reader = csv.reader(decoded_contents.splitlines(), delimiter=',')

    # Extract column names from the first row
    column_names = next(reader)

    # Initialize an empty list to store rows as objects
    rows = []

    # this statement is to remove previous table before creating new table
    cursor.execute("DROP TABLE IF EXISTS company_details;")

    cursor.execute(f'''CREATE TABLE IF NOT EXISTS company_details (
                    {column_names[0]} TEXT,
                    {column_names[1]} REAL,
                    {column_names[2]} REAL,
                    {column_names[3]} REAL,
                    {column_names[4]} REAL,
                    {column_names[5]} REAL,
                    {column_names[6]} TEXT
                )''')

    conn.commit()
    # Process each row and create objects
    for row in reader:
        row_object = {}
        for i, value in enumerate(row):
            column_name = column_names[i]
            row_object[column_name] = value
        rows.append(row_object)
        # cursor.execute("""
        #     INSERT INTO company_details ('datetime', 'close', 'high', 'low', 'open', 'volume', 'instrument')
        #     VALUES
        #         (?, ?, ?, ?, ?, ?, ?)
        # """, (
        #     row_object['datetime'],
        #     row_object['close'],
        #     row_object['high'],
        #     row_object['low'],
        #     row_object['open'],
        #     row_object['volume'],
        #     row_object['instrument']
        # ))
        # starting
        try: 
            cursor.execute(f"""
                INSERT INTO company_details (`datetime`, `close`, `high`, `low`, `open`, `volume`, `instrument`)
                VALUES
                    ("{row_object['datetime']}", {row_object['close']}, {row_object['high']}, {row_object['low']}, {row_object['open']}, {row_object['volume']}, "{row_object['instrument']}")
            """)
            conn.commit()
        except Exception as e:
            print("Error during table creation:", e)
        # ending 

    print("Column Names:", column_names)
    print("Row first", rows[0])

    # for rowElement in rows:
    #     row_object = rowElement
    #     cursor.execute(f"""
    #         INSERT INTO company_details (`datetime`, `close`, `high`, `low`, `open`, `volume`, `instrument`)
    #         VALUES
    #             ("{row_object['datetime']}", {row_object['close']}, {row_object['high']}, {row_object['low']}, {row_object['open']}, {row_object['volume']}, "{row_object['instrument']}")
    #     """)

    conn.close()

    return {"message": "CSV file uploaded and processed."}

@app.get("/saved-data")
async def bringSavedData():

    # Connect to the SQLite database
    conn = sqlite3.connect('mydatabase.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM company_details;")
    fetch_size = 100
    totalRows = []
    rows = cursor.fetchmany(fetch_size)
    while rows:
        totalRows.extend(rows)
        # print(rows)
        # Fetch the next batch of rows
        rows = cursor.fetchmany(fetch_size)
    conn.close()
    return {"data": totalRows}
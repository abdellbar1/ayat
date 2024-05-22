from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    # Connect to SQLite database
    conn = sqlite3.connect('quran_data.db')
    cursor = conn.cursor()
    
    # Get the list of tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # Fetch data from each table and store in a dictionary
    data = {}
    for table in tables:
        table_name = table[0]
        cursor.execute("PRAGMA table_info({})".format(table_name))
        columns = cursor.fetchall()
        
        cursor.execute("SELECT * FROM {}".format(table_name))
        table_data = cursor.fetchall()
        
        data[table_name] = {'columns': [col[1] for col in columns], 'data': table_data}
    
    # Close the connection
    cursor.close()
    conn.close()
    
    # Pass data to template and render HTML
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

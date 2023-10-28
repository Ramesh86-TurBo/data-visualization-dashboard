# Import necessary libraries
import sqlite3
import json
from flask import Flask, jsonify, render_template

# Initialize a Flask application
app = Flask(__name__)

# Create an SQLite database
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Define a table schema
cursor.execute('''
    CREATE TABLE IF NOT EXISTS insights (
        id INTEGER PRIMARY KEY,
        intensity INTEGER,
        sector TEXT,
        topic TEXT,
        insight TEXT,
        url TEXT,
        region TEXT,
        added TEXT,
        published TEXT,
        country TEXT,
        relevance INTEGER,
        pestle TEXT,
        source TEXT,
        title TEXT,
        likelihood INTEGER
    )
''')

# Import data from the JSON file into the SQLite database
with open('files\jsondata.json', 'r',  encoding='utf-8') as json_file:
    data = json.load(json_file)
    for item in data:
        cursor.execute('INSERT INTO insights (intensity, sector, topic, insight, url, region, added, published, country, relevance, pestle, source, title, likelihood) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (item['intensity'], item['sector'], item['topic'], item['insight'], item['url'], item['region'], item['added'], item['published'], item['country'], item['relevance'], item['pestle'], item['source'], item['title'], item['likelihood']))

# Commit changes and close the database
conn.commit()
conn.close()

# difine the route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# Define an API endpoint to get insights
@app.route('/api/insights', methods=['GET'])
def get_insights():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM insights')
    data = cursor.fetchall()

    conn.close()

    # Convert data to JSON and return it
    insights = [{'intensity': row[1], 'sector': row[2], 'topic': row[3], 'insight': row[4], 'url': row[5],
                'region': row[6], 'added': row[7], 'published': row[8], 'country': row[9], 'relevance': row[10],
                'pestle': row[11], 'source': row[12], 'title': row[13], 'likelihood': row[14]} for row in data]

    return jsonify(insights)

if __name__ == '__main__':
    app.run(debug=True)

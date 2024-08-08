from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error
import requests

app = Flask(__name__)

def get_weather(city, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

    res = requests.get(url)
    
    if res.status_code == 200:
        data = res.json()

        if 'main' in data and 'weather' in data and 'wind' in data:
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            wind = data['wind']['speed']
            description = data['weather'][0]['description']
            temp = data['main']['temp']

            return description
        else:
            return ("Error: Unexpected response structure:", data)
    else:
        return ("Error: Unable to fetch data, HTTP Status code:", res.status_code)

# データベースへの接続情報 / Database connection information
db_config = {
    'host': 'localhost',
    'database': 'cae',
    'user': 'cae',
    'password': 'keksr'
}

# コメントを取得する関数 / Function to get comments
def get_comments():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM impression ORDER BY datetime DESC")
        records = cursor.fetchall()
        return records
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# コメントを挿入する関数 / Function to insert a comment
def insert_comment(city, content, remote_ip):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        weather = f'({city}) {get_weather(city, "584dda13b490011db77924b4e8efc730")}'
        cursor.execute("INSERT INTO impression (content, weather) VALUES (%s, %s)",
                       (content, weather))
        connection.commit()
    except Error as e:
        print("Error inserting data into MySQL table", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# すべてのコメントを削除する関数 / Function to delete all comments
def delete_comments():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM impression")
        connection.commit()
    except Error as e:
        print("Error deleting data from MySQL table", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/v1/comment', methods=['GET', 'POST', 'DELETE'])
def comment_api():
    if request.method == 'GET':
        return jsonify(get_comments())
    elif request.method == 'POST':
        data = request.get_json()
        city = data.get('city')
        content = data.get('content')
        remote_ip = request.remote_addr
        insert_comment(city, content, remote_ip)
        return '', 201
    elif request.method == 'DELETE':
        delete_comments()
        return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

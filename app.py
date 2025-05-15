from flask import Flask, render_template, redirect, request
from dotenv import load_dotenv
import os
import mysql.connector
import re
import psycopg2

app = Flask(__name__)

load_dotenv()

# db_config = {
#     'host': os.getenv('DB_HOST'),
#     'user': os.getenv('DB_USER'),
#     'password': os.getenv('DB_PASSWORD'),
#     'database': os.getenv('DB_DATABASE'),
#     'port': int(os.getenv('DB_PORT')),
# }
# connection = psycopg2.connect(os.getenv('DATABASE_URL'))

def get_db_connection():
    return psycopg2.connect(os.getenv('DATABASE_URL'))

@app.route("/")
def index():

    connection =get_db_connection()
    cursor = connection.cursor()

    # SQL statement to get all books
    select_query = '''
        SELECT * FROM flights;
    '''

    cursor.execute(select_query)
    flights = cursor.fetchall()
    connection.close()

    flight_dict =[]
    keys = ["id", "flight_number", "origin", "destination", "departure_time", "arrival_time"]
    for flight_list in flights:
        flight_values ={}
        for idx in range(6):
            if idx == 3:
                flight_values[keys[idx]] = str(flight_list[idx])[0:4]
            else:
                flight_values[keys[idx]] =  flight_list[idx]
        flight_dict.append(flight_values)

    return render_template("index.html", books = flight_dict)

@app.route("/create", methods = ["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        published = request.form.get("published")

        result1 = re.match(r"^\S.{0,68}\S$", title)
        result2 = re.match(r"^\S.{0,48}\S$", author)
        result3 = re.match(r"^\d{4}$", published)

        if result1 is None or result2 is None or result3 is None:
            return redirect('/create')
        
        published += '-01-01';
        connection = get_db_connection()
        cursor = connection.cursor()

        # SQL statement to get all books
        identifier = request.form.get('identifier')
        print(identifier)
        if identifier:
            insert_query = f'''
                update books set author ='{author}', title ='{title}', published ='{published}'
                where id = {identifier};

            '''
        else:
            insert_query = f'''
                insert into books (author, title, published)
                values
                ('{author}', '{title}', '{published}');

            '''

        cursor.execute(insert_query)
        connection.commit()
        connection.close()
        return redirect('/')
    
    return render_template("create.html" )


@app.route("/delete", methods =["POST", "GET"])
def delete():

    id = request.args.get("id")
    print("hello", id)
    connection = get_db_connection()
    cursor = connection.cursor()

    # SQL statement to get all books
    delete_query = f'''
        delete from books 
        where id = '{id}';
    '''

    cursor.execute(delete_query)
    connection.commit()
    connection.close()
    return redirect('/')


@app.route("/edit", methods =["POST", "GET"])
def edit():

    id = request.args.get("id")

    connection = get_db_connection()
    cursor = connection.cursor()

    # SQL statement to get all books
    select_query = f'''
        select * from books 
        where id = '{id}';
    '''
    cursor.execute(select_query)
    row = cursor.fetchone()
    connection.close()

    year = str(row[3])[0:4]
    row = list(row)
    row[3] = year
    return render_template("create.html", row = row)

if __name__ == '__main__':
    app.run(debug=True)
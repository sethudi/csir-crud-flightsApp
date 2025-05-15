from flask import Flask, render_template, redirect, request
from dotenv import load_dotenv
import os
import re
import psycopg2

app = Flask(__name__)

load_dotenv()

def get_db_connection():
    return psycopg2.connect(os.getenv('DATABASE_URL'))

@app.route("/")
def index():

    connection =get_db_connection()
    cursor = connection.cursor()

    # SQL statement to get all flights
    select_query = '''
        SELECT * FROM flights;
    '''

    cursor.execute(select_query)
    flights = cursor.fetchall()
    connection.close()

    flight_dict =[]
    keys = ["id", "flight_number", "origin", "destination"]
    for flight_list in flights:
        flight_values ={}
        for idx in range(4):
            flight_values[keys[idx]] =  flight_list[idx]
        flight_dict.append(flight_values)

    return render_template("index.html", flights = flight_dict)

@app.route("/create", methods = ["GET", "POST"])
def create():
    if request.method == "POST":
        flight_number = request.form.get("flight_number")
        origin = request.form.get("origin")
        destination = request.form.get("destination")

        result1 = re.match(r"^\S.{0,68}\S$", flight_number)
        result2 = re.match(r"^\S.{0,48}\S$", origin)
        result3 = re.match(r"^\S.{0,48}\S$", destination)

        if result1 is None or result2 is None or result3 is None:
            return redirect('/create')
        
        connection = get_db_connection()
        cursor = connection.cursor()

        # SQL statement to update a flight
        identifier = request.form.get('identifier')
        print(identifier)
        if identifier:
            insert_query = f'''
                update flights set flight_number ='{flight_number}', origin ='{origin}', destination ='{destination}'
                where id = {identifier};

            '''
        else:
            insert_query = f'''
                insert into flights (flight_number, origin, destination)
                values
                ('{flight_number}', '{origin}', '{destination}');

            '''

        cursor.execute(insert_query)
        connection.commit()
        connection.close()
        return redirect('/')
    
    return render_template("create.html" )


@app.route("/delete", methods =["POST", "GET"])
def delete():

    id = request.args.get("id")
    connection = get_db_connection()
    cursor = connection.cursor()

    # SQL statement to delete a flight
    delete_query = f'''
        delete from flights 
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

    # SQL statement to get a flight
    select_query = f'''
        select * from flights 
        where id = '{id}';
    '''
    cursor.execute(select_query)
    row = cursor.fetchone()
    connection.close()

    row = list(row)
    return render_template("create.html", row = row)

if __name__ == '__main__':
    app.run(debug=True)
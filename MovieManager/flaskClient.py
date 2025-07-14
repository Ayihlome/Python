from flask import Flask, render_template, redirect, url_for, flash, request
import socket
import json
from datetime import datetime
import re
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)

# Home page
@app.route("/", methods=['GET', 'POST'])
def homePage():
    if request.method == 'GET':
        # return render_template('index.html')    
        while True:
            try:
                SERADDR = ("localhost", 12345)
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.settimeout(10)
                client.connect(SERADDR)
                reqServer = {"action": "load"}
        
                client.send(json.dumps(reqServer).encode('utf-8'))
                response = client.recv(1048).decode('utf-8')
                data = json.loads(response)
                if not data:
                    flash("Data not found", "error")
                    return redirect(url_for("index"))
                elif data["record"] == " ":
                    return render_template("index.html")
                else:
                    print(f"Records=={data['record']}")
                    return render_template("index.html", movies=data["record"])
                
            except Exception as e:
                print(f"Home Page Error: {e}")
                flash(f"Error occurred: {e}", "error")
                return redirect(url_for('index'))
    
    elif request.method == 'POST':
        movieID = request.form['movie']
        print(f'MOVIE ID: {movieID}')
        name = request.form['customer_name']
        tickets = request.form['tickets']
        # cinema_room = request.form.get('cinema_room')
        
        # data validation
        for num in (movieID, tickets):
            if not re.match(r"[0-9]+", num):
                flash("Invalid Input!", "error")
                return render_template('index.html')
        
        if not re.match(r"\b[a-zA-Z.]+\b", name):
            flash("Invalid Input!", "error")
            return render_template('index.html')
        
        # send to server
        reqServer = {"action": "sale", "payload": {
            "movie_id": int(movieID),
            "customer_name": name,
            "number_of_tickets": float(tickets)
        }}
        
        print(f"Request: {reqServer}")
        try:
            # connection to backend
            SERADDR = ("localhost", 12345)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(10)
            client.connect(SERADDR)
            
            client.send(json.dumps(reqServer).encode('utf-8'))
            response = json.loads(client.recv(1048).decode('utf-8'))
            if response["status"] == "ok":
                flash("Successful Purchase!", "success") 
                return render_template('index.html')
            elif response['status'] == "error":
                flash(f"System Error: {response["error"]}", "error")
                return render_template('index.html')
        except Exception as e:
            print(f"ERROR: {e}")
            flash(f"POST Error: {e}", "error")
            return render_template('index.html')
            # return f"POST error{e}", 500
    return render_template('index.html')



# Add Movie page
@app.route("/addMovie", methods=['GET', 'POST'])
def addMovie():
    if request.method == 'GET':
        return render_template('addMovie.html', header_from_color='from-green-600',
        header_to_color='to-teal-600',
        header_title='Add a Movie',
        header_subtitle='Fill in the details below')
    elif request.method == 'POST':
        # get the variables
        title = request.form['title']
        ticket_price = request.form['ticket_price']
        cinema_room = request.form['cinema_room']
        tickets_available = request.form['tickets_available']
        end_date = request.form['end_date']
        release_date = request.form['release_date']
        
        # Data validation
        for num in (cinema_room, ticket_price, tickets_available):
            if not re.match(r"[0-9]+", num):
                return f"Value Error {num}", 400
        for words in (title, end_date, release_date): #the dates have to be in string format in order for them to be converted into JSON
            if not re.match(r"\b[a-zA-Z0-9-]+\b", words):
                return f"Value Error: {words}", 400
        
        # create request
        reqServer ={"action":"create",
                    "payload":{
                        "title": title,
                        "cinema_room": cinema_room,
                        "release_date": release_date,
                        "end_date": end_date,
                        "tickets_available": tickets_available,
                        "ticket_price": ticket_price
                    }}
        
        print(f"reqServer: {reqServer}")
        try: 
            # connection to backend
            SERADDR = ("localhost", 12345)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(10)
            client.connect(SERADDR)
            
            # Sending data
            client.send(json.dumps(reqServer).encode('utf-8'))
            resServer = json.loads(client.recv(1048).decode('utf-8')) 
            if resServer['status'] == 'ok':
                flash('Movie added successfully!', 'success')
                return render_template('addMovie.html', header_from_color='from-green-600',
        header_to_color='to-teal-600',
        header_title='Add a Movie',
        header_subtitle='Fill in the details below')
            else:
                flash('An Error Occurred', 'error')
                return render_template('addMovie.html', header_from_color='from-green-600',
        header_to_color='to-teal-600',
        header_title='Add a Movie',
        header_subtitle='Fill in the details below')
        except Exception as e:
            print(f"ERROR: {e}")
            return render_template('addMovie.html', header_from_color='from-green-600',
        header_to_color='to-teal-600',
        header_title='Add a Movie',
        header_subtitle='Fill in the details below')
    # return render_template('addMovie.html')


# Update Movie page
@app.route("/updateMovie", methods=['GET', 'POST'])
def updateMovie():
    if request.method == 'GET':
        # Load movies
        SERADDR = ("localhost", 12345)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(10)
        client.connect(SERADDR)
        
        try:
            reqServer = {"action":"load"}
            client.send(json.dumps(reqServer).encode('utf-8'))
            response = json.loads(client.recv(1048).decode('utf-8'))
            if response['status'] == 'ok':
                return render_template("updateMovie.html", movies=response['record'],header_from_color='from-blue-600',
                    header_to_color='to-indigo-600',
                    header_title='Update a Movie',
                    header_subtitle='Fill in the details below')
            elif response['status'] == 'error':
                flash(f"An Error Occurred: {response['error']}", "error")
                return render_template("updateMovie.html", header_from_color='from-blue-600',
                    header_to_color='to-indigo-600',
                    header_title='Update a Movie',
                    header_subtitle='Fill in the details below')
        except Exception as e:
            print(f"ERROR: {e}")
            flash(f"An Error Occurred: {e}", "error")
            return render_template("updateMovie.html", header_from_color='from-blue-600',
                header_to_color='to-indigo-600',
                header_title='Update a Movie',
                header_subtitle='Fill in the details below')
    elif request.method == 'POST':
        # Get the changes
        print("Form data:", request.form)
        movieID = request.form.get('movie_select')
        title = request.form['title']
        ticket_price = request.form['ticket_price']
        cinema_room = request.form['cinema_room']
        tickets_available = request.form['tickets_available']
        end_date = request.form['end_date']
        release_date = request.form['release_date']
        newData = {}
        # if there is a value, add it to the dictionary
        for index, val in enumerate([title, end_date, release_date]):
            if val:
                if not re.match(r"\b[a-zA-Z0-9-]+\b", val):
                    flash(f"Invalid Input {val}", "error")
                    return render_template("updateMovie.html", header_from_color='from-blue-600',
                        header_to_color='to-indigo-600',
                        header_title='Update a Movie',
                        header_subtitle='Fill in the details below')
                else:
                    if index == 0:
                        newData['title'] = val
                        print(f"title: {val}")
                    elif index == 1:
                        newData['end_date'] = val
                    elif index == 2:
                        newData['release_date'] = val
        
        for index, nums in enumerate([ticket_price, tickets_available, cinema_room]):
            if nums:
                if re.match(r"[0-9]+", nums):
                    if index == 0:
                        newData['ticket_price'] = float(nums)
                    elif index == 1:
                        newData['tickets_available'] = int(nums)
                    elif index == 2:
                        newData['cinema_room'] = int(nums)
                else:   
                    flash(f"Invalid Input {nums}", "error")
                    return render_template("updateMovie.html", header_from_color='from-blue-600',
                        header_to_color='to-indigo-600',
                        header_title='Update a Movie',
                        header_subtitle='Fill in the details below')
        
        print(f"The new Data: {newData}")
        # Send to Server
        # connection to backend
        SERADDR = ("localhost", 12345)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(10)
        client.connect(SERADDR)
        reqServer = {"action":"update", "payload": {"movie_id":int(movieID), "newData":newData}}
        
        client.send(json.dumps(reqServer).encode('utf-8'))
        response = json.loads(client.recv(1048).decode('utf-8'))
        print(response)
        
        if response['status'] == 'ok':
            flash("Movie Successfully Updated", "success")
            return render_template("updateMovie.html", header_from_color='from-orange-600',
                header_to_color='to-amber-600',
                header_title='Delete a Movie',
                header_subtitle='Fill in the details below')
        elif response['status'] == 'error':
            flash(f"An Error Occurred: {e}", "error")
            return render_template("updateMovie.html", header_from_color='from-orange-600',
                header_to_color='to-amber-600',
                header_title='Delete a Movie',
                header_subtitle='Fill in the details below')



# Delete Movie page
@app.route("/deleteMovie", methods=['GET', 'POST'])
def deleteMovie():
    if request.method == 'GET':
        # load movies
        while True:
            try:
                # connection to backend
                SERADDR = ("localhost", 12345)
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.settimeout(10)
                client.connect(SERADDR)
                reqServer = {"action":"load"}
                
                client.send(json.dumps(reqServer).encode('utf-8'))
                response = json.loads(client.recv(1048).decode('utf-8'))
                if response['status'] == 'ok':
                    return render_template("deleteMovie.html", movies=response['record'], header_from_color='from-orange-600',
        header_to_color='to-amber-600',
        header_title='Delete a Movie',
        header_subtitle='Fill in the details below')
                elif response['status'] == 'error':
                    print(f"ERROR: {response['error']}")
                    flash(f"POST Error: {response['error']}", "error")
                    return render_template("deleteMovie.html", movies=response['record'], header_from_color='from-orange-600',
        header_to_color='to-amber-600',
        header_title='Delete a Movie',
        header_subtitle='Fill in the details below')
            except Exception as e:
                print(f"ERROR: {e}")
                flash(f"POST Error: {e}", "error")
                return render_template("deleteMovie.html", movies=response['record'], header_from_color='from-orange-600',
        header_to_color='to-amber-600',
        header_title='Delete a Movie',
        header_subtitle='Fill in the details below')
    
    elif request.method == 'POST':
        
        movieID = int(request.form["movie_select"])
        print(f"ID :{movieID}")
        flash(f"ID: {movieID}", "success")
        # data validation
        if not movieID:
            flash("no ID found", "error")
            return redirect(url_for('deleteMovie'))
        
        # connection to backend
        SERADDR = ("localhost", 12345)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(10)
        client.connect(SERADDR)
        reqServer = {"action":"delete", "payload":{"movie_id":movieID}}
        
        try:
            client.send(json.dumps(reqServer).encode('utf-8'))
            response = json.loads(client.recv(1048).decode('utf-8'))
            
            if response['status'] == 'ok':
                flash("Movie Successfully Deleted", "success")
                return redirect(url_for("deleteMovie"))
            elif response['status'] == 'error':
                flash(f"An Error occurred: {response['error']}", "error")
                return redirect(url_for("deleteMovie"))
                # return render_template("deleteMovie.html")
        except Exception as e:
            print(f"Error: {e}")
            flash(f"Delete Failed: {e}", "error")
            redirect(url_for("deleteMovie"))



if __name__ == "__main__":
    host = "127.0.0.1"
    port= "5001"
    app.run(host, port, debug=True)
    print(f"Server running at {host}:{port}")
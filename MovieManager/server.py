import json
import socket
import re
import threading
import sqlalchemy
from datetime import datetime

from Database import SessionLocal, Movies, Sales, startupDB, addMovie, updateMovie, changeNoOfTickets, deleteMovie, sale, showAll

'''
All data will be sent via WebSocket in JSON format:
{
    "action":"..." CRUD operations here
    "payload":{....}
}
'''
# Making sure the DB is ready
startupDB()

# user validation string
def validInput(pattern, fields):
    for field in fields:
        if re.findall(pattern, str(field).strip()):
            return True
        else:
            return False


# CRUD operations
db_session = SessionLocal()


def logging(action, addr, msg):
    # write to a file all actions performed
    try:
        with open('logfile.txt', "+a") as file:
            file.write(f"[{action}] [FROM {addr}]: {msg}------{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} \n")
    except Exception as e:
        print(f"Logging error: {e}")


# Websocket handler
# JSON data is filtered, CRUD functions are called, Response sent
# At this stage we can try input validation
# async def handler(messages):
def handler(client, addr):
    #for each connection we create a db session
    db = SessionLocal()
    logging("Connection", addr, "new client connected to the server")
    
    
    try:
        while True:
            # load data
            request = client.recv(1024)
            if not request:
                print("Gracefully disconnected...")
                break
            try:
                message = request.decode()
                data = json.loads(message)
                action = data.get("action")
                payload = data.get("payload", {})
            except json.JSONDecodeError:
                errorResponse = {
                    "status":"error",
                    "error":"Invalid JSON"
                }
                
                client.send(errorResponse.encode())
                continue
            
            if action == "create":
                print("creating new movie entry...")
                title = payload.get("title")
                cinema_room = payload.get("cinema_room")
                release_date_str = payload.get("release_date")
                end_date_str = payload.get("end_date")
                tickets_available = payload.get("tickets_available")
                ticket_price = payload.get("ticket_price")
                
                # input validation:
                # Convert string to date
                release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date() if release_date_str else None
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None
                pattern = r"[ a-zA-Z0-9,. ]"
                fields = [title, cinema_room, ticket_price, tickets_available]
                if not validInput(pattern, fields=fields):
                    print("invalid user input")
                    response = {"status": "error","error": "Invalid input"}
                elif not title:
                    response = {"status": "error","error": "Missing Title"}
                    print("invalid user input, missing title")
                else:
                    try:
                        newItem = addMovie(db, title, cinema_room, release_date, end_date, tickets_available, ticket_price)
                        response = {"status": "ok", "item": newItem.as_dict() }
                        print(f"new entry complete: {newItem.title}")
                        logging(action, addr, f"new entry complete: {newItem.title}")
                        
                    except sqlalchemy.exc.IntegrityError as e:
                        print(f"Integrity error : {e}")
                        response = {"status": "error", "error":"cinema room is between 1 and 7"}
                    except Exception as e:
                        print(f"Error: {e}")
                        response = {"status": "error", "error": e}
            
            elif action == "update":
                print("updating movie")
                movie_id = payload.get("movie_id")
                newData = payload.get("newData")
                
                # input validation
                pattern = r"[ a-zA-Z0-9,. ]"
                data = json.dumps(newData)
                fields = [movie_id, data]
                if not validInput(pattern, fields=fields):
                    print("invalid user input")
                    response = {"status": "error", "error": "Invalid input"}
                elif not newData:
                    response = {"status": "error", "error": "data not found"}
                    print("invalid user input, data not found ")
                elif not movie_id:
                    response = {"status": "error", "error": "Movie not found"}
                    print("invalid user input, movie not found")
                    
                    try:
                        int(movie_id)
                    except (ValueError, TypeError):
                        print("Invalid movie ID")
                        response = {"status": "error", "error": "Invalid movie ID"}
                else:
                    try:
                        updateMovie(db, movie_id=movie_id, newData=newData)
                        response = {"status": "ok", "newMovie":newData}
                        print("new entry made")
                        logging(action, addr, f"movie updated :{movie_id} -> {newData}")
                        
                    except sqlalchemy.exc.IntegrityError as e:
                        print(f"Integrity error : {e}")
                        response = {"status": "error", "error":"cinema room is between 1 and 7"}
                    except Exception as e:
                        print(f"Error: {e}")
                        response = {"status": "error", "error": e}
            
            
            elif action == "delete":
                print("deleting movie entry...")
                delItem = payload.get("movie_id")
                
                # input validation
                try:
                    int(delItem)
                except (ValueError, TypeError):
                    response = {"status": "error", "error": "Invalid movie ID"}
                    print("invalid user input, invalid movie ID")
                
                if not delItem:
                    response = {"status": "error", "error":"Movie not found"}
                    print("invalid user input, movie ID not found")
                else:
                    deleteMovie(db, delItem)
                    response = {"status": "ok"}
                    print(f"movie entry removed: id:{delItem}")
                    logging(action, addr, f"movie removed: {delItem}")
                    
            
            elif action == "load":
                print("Fetching all movies...")
                movies = showAll(db)
                print(f"Found {len(movies)} movie(s)")
                for movie in movies:
                    print(movie.title)
                response = {"status": "ok", "record": [movie.as_dict() for movie in movies]}
                
            
            elif action == "sale":
                print("processing sale...")
                # movie_id, customer_name, number_of_tickets
                movie_id = payload.get("movie_id")
                customer_name = payload.get("customer_name")
                noOfTickets = payload.get("number_of_tickets")
                
                # input validation
                pattern = r"[ a-zA-Z0-9,. ]"
                fields = [movie_id, customer_name, noOfTickets]
                if not validInput(pattern=pattern, fields=fields):
                    print("invalid user input")
                    response = {"status": "error","error": "Invalid input"}
                elif not movie_id:
                    response = {"status": "error","error": "Movie not found"}
                    print("invalid user input, movie ID not found")
                    try:
                        int(movie_id)
                    except (ValueError, TypeError):
                        response = {"status": "error", "error": "Invalid movie ID"}
                        print("invalid user input, invalid movie ID")
                elif not noOfTickets:
                    response = {"status": "error","error": "No amount given"}
                    print("invalid user input, No amount given")
                    try:
                        int(noOfTickets)
                    except (ValueError, TypeError):
                        response = {"status": "error", "error": "Invalid Number of tickets"}
                        print("Invalid user input, no amount given")
                else:
                    newSale = sale(db, movie_id=movie_id, customer_name=customer_name, number_of_tickets=noOfTickets)
                    response = {"status": "ok", "sale": newSale}
                    print("Sale successful")
                    logging(action, addr, f"movie ticket sold for {movie_id} (tickets:{noOfTickets}) by {customer_name}")
                    
            
            else:
                response = {"status": "error", "error":"Command not found"}
            
            
            # send back response 
            client.send(json.dumps(response).encode('utf-8'))
    except ConnectionResetError:
        print(f"[DISCONNECTED] Client {addr} connection reset")
    # except Exception as e:
    #     print(f"Error from Handler: {e}")
    #     response = {"status": "error", "error":"system error"}
    #     client.send(json.dumps(response).encode('utf-8'))
    finally:
        db.close()
        print(f"[CLOSED] Client {addr} connection closed")


# Web Sockets route and ports
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 12345
host = "localhost" 
server_socket.bind((host, port))
try:
    server_socket.listen(10)
    print(f"Server listening on: {host}:{port}")
except OSError as e:
    print(f"Error: {e}")

while True:
    client, addr = server_socket.accept()
    print(f"Connection from: {addr}")
    handler(client, addr)
    server_socket.close()
    # break

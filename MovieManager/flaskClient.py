from flask import Flask, render_template, request

app = Flask(__name__)

# Home page
@app.route("/")
def homePage():
    
    return render_template("index.html")

# Add Movie page
@app.route("/addMovie")
def addMovie():
    
    return render_template("addMovie.html")


# Update Movie page
@app.route("/updateMovie")
def updateMovie():
    
    return render_template("updateMovie.html")
# Delete Movie page


@app.route("/deleteMovie")
def deleteMovie():
    
    return render_template("deleteMovie.html")



host = "127.0.0.1"
port= "5001"
app.run(host, port, debug=True)
print(f"Server running at {host}:{port}")
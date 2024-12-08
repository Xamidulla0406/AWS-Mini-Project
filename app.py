from flask import Flask, render_template, request
import pg8000

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        day = request.form["day"]
        return render_template("timetable.html", day=day, data=[], message="Loading timetable...")

    return render_template("index.html")

@app.route("/timetable", methods=["GET"])
def timetable():
    day = request.args.get('day')
    if not day:
        return "Day not provided", 400

    conn = pg8000.connect(
        user="",          # The username for the database (e.g., 'postgres')
        password="",      # The password for the database user
        host="",          # The host address of the database (RDS endpoint)
        port=5432,        # The port number for PostgreSQL (default is 5432)
        database=""       # The name of the database you want to connect to (e.g., 'your_name')
    )

    cur = conn.cursor()
    query = "SELECT * FROM your_name WHERE day = %s;" # your_name - table name
    cur.execute(query, (day,))
    rows = cur.fetchall()

    if rows:
        return render_template("timetable.html", day=day, data=rows, message="")
    else:
        return render_template("timetable.html", day=day, data=[], message="No data found for this day.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
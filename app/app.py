import psycopg
from flask import Flask, render_template
from flask_compress import Compress

app = Flask(__name__)
DATABASE_URL = ""
Compress(app)


@app.route("/")
def index():
    with psycopg.connect(DATABASE_URL, sslmode="require") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM topics;")
            items = cur.fetchall()
            return render_template("index.html", items=items)

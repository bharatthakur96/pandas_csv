from tkinter import N
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

db = SQLAlchemy(app)


df = pd.read_csv("nifty50.csv")
df.to_csv("nifty50.csv", index=None)


@app.route("/")
def table():
    data = pd.read_csv("nifty50.csv")
    return render_template("base.html", tables=[data.to_html()], titles=[""])


@app.route("/index_data", methods=["GET", "POST"])
def index_data():
    if request.method == 'GET':
         return render_template('index_data.html')
    elif request.method == 'POST':
        df = pd.read_csv('nifty50.csv')
        cv = int(request.form['filterdata'])
        data = pd.DataFrame(df)
        filter_data = data.head(cv)
    return render_template('index_data.html', tables=[filter_data.to_html()])

@app.route("/search_data", methods=["GET", "POST"])
def search_data():
    if request.method == 'GET':
         return render_template('search_data.html')
    elif request.method == 'POST':
        cv = request.form['filterdata']
        print(cv)
        df = pd.read_csv('nifty50.csv')
        data = pd.DataFrame(df)
        search = data.loc[data['Symbol'] == cv]
    return render_template('search_data.html', tables=[search.to_html()])

@app.route("/filter_data", methods=["GET", "POST"])
def filter_data():
    if request.method == 'GET':
         return render_template('filter_data.html')
    elif request.method == 'POST':
        df = pd.read_csv('nifty50.csv')
        cv = str(request.form['data'])
        t=cv.split(',')
        data = df.filter(t)
        return render_template('filter_data.html', tables=[data.to_html()])

@app.route("/sort_data", methods=["GET", "POST"])
def sort_data():
    if request.method == 'GET':
         return render_template('sort_data.html')
    elif request.method == 'POST':
        df = pd.read_csv('nifty50.csv')
        cv = str(request.form['data'])
        data = pd.DataFrame(df)
        sort1 =  data.sort_values(by=[cv])
        if 'desc' in request.form:
            sort2 = data.sort_values(by=[cv], ascending=False)
            return render_template('sort_data.html', tables=[sort2.to_html()])
        return render_template('sort_data.html', tables=[sort1.to_html()])

        



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)


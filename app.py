import os
import urllib.parse 
from django.shortcuts import render
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine


driver = "{SQL Server}"
server = "cloud-server31.database.windows.net"
database = "Cmpe363Final"
user = "admin123"
password = "Bilgi123123"




# Configure Database URI: 
params = urllib.parse.quote_plus(f"DRIVER={driver};SERVER={server};DATABASE={database};UID={user};PWD={password}")


# initialization
app = Flask(__name__)

app.config['SECRET_KEY'] = 'supersecret'
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# app.config['FLASK_ENV'] = "development"
# app.config['FLASK_APP'] = "debug"


# extensions
db = SQLAlchemy(app)


# db.engine.execute("CREATE TABLE Deneme2 (isim varchar(255))")

#db.engine.execute("INSERT INTO Deneme2 VALUES ('mehmet3')")


a = db.engine.execute("""SELECT * FROM Deneme2""")
row = a.fetchall()
for r in row:
    print(r[0])



print(db.engine.table_names())

@app.route("/")
def hello():
    return render_template('index.html')



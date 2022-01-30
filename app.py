import os
from urllib import response
import urllib.parse
from django.shortcuts import render
from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from upload_image import upload_blob
from face import detect_faces
import datetime

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

db = SQLAlchemy(app)


db.engine.execute("DROP TABLE Faces ")
db.engine.execute("DROP TABLE Images ")

class Faces(db.Model):
    id = db.Column(db.String(255),primary_key=True)
    wearing_mask = db.Column(db.String(255))
    nose_mouth = db.Column(db.String(255))
    image_id = db.Column(db.String(255))
    
    def __repr__(self):
        return f"<Task {self.id}>"

class Images(db.Model):
    id = db.Column(db.String(255),primary_key = True)
    date_uploaded = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    number_of_people = db.Column(db.Integer)

   
    def __repr__(self):
        return f"<Task {self.id}>"


#db.engine.execute("INSERT INTO Deneme2 VALUES ('mehmet3')")

db.create_all()

# a = db.engine.execute("""SELECT * FROM Deneme2""")
# row = a.fetchall()
# for r in row:
#     print(r[0])



# print(db.engine.table_names())

@app.route("/",methods=['POST','GET'])
def index():

    if request.method  == "POST":
        f = request.files['uploaded_image']
        if f:
            upload_url = upload_blob(f)
            
            image_url,face_count, maskCount,faces = detect_faces(upload_url)
            #TODO: Add database

            #create a model of the row
            image_id = image_url.split('/')[-1]

            for face in faces:
                try:
                    face_model = Faces(id=face[0], wearing_mask = face[1], nose_mouth = face[2], image_id=image_id)
                    db.session.add(face_model)
                    db.session.commit()
                except:
                    return "Could not add the entry to the database"

            image_model = Images(id=image_id,number_of_people=len(faces))
            db.session.add(image_model)
            db.session.commit()
                        
            return render_template('index.html',image_url = image_url, face_count = face_count, mask_count = maskCount, faces=faces)



        else:
            return render_template('index.html')
            
    else:
        return render_template('index.html')


@app.route("/logs")
def logs():
    return render_template('logs.html')

if __name__ == "__main__":
    app.run(debug=True)

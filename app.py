import os
import urllib.parse
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from upload_image import upload_blob
from face import detect_faces
import datetime
from config import (
    SERVER_NAME,
    DATABASE_USERNAME,
    DATABASE_NAME,
    DATABASE_PASSWORD,
    STORAGE_NAME,
    CONTAINER_NAME,
)


driver = "{ODBC Driver 17 for SQL Server}"
server = SERVER_NAME
database = DATABASE_NAME
user = DATABASE_USERNAME
password = DATABASE_PASSWORD


# Configure Database URI:
params = urllib.parse.quote_plus(
    f"DRIVER={driver};SERVER={server};DATABASE={database};UID={user};PWD={password}"
)

# initialization
app = Flask(__name__)

app.config["SECRET_KEY"] = "supersecret"
app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True


db = SQLAlchemy(app)


# db.engine.execute("DROP TABLE Face")
# db.engine.execute("DROP TABLE Image")


class Face(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    wearing_mask = db.Column(db.String(255))
    nose_mouth = db.Column(db.String(255))
    image_id = db.Column(db.String(255), db.ForeignKey("image.id"), nullable=False)

    def __repr__(self):
        return f"<Task {self.id}>"


class Image(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    date_uploaded = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    number_of_people = db.Column(db.Integer)
    faces = db.relationship("Face", backref="image", lazy=True)

    def __repr__(self):
        return f"<Task {self.id}>"


def addFacesToDB(faces, image_id):

    for face in faces:
        try:
            face_model = Face(
                id=face[0],
                wearing_mask=str(face[1]),
                nose_mouth=str(face[2]),
                image_id=image_id,
            )
            db.session.add(face_model)
            db.session.commit()
        except:
            return "Could not add the entry to the database"


def addImageToDB(img_id, number_of_people):

    image_model = Image(id=img_id, number_of_people=number_of_people)
    db.session.add(image_model)
    db.session.commit()


# db.engine.execute("INSERT INTO Deneme2 VALUES ('mehmet3')")

db.create_all()

# a = db.engine.execute("""SELECT * FROM Deneme2""")
# row = a.fetchall()
# for r in row:
#     print(r[0])


# print(db.engine.table_names())


@app.route("/", methods=["POST", "GET"])
@app.route("/<string:id>", methods=["POST", "GET"])
def index(id=""):

    if id:
        # create the url by using the given id
        image_url = (
            f"https://{STORAGE_NAME}.blob.core.windows.net/{CONTAINER_NAME}/{id}.png"
        )

        # get the image from the DB
        img = Image.query.get(id)

        # loop through the faces in img
        maskCount = 0
        faces = []

        for face in img.faces:
            if face.wearing_mask == "True":
                maskCount += 1
            faces.append([face.id, face.wearing_mask, face.nose_mouth])
        print(faces)

        return render_template(
            "index.html",
            image_url=image_url,
            face_count=len(img.faces),
            mask_count=maskCount,
            faces=faces,
        )

    if request.method == "POST":
        f = request.files["uploaded_image"]
        if f:
            upload_url = upload_blob(f)

            image_url, face_count, maskCount, faces = detect_faces(upload_url)
            image_id = image_url.split("/")[-1].rstrip(".png")

            addImageToDB(image_id, len(faces))
            addFacesToDB(faces, image_id)

            return render_template(
                "index.html",
                image_url=image_url,
                face_count=face_count,
                mask_count=maskCount,
                faces=faces,
            )

        else:
            return render_template("index.html")

    else:
        return render_template("index.html")


@app.route("/logs")
def logs():

    # TODO: Get all the images and log them in a table

    images = Image.query.order_by(Image.date_uploaded.desc()).limit(20).all()
    print(images)
    return render_template("logs.html", images=images)


if __name__ == "__main__":
    app.run(debug=True)

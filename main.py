from flask import Flask, render_template,request, redirect,session,url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import  MySQL
import MySQLdb.cursors
from model.Predict import *
from PIL import Image
import os

app=Flask(__name__)

app.config["VIDEO_UPLOADS"] = "C:\\Users\\singh\\OneDrive\\Desktop\\Deep_Fakes\\FInal_Code\\static\\uploaded_videos"
app.config["ALLOWED_VID_EXTENSIONS"] = ["MP4"]
app.config["MAX_VID_FILESIZE"] = 100 * 1024 * 1024

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/dcf_webapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
db = SQLAlchemy(app)

app.secret_key='dgzsjgjf1232'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='password'
app.config['MYSQL_DB']='dcf_webapp'
mysql = MySQL(app)
#****************************************************** Database Table Info *******************************************************

class user_table(db.Model):
    srno=db.Column(db.Integer, primary_key=True)
    firstname= db.Column(db.String(100), nullable=False)
    lastname= db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    mobno = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(100), nullable=False)                                                      #

#************************************************** Basic Routes *****************************************************************

@app.route("/")
def index():
    print("hii from index")
    return render_template("homepage.html")

@app.route("/about")
def about():
    return  render_template("about.html")

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/display-vid")
def display_vid():
    return render_template("display_video.html")

#************************************************* Functional Routes **********************************************************************

@app.route("/login",methods = ['GET', 'POST'])
def login():

    msg = ''

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:

        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_table WHERE email = %s AND password = %s', (email, password))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['firstname'] = account['firstname']
            session['lastname'] = account['lastname']
            session['email'] = account['email']
            session['mobno'] = account['mobno']
            return redirect(url_for('/'))

        else:
            msg = 'Incorrect username/password!'

    return render_template("login.html", msg=msg)


@app.route("/reg",methods = ['GET', 'POST'])
def registration():

    if (request.method == 'POST'):
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        mobno = request.form.get('mobno')
        password = request.form.get('password')

        entry = user_table(firstname=firstname, lastname=lastname,email=email, mobno=mobno, password=password)

        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('login'))

    else:
        return render_template('registration.html')

#***********************************************************************************************************************

def allowed_video(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_VID_EXTENSIONS"]:
        return True
    else:
        return False
    print("hii from allowed vid")


def allowed_video_filesize(filesize):

    if int(filesize) <= app.config["MAX_VID_FILESIZE"]:
        return True
    else:
        return False
    print("hii from filesize checking")


@app.route("/upload-vid", methods=["GET", "POST"])
def upload_video():
    print("hii from starting vid upload")
    if request.method == "POST":
        if request.files:
            vid = request.files["vid"]
            print("type",type(vid))


            if vid.filename == "":
                    print("No filename")
                    return redirect(request.url)


            filename = secure_filename(vid.filename)
            print("type filename", type(filename))

            filename=filename[:-4]
            print(filename)


            vid.save(os.path.join(app.config["VIDEO_UPLOADS"], filename))
            print("Video saved")

            frames = final_video_process("C:\\Users\\singh\\OneDrive\\Desktop\\Deep_Fakes\\FInal_Code\\static\\uploaded_videos\\"+filename)
            #print(frames)
            images=[]


            for i in range(5):
                img=Image.fromarray(frames[i])
                images.append(filename+str(i)+".jpeg")
                img.save("C:\\Users\\singh\\OneDrive\\Desktop\\Deep_Fakes\\FInal_Code\\static\\images\\"+filename+str(i)+".jpeg")

            p,a=prediction("C:\\Users\\singh\\OneDrive\\Desktop\\Deep_Fakes\\FInal_Code\\static\\uploaded_videos\\"+filename)
           # return render_template('display_video.html',file=filename)


            if (p==1):
                msg1='Real'
                output_image="real.png"
                return render_template('display_video.html', img1=images[0], img2=images[1], img3=images[2],
                                       img4=images[3], img5=images[4],msg=msg1,output=output_image,avg=str(int(a*100))+"%")
            elif(p==0):
                msg2='Fake'
                output_image = "fake.png"
                return render_template('display_video.html',img1=images[0],img2=images[1],img3=images[2],img4=images[3],img5=images[4],msg=msg2,output=output_image,avg=str(int((1-a)*100))+"%")

            return redirect(request.url)

    print("hii from ending vid")
    return render_template('upload_video.html')

#***********************************************************************************************************************

if __name__== '__main__' :
    app.run(debug="True")


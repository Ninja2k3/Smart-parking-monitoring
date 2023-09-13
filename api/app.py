from flask import Flask,render_template,Response,request,redirect,url_for,flash
from flask_pymongo import PyMongo
import yaml
from coordinates_generator import CoordinatesGenerator
from motion_detector import MotionDetector
from colors import *
import logging
import pyrebase
import cv2
import numpy as np

config = {
    "apiKey": "AIzaSyCRvuaXLQAW-PZJ3H72wZdSTvJDisLsVOQ",
    "authDomain": "mcesel-226bf.firebaseapp.com",
    "databaseURL": "https://mcesel-226bf-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "mcesel-226bf",
    "storageBucket": "mcesel-226bf.appspot.com",
    "messagingSenderId": "426130337344",
    "appId": "1:426130337344:web:b08cc855283f8afd7039a5",
    "measurementId": "G-XBMHP9C12K"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

email = ''


def feeder(image_file,data_file,video_file,start_frame,c):
    logging.basicConfig(level=logging.INFO)
    monitor = mongo.db.counts.find_one()
    print(monitor)
    image_file = image_file
    data_file = data_file
    start_frame = start_frame

    if image_file is not None:
        with open(data_file, "w+") as points:
            generator = CoordinatesGenerator(image_file, points, COLOR_RED)
            generator.generate()

    with open(data_file, "r") as data:
        points = yaml.load(data)
        detector = MotionDetector(video_file, points, int(start_frame))
        detector.detect_motion()


app = Flask(__name__)
coins = 1000


app.secret_key = '_5#y2LF4Q8zxec/'
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

@app.route('/user/<id>')
def user(id):
    return "<h1>hello{}</h1>".format(id)

@app.route('/test')
def test():
    print(db.child('Sensor').get().val()['out'])
    out = db.child('Sensor').get("out").val()['out']
    return render_template('test.html',out=out)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        if(mongo.db.users.find_one({"username":username,
                                   "password":password})):
            user = mongo.db.users.find_one({"username":username,
                                   "password":password})
            if username==user["username"] and password==user["password"]:
                return redirect(url_for('home',username=username))

        else:
                flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
    
        if(mongo.db.users.find_one({"username":username,
                                   "password":password})):
            user = mongo.db.users.find_one({"username":username,
                                   "password":password})
            if username==user['username']:
                flash('Invalid username provided', 'error')
        else:
            mongo.db.users.insert_one({"username":username,
                                   "password":password
                                  })
            flash('You were successfully registered')
    return render_template('register.html')
            

@app.route('/home/<username>/park',methods=['GET','POST'])
def home(username):
    locations=mongo.db.locations.find()
    loc = []
    coordinates = []
    for location in locations:
        lox = location['location'].split("\"")
        coor = location['location'].split("!")
        coort = (coor[6][2:],coor[5][2:])
        coordinates.append(coort)
        loc.append([location['username'],0])
        loc.append([location['locationName'],0])
        loc.append([lox[1],0])
        loc.append([location['imageURL'],0])
        loc.append([location['coverCharge'],0])
        loc.append([location['hourlyCharge'],0])
        out = db.child('Sensor').get("out").val()['out']
        if out==2:
            out='?'
            feeder('images/parking_lot_1.png','data/coordinates_1.y','videos/parking_lot_1.mp4',400,0)
            

    return render_template('home.html',username=username,loc=loc,x=int((len(loc)/6)),coordinates=coordinates,out=out)

def _coordinates(p):
    return np.array(p["coordinates"])

#cap = cv2.VideoCapture('F:/Programming/EL/Smart-parking-monitoring/api/videos/parking_lot_1.mp4')
#md = MotionDetector('videos/parking_lot_1.mp4','data/coordinates_1.y')

with open('data/coordinates_1.y', "r") as data:
    points = yaml.load(data)
    md = MotionDetector('videos/parking_lot_1.mp4',points)

def generate_frames():
    md.detect_motion()
    '''while True:
        success,frame = cap.read()
        if not success:
            print('no video')
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        else:
            ret,buffer = cv2.imencode('.jpg',frame)
            frame = buffer.tobytes()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n')
              points = yaml.load('data/coordinates_1.y')
    contours = []
    bounds = []
    m=[]
    for p in points:
        coordinates = _coordinates(p)
        rect = cv2.boundingRect(coordinates)
        new_coordinates = coordinates.copy()
        new_coordinates[:, 0] = coordinates[:, 0] - rect[0]
        new_coordinates[:, 1] = coordinates[:, 1] - rect[1]
        contours.append(coordinates)
        bounds.append(rect)
        mask = cv2.drawContours(
                np.zeros((rect[3], rect[2]), dtype=np.uint8),
                [new_coordinates],
                contourIdx=-1,
                color=255,
                thickness=-1,
                lineType=cv2.LINE_8)
        mask = mask == 255
        m.append(mask)
        statuses = [False] * len(points)
        times = [None] * len(points)
        '''

@app.route('/video',methods=['GET','POST'])
def video():
    return Response(md.detect_motion(), mimetype='multipart/x-mixed-replace; boundary=frame')

    

@app.route('/home/<username>/feed',methods=['GET','POST'])
def feed(username):
    #c = 0
    #feeder('images/parking_lot_1.png','data/coordinates_1.y','videos/parking_lot_1.mp4',400,c)
    return render_template('feed.html',username=username)
       
       

@app.route('/home/<username>/upload',methods=['GET','POST'])
def upload(username):
    userlocations = mongo.db.locations.find({"username":username})
    ull = []
    for location in userlocations:
        ull.append(location['username'])
        ull.append(location['locationName'])
        ull.append(location['location'])
        ull.append(location['imageURL'])
        ull.append(location['coverCharge'])
        ull.append(location['hourlyCharge'])
    return render_template('upload.html',username=username,x=int((len(ull)/6)),loc=ull)

@app.route('/home/<username>/upload/quest',methods=['GET','POST'])
def quest(username):
   
        if request.method=='POST':
            username=request.form.get('username')
            locationName=request.form.get('locationName')
            location=request.form.get('location')
            imageURL=request.form.get('imageURL')
            coverCharge=request.form.get('coverCharge')
            hourlyCharge=request.form.get('hourlyCharge')
            print(username)
            print(locationName)
            if(mongo.db.locations.find_one({"location":location})):
                flash('Location declared in this area') 
                
            else:
                mongo.db.locations.insert_one({"username":username,
                                    "locationName":locationName,
                                    "location":location,
                                    "imageURL":imageURL,
                                    "coverCharge":coverCharge,
                                    "hourlyCharge":hourlyCharge})
                flash('Location registered!') 

    
        return render_template('quest.html',usern=username)

@app.route('/home/<username>/wallet',methods=['GET','POST'])
def wallet(username):
    incr=request.form.get('recharge')
    global coins
    if(incr):
        coins = coins + int(incr)
    return render_template('wallet.html',coin=coins,username=username)

if __name__=="__main__":
    app.run(debug=True)
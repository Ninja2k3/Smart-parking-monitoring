from flask import Flask,render_template,Response,request,redirect,url_for,flash
from flask_pymongo import PyMongo



app = Flask(__name__)
coins = 1000


app.secret_key = '_5#y2LF4Q8zxec/'
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

@app.route('/user/<id>')
def user(id):
    return "<h1>hello{}</h1>".format(id)

    
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

    return render_template('home.html',username=username,loc=loc,x=int((len(loc)/6)),coordinates=coordinates)
       
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
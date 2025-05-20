from flask import Flask , render_template , request , redirect 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracker.db'
db = SQLAlchemy(app)

class Tracker(db.Model):
    SNO = db.Column(db.Integer, primary_key=True)
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self) -> str:
        return f"{self.calories} {self.protein}"
    
@app.route("/", methods=["GET", "POST"])
def html():
    if request.method == "POST":
        calories=request.form['calories']
        protein=request.form['protein']
        tracker = Tracker( calories=calories, protein=protein) 
        db.session.add(tracker)
        db.session.commit()
    allTracker=Tracker.query.all()
    return render_template("index.html", allTracker=allTracker)
    

@app.route("/show")
def hello_world():
    allTracker=Tracker.query.all()
    print(allTracker)

    return "<p>Hello, World!</p>"

@app.route("/update/<int:SNO>", methods=["GET" ,"POST"])
def update(SNO):
    tracker = Tracker.query.filter_by(SNO=SNO).first()  
    if tracker:
        new_cal = request.form.get('newcalories')
        new_prot = request.form.get('newprotein')
        print(new_cal, new_prot)
        if new_cal and new_prot:
            tracker.calories = int(new_cal)
            tracker.protein = int(new_prot)
            print("successfully updated")
            db.session.commit()
    return redirect("/")
@app.route("/delete/<int:SNO>")
def delete(SNO):
    tracker=Tracker.query.filter_by(SNO=SNO).first()
    db.session.delete(tracker)
    db.session.commit()
    
    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)
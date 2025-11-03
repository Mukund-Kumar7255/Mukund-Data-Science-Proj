from flask import *
from flask_sqlalchemy import SQLAlchemy
from customer.models import *
from send_mail import *
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://flask_user:flask_123@localhost/my_flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False

app.secret_key = "your_secret_key"
db.init_app(app)

with app.app_context():
    db.create_all()

def load_template(filename,**kwargs):
    with open(filename,"r",encoding="utf-8") as f:
        template=f.read()
    return template.format(**kwargs)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/sign_up",methods=['GET', 'POST'])
def customer_reg():
    if request.method == "POST":
        # stu_id=request.form.get('stu-id')
        stu_name = request.form.get('full-name')
        email = request.form.get('email')
        password = request.form.get('password')
        phoneno = request.form.get('phoneno')
        gender=request.form.get('gender')
        print(stu_name,email,password,phoneno,gender)
        exists=Customer.query.filter_by(email=email).first()
        if exists:
            flash("This email already exists.","error")
            return render_template("signup.html")
        
        exists=Customer.query.filter_by(phone=phoneno).first()
        if exists:
            flash("This phone already exists.","error")
            return render_template("signup.html")
        
        try:
            new_customer=Customer(email=email,password=password,name=stu_name,gender=gender,phone=phoneno)
            db.session.add(new_customer)
            db.session.commit()
            subject=load_template("subject.txt")
            body=load_template("body.txt",username=stu_name,email=email,phone=phoneno)
            send_mail([email],subject,body)

            return redirect(url_for('get_all'))
        except Exception as e:
            return f"Error : {e}"
    else:
        return render_template("signup.html")
    
@app.route("/getall",methods=["GET"])
def get_all():
    if "Email" not in session:
        return redirect(url_for("login_user"))
    customers = Customer.query.all()
    return render_template("getallstudent.html", users=customers)

@app.route("/delete/<int:id>")
def delete_stud(id):
    student=Customer.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('get_all'))

@app.route("/update/<int:id>",methods=["GET", "POST"])
def update_user(id):
    student=Customer.query.get(id)
    if request.method=='POST':
        student.name = request.form.get('full-name')
        student.email = request.form.get('email')
        student.password = request.form.get('password')
        student.phoneno = request.form.get('phoneno')
        student.gender=request.form.get('gender')
        db.session.commit()
        return redirect(url_for('get_all'))
    else:
        return render_template("signup.html")

@app.route("/search")
def search_user():
    id = request.args.get('query')
    student = Customer.query.get(id)
    if student:
        return render_template("getallstudent.html", users=[student])
    else:
        return render_template("getallstudent.html", users=[])
    
@app.route("/login",methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        customer = Customer.query.filter_by(email=email, password=password).first()
        if customer:
            session["Email"] = customer.email
            return redirect(url_for("get_all"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/dashboard")
def user_dashboard():
    customers=Customer.query.all()
    counts=0
    male_counts=0
    female_counts=0
    for i in customers:
        counts+=1
        if i.gender=='male':
            male_counts+=1
        elif i.gender=='female':
            female_counts+=1
    return render_template("dashboard.html",total_students=counts,male_count=male_counts,female_count=female_counts)

@app.route("/book")
def book_details():
    return render_template("bookdetails.html")

@app.route("/logout")
def log_out():
    session.pop('email',None)
    return redirect(url_for('login_user'))

if __name__=="__main__":
    app.run(debug=True)
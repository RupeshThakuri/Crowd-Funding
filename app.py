from flask import Flask, request, render_template,jsonify,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/hackathon'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    
    # Check if username or email already exists
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    
    if existing_user:
        # Redirect back to login page with an error parameter
        return render_template('login.html', error='user_exists')
    
    new_user = User(username=username, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()
    
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def login(): 
    username = request.form['username']
    password = request.form['password']
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.password == password:
        return render_template("index.html")
    else:
        # Redirect back to login page with an error parameter
        return render_template('login.html', error='password')

@app.route('/')
def home():
    return render_template("login.html")

@app.route('/logout')
def logout():
    return render_template("login.html") 

@app.route('/Donation')
def donation():
    return render_template("donation.html") 

@app.route('/redirect', methods=['POST'])
def redirect_to_success():
    data = request.get_json()
    amount = data['amount']
    return jsonify({'redirect': url_for('success', amount=amount)})

@app.route('/templates/success.html')
def success():
    amount = request.args.get('amount')
    return render_template('success.html', amount=amount)

@app.route('/codePay')
def codepay():
    return render_template('codePay.html')

if __name__ == '__main__':
    app.run(debug=True)
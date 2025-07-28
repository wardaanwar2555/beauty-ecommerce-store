from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hello1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Setup database
db = SQLAlchemy(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
db_session = Session()
Base = declarative_base()

# Define the User model
class Users(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Users {self.email}>'

# Create tables
with app.app_context():
    db.create_all()
Base.metadata.create_all(engine)

# ✅ Correct Gemini model initialization
model = genai.GenerativeModel(model_name='gemini-2.0-flash')

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = db_session.query(Users).filter(Users.email == email).first()

        if user and user.password == password:
            return redirect(url_for('shop'))
        else:
            flash('Invalid email or password')
    return render_template('login.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            user = Users(email=email, password=password)
            db_session.add(user)
            db_session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            db_session.rollback()
            flash("Error creating user.")
    return render_template('signup.html')

# Chat endpoint for Gemini
@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")
    if not user_msg:
        return jsonify({"reply": "No message provided."}), 400

    try:
        response = model.generate_content(user_msg)
        reply = response.text
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"}), 500

# Additional routes
@app.route('/platform')
def platform(): return render_template('platform.html')

@app.route('/service')
def service(): return render_template('service.html')

@app.route('/about')
def about(): return render_template('about.html')

@app.route('/completeorder')
def completeorder(): return render_template('completeorder.html')

@app.route('/resources')
def resources(): return render_template('resources.html')

@app.route('/shop')
def shop(): return render_template('shop.html')

@app.route('/skin')
def skin(): return render_template('skin.html')

@app.route('/hair')
def hair(): return render_template('hair.html')

@app.route('/makeup')
def makeup(): return render_template('makeup.html')

@app.route('/cart')
def cart(): return render_template('cart.html')

@app.route('/checkout')
def checkout(): return render_template('checkout.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

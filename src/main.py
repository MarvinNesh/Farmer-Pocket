from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def dashboard():
    """lending page"""
    return render_template('index.html')

@app.route('/login')
def login():
    """login page."""
    return render_template('login.html')

@app.route('/register')
def register():
    """Registration page."""
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session

users = {}

@app.route('/')
def index():
    # Serve your Index.html here
    return render_template('index.html')

@app.route('/home')
def home():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', username=username)
    return render_template('login.html') 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if username in users:
            # If the username already exists, display an error on the register page
            return render_template('register.html', error="Username already exists. Try a different one.")
        
        # Save the user to the 'users' dictionary
        users[username] = {'email': email, 'password': password}
        
        # Redirect to login page after successful registration
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.get(username)
        if user and user['password'] == password:
            session['username'] = username
            # After successful login, redirect to the homepage
            return redirect(url_for('home'))
        else:
            # Show an error on the login page if the username or password is incorrect
            return render_template('login.html', error="Invalid username or password.")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from the session
    return redirect(url_for('login'))  # Redirect back to the login page


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        print("Customer Details:")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Phone: {phone}")
        print(f"Address: {address}")
        
        return redirect('/payment')

    return render_template('checkout.html')

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    return render_template('payment.html')

@app.route('/thankyou', methods=['GET', 'POST'])
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(debug=True)

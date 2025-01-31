import os
from flask import Flask, redirect, request, session, render_template, url_for
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = "67e09890ebcb0b32c0fc7a5300fb2da70faa4769433ae4f54f0273c801585fc8"

SUPABASE_URL = "https://ynncaddxhrawalpvfxvy.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlubmNhZGR4aHJhd2FscHZmeHZ5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzgyMjAzOTAsImV4cCI6MjA1Mzc5NjM5MH0.3gWd0TAUEaXMr-Oh2q2tFQeY7usnlQm7MZVTJzmPXuI"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.route('/')
@app.route('/landingPage')
def landingPage():
    return render_template('main/landingPage.html')


@app.route('/loginPage', methods=['GET', 'POST'])
def loginPage():
    if request.method == 'POST':
        userEmail = request.form.get('email')
        userPassword = request.form.get('password')
        try:
            user = supabase.auth.sign_in_with_password({"email": userEmail, "password": userPassword})
            session["user_id"] = user.user.id  # Store user ID in session
            session["display_name"] = user.user.user_metadata.get("display_name", "No Name")  # Store display name

            print('Successfully Logged In')
            return redirect(url_for('home'))  # Redirect to home after login
        except Exception as e:
            print(f"Login error: {e}")
            return redirect(url_for('loginPage'))

    return render_template('authentication/loginPage.html')


@app.route('/signupPage', methods=['GET', 'POST'])
def signupPage():
    if request.method == 'POST':
        userEmail = request.form.get('email')
        userUsername = request.form.get('username')
        userPassword = request.form.get('password')
        userCPassword = request.form.get('password1')

        if userPassword != userCPassword:
            print("Passwords do not match!")
            return redirect(url_for('signupPage'))

        try:
            user = supabase.auth.sign_up({
                "email": userEmail,
                "password": userPassword,
                "options": {"data": {"display_name": userUsername}}
            })
            print(user)
            print('Successfully Signed Up')
            return redirect(url_for('loginPage'))
        except Exception as e:
            print(f"Signup error: {e}")
            return redirect(url_for('signupPage'))

    return render_template('authentication/signupPage.html')

@app.route('/home')
def home():
    display_name = session.get("display_name", "Guest")  # Get display name from session
    return render_template('home/home.html', display_name=display_name)

@app.route('/logout')
def logout():
    session.clear()
    supabase.auth.sign_out()
    return redirect(url_for('loginPage'))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from database import add_user_to_db, validate_username, verify_login

#Name Initialization
app = Flask(__name__)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

#Home route
@app.route("/")
def landing_page():
  if 'username' in session:
    return render_template('dashboard.html', username=session['username'])
  else:
    return render_template("home.html")

#Login route
@app.route("/login/")
def login_page():
  if request.method == 'POST':
    data = []
    data = request.form
    lusername = request.form.get('lusername')
    lpassword = request.form.get('lpassword')
    found_stat = 'N'
    pwd = " "
    found_stat, pwd = verify_login(lusername, data, found_stat, pwd)
    if found_stat == 'Y':
      if (lpassword == pwd):
        session['username'] = lusername
        username = session['username']
        return render_template("dashboard.html", username=username)
      else:
        return render_template("login.html",
                               error="Invalid username or password")
    else:
      return render_template("login.html",
                             error="Invalid username or password")
  else:
    return render_template("login.html")

@app.route("/login/submitted", methods=['GET', 'POST'])
def login_page_submitted ():
  if request.method == 'POST':
    data = []
    data = request.form
    lusername = request.form.get('lusername')
    lpassword = request.form.get('lpassword')
    found_stat = 'N'
    pwd = " "
    found_stat, pwd = verify_login(lusername, data, found_stat, pwd)
    if found_stat == 'Y':
      if (lpassword == pwd):
        session['username'] = lusername
        username = session['username']
        return render_template("dashboard.html", username=username)
      else:
        return render_template("login.html",
                               error="Invalid username or password")
    else:
      return render_template("login.html",
                             error="Invalid username or password")
  else:
    return render_template("login.html")


#Logout route
@app.route("/logout/", methods=['GET', 'POST'])
def logout_page():
  print("LOGOUT")
  session.pop('username', None)
  session.clear()
  return redirect(url_for('login_page'))
  #return redirect(url_for('home'))

#Register route
                  
@app.route("/register/")
def register_page():
  print("Control1 here.....")
  return render_template("register.html")

#Form submitted route
@app.route("/register/submitted", methods=['GET', 'POST'])
def get_user_details():
  if request.method == 'POST':
    data = []
    data = request.form
    print("POST DATA:", data)
    user_name = data.get("username")
    print("before check user name:", user_name)
    if not data:
      return "Not Found", 404
    else:
      insert_status = 'N'
      pwd = " "
      print("insert_status B:", insert_status)
      insert_status = validate_username(user_name, data, insert_status, pwd)
      print("insert_status A:", insert_status)
      return render_template("registration_submitted.html",
                             data=data,
                             insert_status_s=insert_status,
                             pwd=pwd)


print(__name__)
if (__name__ == "__main__"):
  app.secret_key = 'super secret key'
  app.config['SESSION_TYPE'] = 'filesystem'
  app.run(host="0.0.0.0", port=8080, debug=True)

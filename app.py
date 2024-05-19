from operator import inv
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from database import add_stock_to_db, add_user_to_db, validate_username, verify_login,load_stocks_from_db
import requests
from bs4 import BeautifulSoup
import time

#Name Initialization
app = Flask(__name__)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

#Home route
@app.route("/")
def landing_page():
  if 'username' in session:
    username=session['username']
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
    print("F STAT after DB call", found_stat)
    if found_stat == 'Y':
      if (lpassword == pwd):
        session['username'] = lusername
        username = session['username']
        return render_template("dashboard.html", username=username)
      else:
        return render_template("login.html",
                               error="Invalid username or password")
    else:
      print("IN ELSE", found_stat)
      return render_template("login.html",
                             error="User not found. Please register")
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
    print("F STAT after DB call 1", found_stat)
    if found_stat == 'Y':
      if (lpassword == pwd):
        session['username'] = lusername
        username = session['username']
        return render_template("dashboard.html", username=username)
      else:
        return render_template("login.html",
                               error="Invalid username or password")
    else:
      print("IN ELSE1 ", found_stat)
      return render_template("login.html",
                             error="User not found. Please register")
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
   
@app.route("/stock_dashboard")
def stock_portfolio():
    print("stock dashboard")
    print(session['username'])
    if 'username' in session:
      print('YES')
      username = session['username']  
      stocks = load_stocks_from_db()
      stocks = [tuple(row) for row in stocks]
      #print("stockss ...",  stocks)
      curr_prices = []
      Names       = []
      general_dist = []
      #  general_dist = {
      #    'Stocks'      : sum(values),
      #    'Crypto'      : sum(crypto_values),
      #    'Mutual Fund' : sum(MF_values),
      #    'Cash'        : cash 
      #    }
      stock_details = []
      total_invested = 0
      total_pl       = 0
      total_cnt      = 0
      for stock in stocks:
        total_cnt = total_cnt + 1
        ticker    = stock [2]
        sname     = stock [1]
        exchange  = stock [3]
        broker    = stock [4]
        quantity  = stock [6]
        avg_price = stock [7]
        inv_amt   = quantity * avg_price 
        url       =f'https://www.google.com/finance/quote/{ticker}'
        #print("url>>>>> ...",  stocks)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        class1='YMlKec fxKbKc'
        curr_price = float(soup.find(class_= class1).text.strip()    [1:].replace("," , ""))
        curr_val = curr_price * quantity
        curr_val = round(curr_val, 2)
        p_l = float(curr_val) - float(inv_amt)
        p_l = round(p_l, 2)
        p_l_p1 = (p_l / float(inv_amt)) 
        p_l_p  = '{:.2%}'.format(p_l_p1)
        total_invested = total_invested + float(inv_amt)
        total_invested = round(total_invested, 2)
        total_pl  = total_pl + float(p_l)
        total_pl = round(total_pl, 2)
        p_l_pt1 = (total_pl / float(total_invested)) 
        p_l_p_t  = '{:.2%}'.format(p_l_pt1)
        t1 =(sname,broker,quantity,avg_price,inv_amt,curr_price,curr_val,p_l,p_l_p)
        #print("t1::", t1 )
        stock_details.append(t1)
        #print("stock_details::", stock_details )
      return render_template("stock_dashboard.html",stock_details =stock_details,total_invested=total_invested,total_pl=total_pl,p_l_p_t=p_l_p_t,total_cnt=total_cnt, username=username)
    else:
      return render_template("home.html")
 
@app.route("/add_stock1")
def add_stock():
    print("in add stock")
    if 'username' in session:
      username = session['username'] 
      return render_template("add_stock.html",username = username)
    else:
      return render_template("home.html")
   
@app.route("/addstock/submitted", methods=['GET', 'POST'])
def add_stock_submitted ():
  if request.method == 'POST':
    data = []
    data = request.form
    print("POST DATA s sub:", data)
    username = session['username'] 
    # a_stock_name = request.form.get('a_stock_name')
    # a_stock_symbol = request.form.get('a_stock_symbol')
    #a_stock_exchage = request.form.get('a_stock_exchage')
    #a_stock_broker = request.form.get('a_stock_broker')
    #a_stock_quantity = request.form.get('a_stock_quantity')
    #a_stock_buyp = request.form.get('a_stock_buyp')
    #a_stock_username = 'jogeswarnanda' 
    found_stat = 'N'
    pwd = " "
    add_stock_to_db (data)
    return render_template("add_stock_form_sub.html",username = username)


#######
#@app.route("/test")
#def test_something ():
#  return render_template("test.html")
    
#######

print(__name__)
if (__name__ == "__main__"):
  app.secret_key = 'super secret key'
  app.config['SESSION_TYPE'] = 'filesystem'
  app.run(host="0.0.0.0", port=8080, debug=True)

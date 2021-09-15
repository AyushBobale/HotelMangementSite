"""
Author : 
Date   :
"""
from flask import Flask, render_template, request, session, flash
from datetime import datetime, date
import dbmanager, os, config

#-------------------------Debug------------------------------#
#------------------------------------------------------------#

config = config.Config()
app = Flask(__name__)
app.secret_key = 'key'
#Variables
HOST = config.HOST
PORT = config.PORT
DEBUG = True
TOTALTABLES = 32
RESERVATIONCOUNT = dbmanager.getcount("RESERVATION")
TRUE = "True"
FALSE = "False"
app.config["FEEDBACK_IMAGES"] = config.FEEDBACK_IMAGES
app.config["PROFILE_IMAGES"] = config.PROFILE_IMAGES
#Session variable
"""
information = {"iflogin":False,
              "username":None,
              "reservation":False,
              "reservationcount":RESERVATIONCOUNT,
              "menuitems": [],
              "bill": [],
              "order":False,
              "feedback":[] }
"""

#------------------------------------------------------------------------------------------------------#
#Main Home page#
@app.route('/',methods=['GET','POST'])
def index():
  try:
    #raise TypeError("Error test")
    if 'information' in session:
      return render_template('index.html', info = session['information'])
    else :
      session['information'] = {'iflogin':False,
                                'username':None,
                                "reservation":False,
                                "reservationcount":RESERVATIONCOUNT,
                                "menuitems": [],
                                "bill": [],
                                "order":False,
                                "feedback":[] }
      session.modified = True
      return render_template('index.html', info = session['information'])
  except Exception as error:
    return render_template('error.html', info = session['information'])

#Sign up
@app.route('/signup', methods=["POST","GET"])
def signup():
  try:
    if request.method == "POST":
      if request.form['submit_button'] == 'Sign up':
        user = request.form["username"]
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirmpassword = request.form["confirmpassword"]
        phone = request.form["phone"]
        address = request.form["address"]
        ifuserexists = dbmanager.checkuserifexists(user,email)
        if ifuserexists:
          flash("This user already exists ! or this email is previously used by anyone else","info")
          return render_template('signup.html', info = session['information'])
        else:
          if confirmpassword == password:
            curdate = date.today()
            today = str(curdate.strftime("%d/%m/%Y"))
            curtime = datetime.now()
            now = str(curtime.strftime("%H:%M:%S"))
            dbmanager.insert_default("USERID","(USERNAME,NAME,EMAIL,PASSWORD,PHONENO,ADDRESS,SIGNUPDATE,SIGNUPTIME)",(user,name,email,password,phone,address,today,now))
            session['information']['iflogin'] = True
            session['information']['username'] = user
            session.modified = True
            return render_template('index.html',info  = session['information'])
          else:
            flash("The passwords don't match !","info")
            return render_template('signup.html', info = session['information'])
    else:
      print("else part")
      return render_template('signup.html', info = session['information'])
  except Exception as e:
    return render_template('error.html', info = session['information'])

#Login
@app.route('/signin', methods=["POST","GET"])
def signin():
  try:
    if request.method == "POST":
      if request.form['submit_button'] == 'Login':
        user = request.form["username"]
        password = request.form["password"]
        ifuserexists = dbmanager.checkuser(user,password)
        if ifuserexists:
          session['information']['iflogin'] = True
          session['information']['username'] = user
          session.modified = True
          return render_template('index.html', info = session['information'])
        else:
          flash("Sorry Either the password or E-mail was wrong !","info")
          return render_template('signin.html', info = session['information'])
      elif request.form['submit_button'] == 'Forgot Password':
        return 'To make forgot password page'
      elif request.form['submit_button'] == 'Sign up':
        return render_template('signup.html', info = session['information'])
    else:
      return render_template('signin.html', info = session['information'])
  except Exception as e :
    return render_template('error.html', info = session['information'])

#Logout
@app.route('/logout',methods=['GET','POST'])
def logout():
  try:
    if session["information"]["iflogin"]:
      session['information'] = {'iflogin':False,
                                'username':None,
                                "reservation":False,
                                "reservationcount":RESERVATIONCOUNT,
                                "menuitems": [],
                                "bill": [],
                                "order":False,
                                "feedback":[] }
      session.modified = True
      flash("You have logged out successfully !",'info')
      return render_template('index.html', info = session['information'])
    else :
      flash("You have already logged out !","info")
      session['information']['iflogin'] = False
      session['information']['username'] = None
      session.modified = True
      return render_template('index.html', info = session['information'])
  except Exception as error:
    return render_template('error.html', info = session['information'])

#Reservation
@app.route('/reservation',methods=['GET','POST'])
def reservation():
  session['information']['reservationcount'] = dbmanager.getcount('RESERVATION')
  try:
    if request.method == "POST":
      if request.form['submit_button'] == 'Register':
        if session['information']['iflogin']:
          regdate = request.form['date']
          regtime = request.form['time']
          noofpeople = request.form['noofpeople']
          user = session["information"]['username']
          userid = dbmanager.getuserid(user)
          ifrevexist = dbmanager.checkreservation(user)
          if ifrevexist:
            revinfo = dbmanager.getreservationinfo(user)
            print(revinfo)
            session['information']['reservation'] = True
            flash("You have already reserved a table "+ revinfo[1] +revinfo[2],"info")
            return render_template('reservation.html', info = session['information'])
          dbmanager.insert_default("RESERVATION","(ID,NOOFPEOPLE,REGDATE,REGTIME)",(userid,noofpeople,regdate,regtime))
          flash("You have reserved yourself a table for "+noofpeople+" people on "+regdate+ " at time "+regtime,"info")
          session['information']['reservation'] = True
          return render_template('reservation.html', info = session['information'])
        else:
          flash("Please login first or if you don't have an account you can sign up for free !","info")
          return render_template('reservation.html', info = session['information'])
      elif request.form['submit_button'] == 'Cancel Registration':
        user = session['information']['username']
        dbmanager.cancelreservation(user)
        session['information']['reservation'] = False
        session.modified = True
        return render_template('reservation.html', info = session['information'])
    else:# get request
      if session['information']['iflogin']:# login check
        user = session['information']['username']
        print('In get reservation')
        ifrevexist = dbmanager.checkreservation(user)
        if ifrevexist:
          print('In if rev exists')
          revinfo = dbmanager.getreservationinfo(user)
          print(revinfo)
          session['information']['reservation'] = True
          flash("You already have a table reserverd for "+revinfo[1]+ " people on "+revinfo[2]+" at "+revinfo[3],"info")
          session.modified = True
          return render_template('reservation.html', info = session['information'])
        else :
          return render_template('reservation.html', info = session['information'])
      else:
        return render_template('reservation.html', info = session['information'])
  except Exception as error:
    return render_template('error.html', info = session['information'])

#Specials
@app.route('/special',methods=['GET','POST'])
def special():
  try:
    rows = dbmanager.select_table('*','SPECIAL')
    session['information']["menuitems"] = rows
    session.modified = True
    return render_template('special.html', info = session['information'])
  except Exception as error:
    return render_template('error.html', info = session['information'])

#Menu
@app.route('/menu',methods=['GET','POST'])
def menu():
  try:
    return render_template('menu.html', info = session['information'])
  except Exception as error:
    return render_template('error.html', info = session['information'])

#Menu_breakfast
@app.route('/menu_breakfast',methods=['GET','POST'])
def menu_breakfast():
  try:
    rows = dbmanager.select_menuitem('BREAKFAST')
    session['information']["menuitems"] = rows
    session.modified = True
    return render_template('menu_breakfast.html', info = session['information'])
  except Exception as error:
    return render_template('error.html', info = session['information'])

#Menu_maincourse
@app.route('/menu_maincourse',methods=['GET','POST'])
def menu_maincourse():
  try:
    rows = dbmanager.select_menuitem('MEAL')
    session['information']["menuitems"] = rows
    session.modified = True
    return render_template('menu_maincourse.html', info = session['information'])
  except Exception as error:
    return render_template('error.html', info = session['information'])

#Menu_Desert
@app.route('/menu_desert',methods=['GET','POST'])
def menu_desert():
  try:
    rows = dbmanager.select_menuitem('DESERT')
    session['information']["menuitems"] = rows
    session.modified = True
    return render_template('menu_desert.html', info = session['information'])
  except Exception as error:
    return render_template('error.html', info = session['information'])

#Menu_drinks
@app.route('/menu_drink',methods=['GET','POST'])
def menu_drink():
  try:
    rows = dbmanager.select_menuitem('DRINK')
    session['information']["menuitems"] = rows
    session.modified = True
    return render_template('menu_drink.html', info = session['information'])
  except Exception as error:
    return render_template('error.html', info = session['information'])

#Feedback
@app.route('/feedback',methods=['GET','POST'])
def feedback():
  try:
    if request.method == "POST":
      if request.form['submit_button'] == 'Give Feedback':
        image = request.files["image"]
        try :
          image.save(os.path.join(app.config["FEEDBACK_IMAGES"],image.filename))
        finally :
          feedback = request.form["feedback"]
          stars = request.form["stars"]
          user = session['information']["username"]
          imagepath = os.path.join("static/images/feedback",image.filename)
          userid = dbmanager.getuserid(user)
          dbmanager.add_feedback(userid,feedback,stars,imagepath)
          session['information']["feedback"] = dbmanager.get_feedback()
          session.modified = True
          return render_template('feedback.html', info = session['information'])      
    else:
      session['information']["feedback"] = dbmanager.get_feedback()
      session.modified = True
      return render_template('feedback.html', info = session['information'])
  except Exception as error:
    return render_template('error.html', info = session['information'])


#Homedelivery =========================== To do not working session var error at add item

@app.route('/homedelivery',methods=['GET','POST'])
def homedelivery():
  try:
    if session['information']["iflogin"] :
      if "bill" not in session['information']:
        # Used to create the bill key if it does not exist so that to avoid key error
        session['information']['bill'] = []
        session.modified = True
      if request.method == "POST":
        #for getting pst requests
        if request.form['menu_type'] == 'Breakfast':
          rows = dbmanager.select_menuitem('BREAKFAST')
          session['information']["menuitems"] = rows
          session.modified = True
          return render_template('homedelivery.html', info = session['information'])
        if request.form['menu_type'] == 'Main Course':
          rows = dbmanager.select_menuitem('MEAL')
          session['information']["menuitems"] = rows
          session.modified = True
          return render_template('homedelivery.html', info = session['information'])
        if request.form['menu_type'] == 'Deserts':
          rows = dbmanager.select_menuitem('DESERT')
          session['information']["menuitems"] = rows
          session.modified = True
          return render_template('homedelivery.html', info = session['information'])
        if request.form['menu_type'] == 'Drinks':
          rows = dbmanager.select_menuitem('DRINK')
          session['information']["menuitems"] = rows
          session.modified = True
          return render_template('homedelivery.html', info = session['information'])

        if request.form['menu_type'] == 'Add Item':
          idty = request.form['hidden_value']
          quantity = request.form['quantity']

          if not session['information']["bill"]:
            #Executed when the bill var is empty
            print("Bill variable was empty")
            session['information']['bill'].append(dbmanager.get_bill_values(idty,quantity))
            session.modified = True
          else :
            print("In else ie the bill was not empty")
            flag_does_not_exists = True #we assume that the item is not in the bill
            session['information']['bill'].append(dbmanager.get_bill_values(idty,quantity))
            session.modified = True
            return render_template('homedelivery.html', info = session['information'])   
            ''''
            for i in session['information']['bill']:
              print("in for loop")
              if str(i[0]) == str(idty):
                print("in for if")
                flag_does_not_exists = False #we flag that the item exists and update its quantity
                print("flagged false")
                i[3] = int(i[3]) + int(quantity)
                print('in after if',i)
                return render_template('homedelivery.html', info = session['information'])   
              else:
                session['information']['bill'].append(dbmanager.get_bill_values(idty,quantity))
                session.modified = True
                return render_template('homedelivery.html', info = session['information'])   
          '''
          '''
            if flag_does_not_exists: 
              #based on the flag we determine wether it was a new item or not if ye then we add it if not it was previously upadted in the for loop
              session['information']['bill'].append(dbmanager.get_bill_values(idty,quantity))
              session.modified = True
              return render_template('homedelivery.html', info = session['information'])  
'''

          session['information']['menuitems'] = dbmanager.select_menuitem('BREAKFAST')
          session.modified = True
          #Finally got it to work it was a wreck
          return render_template('homedelivery.html', info = session['information'])  

        
        if request.form['menu_type'] == 'Remove Item':        
          idty = request.form['hidden_value']
          print('Idty : ', idty)
          for i in range(len(session['information']["bill"])):
            print('count',i)
            if str(session['information']["bill"][i][0]) == str(idty):
              print("item : ",session['information']["bill"][i])
              session['information']["bill"].pop(i)
              session.modified = True
            return render_template('homedelivery.html', info = session['information'])  

        #-----------------------------------------------currently working
        if request.form['menu_type'] == 'Place Order':
          userid = dbmanager.getuserid(session['information']["username"])
          for item in session['information']["bill"]:
            dbmanager.place_order(userid,str(item[0]),str(item[3]))
          session['information']["order"] = True
          return render_template('homedelivery.html', info = session['information'])  

        if request.form['menu_type'] == 'Cancel Order':
          session['information']["bill"] = []
          session['information']["order"] = False
          userid = dbmanager.getuserid(session['information']["username"])
          dbmanager.cancel_order(userid)
          session.modified = True
          return render_template('homedelivery.html', info = session['information'])  
        else:
          rows = dbmanager.select_menuitem('BREAKFAST')
          session['information']["menuitems"] = rows
          session.modified = True
          return render_template('homedelivery.html', info = session['information'])  
      #this else if for get request
      else:
        rows = dbmanager.select_menuitem('BREAKFAST')
        session['information']["menuitems"] = rows
        session.modified = True
        return render_template('homedelivery.html', info = session['information'])
    #this else is when if there is no logged in user
    else:
      #to do
      if request.method == "POST":
        if request.form['menu_type'] == 'Sign In':
          return render_template('signin.html', info = session['information'])
        if request.form['menu_type'] == 'Sign Up':
          return render_template('signup.html', info = session['information'])
      # for get request
      else :
        return render_template('homedelivery.html', info = session['information'])

  except Exception as error :
    return render_template('error.html', info = session['information'])

#------------------------------------------------------------------------------------------------------#

#=================================================Staff Side Pages=================================================#
staffinformation ={ "iflogin":False,
                    "username":None,
                    "ifadmin":False,
                    "employees": [],
                    "reservations":[],
                    "homedeliverys":[],
                    "special":[],
                    "specialcount":0 }

#Home Page
@app.route('/staffhome',methods=['GET','POST'])
def staffhome():
  try:
    if 'staffinformation' in session:
      session['staffinformation']['employees'] = []
      session['staffinformation']['reservations'] = []
      session['staffinformation']['homedeliverys'] = []
      session['staffinformation']['special'] = []
      session.modified = True
      return render_template('staffhome.html', info = session['staffinformation'])
    else:
      session['staffinformation'] = { "iflogin":False,
                      "username":None,
                      "ifadmin":False,
                      "employees": [],
                      "reservations":[] }
      return render_template('staffhome.html', info = session['staffinformation'])
  except Exception as error:
    return render_template('error.html', info = session['staffinformation'])

#Special manager
@app.route('/specialmanager', methods = ['GET','POST'])
def specialmanager():
  try:
    if 'staffinformation' in session:
      session['staffinformation']['employees'] = []
      session['staffinformation']['reservations'] = []
      session['staffinformation']['homedeliverys'] = []
      session['staffinformation']['special'] = dbmanager.select_table('*','SPECIAL')
      rows = dbmanager.select_table('*','SPECIAL')
      session['staffinformation']['specialcount'] = len(rows)
      session.modified = True
      if request.method == 'POST':
        if request.form['submit_button'] == 'Remove':
          itemid = request.form['itemid']
          dbmanager.remove_special(itemid)
          session['staffinformation']['special'] = dbmanager.select_table('*','SPECIAL')
          rows = dbmanager.select_table('*','SPECIAL')
          session['staffinformation']['specialcount'] = len(rows)
          session.modified = True
          return render_template('specialmanager.html', info = session['staffinformation'])


        if request.form['submit_button'] == 'Add Item':
          name = request.form['name']
          description = request.form['description']
          ingredient = request.form['ingredient']
          image1 = request.files["image1"]
          image1.save(os.path.join(config.SPECIAL_IMAGES,image1.filename))
          image1path = os.path.join("static/images/menu/special",image1.filename)
          image2 = request.files["image2"]
          image2.save(os.path.join(config.SPECIAL_IMAGES,image2.filename))
          image2path = os.path.join("static/images/menu/special",image2.filename)
          image3 = request.files["image3"]
          image3.save(os.path.join(config.SPECIAL_IMAGES,image3.filename))
          image3path = os.path.join("static/images/menu/special",image3.filename)
          image4 = request.files["image4"]
          image4.save(os.path.join(config.SPECIAL_IMAGES,image4.filename))
          image4path = os.path.join("static/images/menu/special",image4.filename)
          dbmanager.insert_special((name,description,ingredient,image1path,image2path,image3path,image4path))
          session['staffinformation']['special'] = dbmanager.select_table('*','SPECIAL')
          rows = dbmanager.select_table('*','SPECIAL')
          session['staffinformation']['specialcount'] = len(rows)
          session.modified = True
          return render_template('specialmanager.html', info = session['staffinformation'])
      
      
      else:
        #get request
        return render_template('specialmanager.html', info = session['staffinformation'])  
    else:#if unauthorized access
      return render_template('stafflogin.html', info = session['staffinformation'])
  except Exception as error:
    return render_template('error.html', info = session['staffinformation'])

#Admin page
@app.route('/adminpage',methods=['GET','POST'])
def adminpage():
  try:
    if session['staffinformation']['iflogin']:
      session['staffinformation']['reservations'] = []
      session['staffinformation']['homedeliverys'] = []
      session['staffinformation']['special'] = []
      session['staffinformation']["employees"] = dbmanager.select_table('*','EMPLOYEE')
      session.modified = True
      if request.method == 'POST':
        if request.form['submit_button'] == 'Add Employee':
          username = request.form['username']
          password = request.form['password']
          confirmpassword = request.form['confirmpassword']
          emptype = request.form['type']
          image = request.files["image"]
          image.save(os.path.join(app.config["PROFILE_IMAGES"],image.filename))
          imagepath = os.path.join("static/images/profile",image.filename)
          if password == confirmpassword:
            if not dbmanager.if_emp_exists(username):
              dbmanager.add_emp(username,password,emptype,imagepath)
              session['staffinformation']["employees"] = dbmanager.select_table('*','EMPLOYEE')
              flash("New user added","info")
              session.modified = True
              return render_template('adminpage.html', info = session['staffinformation'])  
            else:
              # user already exists
              flash("The user already exists","info")
              return render_template('adminpage.html', info = session['staffinformation'])  
          else:
            #if passwords dont match
            flash("passwords don't match","info")
            return render_template('adminpage.html', info = session['staffinformation']) 
        elif request.form['submit_button'] == 'Remove Employee':
          username = request.form['username']
          print("username ------------------",username)
          if dbmanager.if_emp_exists(username):
            print("Inside if")
            dbmanager.del_emp(username)
            print("after del")
            session['staffinformation']["employees"] = dbmanager.select_table('*','EMPLOYEE')
            print("after dstaff info")
            session.modified = True
            flash("The user " + username + " removed","info")
            return render_template('adminpage.html', info = session['staffinformation']) 
          else :
            print("Inside else")
            return render_template('adminpage.html', info = session['staffinformation']) 

      else:# for get request
        print('get request')
        return render_template('adminpage.html', info = session['staffinformation'])  
    else:
      print('unauthorized access')
      #if there is no login [unauthorized access]
      return render_template('stafflogin.html', info = session['staffinformation'])
  except Exception as error:
    return render_template('error.html', info = session['staffinformation'])

#Reservation management
@app.route('/reservationmanagement',methods=['GET','POST'])
def reservationmanagement():
  try:
    if session['staffinformation']['iflogin']:
      session['staffinformation']['employees'] = []
      session['staffinformation']['homedeliverys'] = []
      session['staffinformation']['special'] = []
      rows = dbmanager.get_reservation()
      session['staffinformation']['reservations'] = rows
      session.modified = True
      if request.method == 'POST':
        if request.form['submit_button'] == 'Expired':
          
          dbmanager.reservation_expired(request.form['username'])
          session['staffinformation']['reservations'] = dbmanager.get_reservation()
          session.modified = True
          return render_template('reservationmanagement.html', info = session['staffinformation'])
        if request.form['submit_button'] == 'Occupied':
          
          dbmanager.reservation_occupied(request.form['username'])
          session['staffinformation']['reservations'] = dbmanager.get_reservation()
          session.modified = True
          return render_template('reservationmanagement.html', info = session['staffinformation'])
      else:# Get request
        return render_template('reservationmanagement.html', info = session['staffinformation'])
    else:
      return render_template('stafflogin.html', info = session['staffinformation'])
  except Exception as error:
    return render_template('error.html', info = session['staffinformation'])

#Home Delivery Managment homedeliverymanagment
@app.route('/homedeliverymanagement', methods=['GET','POST'])
def homedeliverymanagement():
  try:
    if session['staffinformation']['iflogin']:
      session['staffinformation']['employees'] = []
      session['staffinformation']['reservations'] = []
      session['staffinformation']['special'] = []
      session['staffinformation']['homedeliverys'] = dbmanager.format_orders()
      session.modified = True
      print('In session')
      if request.method == 'POST':
        username = request.form['username']

        if request.form['submit_button'] == 'Placed':
          dbmanager.order_placed(username)
          session['staffinformation']['homedeliverys'] = dbmanager.format_orders()
          session.modified = True
          return render_template('homedeliverymanagement.html', info = session['staffinformation'])
        if request.form['submit_button'] == 'Delivered':
          dbmanager.order_delivered(username)
          session['staffinformation']['homedeliverys'] = dbmanager.format_orders()
          session.modified = True
          return render_template('homedeliverymanagement.html', info = session['staffinformation'])
        if request.form['submit_button'] == 'Cancelled':
          dbmanager.order_cancelled(username)
          session['staffinformation']['homedeliverys'] = dbmanager.format_orders()
          session.modified = True
          return render_template('homedeliverymanagement.html', info = session['staffinformation'])


      else:# get request
        return render_template('homedeliverymanagement.html', info = session['staffinformation'])
    else:# if unauthorized access
      return render_template('stafflogin.html', info = session['staffinformation'])
  except Exception as error :
    return render_template('error.html', info = session['staffinformation'])


@app.route('/stafflogin',methods=['GET','POST'])
def stafflogin():
  try:
    if request.method == "POST":
      if request.form['submit_button'] == 'Login':
        username = request.form["username"]
        password = request.form["password"]
        if dbmanager.emp_login(username,password):
          if dbmanager.if_admin(username):
            #this is for is the person is admin
            session['staffinformation']["iflogin"] = True
            session['staffinformation']["username"] = username
            session['staffinformation']["ifadmin"] = True
            session.modified = True
            return render_template('staffhome.html', info = session['staffinformation'])
          else:
            #this is for if the person is normal employee
            session['staffinformation']["iflogin"] = True
            session['staffinformation']["username"] = username
            session['staffinformation']["ifadmin"] = False
            session.modified = True
            return render_template('staffhome.html', info = session['staffinformation'])
        else:
          #this is if the username and passwords didnt match
          flash("The username or password you entered is wrong","info")
          return render_template('stafflogin.html', info = session['staffinformation'])
    else:
      return render_template('stafflogin.html', info = session['staffinformation'])
  except Exception as error:
    return render_template('error.html', info = session['staffinformation'])

#StaffLogout
@app.route('/stafflogout',methods=['GET','POST'])
def stafflogout():
  try:
    print('in try ')
    if session['staffinformation']["iflogin"]:
      session['staffinformation']['iflogin'] = False
      session['staffinformation']['username'] = None
      session['staffinformation']['ifadmin'] = False
      session['staffinformation']['employees'] = []
      session['staffinformation']['special'] = []
      session.modified = True
      flash("You have logged out successfully !",'info')
      return render_template('staffhome.html', info = session['staffinformation'])
    else :
      flash("You have already logged out !","info")
      session['staffinformation']['iflogin'] = False
      session['staffinformation']['username'] = None
      session['staffinformation']['ifadmin'] = False
      session['staffinformation']['employees'] = []
      session.modified = True
      return render_template('staffhome.html', info = session['staffinformation'])
  except Exception as error:
    return render_template('error.html', info = session['staffinformation'])


#===================#
if __name__ =='__main__':
    app.run(debug = DEBUG,
            host = HOST,
            port = PORT)
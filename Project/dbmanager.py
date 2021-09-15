import sqlite3
import os, config
from datetime import datetime, date
print('==================================')
print('| Database manager has begun.... |')
print('==================================')
config = config.Config()
DATABASE = config.CURRENTDATABASE
def create_connection(name):# Connects to the specified database
  return sqlite3.connect(name)

def tupletostr(tpl):
  mystr = "("
  for _ in tpl:
      mystr = mystr + "'" + _  + "'" + ","
  mystr = mystr[:-1]
  mystr = mystr + ")" 
  return mystr
def close_connection(connection):# Creates a connection to the database
  connection.close()

def create_table_default(connection): # Creates all the default tables and inserts any default values if mentioned 
  print('Default tabes was called all previous data was erased.')
  sql1 = "DROP TABLE IF EXISTS LOGIN"
  sql2 = '''CREATE TABLE LOGIN (
    ID VARCHAR(5) NOT NULL UNIQUE,
    EMAIL VARCHAR(50) NOT NULL UNIQUE,
    PASSWORD VARCHAR(16) NOT NULL UNIQUE)'''
  ############
  sql3 = 'DROP TABLE IF EXISTS ERRORLOGGER'
  sql4 = '''CREATE TABLE ERRORLOGGER (
    ID INTEGER PRIMARY KEY AUTOINCREMENT ,
    ERROR VARCHAR(500),
    TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP  )'''
  sql5 = "INSERT INTO ERRORLOGGER (ID,ERROR) VALUES (1,'NO ERROR SYSTEM BOOTED')"
  ###############
  sql6 = 'DROP TABLE IF EXISTS USERID'
  sql7 = '''CREATE TABLE USERID (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    USERNAME VARCHAR(15) UNIQUE NOT NULL,
    NAME VARCHAR(25),
    EMAIL VARCHAR(50) UNIQUE NOT NULL,
    PASSWORD VARCHAR(16) NOT NULL,
    PHONENO VARCHAR(12),
    ADDRESS VARCHAR(100),
    SIGNUPDATE DATE,
    SIGNUPTIME TIME  )'''
  ########
  sql8 = "INSERT INTO USERID (USERNAME,EMAIL,PASSWORD) VALUES('ADMIN','ADMIN','ADMIN')"
  sql8copy = "INSERT INTO USERID (USERNAME,EMAIL,PASSWORD) VALUES('ADMIN1','ADMIN1','ADMIN1')"
  sql9 = "DROP TABLE IF EXISTS RESERVATION"
  sql10 =  '''CREATE TABLE RESERVATION (
    ID VARCHAR(5) ,
    NOOFPEOPLE VARCHAR(1) ,
    REGDATE DATE ,
    REGTIME TIME,
    EXPIRED VARCHAR(5),
    OCCUPIED VARCHAR(5) ) '''
  #############
  sql11 = "DROP TABLE IF EXISTS MENU"
  sql12 = '''CREATE TABLE MENU(
    ITEMID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME VARCHAR(20),
    DESCRIPTION VARCHAR(150),
    INGREDIENT VARCHAR(150),
    IMAGEPATH VARCHAR(100),
    COST REAL,
    TYPE VARCHAR(10) )'''
  ############
  sql13 = "DROP TABLE IF EXISTS HOMEDELIVERY"
  sql14 = '''CREATE TABLE HOMEDELIVERY(
    USERID INTEGER,
    ITEMID INTEGER,
    QUANTITY INTEGER,
    ORDERTIME TIME,
    ORDERDATE DATE,
    PLACED VARCHAR(5),
    DELIVERED VARCAHR(5),
    CANCELLED VARCHAR(5) ) '''
  ######
  sql15 = "DROP TABLE IF EXISTS FEEDBACK"
  sql16 = '''CREATE TABLE FEEDBACK(
    USERID VARCHAR(50),
    FEEDBACKID INTEGER PRIMARY KEY AUTOINCREMENT,
    FEEDBACK VARCHAR(200),
    STARS INTEGER,
    IMAGE VARCHAR(100),
    FEEDBACKTIME TIME,
    FEEDBACKDATE DATE ) '''
  #########
  sql17 = "DROP TABLE IF EXISTS EMPLOYEE"
  sql18 = ''' CREATE TABLE EMPLOYEE(
    EMPID INTEGER PRIMARY KEY AUTOINCREMENT,
    USERNAME VARCHAR(20) UNIQUE,
    PASSWORD VARCHAR(20),
    TYPE VARCHAR(5),
    IMAGE VARCHAR(150) ) '''
  ###########
  sql19 = "DROP TABLE IF EXISTS SPECIAL"
  sql20 = '''CREATE TABLE SPECIAL(
  ITEMID INTEGER PRIMARY KEY AUTOINCREMENT,
  NAME VARCHAR(100),
  DESC VARCHAR(200),
  INGREDIENT VARCHAR(200),
  IMAGE1 VARCHAR(100),
  IMAGE2 VARCHAR(100),
  IMAGE3 VARCHAR(100),
  IMAGE4 VARCHAR(100) ) '''
  


  connection = create_connection(DATABASE)
  cursor = connection.cursor()
  cursor.execute(sql1)
  cursor.execute(sql2)
  cursor.execute(sql3)
  cursor.execute(sql4)
  cursor.execute(sql5)
  cursor.execute(sql6)
  cursor.execute(sql7)
  cursor.execute(sql8)
  cursor.execute(sql8copy)
  cursor.execute(sql9)
  cursor.execute(sql10)
  cursor.execute(sql11)
  cursor.execute(sql12)
  cursor.execute(sql13)
  cursor.execute(sql14)
  cursor.execute(sql15)
  cursor.execute(sql16)
  cursor.execute(sql17)
  cursor.execute(sql18)
  cursor.execute(sql19)
  cursor.execute(sql20)
  connection.commit()
  

def insert_default(tabelname,colnames,values):# Inserts values in the table provided tabelname, column name, values, and the connection object 
  value = tupletostr(values)
  sql1 = 'INSERT INTO ' + tabelname + colnames +' VALUES ' + value
  connection = create_connection(DATABASE)
  cursor = connection.cursor()
  cursor.execute(sql1)
  connection.commit()


def select_table(colnames, tabelname): # Returns a list of tuples of the rows provided with column names , table name and the connection object
  print("=======",tabelname)
  sql1 = 'SELECT ' + colnames + ' FROM ' + tabelname
  connection = create_connection(DATABASE)
  cursor = connection.cursor()
  cursor.execute(sql1)
  rows= cursor.fetchall()
  return rows
  
def checkuser(username,password):
  sql1 = "SELECT * FROM USERID WHERE USERNAME = '"+ username + "' AND PASSWORD = '" + password + "'"
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1)
  rows = cursor.fetchall()
  if not rows:
    return False
  else:
    return True

def checkuserifexists(username,email):
  sql1 = "SELECT * FROM USERID WHERE USERNAME = '"+ username + "' OR EMAIL = '" + email + "'"
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1)
  rows = cursor.fetchall()
  if not rows:
    return False
  else :
    return True
  
def checkreservation(username):
  sql1 = "SELECT ID  FROM USERID WHERE USERNAME = '" + username + "'"
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1)
  userid = cursor.fetchall()
  if not userid:
    return False
  userid = userid[0][0]
  userid = str(userid)
  sql2 = "SELECT * FROM RESERVATION WHERE ID = '" + userid + "'"
  cursor.execute(sql2)
  rows = cursor.fetchall()
  if not rows:
    return False
  else :
    return True

def getreservationinfo(username):
  sql1 = "SELECT ID  FROM USERID WHERE USERNAME = '" + username + "'"
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1)
  userid = cursor.fetchall()
  if not userid:
    return False
  userid = userid[0][0]
  userid = str(userid)
  sql2 = "SELECT * FROM RESERVATION WHERE ID = '" + userid + "'"
  cursor.execute(sql2)
  rows = cursor.fetchall()
  return rows[0]

def datepreprocessor(regdate):
  regdate = regdate[:-3]
  regdate = regdate + ":00"
  return regdate  

def cancelreservation(username):
  sql1 = "SELECT ID  FROM USERID WHERE USERNAME = '" + username + "'"
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1)
  userid = cursor.fetchall()
  userid = userid[0][0]
  userid = str(userid)
  sql2 = "DELETE FROM RESERVATION WHERE ID = '" + userid +"'"
  cursor.execute(sql2)
  con.commit()
  con.close()

def getuserid(username):
  sql1 = "SELECT ID  FROM USERID WHERE USERNAME = '" + username + "'"
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1)
  userid = cursor.fetchall()
  userid = userid[0][0]
  userid = str(userid)
  return userid

def getusername(userid):
  sql1 = "SELECT USERNAME FROM USERID WHERE ID = ?"
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1,(str(userid),))
  username = cursor.fetchall()
  username = username[0][0]
  return username

def getcount(tablename):
  sql1 = "SELECT COUNT(*) FROM '" +tablename+ "'"
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1)
  rowcount = cursor.fetchone()
  return rowcount[0]

def converttobinary(filename):
  #Convert digital data to binary format
  filepath = 'Project/static/images/' + filename 
  with open(filepath, 'rb') as file:
    blobData = file.read()
  return blobData

def insert_menuitem(values):
  sql1 = "INSERT INTO MENU (NAME,DESCRIPTION,INGREDIENT,IMAGEPATH,COST,TYPE) VALUES(?, ?, ?, ?, ?, ?)"
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1,values)
  con.commit()
  con.close()

def select_menuitem(itemtype):
  sql1 = "SELECT * FROM MENU WHERE TYPE= '" + itemtype + "'" 
  connection = create_connection(DATABASE)
  cursor = connection.cursor()
  cursor.execute(sql1)
  rows = cursor.fetchall()
  return rows

def bill_values(itemid):
  sql1 = "SELECT * FROM MENU WHERE ITEMID = ? "
  con = create_connection(DATABASE)
  cursor = con.cursor()
  rows = []
  for i in itemid:
    cursor.execute(sql1,str(i[0]))
    row = cursor.fetchall()
    row[0] = list(row[0])
    row[0][5] = row[0][5] * int(i[1])
    rows.append(row)
  con.close()
  return rows

def place_order(userid,itemid,quantity):
  curdate = date.today()
  today = str(curdate.strftime("%d/%m/%Y"))
  curtime = datetime.now()
  now = str(curtime.strftime("%H:%M:%S"))
  insert_default("HOMEDELIVERY","(USERID,ITEMID,QUANTITY,ORDERTIME,ORDERDATE)",(userid,itemid,quantity,now,today))
  print("The place order was called ")

def cancel_order(userid):
  sql1 = "DELETE FROM HOMEDELIVERY WHERE USERID = " + userid
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1)
  con.commit()
  con.close()

def add_feedback(userid,feedback,stars,image = None):
  user = getusername(userid)
  feedbackexists = if_feedback_exists(user)
  if feedbackexists:
    update_feedback(user,feedback,stars,image)
  else:
    curdate = date.today()
    today = str(curdate.strftime("%d/%m/%Y"))
    curtime = datetime.now()
    now = str(curtime.strftime("%H:%M:%S"))
    sql1 = "INSERT INTO FEEDBACK (USERID,FEEDBACK,STARS,FEEDBACKTIME,FEEDBACKDATE,IMAGE) VALUES(?, ?, ?, ?, ?, ?)"
    con = create_connection(DATABASE)
    cursor = con.cursor()
    cursor.execute(sql1,(user,feedback,stars,now,today,image))
    con.commit()
    con.close()

def update_feedback(username,feedback,stars,image = None):
  curdate = date.today()
  today = str(curdate.strftime("%d/%m/%Y"))
  curtime = datetime.now()
  now = str(curtime.strftime("%H:%M:%S"))
  print("Username : ",username)
  sql1 = '''UPDATE FEEDBACK SET 
    FEEDBACK = ?,
    STARS = ?,
    FEEDBACKTIME = ?,
    FEEDBACKDATE = ?,
    IMAGE = ?
    WHERE USERID = ?'''
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1,(feedback,stars,now,today,image,username))
  con.commit()
  con.close()

def get_feedback():
  rows = select_table("*","FEEDBACK")
  return rows

def if_feedback_exists(username):
  sql1 = "SELECT * FROM FEEDBACK WHERE USERID = ?"
  con = create_connection(DATABASE)
  cursor = con.cursor()
  username = username
  cursor.execute(sql1,(str(username),))
  row = cursor.fetchall()
  con.close()
  if not row:
    return False
  else:
    return True

def add_emp(username,password,emptype,image="static/images/profile/profile.jpg"):
  sql1 = "INSERT INTO EMPLOYEE (USERNAME,PASSWORD,TYPE,IMAGE) VALUES(?, ?, ?, ?)"
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1,(username,password,emptype,image))
  con.commit()
  con.close()

def get_emp_id(username):
  sql1 = "SELECT EMPID FROM EMPLOYEE WHERE USERNAME = ?"
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1,(username,))
  rows = cursor.fetchall()
  userid = rows[0][0]
  con.close()
  return userid

def if_emp_exists(username):
  sql1 = "SELECT * FROM EMPLOYEE WHERE USERNAME = ?"
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1,(username,))
  rows = cursor.fetchall()
  con.close()
  if not rows:
    return False
  else :
    return True

def emp_login(username,password):
  sql1 = "SELECT * FROM EMPLOYEE WHERE USERNAME = ? AND PASSWORD = ?"
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1,(username,password))
  rows = cursor.fetchall()
  con.close()
  if not rows:
    return False
  else :
    return True


def if_admin(username):
  if if_emp_exists(username):
    sql1 = "SELECT * FROM EMPLOYEE WHERE USERNAME = ?"
    con = create_connection(DATABASE)
    cursor = con.cursor()
    cursor.execute(sql1,(username,))
    rows = cursor.fetchall()
    con.close()
    if rows[0][3] == "ADMIN":
      return True
    elif rows[0][3] == "EMP":
      return False
  else:
    return False

def del_emp(username):
  if if_emp_exists(username):
    sql1 = "DELETE FROM EMPLOYEE WHERE USERNAME = ?"
    con = create_connection(DATABASE)
    cursor = con.cursor()
    cursor.execute(sql1,(username,))
    con.commit()
    con.close()
  else:
    return

def get_reservation():
  sql1 = "SELECT * FROM RESERVATION"
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1)
  rowstuple = cursor.fetchall()
  rows = list(rowstuple)
  print(rows)
  for i in range(0, len(rows)):
    rows[i] = list(rows[i])
  for i in range(0,len(rows)):
    rows[i][0] = getusername(rows[i][0])
  return rows

def reservation_expired(username):
  userid = getuserid(username)
  sql1 = "UPDATE RESERVATION SET EXPIRED = ?, OCCUPIED = ? WHERE ID = ?"
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1,('True','False',userid))
  con.commit()
  con.close()

def reservation_occupied(username):
  userid = getuserid(username)
  sql1 = "UPDATE RESERVATION SET OCCUPIED = ? WHERE ID = ?"
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1,('True',userid))
  con.commit()
  con.close()

def get_orders(userid):
  #userid = getuserid(username)
  sql1 = "SELECT * FROM HOMEDELIVERY WHERE USERID = ?"
  sql2 = "SELECT NAME FROM MENU WHERE ITEMID = ?"
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1,(userid,))
  rows = cursor.fetchall()
  for i in range(0, len(rows)):
    rows[i] = list(rows[i])
  for i in range(0,len(rows)):
    rows[i][0] = getusername(rows[i][0])
    cursor.execute(sql2,(rows[i][2],))
    name = cursor.fetchone()
    rows[i][2] = name[0] 
    rows[i] = rows[i][1:]
  return rows



def format_orders():
  sql1 = "SELECT USERID FROM HOMEDELIVERY GROUP BY USERID"
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1)
  rows = cursor.fetchall()
  carts = []
  for i in rows:
    cart = []
    username = getusername(i[0])
    cart.append(username)
    cart.append(get_orders(i[0]))
    carts.append(cart)
    row = get_orders(i[0])
    now = row[0][2]
    today = row[0][3]
    placed = row[0][4]
    delivered = row[0][5]
    cancelled = row[0][6]
    if len(cart) == 2:
      cart.append(now)
      cart.append(today) 
      cart.append(placed) 
      cart.append(delivered) 
      cart.append(cancelled) 
  for cart in carts:
    for i in cart[1]:
      i.pop(2)
      i.pop(2)
      i.pop(2)
      i.pop(2)
      i.pop(2)
  return carts

def order_placed(username):
  sql1 = "UPDATE HOMEDELIVERY SET PLACED = ? WHERE USERID = ?"
  userid = getuserid(username)
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1,('True',userid))
  con.commit()
  return None

def order_delivered(username):
  sql1 = "UPDATE HOMEDELIVERY SET DELIVERED = ?, PLACED = ? WHERE USERID = ?"
  userid = getuserid(username)
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1,('True','True',userid))
  con.commit()
  return None

def order_cancelled(username):
  sql1 = "UPDATE HOMEDELIVERY SET CANCELLED = ?, DELIVERED = ?, PLACED = ? WHERE USERID = ?"
  userid = getuserid(username)
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1,('True','False','False',userid))
  con.commit()
  return None

def insert_special(values):
  sql1 = "INSERT INTO SPECIAL (NAME,DESC,INGREDIENT,IMAGE1,IMAGE2,IMAGE3,IMAGE4) VALUES(?, ?, ?, ?, ?, ?, ?)" 
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1,values)
  con.commit()
  con.close

def remove_special(itemid):
  sql1 = "DELETE FROM SPECIAL WHERE ITEMID = ?"
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1,(itemid,))
  con.commit()
  con.close


def get_bill_values(idty,quantity):
  sql1 = "SELECT * FROM MENU WHERE ITEMID = ? "
  con = create_connection(DATABASE)
  cursor = con.cursor()
  cursor.execute(sql1, (idty,))
  row = cursor.fetchall()
  myrow = []
  myrow.append(row[0][0])
  myrow.append(row[0][1])
  myrow.append(row[0][5])
  myrow.append(quantity)
  return myrow


def debugger():
  print("=================Debugger called==================")
  con = None
  con = create_connection(DATABASE)
  create_table_default(con)
  insert_default("RESERVATION","(ID,NOOFPEOPLE,REGDATE,REGTIME)",('1','5','2000-9-6',datepreprocessor('10:20')))
  print(select_table('*','ERRORLOGGER'))
  print(select_table('*','USERID'))
  print(select_table('*','RESERVATION'))
  insert_menuitem(('BREAKFAST ITEM',' BREAKFAST DESCREPTION','BREAKFAST INGREDIENTS','hero.jpg',2000,'BREAKFAST'))
  insert_menuitem(('MEAL ITEM','MEAL DESCREPTION','MEAL INGREDIENTS','hero.jpg',2000,'MEAL'))
  insert_menuitem(('DESERT ITEM','DESERT DESCREPTION','DESERT INGREDIENTS','hero.jpg',2000,'DESERT'))
  insert_menuitem(('DRINK ITEM','DRINK DESCREPTION','DRINK INGREDIENTS','hero.jpg',2000,'DRINK'))
  insert_menuitem(('Specail ITEM 1','Specail DESCREPTION 1','Special INGREDIENTS 1 ','hero.jpg',2000,'SPECIAL'))
  insert_menuitem(('Specail ITEM 2','Specail DESCREPTION 2','Special INGREDIENTS 2 ','hero.jpg',2000,'SPECIAL'))
  insert_menuitem(('Specail ITEM 3','Specail DESCREPTION 3','Special INGREDIENTS 3 ','hero.jpg',2000,'SPECIAL'))
  print(select_table('*','MENU'))
  ids = [('1','5'),('2','3')]
  print(bill_values(ids))
  place_order('1','1','3')
  place_order('2','3','3')
  place_order('1','2','3')
  print(select_table("*","HOMEDELIVERY"))
  add_feedback(1,"good",5)
  print("==============",get_feedback())
  add_feedback(1,"Very good changed",4)
  print("Upadated feedback : ",get_feedback())

  add_emp("admin","password","ADMIN")
  add_emp("employee","password","EMP")
  print(select_table('*','EMPLOYEE'))
  print(if_emp_exists("admin"))
  print(if_admin("employee"))
  print(get_emp_id("employee"))

  insert_special(('Special 1','Special 1 description','Special 1 ingredients','static/images/menu/special/sample.jpg','static/images/menu/special/sample.jpg','static/images/menu/special/sample.jpg','static/images/menu/special/sample.jpg'))

  insert_special(('Special 2','Special 2 description','Special 2 ingredients','static/images/menu/special/sample.jpg','static/images/menu/special/sample.jpg','static/images/menu/special/sample.jpg','static/images/menu/special/sample.jpg'))

  insert_special(('Special 3','Special 3 description','Special 3 ingredients','static/images/menu/special/sample.jpg','static/images/menu/special/sample.jpg','static/images/menu/special/sample.jpg','static/images/menu/special/sample.jpg'))
  print(select_table('*','SPECIAL'))

  print("Bill  ------- ",get_bill_values(1,3))
  
  '''
  print('----------------Fromat orders : ',format_orders())
  print("--------HOMEDELIVERY",select_table('*','HOMEDELIVERY'))
  order_cancelled('ADMIN')
  print("--------HOMEDELIVERY",select_table('*','HOMEDELIVERY'))
  print('---------------Reservation : ', get_reservation())
  reservation_occupied('ADMIN')
  print('---------------Reservation : ', get_reservation())
  reservation_expired('ADMIN')
  print('---------------Reservation : ', get_reservation())
  '''
  close_connection(con)
  print("====================Debug info ended========================")

#debugger()
print('==================================')
print('| Database manager has ended.... |')
print('==================================')
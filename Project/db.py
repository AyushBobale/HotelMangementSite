import dbmanager
import config


config = config.Config()
generator = open(config.GENERATOR)
connection = dbmanager.create_connection(config.CURRENTDATABASE)
cursor = connection.cursor() 
lines = generator.readlines()
joinedline = ''
for line in lines:
  if line != '\n':
    joinedline = joinedline + line
  else:
    #print('Executing :', joinedline)
    cursor.execute(joinedline)
    #print('-----------------------')
    joinedline = ''
    continue

tablenames = ['USERID','USER','RESERVATION','MENU','HOMEDELIVERY','FEEDBACK','EMPLOYEE','SPECIAL']


def table_columns(db, table_name):
  curs = db.cursor()
  sql = "select * from %s where 1=0;" % table_name
  curs.execute(sql)
  return [d[0] for d in curs.description]

def print_tables(tablenames):
  for tablename in tablenames:
    print("\n\nTable : ",tablename)
    print(table_columns(connection,tablename))
    sql1 = "SELECT * FROM " + tablename
    rows = cursor.execute(sql1)
    for row in rows:
      print(row)
      
print_tables(tablenames)



connection.commit()
generator.close()
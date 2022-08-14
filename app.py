from flask import Flask
from flask import render_template
import socket
import mysql.connector
import os

app = Flask(__name__)

DB_Host = os.environ.get('DB_Host') or "localhost"
DB_Database = os.environ.get('DB_Database') or "mysql"
DB_User = os.environ.get('DB_User') or "root"
DB_Password = os.environ.get('DB_Password') or "paswrd"

#Added to read evnironment variables of IMG_URL, Name and Bucket
image_url=os.environ.get('IMG_URL') 
my_name=os.environ.get('Name')
s3_bucket = os.environ.get('Bucket')

#Command to read all the files in S3 bucket
cmd= 'aws s3 cp s3://'+s3_bucket+'/  static/  --recursive'
#Added aws S3 command and it's output for better debugging
print(cmd + "\n\tThe Output:\n")

os.system(cmd)

#To add the log message with full details:
cnts="\nBackground Image URL: \n" +  image_url

print ("\nLOGS:" + cnts+"\n")

#To get the image name from the passed URL
image = image_url.split('/')
image=image[-1]

@app.route("/")
def main():
    db_connect_result = False
    err_message = ""
    try:
        mydb=mysql.connector.connect(host=DB_Host, database=DB_Database, user=DB_User, password=DB_Password)
        color = '#39b54b'
        db_connect_result = True
        #Added logic to create a table and insert a record whenever the page is fetched 
        mycursor = mydb.cursor()
        mycursor.execute("CREATE TABLE IF NOT EXISTS LOGS ( \
                            ID INT auto_increment, \
                            Image_Name VARCHAR(255), \
                            Time_Stamp TIMESTAMP,  \
                            Image_URL VARCHAR(255), \
                            primary key (id) ); ")
                            
          
        sql = "INSERT INTO LOGS (Image_Name, Time_Stamp, Image_URL) VALUES (%s,CURRENT_TIMESTAMP,%s)"
        val = (image,image_url)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
    except Exception as e:
        color = '#ff3f3f'
        err_message = str(e)

    return render_template('hello.html', debug="Environment Variables: DB_Host=" + (os.environ.get('DB_Host') or "Not Set") + "; DB_Database=" + (os.environ.get('DB_Database')  or "Not Set") + "; DB_User=" + (os.environ.get('DB_User')  or "Not Set") + "; DB_Password=" + (os.environ.get('DB_Password')  or "Not Set") + "; " + err_message, db_connect_result=db_connect_result, name=socket.gethostname(), color=color,image_s=image,  my_name=my_name , contents=cnts)

#Added logs pags to show the output of the slect query from the mysql database
@app.route("/logs")
def logs():
    db_connect_result = False
    err_message = ""
    logs_table="<tr> <td> ID </td> <td> Image_Name </td> <td> Time_Stamp </td> <td> Image_URL </td>"
    try:
        db=mysql.connector.connect(host=DB_Host, database=DB_Database, user=DB_User, password=DB_Password)
        color = '#453f3f'
        db_connect_result = True
        fetchcursor = db.cursor()
        fetchcursor.execute("SELECT * FROM LOGS")
        myresult = fetchcursor.fetchall()
        
            
    except Exception as e:
        color = '#ff3f3f'
        err_message = str(e)
        
    return render_template('hello.html', debug="Environment Variables: DB_Host=" + (os.environ.get('DB_Host') or "Not Set") + "; DB_Database=" + (os.environ.get('DB_Database')  or "Not Set") + "; DB_User=" + (os.environ.get('DB_User')  or "Not Set") + "; DB_Password=" + (os.environ.get('DB_Password')  or "Not Set") + "; " + err_message, db_connect_result=db_connect_result, name=socket.gethostname(), color=color,image_s=image,  my_name=my_name , logs=myresult)


@app.route("/debug")
def debug():
    color = '#2196f3'
    return render_template('hello.html', debug="Environment Variables: DB_Host=" + (os.environ.get('DB_Host') or "Not Set") + "; DB_Database=" + (os.environ.get('DB_Database')  or "Not Set") + "; DB_User=" + (os.environ.get('DB_User')  or "Not Set") + "; DB_Password=" + (os.environ.get('DB_Password')  or "Not Set"), color=color,image_s=image,  my_name=my_name, contents=cnts)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)

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
cmd= 'aws s3 cp s3://'+s3_bucket+'/ /opt/webapp-mysql/static --recursive'
os.system(cmd)

#To add the log message with full details:
cnts="\nBackground Image URL: \n" +  image_url

#To get the image name from the passed URL
image = image_url.split('/')
image=image[-1]

@app.route("/")
def main():
    db_connect_result = False
    err_message = ""
    try:
        mysql.connector.connect(host=DB_Host, database=DB_Database, user=DB_User, password=DB_Password)
        color = '#39b54b'
        db_connect_result = True
    except Exception as e:
        color = '#ff3f3f'
        err_message = str(e)

    return render_template('hello.html', debug="Environment Variables: DB_Host=" + (os.environ.get('DB_Host') or "Not Set") + "; DB_Database=" + (os.environ.get('DB_Database')  or "Not Set") + "; DB_User=" + (os.environ.get('DB_User')  or "Not Set") + "; DB_Password=" + (os.environ.get('DB_Password')  or "Not Set") + "; " + err_message, db_connect_result=db_connect_result, name=socket.gethostname(), color=color,image_s=image,  my_name=my_name ,contents=cnts)

@app.route("/debug")
def debug():
    color = '#2196f3'
    return render_template('hello.html', debug="Environment Variables: DB_Host=" + (os.environ.get('DB_Host') or "Not Set") + "; DB_Database=" + (os.environ.get('DB_Database')  or "Not Set") + "; DB_User=" + (os.environ.get('DB_User')  or "Not Set") + "; DB_Password=" + (os.environ.get('DB_Password')  or "Not Set"), color=color,image_s=image,  my_name=my_name, contents=cnts)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)

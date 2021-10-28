from flask import Flask

app = Flask(__name__)



@app.route('/getlocation')
def home():
    return "hello you are in denmark"


app.run()
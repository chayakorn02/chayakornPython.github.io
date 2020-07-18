from flask import Flask,render_template,send_from_directory,session,jsonify,abort,make_response
from Member import *
from User import *
from Api import *
from datetime import timedelta
import os
import json

app = Flask(__name__)
app.secret_key = "chayakorn"
app.permanent_session_lifetime = timedelta(minutes=30)
app.register_blueprint(member)
app.register_blueprint(user)
app.register_blueprint(memberapi)

@app.route("/")
def Index():
    if "username" not in session:
        return render_template("login/login.html",headername="Login")
    else:
        return redirect(url_for('member.Showdatamember'))

@app.route("/creammyzshop")
def Creammyzshop():
    return render_template('/index.html')

#แจ้งหน้า Error 404
@app.errorhandler(404)
def not_found(error):
    return redirect(url_for("notfound"))

@app.route("/notfound")
def notfound():
    return render_template('error/error.html')

#ป้องกันการขโมยรูปภาพ
@app.route('/static/images/<filename>')
def protect(filename):
    if "username" not in session:
        return "Not Allowed"
    return send_from_directory("static/images",filename)




if __name__ == '__main__':
    app.run(debug = True,host="0.0.0.0",port=5000)

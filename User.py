from flask import Blueprint,render_template,request,redirect,url_for,session,flash
import pymysql
from config import *
con = pymysql.connect(HOST,USER,PASS,DATABASE)
user = Blueprint('user',__name__)


@user.route("/loginpage")
def Loginpage():
    if "username" not in session:
        return render_template("login/login.html",headername="Login")
    else:
        return redirect(url_for('member.Showdatamember'))

@user.route("/checklogin",methods=["POST"])
def Checklogin():
    username = request.form['username']
    password = request.form['password']
    with con:
        cur = con.cursor()
        sql = "SELECT * FROM tb_user WHERE user_username = %s AND user_password = %s and user_status = 1"
        cur.execute(sql,(username,password))
        rows = cur.fetchall()
        print("rows in data login =" + str(len(rows)))
    if len(rows) > 0:
        session['username'] = username
        session['fname'] = rows[0][1]
        session['lname'] = rows[0][2]
        session.permanent = True
        print(session)
        return redirect(url_for('member.Showdatamember'))
    else:
        flash("Not found data")
        return render_template('login/login.html',headername="Login")

@user.route("/logout")
def Logout():
    session.clear()
    print(session)
    return redirect(url_for('user.Loginpage'))

@user.route("/regisuser")
def Regisuser():
    return render_template('User/adduser.html',headername="Register User")

@user.route("/adduser",methods=["POST"])
def Adduser():
    if request.method == "POST":
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['repassword']
# เช็คข้อมูล username ซ้ำ
        with con:
            cur = con.cursor()
            sql = "SELECT * FROM tb_user WHERE user_username = %s"
            cur.execute(sql,(username))
            rows = cur.fetchall()
            if len(rows) >0:
                flash("Username Duplicated")
                return render_template('User/adduser.html',headername="Register Member")
        if password != repassword:
            flash("Repassword Wrong")
            return render_template('User/adduser.html',headername="Register Member")
        with con:
            cur = con.cursor()
            sql = "insert into tb_user (user_fname,user_lname,user_username,user_password) values(%s,%s,%s,%s)"
            cur.execute(sql,(fname,lname,username,password))
            con.commit()
            flash("Register Finish Pless Wait")
            return render_template('login/login.html',headername="Register Member",status="wait")

#เพิ่มตารางและหน้าแก้ไขสเตตัส user
@user.route("/showuser")
def Adduserstatus():
    if "username" not in session:
        return render_template("login/login.html",headername="Login")
    with con:
        cur = con.cursor()
        sql = "SELECT * FROM tb_user"
        cur.execute(sql)
        rows = cur.fetchall()
        print(rows)
    return render_template("User/showdauser.html",headername="Add user status",datas=rows)

#ฟังชั่นเชื่อมกับ Showdauser เพื่อแก้ไขสเตตัส user
@user.route("/edituser",methods=["POST"])
def Edituser():
    if request.method == "POST":
        idtbUser = int(request.form["id"])
        userfname = request.form["userfname"]
        userlname = request.form["userlname"]
        username = request.form["username"]
        password = request.form["userpassword"]
        with con:
            cur = con.cursor()
            # sql = "SELECT * FROM tb_user"
            # sql = "update tb_user set user_fname = 'creammy233333', user_lname = 'naja', user_username = 'creammy1234', user_password = '123456' where user_id = 2"
            sql = "update tb_user set user_fname = %s, user_lname = %s, user_username = %s, user_password = %s where user_id = %s"
            cur.execute(sql,(userfname,userlname,username,password,idtbUser))
            con.commit()
            rows = cur.fetchall()
            print(rows)
        return redirect(url_for('user.Adduserstatus'))
        #(url_for('user.Adduserstatus')) คือการเรียกฟังชั่นให้ลิงค์กับด้านบน

@user.route("/deletuser",methods=["POST"])
def Delelteuser():
    if request.method == "POST":
        id = request.form["id"]
        with con:
            cur = con.cursor()
            sql = "delete from tb_user where user_id = %s"
            cur.execute(sql,(id))
            con.commit()
            return redirect(url_for('user.Adduserstatus'))

@user.route("/approve",methods=["POST"])
def testsss():
    if request.method == "POST":
         idtbUser = request.form["testttt"]

from flask import Blueprint,render_template,request,redirect,url_for,session,jsonify,abort,make_response
import pymysql
from config import *
import os
import json
from flask_paginate import Pagination, get_page_args
import pdfkit

con = pymysql.connect(HOST,USER,PASS,DATABASE)

member = Blueprint('member',__name__)

@member.route("/showmember")
def Showdatamember():
        if "username" not in session:
            return render_template("login/login.html",headername="Login")
        con.connect()
        cur = con.cursor()
        cur.execute("SELECT * FROM tb_member")
        rows = cur.fetchall()
        users = list(range(len(rows)))
        total = len(rows)
        page,per_page,offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
        getuser = users[offset:offset+10]
        pagination_users = getuser
        pagination = Pagination(page=page,per_page=per_page,total=total,css_framework='bootstrap4')
        return render_template("Member/showdatamember.html",headername="Data Member",datas=rows,users=pagination_users,page=page,per_page=per_page,pagination=pagination,len=total)

#เลือกข้อมูลจากวันเกิด
@member.route("/showwithdate",methods=["POST"])
def Showwithdate():
    if "username" not in session:
        return render_template("login/login.html",headername="Login")
    if request.method == "POST":
        dtstart = request.form['dtstart']
        dtend = request.form['dtend']
        with con:
            cur = con.cursor()
            sql = "SELECT * FROM tb_member where mem_birthdate between %s and %s"
            cur.execute(sql,(dtstart,dtend))
            rows = cur.fetchall()
            print(rows)
            return render_template("Member/showdatamember.html",headername="Data Member",datas=rows)

#เลือกข้อมูลจากชื่อ
@member.route("/showsearch",methods=["POST"])
def Showsearch():
    if "username" not in session:
        return render_template('login/login.html',headername="Login")
    with con:
        if request.method == "POST":
            KeySearch = request.form['searchname']
            likeString = "%" + KeySearch +"%"
            cur = con.cursor()
            sql = "SELECT * FROM tb_member where mem_fname like %s or mem_lname like %s"
            cur.execute(sql,(likeString,likeString))
            rows = cur.fetchall()
            cur.close()
            return render_template("Member/showdatamember.html",headername="Data Member",datas=rows)

#เลือกข้อมูลจากเพศ
@member.route("/showwithsex",methods=["POST"])
def Showwithsex():
    if "username" not in session:
        return render_template("login.html",headername="Login")
    if request.method == "POST":
        male = request.form["sex"]
        female = request.form["sex"]
        with con:
            cur = con.cursor()
            sql = "SELECT * FROM tb_member where mem_sex between %s and %s"
            cur.execute(sql,(male,female))
            rows = cur.fetchall()
            print(rows)
            return render_template("Member/showdatamember.html",headername="Data Member",datas=rows)

#ฟังชั่น edit data
@member.route("/editmember",methods=["POST"])
def Editmember():
    if request.method == "POST":
        id = request.form["id"]
        fname = request.form["fname"]
        lname = request.form["lname"]
        sex = request.form["sex"]
        bdate = request.form["bdate"]
        email = request.form["email"]
        file = request.files['files']
        if file.filename == "":
            with con:
                #update with no pic
                cur = con.cursor()
                sql = "update tb_member set mem_fname = %s, mem_lname = %s, mem_sex = %s, mem_birthdate = %s, mem_email = %s where mem_id = %s"
                cur.execute(sql,(fname,lname,sex,bdate,email,id))
                con.commit()
                return redirect(url_for('member.Showdatamember'))
        else:
            #update with pic
            file = request.files['files']
            upload_folder = 'static/images'
            app_folder = os.path.dirname(__file__)
            img_folder = os.path.join(app_folder,upload_folder)
            file.save(os.path.join(img_folder,file.filename))
            path = upload_folder + "/" + file.filename
            with con:
                cur = con.cursor()
                sql = "update tb_member set mem_fname = %s, mem_lname = %s, mem_sex = %s, mem_birthdate = %s, mem_email = %s, mem_pic = %s where mem_id = %s"
                cur.execute(sql,(fname,lname,sex,bdate,email,path,id))
                con.commit()
                return redirect(url_for('member.Showdatamember'))

@member.route("/deletemember",methods=["POST"])
def Deleltemember():
    if request.method == "POST":
        id = request.form["id"]
        with con:
            cur = con.cursor()
            sql = "delete from tb_member where mem_id = %s"
            cur.execute(sql,(id))
            con.commit()
            return redirect(url_for('member.Showdatamember'))

# ระบุ url
@member.route("/adddatamember")
def Adddatamember():
    if "username" not in session:
        return render_template("login/login.html",headername="Login")
    return render_template("Member/adddatamember.html",headername="Add Data")


# ฟังชั่น addatamember
@member.route("/adddata",methods=["POST"])
def Adddata():
    if request.method == "POST":
        file = request.files['files']
        upload_folder = 'static/images'
        app_folder = os.path.dirname(__file__)
        img_folger = os.path.join(app_folder,upload_folder)
        file.save(os.path.join(img_folger,file.filename))
        path = upload_folder + "/" + file.filename
        print(path)
#^^^^^^^^upload pic ไป 'static/images' VVVVVVVV เพิ่ม filed mem_pic
        fname = request.form["fname"]
        lname = request.form["lname"]
        sex = request.form["sex"]
        bdate = request.form["bdate"]
        email = request.form["email"]
        with con:
            cur = con.cursor()
            sql = "insert into tb_member(mem_fname,mem_lname,mem_sex,mem_birthdate,mem_email,mem_pic) VALUES (%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,(fname,lname,sex,bdate,email,path))
            con.commit()
            return redirect(url_for('member.Showdatamember'))

##################### report ############################
@member.route("/report",methods=["POST"])
def Report():
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
    if request.method == "POST":
            sex = request.form['sex']
            cur = con.cursor()
            sql = "SELECT * FROM tb_member where mem_sex = %s"
            cur.execute(sql,(sex))
            rows = cur.fetchall()
            cur.close()
            render = render_template('member/showreport.html',datas=rows,headername="Name List",sum=len(rows))
            pdf = pdfkit.from_string(render,False,configuration=config)
            response = make_response(pdf)
            response.headers['content-Type'] ='application/pdf'
            response.headers['content-Disposition'] = 'attachment; filename=myreport.pdf'
            return response
            # """ with con:
            #     cur = con.cursor()
            #     sql = "SELECT * FROM tb_member"
            #     cur.execute(sql)
            #     rows = cur.fetchall()
            #     cur.close()
            #     render = render_template('member/showreport.html',datas=rows,headername="Name List",sum=len(rows))
            #     pdf = pdfkit.from_string(render,False,configuration=config)
            #     response = make_response(pdf)
            #     response.headers['content-Type'] ='application/pdf'
            #     response.headers['content-Disposition'] = 'attachment; filename=myreport.pdf'
            #     return response """





# #ระบุ url กลับไปData member
# @member.route("/showmember")
# def Backtomain():
#     with con:
#         cur = con.cursor()
#         sql = "SELECT * FROM tb_member"
#         cur.execute(sql)
#         rows = cur.fetchall()
#         print(rows)
#         return render_template("showdatamember.html",headername="Data Member",datas=rows)
#
# # #ระบุ url กลับไปหน้าเดิม
# # @member.route("/127.0.0.1:5000/")
# # def Backtohomepage():
# #     return render_template("/")

from flask import Blueprint,render_template,request,redirect,url_for
from pymongo import MongoClient
from .db import eduQua_collection

app_form=Blueprint('app_form',__name__)

@app_form.route('/page3',methods=['GET','POST'])
def page3():
    return render_template("page3.html")

@app_form.route('/submit',methods=['POST'])
def eduQua_form():
    if request.method=='POST':
        data={
            "10th_standard":{
                "course":request.form.get("course"),
                "board_university":request.form.get("board_university"),
                "college_name":request.form.get("college_name"),
                "year_from":request.form.get("year_from"),
                "year_to": request.form.get("year_to"),
                "grade": request.form.get("grade")
            },
            "12th_standard": {
                "course": request.form.get("course"),
                "board_university": request.form.get("board_university"),
                "college_name": request.form.get("college_name"),
                "year_from": request.form.get("year_from"),
                "year_to": request.form.get("year_to"),
                "grade": request.form.get("grade")
            },
            "graduation": {
                "course": request.form.get("course"),
                "board_university": request.form.get("board_university"),
                "college_name": request.form.get("college_name"),
                "year_from": request.form.get("year_from"),
                "year_to": request.form.get("year_to"),
                "grade": request.form.get("grade")
            },
            "post_graduation": {
                "course": request.form.get("course"),
                "board_university": request.form.get("board_university"),
                "college_name": request.form.get("college_name"),
                "year_from": request.form.get("year_from"),
                "year_to": request.form.get("year_to"),
                "grade": request.form.get("grade")
            },
            "others": {
                "course": request.form.get("course"),
                "board_university": request.form.get("board_university"),
                "college_name": request.form.get("college_name"),
                "year_from": request.form.get("year_from"),
                "year_to": request.form.get("year_to"),
                "grade": request.form.get("grade")
            }
        }
    eduQua_collection.insert_one(data)
    return redirect(url_for('app_form.page3'))
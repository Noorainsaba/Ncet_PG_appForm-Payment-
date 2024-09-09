from flask import Blueprint,render_template,request,redirect,url_for
from pymongo import MongoClient
from .db import eduQua_collection,page2_collection

app_form=Blueprint('app_form',__name__)

@app_form.route('/page3',methods=['GET','POST'])
def page3():
    return render_template("page3.html")

@app_form.route('/page2',methods=['GET','POST'])
def page2():
    return render_template("page2.html")

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

@app_form.route('/page2_submit', methods=['POST'])
def page2_submit():
    form_data = {
        "admission_type": request.form.get("admission_type"),
        "pgcet_no": request.form.get("pgcet_no"),
        "admission_order_no": request.form.get("admission_order_no"),
        "rank": request.form.get("rank"),
        "claimed_category": request.form.get("claimed_category"),
        "allocated_category": request.form.get("allocated_category"),
        "locality": request.form.get("admission_type"),
        "first_name": request.form.get("first_name"),
        "middle_name": request.form.get("middle_name"),
        "surname": request.form.get("surname"),
        "dob": request.form.get("dob"),
        "gender": request.form.get("gender"),
        "nationality": request.form.get("nationality"),
        "religion": request.form.get("religion"),
        "blood_group": request.form.get("blood_group"),
        "physically_challenged": request.form.get("physically_challenged"),
        "category": request.form.get("category"),
        "aadhaar_no": request.form.get("aadhaar_no"),
        "father_name": request.form.get("father_name"),
        "mother_name": request.form.get("mother_name"),
        "father_occupation": request.form.get("father_occupation"),
        "mother_occupation": request.form.get("mother_occupation"),
        "father_phone": request.form.get("father_phone"),
        "mother_phone": request.form.get("mother_phone"),
        "correspondence_city": request.form.get("correspondence_city"),
        "correspondence_pincode": request.form.get("correspondence_pincode"),
        "correspondence_state": request.form.get("correspondence_state"),
        "correspondence_country": request.form.get("correspondence_country"),
        "correspondence_tel": request.form.get("correspondence_tel"),
        "correspondence_mobile": request.form.get("correspondence_mobile"),
        "permanent_city": request.form.get("permanent_city"),
        "permanent_pincode": request.form.get("permanent_pincode"),
         "permanent_state": request.form.get("permanent_state"),
        "permanent_country": request.form.get("permanent_country"),
        "permanent_tel": request.form.get("permanent_tel"),
        "permanent_mobile": request.form.get("permanent_mobile"),
        "preferred_contact_time": request.form.get("preferred_contact_time"),
        "passport": request.form.get("passport"),
        "passport_no": request.form.get("passport_no"),
        "passport_expiry": request.form.get("passport_expiry"),
        "passport_issued_on": request.form.get("passport_issued_on"),
    }

    page2_collection.insert_one(form_data)

    return "Form submitted successfully!"

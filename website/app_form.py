from flask import Blueprint,render_template,request,redirect,url_for,session,flash
from pymongo import MongoClient
from .db import page2_collection,page1_collection,page3_collection

# pdf imports
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from flask import send_file,jsonify
import json
from bson import ObjectId
import re

app_form=Blueprint('app_form',__name__)


# @app_form.route('/page1', methods=['POST','GET'])
# def page1():
#     if 'signin' not in session or not session['signin']:
#         return redirect(url_for('auth.signin'))
    
#     if request.method=='POST':
#         name = request.form['name']
#         email = request.form['email']
#         age = request.form.get('age', type=int)
#         message = request.form['message']

#         # temporarily storing data,even after user clicks back option from the popup
#         session['page1_data']={
#             'name':name,
#             'email':email,
#             'age':age,
#             'message':message
#         }

#         contact_data = {
#             "application_number":session.get("application_number"),
#             'name': name,
#             'email': email,
#             'age': age,
#             'message': message
#         }

#         # Insert data into MongoDB
#         try:
#             page1_collection.insert_one(contact_data)
#             session['progress']['page1']=True
#             session.modified = True
#             return redirect(url_for('app_form.page2'))
#         except ConnectionError as e:
#             flash(f"Error connecting to MongoDB: {e}")
#             return redirect(url_for('app_form.page1'))
        
    
#     page1_data=session.get('page1_data',{})
#     return render_template('page1.html',page1_data=page1_data)

@app_form.route('/page1', methods=['POST', 'GET'])
def page1():
    if 'signin' not in session or not session['signin']:
        return redirect(url_for('auth.signin'))
    if request.method == 'POST':
        candidate_name = request.form.get('candidateName')
        documents = request.form.getlist('documents')
        other_documents = request.form.get('other_documents')

        form_data = {
            "application_number": session.get('application_number'),
            "candidate_name": candidate_name,
            "documents": documents,
            "other_documents": other_documents
        }

        try:
            page1_collection.insert_one(form_data)
            session['progress']['page1']=True
            session.modified = True
            return redirect(url_for('app_form.page2'))
        except ConnectionError as e:
            flash(f"Error Submitting data,Please try again!: {e}")
            return redirect(url_for('app_form.page1'))
        
    return render_template('page1.html')

@app_form.route('/page2', methods=['POST','GET'])
def page2():
    if 'signin' not in session or not session['signin']:
        return redirect(url_for('auth.signin'))
    if not session['progress']['page1']:
        return redirect(url_for('app_form.page1'))
    if request.method=='POST':
        application_number=session.get("application_number")
        admission_type=request.form.get("admission_type")
        pgcet_no=request.form.get("pgcet_no")
        admission_order_no=request.form.get("admission_order_no")
        rank=request.form.get("rank")
        claimed_category=request.form.get("claimed_category")
        allocated_category=request.form.get("allocated_category")
        locality=request.form.get("admission_type")
        first_name=request.form.get("first_name")
        middle_name=request.form.get("middle_name")
        surname=request.form.get("surname")
        dob=request.form.get("dob")
        gender=request.form.get("gender")
        nationality=request.form.get("nationality")
        religion=request.form.get("religion")
        blood_group=request.form.get("blood_group")
        physically_challenged=request.form.get("physically_challenged")
        category=request.form.get("category")
        aadhaar_no=request.form.get("aadhaar_no")
        father_name=request.form.get("father_name")
        mother_name=request.form.get("mother_name")
        father_occupation=request.form.get("father_occupation")
        mother_occupation=request.form.get("mother_occupation")
        father_phone=request.form.get("father_phone")
        mother_phone=request.form.get("mother_phone")
        correspondence_city=request.form.get("correspondence_city")
        correspondence_pincode=request.form.get("correspondence_pincode")
        correspondence_state=request.form.get("correspondence_state")
        correspondence_country=request.form.get("correspondence_country")
        correspondence_tel=request.form.get("correspondence_tel")
        correspondence_mobile=request.form.get("correspondence_mobile")
        permanent_city=request.form.get("permanent_city")
        permanent_pincode=request.form.get("permanent_pincode")
        permanent_state=request.form.get("permanent_state")
        permanent_country=request.form.get("permanent_country")
        permanent_tel=request.form.get("permanent_tel")
        permanent_mobile=request.form.get("permanent_mobile")
        preferred_contact_time=request.form.get("preferred_contact_time")
        passport=request.form.get("passport")
        passport_no=request.form.get("passport_no")
        passport_expiry=request.form.get("passport_expiry")
        passport_issued_on=request.form.get("passport_issued_on")



        form_data = {
            "application_number": str(application_number) if isinstance(application_number, ObjectId) else application_number,
            "admission_type":admission_type ,
            "pgcet_no":pgcet_no,
            "admission_order_no": admission_order_no,
            "rank": rank,
            "claimed_category":claimed_category ,
            "allocated_category":allocated_category ,
            "locality": locality,
            "first_name": first_name,
            "middle_name":middle_name ,
            "surname": surname,
            "dob":dob ,
            "gender": gender,
            "nationality":nationality ,
            "religion": religion,
            "blood_group":blood_group ,
            "physically_challenged":physically_challenged ,
            "category":category ,
            "aadhaar_no": aadhaar_no,
            "father_name":father_name,
            "mother_name":mother_name ,
            "father_occupation": father_occupation,
            "mother_occupation": mother_occupation,
            "father_phone": father_phone,
            "mother_phone":mother_phone ,
            "correspondence_city":correspondence_city ,
            "correspondence_pincode":correspondence_pincode ,
            "correspondence_state":correspondence_state,
            "correspondence_country":correspondence_country ,
            "correspondence_tel": correspondence_tel,
            "correspondence_mobile":correspondence_mobile,
            "permanent_city": permanent_city,
            "permanent_pincode":permanent_pincode ,
            "permanent_state": permanent_state,
            "permanent_country": permanent_country,
            "permanent_tel": permanent_tel,
            "permanent_mobile":permanent_mobile ,
            "preferred_contact_time":preferred_contact_time ,
            "passport": passport,
            "passport_no": passport_no,
            "passport_expiry":passport_expiry ,
            "passport_issued_on": passport_issued_on
        }
        # session['page2_data']=form_data
        # session.modified=True

        try:
            page2_collection.insert_one(form_data)
            session['progress']['page2']=True
            session.modified = True
            return redirect(url_for('app_form.page3'))
        except ConnectionError as e:
            flash(f"Error connecting to MongoDB: {e}")
            return redirect(url_for('app_form.page2'))
        

    # page2_data=session.get('page2_data',{})
    return render_template('page2.html')


@app_form.route('/page3',methods=['POST','GET'])
def page3():
    if 'signin' not in session or not session['signin']:
        return redirect(url_for('auth.signin'))
    if not session['progress']['page2']:
        return redirect(url_for('app_form.page2'))
    if request.method=='POST':
        # save_button=request.form.get('save',None)
        try:
            education_data ={
                "10th_standard":{
                    "course":request.form.get("course_10"),
                    "board_university":request.form.get("board_university_10"),
                    "college_name":request.form.get("college_name_10"),
                    "year_from":request.form.get("year_from_10"),
                    "year_to": request.form.get("year_to_10"),
                    "grade": request.form.get("grade_10")
                },
                "12th_standard": {
                    "course": request.form.get("course_12"),
                    "board_university": request.form.get("board_university_12"),
                    "college_name": request.form.get("college_name_12"),
                    "year_from": request.form.get("year_from_12"),
                    "year_to": request.form.get("year_to_12"),
                    "grade": request.form.get("grade_12")
                },
                "graduation": {
                    "course": request.form.get("course_ug"),
                    "board_university": request.form.get("board_university_ug"),
                    "college_name": request.form.get("college_name_ug"),
                    "year_from": request.form.get("year_from_ug"),
                    "year_to": request.form.get("year_to_ug"),
                    "grade": request.form.get("grade_ug")
                },
                "post_graduation": {
                    "course": request.form.get("course_pg"),
                    "board_university": request.form.get("board_university_pg"),
                    "college_name": request.form.get("college_name_pg"),
                    "year_from": request.form.get("year_from_pg"),
                    "year_to": request.form.get("year_to_pg"),
                    "grade": request.form.get("grade_pg")
                },
                "others": {
                    "course": request.form.get("course_ot"),
                    "board_university": request.form.get("board_university_ot"),
                    "college_name": request.form.get("college_name_ot"),
                    "year_from": request.form.get("year_from_ot"),
                    "year_to": request.form.get("year_to_ot"),
                    "grade": request.form.get("grade_ot")
                }
            }
            work_experience_data = {
                'work_experience': request.form.get('work_experience'),
                'total_years': request.form.get('total_years'),
                'work_from': request.form.get('work_from'),
                'work_to': request.form.get('work_to'),
                'organization': request.form.get('organization'),
                'awards': request.form.get('awards'),
                'interests': request.form.get('interests'),
            }

            finance_data = {
                'family_income': request.form.get('family_income'),
                'finance_source': request.form.getlist('finance_source'),
            }

            entrance_test_data = {
                'entrance_test': request.form.getlist('entrance_test'),
                'other_tests_specify': request.form.get('other_tests_specify'),
                'test_score': request.form.get('test_score'),
                'registration_no': request.form.get('registration_no'),
                'exam_date': request.form.get('exam_date'),
                'no_exams': 'no_exams' in request.form,
            }

            # Combine all data into a single document
            form_data = {
                "application_number":session.get("application_number"),
                'education': education_data,
                'work_experience': work_experience_data,
                'finance': finance_data,
                'entrance_tests': entrance_test_data,
            }
            

            # Insert data into MongoDB collection
            try:
                page3_collection.insert_one(form_data)
                session['progress']['page3']=True
                session.modified = True
                return redirect(url_for('app_form.page4'))
            except Exception as e:
                flash('Error While submitting the data, Please try again!',e)
                return redirect(url_for('app_form.page3'))
        except Exception as e:
            flash('Error While submitting the data, Please try again!',e)
            return redirect(url_for('app_form.page3'))
    
    # page2_data=session.get('page2_data',{})
    return render_template("page3.html")

@app_form.route('/page4',methods=['GET'])
def page4():
    if not session['progress']['page3']:
        return redirect(url_for('app_form.page2'))
    if 'signin' not in session or not session['signin']:
        return redirect(url_for('auth.signin'))
    return render_template("page4.html")

# def generate_pdf(data):
#     # Create a byte stream buffer to hold the PDF data
#     pdf_buffer = io.BytesIO()

#     # Create a PDF canvas
#     pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
#     pdf.setTitle('Application Data PDF')

#     # Add data to the PDF
#     pdf.drawString(100, 750, 'Application Data Summary:')
    
#     y_position = 720
#     for collection_name, collection_data in data.items():
#         pdf.drawString(100, y_position, f'{collection_name}: {str(collection_data)}')
#         y_position -= 20  # Move down for the next line

#     # Save the PDF
#     pdf.save()

#     # Move the buffer cursor to the beginning
#     pdf_buffer.seek(0)

#     return pdf_buffer

def convert_objectid_to_str(data):
    if isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_objectid_to_str(value) for key, value in data.items()}
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data

@app_form.route('/fetch_data',methods=['POST'])
def fetch_data():
    application_number=request.form.get('application_number')

    page1_data=page1_collection.find_one({'application_number':application_number})
    page2_data=page2_collection.find_one({'application_number':application_number})
    page3_data=page3_collection.find_one({'application_number':application_number})

    entireForm_data={
        'page1_data':page1_data,
        'page2_data':page2_data,
        'page3_data':page3_data
    }

    entireForm_data = convert_objectid_to_str(entireForm_data)

    # Create a PDF
    pdf_buffer = io.BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
    pdf.setTitle('Form Preview')

    # Add content to the PDF
    text = pdf.beginText(40, 750)  # Start position (x, y)
    text.setFont("Helvetica", 12)

    for page, data in entireForm_data.items():
        text.textLine(f"{page.capitalize()}:")
        for key, value in data.items():
            text.textLine(f"{key}: {value}")
        text.textLine(" ")

    pdf.drawText(text)
    pdf.showPage()
    pdf.save()

    pdf_buffer.seek(0)  # Move to the beginning of the BytesIO buffer

    # Send the PDF to be previewed in the browser
    return send_file(pdf_buffer, as_attachment=True, download_name='form_preview.pdf', mimetype='application/pdf')

@app_form.route('/pdf_generator',methods=['GET'])
def pdf_generator():
    return render_template("pdf_generator.html")

# @app_form.route('/download_pdf',methods=['POST'])
# def download_pdf():
#     data_json=request.form.get('data')
#     if not data_json:
#         flash("No data provided to download", 400)
#         return '', 400

#     try:
#         data = json.loads(data_json)
#     except (TypeError, json.JSONDecodeError) as e:
#         flash(f"Invalid data format: {e}", 400)
#         return '', 400

#     print(data)
#     # generate pdf
#     pdf_buffer=generate_pdf(data)

#     return send_file(pdf_buffer,as_attachment=True,download_name='NCET_PG_Application_form.pdf',mimetype='application/pdf')

    
@app_form.route('/preview', methods=['POST'])
def preview():
    application_number = request.form.get('application_number')
    return render_template('preview.html', application_number=application_number)


# @app_form.route('/section1', methods=['GET', 'POST'])
# def section1():
#     if request.method == 'POST':
#         # Process the form data for Section 1
#         # ...

#         # Update completion status
#         session['completed_steps'] = [1]  # Mark section 1 as completed
#         return redirect(url_for('auth.home'))

#     return render_template('section1.html')

# @app_form.route('/section2', methods=['GET', 'POST'])
# def section2():
#     # Ensure Section 1 is completed before proceeding
#     if 1 not in session.get('completed_steps', []):
#         return redirect(url_for('home'))

#     if request.method == 'POST':
#         # Process the form data for Section 2
#         # ...

#         # Update completion status
#         session['completed_steps'].append(2)  # Mark section 2 as completed
#         return redirect(url_for('auth.home'))

#     return render_template('section2.html')


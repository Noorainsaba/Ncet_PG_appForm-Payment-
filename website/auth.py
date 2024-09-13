from flask import Blueprint, render_template, request,redirect,url_for,flash,session,jsonify
from werkzeug.security import generate_password_hash,check_password_hash
import re
from .db import users_collection,counters_collection,temp_users_collection
from functools import wraps
from flask_mail import *
from flask_mail import Mail
import random
import time
mail=Mail()
auth=Blueprint('auth',__name__)

@auth.route('/')
def LandingPage():
    return render_template('LandingPage.html')


# route protection decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if 'user' not in session:
            flash('You need to signin first.','error')
            return redirect(url_for('auth.signin'))
        return f(*args,**kwargs)#otherwise,allow access to the route
    return decorated_function

def generate_application_number():
    counter=counters_collection.find_one_and_update(
        {"_id":"application_number"},
        {"$inc":{"sequence_value":1}},
        return_document=True
        )
    sequence_number=counter["sequence_value"]
    app_number=f"1NC21CD{sequence_number:03d}"
    return app_number

# @auth.route('/resend_otp',methods=['POST','GET'])
# def resend_otp():
#     email=session.get('email')
#     if not email:
#         return jsonify({'success':False, 'message':'Session expired.Please sign up again.'})
#         # flash('Session expired.Please sign up again.',category='error')
#         # return redirect(url_for('auth.signup'))
#     if 'otp_resend_count' not in session:
#         session['otp_resend_count']=0

#     # fetches unverified user from temporary collection
#     user=temp_users_collection.find_one({'email':email,'email_verified':False})
#     if user:
#         otp=random.randint(100000,999999)
#         session['otp']=otp
#         session['otp_resend_count']+=1

#         # resend limit
#         if session['otp_resend_count']>3:
#             return jsonify({'success':False,'message':'Maximum OTP resend attempts exceeded. Please try again later.'})
#             # flash('Maximum OTP resend attempts exceeded. Please try again later.',category='error')
#             # return redirect(url_for('auth.signup'))
        
#         # resend otp
#         msg=Message('Resend:Ncet PG Application Form OTP',sender='ncet_aks@outlook.com',recipients=[email])
#         msg.body="Hi"+user['name']+"\nYour OTP is: "+str(otp)
#         mail.send(msg)

#         return jsonify({'success':True,'message':'OTP has been resent.'})
#         # flash('OTP has been resent.',category='info')
#         # return render_template('email_verify.html',email=email)
    
#     return jsonify({'success':False,'message':'Error in resending OTP.Please try again.'})
#     # flash('Error in resending OTP. Please try again',category='error')
#     # return redirect(url_for('auth.signup'))
@auth.route('/resend_otp', methods=['GET', 'POST'])
def resend_otp():
    email = session.get('email')
    otp_resend_count = session.get('otp_resend_count', 0)
    otp_timestamp = session.get('otp_timestamp')

    if not email:
        flash('Invalid request. Please try again.', category='error')
        return redirect(url_for('auth.signup'))

    if otp_resend_count >= 3:
        flash('You have exceeded the OTP resend limit. Please try again later.', category='error')
        return redirect(url_for('auth.signup'))

    # Check if the previous OTP has expired
    current_time = time.time()
    otp_expiration_time = 300  # OTP validity period in seconds (5 minutes)

    if otp_timestamp and (current_time - otp_timestamp) <= otp_expiration_time:
        flash('You can request a new OTP only after the previous OTP expires.', category='error')
        return redirect(url_for('auth.signup'))

    # Render a confirmation template
    return render_template('confirm_resend_otp.html')


@auth.route('/confirm_resend_otp', methods=['POST'])
def confirm_resend_otp():
    email = session.get('email')
    otp_resend_count = session.get('otp_resend_count', 0)
    otp_timestamp = session.get('otp_timestamp')
    
    # Check if the resend is valid
    if not email:
        flash('Invalid request. Please try again.', category='error')
        return redirect(url_for('auth.signup'))

    if otp_resend_count >= 3:
        flash('You have exceeded the OTP resend limit. Please try again later.', category='error')
        return redirect(url_for('auth.signup'))

    # Check if the previous OTP has expired
    current_time = time.time()
    otp_expiration_time = 300  # OTP validity period in seconds (5 minutes)

    if otp_timestamp and (current_time - otp_timestamp) > otp_expiration_time:
        # OTP expired, allow resend
        otp = random.randint(100000, 999999)
        session['otp'] = otp
        session['otp_timestamp'] = current_time
        session['otp_resend_count'] = otp_resend_count + 1

        msg = Message('Ncet PG Application form email verification', sender='ncet_aks1@outlook.com', recipients=[email])
        msg.body = f"Hi,\nYour new email OTP is: {otp}"

        try:
            mail.send(msg)
            flash('OTP has been resent. Please check your email.', category='info')
            return redirect(url_for('auth.verify_otp'))
        except Exception as e:
            print(f"Error sending email: {e}")
            flash('Error sending email. Please try again.', category='error')
    else:
        flash('You can request a new OTP only after the previous OTP expires.', category='error')

    return redirect(url_for('auth.signup'))



# @auth.route('/verify_otp',methods=['POST','GET'])
# def verify_otp():
#     print("check1")
#     print("Request method:", request.method)
#     if request.method == 'POST':
#         print("Form data:", request.form)
#     else:
#         print("Unexpected request method:", request.method)
#     input_otp=request.form.get('otp')
#     email=session.get('email')
#     if not email:
#         flash('Session expired or invalid request. Please sign up again.', category='error')
#         return redirect(url_for('auth.signup'))
    
#     user=temp_users_collection.find_one({'email':email,'email_verified':False})

#     if user:
#         otp_timestamp=user.get('otp_timestamp',0)
#         otp=user.get('otp',None)

#         # otp expired check(3 mins)
#         if time.time()-otp_timestamp>3*60:
#             flash('OTP expired. Please resend OTP.',category='error')
#             session['otp_resend_count'] = session.get('otp_resend_count', 0) + 1
#             return redirect(url_for('auth.resend_otp'))
        
#         # check if OTP matches
#         if otp and int(input_otp)=='otp':
#             # store users permanently
#             users_collection.insert_one(
#                 {
#                     "name":user['name'],
#                     "email":user['email'],
#                     "password":user['password'],
#                     "application_number":user['application_number'],
#                     "email_verified":True
#                 }
#             )

#             # delete user from temp
#             temp_users_collection.delete_one({'email':email})

#             flash('Email verified successfully!Please sign in',category='success')

#             return redirect(url_for('auth.signin'))
#         else:
#             flash('Invalid OTP,please try again!',category='error')
#             return render_template('email_verify.html',email=email,resend_count=session.get('otp_resend_count',0))
    
#     flash('Session expired or invalid request.Please sign up again.',category='error')
#     return redirect(url_for('auth.signup'))
@auth.route('/verify_otp', methods=['POST'])
def verify_otp():
    entered_otp = request.form.get('otp')
    email = session.get('email')
    otp = session.get('otp')
    otp_timestamp = session.get('otp_timestamp')
    print(otp_timestamp)
    print(email)
    print(otp)
    print(entered_otp)
    if not email or not otp or not otp_timestamp:
        flash('Invalid request. Please try again.', category='error')
        return redirect(url_for('auth.signup'))
    user=temp_users_collection.find_one({'email':email,'email_verified':False})

    if user:
        current_time = time.time()
        # application_number = user.get('application_number')
        otp_expiration_time = 300  # OTP validity period in seconds (5 minutes)

        if current_time - otp_timestamp > otp_expiration_time:
            flash('OTP has expired. Please request a new one.', category='error')
            return redirect(url_for('auth.signup'))
            
        if entered_otp == str(otp):
        # store users permanently
            app_number=generate_application_number()
            session['application_number']=app_number
            users_collection.insert_one(
            {
                "name":user['name'],
                "email":user['email'],
                "password":user['password'],
                "application_number":app_number,
                "email_verified":True
            }
        )

            # delete user from temp
            temp_users_collection.delete_one({'email':email})

            flash('Email verified successfully and Application number is generated!Please sign in',category='success')
            try:
                msg = Message('Application Number | NCET-PG Admissions Gateway', sender='ncet_aks1@outlook.com', recipients=[email])
                msg.body = f"Your Application number for NCET-PG Admissions Gateway is {app_number}."
                mail.send(msg)
            except Exception as e:
                flash(f'error sending mail! {e}') 
            
            return render_template('app_num_popup.html', app_number=app_number)
        else:
            flash('Invalid OTP,please try again!',category='error')
            return redirect(url_for('auth.signup'))
    flash('Session expired or invalid request.Please sign up again.',category='error')
    return redirect(url_for('auth.signup'))

@auth.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        password=request.form.get('password')

        # validating email format
        #  [^@]+: This part ensures that the email has one or more characters before the @ symbol, and the ^ inside the brackets ([]) indicates "any character except @".
        # @: This matches the @ symbol, which is mandatory in every email address.

        # [^@]+: This part again ensures that there is at least one character after the @ symbol but before the ..

        # \.: This matches the dot (.) that typically separates the domain name from the top-level domain (e.g., ".com").

        # [^@]+: This part ensures that there is at least one character after the dot.

        if not re.match(r"[^@]+@[^@]+\.[^@]+",email):
            flash('Invalid email address!',category='error')
            return redirect(url_for('auth.signup'))
        
        # check for email already existing in database
        if users_collection.find_one({'email':email}):
            flash('Email already registered!',category='error')
            return redirect(url_for('auth.signup'))
        
        # otp send bfr storing to db
        otp=random.randint(100000,999999)
        session['otp']=otp
        session['email']=email
        session['otp_resend_count']=0
        session['otp_timestamp'] = time.time()

        # email verification
        # Message->class

        # subject
        msg=Message('Ncet PG Application form email verification',sender='ncet_aks1@outlook.com',recipients=[email])

        # msg body,otp must b string so that it can b written in the body
        msg.body="Hi"+name+"\nYour email OTP is:" +str(otp)

        try:
            mail.send(msg)
        except Exception as e:
            print(f"Error sending email: {e}")
            flash('Error sending email. Please try again.', category='error')
            return redirect(url_for('auth.signup'))


        # temporarily store user to db
        hashed_password=generate_password_hash(password)

        # app_number=generate_application_number()

        # inserting user into the data base
        new_user={
            "name":name,
            "email":email,
            "password":hashed_password,
            "application_number":None,
            "email_verified":False,
            "otp":otp,
            "otp_timestamp":time.time()
        }
        temp_users_collection.insert_one(new_user)
        # session['application_number']=app_number
        
        return render_template('email_verify.html',email=email)
    
        
        # flash('Account created successfully! Please signin.',category='success')
        # # return redirect(url_for('auth.signin'))

        # # redirect with a success query parameter
        # return redirect(url_for('auth.signup',success=True))
    
     # Handle GET request
    # if request.args.get('success') == 'True':
    #     # Retrieve application number from the session
    #     app_number = session.get('application_number')
    #     if app_number:
    #         return render_template('signup.html', show_modal=True)
    #     else:
    #         flash('Application number not found!', category='error')
    #         return redirect(url_for('auth.signup'))
    
    return render_template('signup.html')

@auth.route('/reset_password',methods=['GET','POST'])
def reset_password():
    if request.method=='POST':
        new_password=request.form.get('new_password')
        confirm_password=request.form.get('confirm_password')
        email=session.get('email')

        user=users_collection.find_one({"email":email})
        current_hashed_password=user['password']

        if check_password_hash(current_hashed_password, new_password):
            flash('New password cannot be the same as the current password. Please choose a different password.', category='error')
            return redirect(url_for('auth.reset_password'))
        
        if new_password != confirm_password:
            flash('Passwords do not match. Please try again.', category='error')
            return redirect(url_for('auth.reset_password'))

        hashed_password=generate_password_hash(new_password)

        users_collection.update_one({"email":email},{"$set":{"password":hashed_password}})

        session.pop('email',None)

        flash('Your password has been successfully updated. Please log in with your new password.', category='success')
        return redirect(url_for('auth.signin'))
    return render_template('reset_password.html')

@auth.route('/verify_password_reset_otp',methods=['GET','POST'])
def verify_password_reset_otp():
    if request.method=='POST':
        entered_otp=request.form.get('otp')
        email=session.get('email')
        saved_otp=session.get('otp')
        otp_timestamp=session.get('otp_timestamp')
    
        current_time = time.time()
        if otp_timestamp and (current_time - otp_timestamp) > 300:
            flash('OTP has expired. Please request a new one.', category='error')
            return redirect(url_for('auth.forgot_password'))
        
        if int(entered_otp)==saved_otp:
            session.pop('otp', None)
            session.pop('otp_timestamp', None)
            flash('OTP verified. Please set a new password.', category='success')
            return redirect(url_for('auth.reset_password'))
        else:
            flash('Invalid OTP. Please try again.', category='error')
    return render_template('verify_password_reset_otp.html')

@auth.route('/forgot_password',methods=['GET','POST'])
def forgot_password():
    if request.method=='POST':
        email=request.form.get('email')
        user=users_collection.find_one({'email':email})

        if user:
            otp = random.randint(100000, 999999)
            session['otp'] = otp
            session['email'] = email
            session['otp_timestamp'] = time.time()

            try:
                msg = Message('Password Reset OTP', sender='ncet_aks1@outlook.com', recipients=[email])
                msg.body = f"Your OTP for password reset is {otp}."
                mail.send(msg)
                flash('OTP has been sent to your email. Please check your inbox.', category='info')
                return redirect(url_for('auth.verify_password_reset_otp'))
            except Exception as e:
                flash(f'error sending mail! {e}') 
        else:
            flash('This email is not registered.', category='error')
    return render_template('forgot_password.html')


@auth.route('/verify_application_number_otp',methods=['GET','POST'])
def verify_application_number_otp():
    if request.method=='POST':
        entered_otp=request.form.get('otp')
        email=session.get('email')
        saved_otp=session.get('otp')
        otp_timestamp=session.get('otp_timestamp')

        current_time=time.time()
        if otp_timestamp and (current_time-otp_timestamp)>300:
            flash('OTP has expired.Please request a new one.',category='error')
            return redirect(url_for('auth.forgot_application_number'))
        
        if int(entered_otp)==saved_otp:
            user =users_collection.find_one({"email":email})
            if user:
                application_number=user.get('application_number')

                session.pop('otp',None)
                session.pop('otp_timestamp',None)

                try:
                    msg=Message('Your Application Number', sender='ncet_aks1@outlook.com',recipients=[email])
                    msg.body = f"Hi,\nYour application number is: {application_number}."
                    mail.send(msg)
                    flash('Your application number has been sent to your email.', category='success')
                    return redirect(url_for('auth.signin'))
                except Exception as e:
                    flash(f'Error sending mail! {e}')
                    return redirect(url_for('auth.forgot_application_number'))
            else:
                flash('User not found.',category='error')
                return redirect(url_for('auth.forgot_application_number'))
        else:
            flash('Invalid OTP. Please try again.', category='error')
    return render_template('verify_application_number_otp.html')

@auth.route('/forgot_application_number',methods=['GET','POST'])
def forgot_application_number():
    if request.method=='POST':
        email=request.form.get('email')

        user =users_collection.find_one({"email":email})
        if user:
            otp=random.randint(100000,999999)
            session['otp']=otp
            session['email']=email
            session['otp_timestamp']=time.time()

            try:
                msg=Message('Application Number Retrieval OTP',sender='ncet_aks1@outlook.com',recipients=[email])
                msg.body=f"Your OTP for retrieving the application number is {otp}."
                mail.send(msg)
                flash('OTP sent to your email.Please check your inbox.',category='info')
                return redirect(url_for('auth.verify_application_number_otp'))
            except Exception as e:
                flash(f"Error sending mail! {e}")
                return redirect(url_for('auth.forgot_application_number'))
        else:
            flash('This email is not registered.',category='error')
    return render_template('forgot_application_number.html')
            

@auth.route('/signin',methods=['GET','POST'])
def signin():
    if request.method=='POST':
        app_number=request.form.get('application_number')
        password=request.form.get('password')

        user=users_collection.find_one({"application_number":app_number})

        if user:
            if check_password_hash(user['password'],password):
                # user session
                session['user']=user['name']
                session['application_number']=user['application_number']

                flash(f'Welcome, {user["name"]}!','success')
                return redirect(url_for('auth.home'))
            else:
                flash('Invalid password!','error')
        else:
            flash('Invalid application number!','error')
        
        return redirect(url_for('auth.signin'))#after encountering errors
    return render_template('signin.html')#get request

@auth.route('/signout')
def signout():
    # clearing session
    session.pop('user',None)
    session.pop('application_number',None)

    flash('You have been signed out!','success')
    return redirect(url_for('auth.signin'))

@auth.route('/home')
@login_required
def home():
    if 'user' not in session:
        flash('You need to sign in to access the home page','error')
        return redirect(url_for('auth.signin'))
    
    user_name=session.get('user')
    application_number=session.get('application_number')

    return render_template('home.html',user_name=user_name,application_number=application_number)


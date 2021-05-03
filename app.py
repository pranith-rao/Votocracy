from flask import Flask, flash, render_template, request, redirect,url_for,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from passlib.hash import sha256_crypt
import os
from werkzeug.utils import secure_filename
import re

app = Flask(__name__)
mysql=MySQL(app)

app.config["SECRET_KEY"] = os.urandom(16)                                                                        
app.config['UPLOAD_FOLDER'] = "static/Uploaded_images"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = "voting"
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_UNIX_SOCKET'] =None
app.config['MYSQL_CONNECT_TIMEOUT'] =None
app.config['MYSQL_READ_DEFAULT_FILE'] =None
app.config['MYSQL_USE_UNICODE']=None
app.config['MYSQL_CHARSET']= None
app.config['MYSQL_SQL_MODE'] = None
app.config['MYSQL_CURSORCLASS'] = None


@app.route("/")
def home():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM candidate")
    candidates_Data = cur.fetchall()
    return render_template("index.html",data=candidates_Data)

@app.route("/login_form")
def login_form():
    return render_template("login.html")

@app.route("/register_form")
def register_form():
    return render_template("signup.html")

@app.route("/admin_login")
def admin_login():
    return render_template("admin_login.html")

@app.route("/admin_register")
def admin_register():
    return render_template("admin_signup.html")

@app.route("/add_candidate")
def add_candidate():
    return render_template("add_candidate.html")

@app.route("/update_candidate")
def update_candidate():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM candidate")
    candidates_Data = cur.fetchall()
    return render_template("update_candidate.html",data=candidates_Data)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/fpass_user")
def fpass_user():
    return render_template("fpass_user.html")

@app.route("/fpass_admin")
def fpass_admin():
    return render_template("fpass_admin.html")

@app.route("/userpass_change")
def userpass_change():
    return render_template("userpass_change.html")

@app.route("/candidate")
def candidate():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM candidate")
    candidates_Data = cur.fetchall()
    if 'user' in session:
        cur.execute("SELECT * FROM vote where user_id=%s",(session['user_id'],))
        data=cur.fetchone()
        return render_template("candidate.html",data=candidates_Data,data1=data)
    return render_template("candidate.html",data=candidates_Data)


@app.route("/register", methods=['POST'])
def register():
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails['name']
        dob = userDetails['dob']
        pimage = userDetails['pimage']
        mail = userDetails['mail']
        gender = userDetails['gender']
        phno = userDetails['phno']
        username = userDetails['username']
        pass1 = userDetails['pass1']
        flag = 0
        while True:  
            if (len(pass1)<8):
                flag = -1
                break
            elif not re.search("[a-z]", pass1):
                flag = -1
                break
            elif not re.search("[A-Z]", pass1):
                flag = -1
                break
            elif not re.search("[0-9]", pass1):
                flag = -1
                break
            elif not re.search("[_@$]", pass1):
                flag = -1
                break
            elif re.search("\\s", pass1):
                flag = -1
                break
            else:
                flag = 0
                break
        if flag ==-1:
            flash("Not a Valid Password","error")
            return redirect(url_for("register_form"))
        pass2 = userDetails['pass2']
        if pass1 == pass2:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM users WHERE username=%s",(username,))
            data = cur.fetchone()
            cur.close()
            if data:
                flash("Username already taken","error")
                return redirect(url_for("register_form"))
            else:
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("SELECT * FROM users WHERE email=%s",(mail,))
                mailData = cur.fetchone()
                cur.close()
                if mailData:
                    flash("Email ID is already used by someone","error")
                    return redirect(url_for("register_form"))
                else:
                    if(len(phno) != 10):
                        flash("Please enter a valid phone number","error")
                        return redirect(url_for("register_form"))
                    else:
                        hashpas = sha256_crypt.hash(pass1)
                        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                        cur.execute("INSERT INTO users(name,dob,image,email,gender,phno,username,password)values(%s,%s,%s,%s,%s,%s,%s,%s)",(name,dob,pimage,mail,gender,phno,username,hashpas))
                        mysql.connection.commit()
                        cur.close()
                        flash('Registration Successfull',"success")
                        return redirect(url_for("login_form"))
        else:
            flash("Password didnt match","error")
            return redirect(url_for("register_form"))
    else:
        flash('Some error occured',"error")
        return redirect(url_for("register_form"))

@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        loginDetails = request.form
        username = loginDetails['username']
        password = loginDetails['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE username=%s",(username,))
        username_Data = cur.fetchone()
        if username_Data is None:
            flash('Username not registered',"error")
            return redirect(url_for("login_form"))
        else:
            checkpass = sha256_crypt.verify(password,username_Data['password']) 
            cur.close()
            if username == username_Data['username'] and checkpass == True:
                session['user'] = True
                session['user_username'] = username_Data['username']
                session['user_id'] = username_Data['user_id']
                flash('You were successfully logged in',"success")
                return redirect(url_for("home"))
            else:
                flash('Invalid Credentials',"error")
                return redirect(url_for("login_form"))
    else:
        flash('Some error occured',"error")
        return redirect(url_for("login_form"))

@app.route("/register_admin", methods=['POST'])
def register_admin():
    if request.method == 'POST':
        adminDetails = request.form
        secret_key = adminDetails['key']
        name = adminDetails['name']
        email = adminDetails['mail']
        password = adminDetails['pass']
        flag = 0
        while True:  
            if (len(password)<8):
                flag = -1
                break
            elif not re.search("[a-z]", password):
                flag = -1
                break
            elif not re.search("[A-Z]", password):
                flag = -1
                break
            elif not re.search("[0-9]", password):
                flag = -1
                break
            elif not re.search("[_@$]", password):
                flag = -1
                break
            elif re.search("\\s", password):
                flag = -1
                break
            else:
                flag = 0
                break
        if flag ==-1:
            flash("Not a Valid Password","error")
            return redirect(url_for("admin_register"))
        if secret_key != 'URADMIN':
            flash("Wrong secret key","error")
            return redirect(url_for("admin_register"))
        else:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM admin WHERE email=%s",(email,))
            mailData = cur.fetchone()
            cur.close()
            if mailData:
                flash("Email ID is already used","error")
                return redirect(url_for("admin_register"))
            else:
                hashpas = sha256_crypt.hash(password)
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("INSERT INTO admin(name,email,password)values(%s,%s,%s)",(name,email,hashpas))
                mysql.connection.commit()
                cur.close()
                flash('Registration Successfull',"success")
                return redirect(url_for("admin_login"))


@app.route("/login_admin", methods=['GET','POST'])
def login_admin():
    if request.method == 'POST':
        loginDetails = request.form
        email = loginDetails['mail']
        password = loginDetails['pass']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM admin WHERE email=%s",(email,))
        admin_Data = cur.fetchone()
        if admin_Data is None:
            flash('Email ID not registered',"error")
            return redirect(url_for("admin_login"))
        else:
            checkpass = sha256_crypt.verify(password,admin_Data['password']) 
            cur.close()
            if email == admin_Data['email'] and checkpass == True:
                session['admin'] = True
                session['admin_email'] = admin_Data['email']
                session['admin_name'] = admin_Data['name']
                session['admin_id'] = admin_Data['admin_id']
                flash('You were successfully logged in',"success")
                return redirect(url_for("home"))
            else:
                flash('Invalid Credentials',"error")
                return redirect(url_for("admin_login"))
    else:
        flash('Some error occured',"error")
        return redirect(url_for("admin_login"))

@app.route("/candidate_add", methods=['POST'])
def candidate_add():
    if 'admin' in session:
        if request.method == 'POST':
            candidateDetails = request.form
            name = candidateDetails['name']
            slogan = candidateDetails['slogan']
            photo = request.files['logo']
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM candidate WHERE name=%s",(name,))
            nameData = cur.fetchone()
            cur.close()
            if nameData is None:
                if len(slogan) > 50:
                    flash('Failed to add.Slogan exceeds 50 characters',"error") 
                    return redirect(url_for('add_candidate'))      
                else:
                    filename = secure_filename(photo.filename)
                    photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cur.execute("INSERT INTO candidate(name,slogan,logo)values(%s,%s,%s)",(name,slogan,photo.filename))
                    mysql.connection.commit()
                    cur.close()
                    flash('Candidate added Successfully',"success")
                    return redirect(url_for("home"))
            elif nameData:
                flash("Name is already used","error")
                return redirect(url_for("add_candidate"))
    else:
        flash('Please login as a admin',"error")
        return redirect(url_for('home'))

@app.route("/edit/<int:id>")
def candidate_edit(id):
    if 'admin' in session:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM candidate WHERE candidate_id=%s",(id,))
        data = cur.fetchone()
        cur.close()
        return render_template('edit.html',data=data)
    else:
        flash('Please login as a admin',"error")
        return redirect(url_for('home'))

@app.route("/update/<int:id>",methods=['POST'])
def candidate_update(id):
    if 'admin' in session:
        if request.method == 'POST':
            candidateDetails = request.form
            name = candidateDetails['name']
            slogan = candidateDetails['slogan']
            photo = request.files['logo']
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)   
            cur.execute("SELECT * FROM candidate WHERE name=%s",(name,))
            name_Data = cur.fetchone()
            if name_Data:
                if (name_Data['candidate_id'] != id):
                    flash('Name already used',"error")
                    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)   
                    cur.execute("SELECT * FROM candidate WHERE candidate_id=%s",(id,))  
                    name_Data = cur.fetchone()
                    cur.close()
                    return render_template("edit.html",data=name_Data) 
                elif(name_Data['candidate_id'] == id):
                    if len(slogan) > 50:
                        flash('Update failed.Slogan exceeds 50 characters',"error") 
                        return redirect(url_for('update_candidate'))
                    else:
                        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)   
                        filename = secure_filename(photo.filename)
                        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        cur.execute("UPDATE candidate SET name=%s, slogan =%s,logo=%s where candidate_id=%s",(name,slogan,photo.filename,id))
                        mysql.connection.commit()
                        cur.close()
                        flash('Candidate updated Successfully',"success")
                        return redirect(url_for('update_candidate'))
            else:
                if len(slogan) > 50:
                        flash('Update failed.Slogan exceeds 50 characters',"error") 
                        return redirect(url_for('update_candidate'))
                else:
                    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)   
                    filename = secure_filename(photo.filename)
                    photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    cur.execute("UPDATE candidate SET name=%s, slogan =%s,logo=%s where candidate_id=%s",(name,slogan,photo.filename,id))
                    mysql.connection.commit()
                    cur.close()
                    flash('Candidate updated Successfully',"success")
                    return redirect(url_for('update_candidate'))
    else:
        flash('Please login as a admin',"error")
        return redirect(url_for('home'))


@app.route("/delete/<int:id>")
def delete(id):
    if 'admin' in session:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("DELETE FROM candidate WHERE candidate_id=%s",(id,))
        mysql.connection.commit()
        cur.close()
        flash("Candidate deleted successfully","success")
        return redirect(url_for('update_candidate'))
    else:
        flash('Please login as a admin',"error")
        return redirect(url_for('home'))

@app.route("/user_profile/<int:id>")
def user_profile(id):
    if 'user' in session:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE user_id=%s",(id,))
        users_data = cur.fetchone()
        cur.close()
        return render_template("user_profile.html",data=users_data)
    else: 
        flash('Please login as a admin',"error")
        return redirect(url_for('home'))

@app.route("/profile_user/<int:id>",methods=['POST'])
def profile_user(id):
    if 'user' in session:
        if request.method == 'POST':
            userDetails = request.form
            name = userDetails['name']
            dob = userDetails['dob']
            photo = request.files['pimage']
            email = userDetails['mail']
            gender = userDetails['gender']
            phno = userDetails['phno']
            username = userDetails['username']
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM users WHERE username=%s",(username,))
            username_Data = cur.fetchone()
            if username_Data:
                if (username_Data['user_id'] != id):
                    flash('Username already used',"error")
                    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cur.execute("SELECT * FROM users WHERE user_id=%s",(id,))
                    users_data = cur.fetchone()
                    cur.close()
                    return render_template("user_profile.html",data=users_data)
                elif (username_Data['user_id'] == id):
                    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)       
                    filename = secure_filename(photo.filename)
                    photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    cur.execute("UPDATE users SET name =%s,dob=%s,image=%s,email=%s,gender=%s,phno=%s,username=%s where user_id=%s",(name,dob,photo.filename,email,gender,phno,username,id))
                    mysql.connection.commit()
                    cur.close()
                    flash('Profile updated Successfully.Login again to see the changes',"success")
                    return redirect(url_for('logout'))
            else:
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)       
                filename = secure_filename(photo.filename)
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cur.execute("UPDATE users SET name =%s,dob=%s,image=%s,email=%s,gender=%s,phno=%s,username=%s where user_id=%s",(name,dob,photo.filename,email,gender,phno,username,id))
                mysql.connection.commit()
                cur.close()
                flash('Profile updated Successfully.Login again to see the changes',"success")
                return redirect(url_for('logout'))
    else:
        flash('Please login first',"error")
        return redirect(url_for('home'))

@app.route("/change_pass")
def change_pass():
    return render_template("change_pass.html")

@app.route("/pass_change/<int:id>",methods=['POST','GET'])
def pass_change(id):
    if 'user' in session:
        if request.method == 'POST':
            passDetails = request.form
            pass1 = passDetails['pass1']
            flag = 0
            while True:  
                if (len(pass1)<8):
                    flag = -1
                    break
                elif not re.search("[a-z]", pass1):
                    flag = -1
                    break
                elif not re.search("[A-Z]", pass1):
                    flag = -1
                    break
                elif not re.search("[0-9]", pass1):
                    flag = -1
                    break
                elif not re.search("[_@$]", pass1):
                    flag = -1
                    break
                elif re.search("\\s", pass1):
                    flag = -1
                    break
                else:
                    flag = 0
                    break
            if flag ==-1:
                flash("Not a Valid Password","error")
                return render_template("change_pass.html")
            pass2 = passDetails['pass2']
            if pass1 != pass2:
                flash("Passwords dont match","error")
                return render_template("change_pass.html")
            else:
                hashpas = sha256_crypt.hash(pass1)
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("UPDATE users SET password=%s where user_id=%s",(hashpas,id))
                mysql.connection.commit()
                cur.close()
                flash('Password changed Successfull',"success")
                return redirect(url_for("home"))
    else:
        flash('Please login first',"error")
        return redirect(url_for('home'))

@app.route("/admin_pass")
def admin_pass():
    return render_template("admin_pass.html")


#change admin-password 
@app.route("/pass_admin/<int:id>",methods=['POST','GET'])
def pass_admin(id):
    if 'admin' in session:
        if request.method == 'POST':
            passDetails = request.form
            pass1 = passDetails['pass1']
            flag = 0
            while True:  
                if (len(pass1)<8):
                    flag = -1
                    break
                elif not re.search("[a-z]", pass1):
                    flag = -1
                    break
                elif not re.search("[A-Z]", pass1):
                    flag = -1
                    break
                elif not re.search("[0-9]", pass1):
                    flag = -1
                    break
                elif not re.search("[_@$]", pass1):
                    flag = -1
                    break
                elif re.search("\\s", pass1):
                    flag = -1
                    break
                else:
                    flag = 0
                    break
            if flag ==-1:
                flash("Not a Valid Password","error")
                return render_template("admin_pass.html")
            pass2 = passDetails['pass2']
            if pass1 != pass2:
                flash("Passwords dont match","error")
                return render_template("admin_pass.html")
            else:
                hashpas = sha256_crypt.hash(pass1)
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("UPDATE admin SET password=%s where admin_id=%s",(hashpas,id))
                mysql.connection.commit()
                cur.close()
                flash('Password changed Successfull',"success")
                return redirect(url_for("home"))
    else:
        flash('Please login as a admin',"error")
        return redirect(url_for('home'))

@app.route("/admin_profile/<int:id>")
def admin_profile(id):
    if 'admin' in session:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM admin WHERE admin_id=%s",(id,))
        admin_data = cur.fetchone()
        cur.close()
        return render_template("admin_profile.html",data=admin_data)
    else:
        flash('Please login as a admin',"error")
        return redirect(url_for('home'))

@app.route("/profile_admin/<int:id>",methods=['POST'])
def profile_admin(id):
    if 'admin' in session:
        if request.method == 'POST':
            adminDetails = request.form
            name = adminDetails['name']
            mail = adminDetails['email']
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM admin WHERE email=%s",(mail,))
            mail_Data = cur.fetchone()
            if mail_Data:
                if(mail_Data['admin_id'] != id):
                    flash('Email ID already used',"error")
                    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cur.execute("SELECT * FROM admin WHERE admin_id=%s",(id,))
                    admin_data = cur.fetchone()
                    cur.close()
                    return render_template("admin_profile.html",data=admin_data)
                elif (mail_Data['admin_id'] == id):
                    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)       
                    cur.execute("UPDATE admin SET name =%s,email=%s where admin_id=%s",(name,mail,id))
                    mysql.connection.commit()
                    cur.close()
                    flash('Profile updated Successfully.Login again to see the changes',"success")
                    return redirect(url_for('logout'))
            else:
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)       
                cur.execute("UPDATE admin SET name =%s,email=%s where admin_id=%s",(name,mail,id))
                mysql.connection.commit()
                cur.close()
                flash('Profile updated Successfully.Login again to see the changes',"success")
                return redirect(url_for('logout'))
    else:
        flash('Please login as a admin',"error")
        return redirect(url_for('home'))

@app.route("/vote/<int:id>",methods=['POST'])
def vote(id):
    if 'user' not in session:
        flash('Please login as a user to vote.',"error")
        return redirect(url_for('candidate'))
    else:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("INSERT INTO vote (user_id,candidate_id)values(%s,%s)",(session['user_id'],id))
        mysql.connection.commit()
        cur.close()
        flash("voted successfully","success")
        return redirect(url_for("home"))

@app.route("/result")
def result():
    if 'admin' in session:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM candidate")
        candidates_Data = cur.fetchall()
        cur.close()
        datas=[]
        cur = mysql.connection.cursor()
        for i in candidates_Data:
            cur.execute("SELECT count(A.candidate_id),B.candidate_id,B.name,B.logo FROM vote A JOIN candidate B ON B.candidate_id=A.candidate_id where A.candidate_id =%s",(i['candidate_id'],))
            candi_data = cur.fetchone()
            datas.append(candi_data)
        max_votes = max(datas)
        max_details = []
        for i in datas:
            if i[0] == max_votes[0]:
                max_details.append(i)
        cur.close()
        return render_template("results.html",data=datas,data1=max_details)
    else:
        flash('Please login as a admin',"error")
        return redirect(url_for('home'))

@app.route("/user_fpass",methods=['POST'])
def user_fpass():
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails['username']
        mail = userDetails['mail']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE username=%s",(name,))
        user_Data = cur.fetchone()
        if user_Data:
            if user_Data['username'] == name and user_Data['email'] == mail:
                user_id = user_Data['user_id']
                return render_template('userpass_change.html',data=user_id)
        else:
            flash('Invalid data',"error")
            return redirect(url_for("login_form"))

@app.route("/change_userpass",methods=['POST'])
def change_userpass():
    if request.method == 'POST':
        passDetails = request.form
        pass1 = passDetails['pass1']
        flag = 0
        while True:  
            if (len(pass1)<8):
                flag = -1
                break
            elif not re.search("[a-z]", pass1):
                flag = -1
                break
            elif not re.search("[A-Z]", pass1):
                flag = -1
                break
            elif not re.search("[0-9]", pass1):
                flag = -1
                break
            elif not re.search("[_@$]", pass1):
                flag = -1
                break
            elif re.search("\\s", pass1):
                flag = -1
                break
            else:
                flag = 0
                break
        if flag ==-1:
            flash("Not a Valid Password","error")
            return render_template("userpass_change.html")
        pass2 = passDetails['pass2']
        user_id = passDetails['user_id']
        print(user_id)
        if pass1 != pass2:
                flash("Passwords dont match","error")
                return render_template("userpass_change.html")
        else:
            hashpas = sha256_crypt.hash(pass1)
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("UPDATE users SET password=%s where user_id=%s",(hashpas,user_id))
            mysql.connection.commit()
            cur.close()
            flash('Password reset Successfull',"success")
            return redirect(url_for("login_form"))

@app.route("/admin_fpass",methods=['POST'])
def admin_fpass():
    if request.method == 'POST':
        adminDetails = request.form
        mail = adminDetails['mail']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM admin WHERE email=%s",(mail,))
        admin_Data = cur.fetchone()
        if admin_Data:
            if admin_Data['email'] == mail:
                admin_id = admin_Data['admin_id']
                return render_template('adminpass_change.html',data=admin_id)
        else:
            flash('Invalid data',"error")
            return redirect(url_for("admin_login"))

@app.route("/change_adminpass",methods=['POST'])
def change_adminpass():
    if request.method == 'POST':
        passDetails = request.form
        pass1 = passDetails['pass1']
        flag = 0
        while True:  
            if (len(pass1)<8):
                flag = -1
                break
            elif not re.search("[a-z]", pass1):
                flag = -1
                break
            elif not re.search("[A-Z]", pass1):
                flag = -1
                break
            elif not re.search("[0-9]", pass1):
                flag = -1
                break
            elif not re.search("[_@$]", pass1):
                flag = -1
                break
            elif re.search("\\s", pass1):
                flag = -1
                break
            else:
                flag = 0
                break
        if flag ==-1:
            flash("Not a Valid Password","error")
            return render_template("adminpass_change.html")
        pass2 = passDetails['pass2']
        admin_id = passDetails['admin_id']
        if pass1 != pass2:
                flash("Passwords dont match","error")
                return render_template("adminpass_change.html")
        else:
            hashpas = sha256_crypt.hash(pass1)
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("UPDATE admin SET password=%s where admin_id=%s",(hashpas,admin_id))
            mysql.connection.commit()
            cur.close()
            flash('Password reset Successfull',"success")
            return redirect(url_for("admin_login"))

@app.route("/logout")
def logout():
    session.clear()
    flash('Logged out successfully',"success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
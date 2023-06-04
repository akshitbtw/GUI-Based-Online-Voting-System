from tkinter import *
import easyocr  #OCR
import re   # regex
from PIL import ImageTk, Image  # loading Python Imaging Library
from tkinter import filedialog  # To get the dialog box to open when required 
import time # to get date & time
import datetime
from datetime import date # to calculate age
from tkinter import messagebox
import numpy as np # to compare images
import cv2
import random # to generate otp
from twilio.rest import Client #send otp to phone
import mysql.connector # for database
from tkinter import ttk
# From the ttkthemes package import the ThemedTk widget
from ttkthemes import ThemedTk
import matplotlib.pyplot as plt
from threading import Thread
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import smtplib
from matplotlib import cm

root = ThemedTk(theme='breeze')
root.title("Online Voting Application")
root_width = 1024
root_height = 700
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (root_width/2)
y = (screen_height/2) - (root_height/2)
root.geometry(f'{root_width}x{root_height}+{int(x)}+{int(y)}')
root.call('wm', 'iconphoto', root._w, PhotoImage(file='Labels and Backgrounds/india1.png'))
root.resizable(width = False, height = False)

bg1 = PhotoImage(file='Labels and Backgrounds/rooot1.png')
bg = PhotoImage(file='Labels and Backgrounds/grad.png')

c1 = Canvas(root, height=900, width=1020)
c1.place(x=0, y=0)
c1.create_image(500,280,image=bg)
c1.create_image(500,350,image=bg1)

def admin_win():
    admin = Toplevel(root)
    admin.title("Administrator Login")

    admin_width = 400
    admin_height = 300

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width/2) - (admin_width/2)
    y = (screen_height/2) - (admin_height/2)

    admin.geometry(f'{admin_width}x{admin_height}+{int(x)}+{int(y)}')
    root.call('wm', 'iconphoto', admin._w, PhotoImage(file='icons/adminicon.png'))

    def admin_login():
        flag = True
        # User ID
        try:
            if userid_input.get()==None or userid_input.get()=='':
                #messagebox.showerror('Alert',"User ID Field Cannot Be Empty", parent = admin)
                flag = None
            elif not (userid_input.get().isdigit()):
                messagebox.showerror('Error',"Invalid User ID", parent = admin)
                flag = False
            elif(userid_input.get().isdigit() and userid_input.get() == '1234'):
                flag = True
            else :
                messagebox.showerror('Error',"Incorrect User ID", parent = admin) 
                flag = False
        except Exception as e:
            messagebox.showerror('Error',e, parent = admin)

        # Email
        try :
            regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
            if(email_input.get() == None or email_input.get() == ''):
                #messagebox.showerror('Alert',"Email Field Cannot Be Empty", parent = admin)
                flag = None
            elif(re.search(regex, email_input.get())):
                if (email_input.get() == 'akshit.4670@gmail.com'):
                    flag = True
                else:
                    messagebox.showerror('Error',"Incorrect Email ID", parent = admin)
                    flag = False
            else:
                messagebox.showerror('Error',"Incorrect Email ID", parent = admin)
                flag = False
        except Exception as e:
            messagebox.showerror('Error',e, parent = admin)

        # Password
        try:
            if pass_input.get()==None or pass_input.get()=='':
                #messagebox.showerror('Alert',"Password Field Cannot Be Empty", parent = admin)
                flag = None
            elif(pass_input.get() == 'akshit'):
                flag = True
            else :
                messagebox.showerror('Error',"Incorrect Password", parent = admin) 
                flag = False
        except Exception as e:
            messagebox.showerror('Error',e, parent = admin)

        # OTP
        try:
            global otp
            if otp_input.get()==None or otp_input.get()=='':
                #messagebox.showerror('Alert',"OTP Field Cannot Be Empty", parent = admin)
                flag = None
            elif(otp_input.get().isdigit() and otp_input.get() == str(otp)):
                flag = True
            elif not (otp_input.get().isdigit()):
                messagebox.showerror('Error',"Invalid OTP", parent = admin)
                flag = False
            else :
                messagebox.showerror('Error',"Incorrect OTP", parent = admin) 
                flag = False
        except Exception as e:
            messagebox.showerror('Error',e, parent = admin)

        if (flag == True):
            result_win()
        elif (flag == None):
            messagebox.showerror('Error',"Field(s) Cannot Be Empty", parent = admin)
        else :
            messagebox.showerror('Error',"Incorrect ID & Password", parent = admin)

    def send():
        try: 
            s = smtplib.SMTP("smtp.gmail.com" , 587)
            s.starttls()
            s.login("sendotptoemail@gmail.com" , "xxxxxx")
            global otp
            otp = random.randint(100000, 999999)
            message = "OTP for Admin Login - " + str(otp)
            s.sendmail("sendotptoemail@gmail.com" , "akshit.4670@gmail.com" , message)
            messagebox.showinfo("Send OTP via Email", f"OTP sent to {'akshit.4670@gmail.com'}", parent = admin)
            s.quit()
        
        except Exception as e:
            messagebox.showerror("Error", e, parent = admin)
    
    def result_win():
        try:
            root.iconify()
            base1 = Toplevel(admin)
            base1.title("Results")
            base1.geometry('1920x1000')
            root.call('wm', 'iconphoto', base1._w, PhotoImage(file='icons/resulticon.png'))
            base1.state("zoomed")
            def cross():
                root.quit()
                root.destroy()

            partyname=[]
            votecount=[]
            connection = mysql.connector.connect(host = "localhost",
                                                    user = "root",
                                                    passwd = "xxxxxx",
                                                    database = "app_database")

            cursor = connection.cursor()
            query1 = """select vote,count(*) AS `VoteFrequency` from app_user_details group by vote;"""
            cursor.execute(query1)
            for i in cursor.fetchall():
                partyname.append(i[0])
                votecount.append(i[1])

            for i in range(len (partyname)):
                if (partyname[i] == 1):
                    partyname[i] = "Bhartiya Janata Party"

                if (partyname[i] == 2):
                    partyname[i] = "Bahujan Samaj Party"

                if (partyname[i] == 3):
                    partyname[i] = "Lok Janshakti Party"

                if (partyname[i] == 4):
                    partyname[i] = "Dravida Munnetra Kazhagam"

                if (partyname[i] == 5):
                    partyname[i] = "Communist Party of India"

                if (partyname[i] == 6):
                    partyname[i] = "Yuvajana Sramika Rythu Congress Party"

                if (partyname[i] == 7):
                    partyname[i] = "Indian National Congress"

                if (partyname[i] == 8):
                    partyname[i] = "Janata Dal"

                if (partyname[i] == 9):
                    partyname[i] = "Shiv Sena"

                if (partyname[i] == 10):
                    partyname[i] = "Biju Janata Dal"

                if (partyname[i] == 11):
                    partyname[i] = "Nationalist Congress Party"

                if (partyname[i] == 12):
                    partyname[i] = "Shiromani Akali Dal"

                if (partyname[i] == 13):
                    partyname[i] = "Aam Aadmi Party"

                if (partyname[i] == 14):
                    partyname[i] = "Samajwadi Party"

                if (partyname[i] == 15):
                    partyname[i] = "All India Trinamool Congress"

            actualFigure = plt.figure(1, figsize=(20,10))
            actualFigure.suptitle("Results", fontsize = 24)

            # The slices will be ordered and plotted counter-clockwise.
            labels = partyname
            fracs = votecount
            explode=(0, 0.05, 0, 0,0)

            explode = list()
            for k in labels:
                explode.append(0.1)

            cs=cm.tab20(np.arange(15)/15.)
            plt.margins(0.1, 0.1)
            pie = plt.pie(fracs, explode=explode, labels=labels,
                            autopct='%1.1f%%', shadow=True, colors=cs)
                            # The default startangle is 0, which would start
                            # the Frogs slice on the x-axis.  With startangle=90,
                            # everything is rotated counter-clockwise by 90 degrees,
                            # so the plotting starts on the positive y-axis.
            plt.legend(pie[0], labels, bbox_to_anchor=(-0.2, 0.5))
            canvas = FigureCanvasTkAgg(actualFigure, base1)
            canvas.get_tk_widget().pack()
            base1.protocol('WM_DELETE_WINDOW', cross)

        except mysql.connector.Error as error:
            print("".format(error))
    
    userid_label = Label(admin, text = "User ID", font=("Calibri",14))
    userid_label.grid(row=0,column=0,padx=25,pady=20)
    userid_input = ttk.Entry(admin, font=("Calibri",14), justify="center", width=22)
    userid_input.grid(row=0,column=1,padx=20)

    email_label = Label(admin, text = "Email ID", font=("Calibri",14))
    email_label.grid(row=1,column=0,padx=20)
    email_input = ttk.Entry(admin, font=("Calibri",14), justify="center", width=22)
    email_input.grid(row=1,column=1,padx=20)

    pass_label = Label(admin, text = "Password", font=("Calibri",14))
    pass_label.grid(row=2,column=0,padx=20)
    pass_input = ttk.Entry(admin,show="*", font=("Calibri",14), justify="center", width=22)
    pass_input.grid(row=2,column=1,padx=20,pady=15)

    otp_label = Label(admin, text = "OTP", font=("Calibri",14))
    otp_label.grid(row=3,column=0,padx=20)
    otp_input = ttk.Entry(admin, font=("Calibri",14), justify="center", width=10)
    otp_input.grid(row=3,column=1,padx=20,sticky=W)

    generate_btn = ttk.Button(admin, text ='Generate OTP', command = send)
    generate_btn.place(x=267,y=182)

    submit_btn = ttk.Button(admin, text ='Log In', width=20, command = admin_login)
    submit_btn.place(x=120,y=240)
    

def details_win():
    if(checkbox1.get() == 0):
        messagebox.showwarning('ALERT', "Please accept the guidelines by clicking on the checkbox to proceed.")
    else:
        root.iconify()
        # Create a window
        base = Toplevel(root)
        # Set Title as Image Loader
        base.title("Details")
        # Set the resolution of window
        base.geometry("1920x1000")
        root.call('wm', 'iconphoto', base._w, PhotoImage(file='icons/employee.png'))
        # Allow Window to be resizable
        base.resizable(width = True, height = True)
        base.state("zoomed")

        bg = PhotoImage(file='Labels and Backgrounds/user details1.png')
        bg1 = PhotoImage(file='Labels and Backgrounds/wallpaper2.png')
        bg2 = PhotoImage(file='Labels and Backgrounds/Uploaded1.png')
        bg3 = PhotoImage(file='Labels and Backgrounds/status.png')
        bg4 = PhotoImage(file='icons/voteicon.png')

        canvas = Canvas(base, height=1080, width=1920)
        canvas.place(x=-2, y=0)
        canvas.create_image(900,500,image=bg1)
        canvas.create_image(340,467,image=bg)
        canvas.create_image(1080,240,image=bg2)
        canvas.create_image(1070,620,image=bg3)
        canvas.create_image(340,85,image=bg4)

        style = ttk.Style(base)

        def openfilename():
            # open file dialog box to select image
            # The dialogue box has a title "Upload"
            filename = filedialog.askopenfilename(title ="Upload")
            return filename

        def entered_details_validation():
            name1 = name.get()
            if (name1 == "" or name1 == None):
                messagebox.showerror('Error','Name Cannot Be Empty', parent = base)
                v1 = False
            else:
                v1 = True

            dob1 = str(dob.get())
            format = '%d/%m/%Y'
            try:
                if (dob1 == "" or dob == None):
                    messagebox.showerror('Error','DOB Cannot Be Empty', parent = base)
                    v2 = False
                else:
                    datetime.datetime.strptime(dob1, format)
                    v2 = True
            except ValueError:
                messagebox.showinfo('Error', 'DOB is not valid', parent = base)
                v2 = False

            gender1 = str(gender.get())
            if (gender1 == ""):
                messagebox.showerror('Error','Gender Cannot Be Empty', parent = base)
                v3 = False
            else:
                v3 = True

            
            age1 = age.get()
            if (str(age1) == None or str(age1) == ''):
                messagebox.showerror('Error','Age Cannot Be Empty', parent = base)
                v4 = False
            elif not (age1.isdigit()):
                messagebox.showerror('Error',"Age must be an Integer", parent = base)
                v4 = False
            elif (int(age1) == 0 or int(age1) < 0):
                messagebox.showerror('Error','Invalid Age', parent = base)
                v4 = False
            elif (int(age1) < 18 or int(age1) > 120):
                messagebox.showerror('Error',"You're Not Eligible To Vote", parent = base)
                v4 = False
            else:
                v4 = True

            phone_regex = '^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$'
            phone1 = phone.get()
            if (phone1 == "" or phone1 == None):
                messagebox.showerror('Error','Phone Number Cannot Be Empty', parent = base)
                v5 = False
            elif (re.search(phone_regex, phone1)):
                v5 = True
            else:
                messagebox.showerror('Error',"Invalid Phone Number", parent = base)
                v5 = False

            aadhaar_regex = '([0-9]{4}\s){2}[0-9]{4}'
            ad1 = aadhaar.get()
            if (ad1 == "" or ad1 == None):
                messagebox.showerror('Error','Aadhaar Number Cannot Be Empty', parent = base)
                v6 = False
            elif (re.search(aadhaar_regex, ad1)):
                v6 = True
            else:
                messagebox.showerror('Error',"Invalid Aadhaar Number. Make sure there is space after every 4 digits", parent = base)
                v6 = False

            voter_regex = '^([A-Z]){3}([0-9]){7}?$'
            voter1 = voter_no.get()
            if (voter1 == "" or voter1 == None):
                messagebox.showerror('Error','Voter ID Number Cannot Be Empty', parent = base)
                v7 = False
            elif (re.search(voter_regex, voter1)):
                v7 = True
            else:
                messagebox.showerror('Error',"Invalid Voter ID Number", parent = base)
                v7 = False
                
            if(v1 == True and v2 == True and v3 == True and v4 == True and v5 == True and v6 == True and v7 == True):
                mydb = mysql.connector.connect(
                host = "localhost",
                    user = "root",
                    passwd = "xxxxxx",
                    database="app_database"
                )

                cursor = mydb.cursor()
                sql = "SELECT COUNT(1) FROM app_user_details WHERE aadhaar_no = %s"
                val = (ad1)
                result = cursor.execute(sql,(val,))
                row = cursor.fetchone()
                if (row[0]==1):
                    messagebox.showwarning('Alert','You Cannot Vote Twice!', parent = base)
                    base.destroy()
                    root.destroy()
                else:
                    messagebox.showinfo('Please Wait','Verifying the Entered Details with the Documents Uploaded',parent=base)
                    Lb1.insert(3,"Verifying the Entered Details with the Documents Uploaded")
                    Lb1.insert(4,"PLEASE WAIT FOR A MOMENT...")
                    Thread(target=extract).start()
                
        def entered_details():
            name1 = name.get()
            dob1 = str(dob.get())
            gender1 = str(gender.get())
            age1 = age.get()
            phone1 = phone.get()
            ad1 = aadhaar.get()
            voter1 = voter_no.get()
            return name1, dob1, gender1, age1, phone1, ad1, voter1

        def aadhaar_upload():
            x = openfilename() # Select the Imagename  from a folder     
            img = Image.open(x) # opens the image
            # saving the image (1 for backend, 1 for image extraction)
            img1 = img.save(r'E:\BCA\Project\Coding\Submissions\SubmittedAdhaar.png')
            img2 = img.save(r'E:\BCA\Project\Coding\aadhaar.png')
            img = img.resize((300, 200), Image.ANTIALIAS) # resize the image and apply a high-quality down sampling filter
            # PhotoImage class is used to add image to widgets, icons etc // 300, 200
            img = ImageTk.PhotoImage(img)   
            # create a label
            panel = Label(base, image = img)      
            # set the image as img 
            panel.image = img
            panel.place(x=750,y=140)
            Lb1.insert(1,"Aadhaar Card Uploaded Successfully")

        def voterid_upload():
            x = openfilename() # Select the Imagename  from a folder
            img = Image.open(x) # opens the image
            # saving the image (1 for backend, 1 for image extraction)
            img1 = img.save(r'E:\BCA\Project\Coding\Submissions\SubmittedVoterID.png')
            img2 = img.save(r'E:\BCA\Project\Coding\voterid.png')
            img = img.resize((250, 350), Image.ANTIALIAS) # resize the image and apply a high-quality down sampling filter
            # PhotoImage class is used to add image to widgets, icons etc // 250, 350
            img = ImageTk.PhotoImage(img)   
            # create a label
            panel = Label(base, image = img)      
            # set the image as img 
            panel.image = img
            panel.place(x=1150,y=60)
            Lb1.insert(2,"Voter ID Card Uploaded Successfully")

        def extract():
            # Disable Widgets
            Upload_btn.config(state=DISABLED)
            input1.config(state=DISABLED)
            input2.config(state=DISABLED)
            input3.config(state=DISABLED)
            input4.config(state=DISABLED)
            input5.config(state=DISABLED)
            input6.config(state=DISABLED)
            input7.config(state=DISABLED)
            input8.config(state=DISABLED)
            input9.config(state=DISABLED)
            ad_upload_btn.config(state=DISABLED)
            voter_upload_btn.config(state=DISABLED)

            def calculateAge(birthDate):
                today = date.today()
                age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
                return age
            
            pb1['value'] += 5
            base.update_idletasks()
            time.sleep(0.1)
            # extracts the whole text from image
            reader = easyocr.Reader(['en'], gpu = False)
            text = reader.readtext('aadhaar.png', detail = 0)

            pb1['value'] += 20
            base.update_idletasks()
            time.sleep(0.1)

            text1 = reader.readtext('voterid.png', detail = 0)

            pb1['value'] += 20
            base.update_idletasks()
            time.sleep(0.1)
            
            text_file = open("aadhaardetails.txt", "w")
            n = text_file.write(str(text))
            text_file.close()

            pb1['value'] += 20
            base.update_idletasks()
            time.sleep(0.5)

            text_file = open("voteriddetails.txt", "w")
            m = text_file.write(str(text1))
            text_file.close()

            pb1['value'] += 20
            base.update_idletasks()
            time.sleep(1)

            f = open("aadhaardetails.txt", "r") # Open the file that you want to search 
            content = f.read() # Will contain the entire content of the img as a string

            #Name
            regex_name=re.search(r"'Name:',\s+\'((\w+\s*){1,3})", content)
            name=regex_name.group(1)

            #Gender
            regex_gender=re.search(r'(Fe)?[mM]ale', content)
            gender=regex_gender.group(0)
            
            #DOB
            dates = re.findall(r'\d{2}[/-]\d{2}[/-]\d{4}', content)
            for date1 in dates:
                if "/" in date1:
                    day, month, year = map(int, date1.split("/"))
            
            #Age
            age_check = calculateAge(date(year, month, day))

            #Aadhar No
            num = re.findall(r'\d{4}[ ]\d{4}[ ]\d{4}', content)
            for no in num:
                if " " in num:
                    day, month, year = map(int, aad.split(" "))

            f.close()

            f = open("voteriddetails.txt", "r") # Open the file that you want to search 
            content1 = f.read() # Will contain the entire content of the img as a string

            # Voter ID Number
            regex_vno=re.search(r"\'(\w+)\',\s+\"Elector\'s\s+Name\"", content1)
            v_no=regex_vno.group(1)
            f.close()

            pb1['value'] += 20
            base.update_idletasks()
            time.sleep(0.5)

            a,b,c,d,e,f,g = entered_details()

            if (a == name and b == date1 and c == gender and d == str(age_check) and f == no and g == v_no):
                messagebox.showinfo('Success','Entered Details Match with the Uploaded Documents. Click on Submit Button to Continue.',parent=base)
                submit_btn.config(state=NORMAL)
                
                pb1['value'] += 45
                base.update_idletasks()
                time.sleep(0.1)
                Lb1.insert(5,'Entered Details Match with the Uploaded Documents')
                
            else:
                messagebox.showerror('Error','Entered Details Do Not Match with the Uploaded Documents. Try Again.',parent=base)
                pb1['value'] = 0
                Lb1.delete('0','end')
                Upload_btn.config(state=NORMAL)
                input1.config(state=NORMAL)
                input2.config(state=NORMAL)
                input3.config(state=NORMAL)
                input4.config(state=NORMAL)
                input5.config(state=NORMAL)
                input6.config(state=NORMAL)
                input7.config(state=NORMAL)
                input8.config(state=NORMAL)
                input9.config(state=NORMAL)
                ad_upload_btn.config(state=NORMAL)
                voter_upload_btn.config(state=NORMAL)
            
        def write_file(data, filename):
            # Convert binary data to proper format and write it on Hard Disk
            with open(filename, 'wb') as file:
                file.write(data)

        def readBLOB(vd1, ad_photo, vd_photo):
            pb1['value'] += 30
            base.update_idletasks()
            time.sleep(0.5)
            try:
                connection = mysql.connector.connect(host = "localhost",
                                                        user = "root",
                                                        passwd = "xxxxxx",
                                                        database = "user_database")

                cursor = connection.cursor()
                sql_fetch_blob_query = """SELECT * from user_details where voter_id = %s LIMIT 0, 200"""
                pb1['value'] += 30
                base.update_idletasks()
                time.sleep(0.5)
                cursor.execute(sql_fetch_blob_query, (vd1,))
                record = cursor.fetchall()
                for row in record:
                    d_name = row[1]
                    d_dob = row[2]
                    d_gender = row[3]
                    d_age = row[4]
                    d_phone = row[5]
                    d_aadhaar = row[6]
                    image = row[7]
                    d_voterid = row[8]
                    image1 = row[9]
                    write_file(image, ad_photo)
                    write_file(image1, vd_photo)

                a,b,c,d,e,f,g = entered_details()
                pb1['value'] += 30
                base.update_idletasks()
                time.sleep(0.5)
                if (a == d_name and b == d_dob and c == d_gender and d == str(d_age) and e == d_phone and f == d_aadhaar and g == d_voterid):
                    
                    ad = cv2.imread(r'E:\BCA\Project\Coding\aadhaar.png')
                    d_ad = cv2.imread(r'E:\BCA\Project\Coding\Database Retrieved Images\aadhaar_db.png')
                    vd = cv2.imread(r'E:\BCA\Project\Coding\voterid.png')
                    d_vd = cv2.imread(r'E:\BCA\Project\Coding\Database Retrieved Images\voter_db.png')
                    # compare aadhaar & voter ID
                    diff_img=cv2.subtract(ad,d_ad)
                    diff_img1=cv2.subtract(vd,d_vd)
                    if (np.sum(diff_img) & np.sum(diff_img1)) == 0 :
                        pb1['value'] += 30
                        base.update_idletasks()
                        time.sleep(0.5)
                        messagebox.showinfo('Success','Entered Details & Documents Match with the Database', parent=base)
                        # Storing Details into the database
                        def convertToBinaryData(filename):
                            with open(filename, 'rb') as file:
                                binaryData = file.read()
                            return binaryData

                        def insertBLOB(name1, dob1, gender1, age1, phone_no1, aadhaar_no1, aadhaar_photo1, voter_id1, voter_id_photo1):
                            try:
                                connection = mysql.connector.connect(
                                    host = "localhost",
                                    user = "root",
                                    passwd = "xxxxxx",
                                    database = "app_database")

                                cursor = connection.cursor()
                                sql_insert_blob_query = """ INSERT INTO app_user_details
                                                (name,dob,gender,age,phone_no,aadhaar_no,aadhaar_photo,voter_id,voter_id_photo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

                                empPicture = convertToBinaryData(aadhaar_photo1)
                                empPicture1 = convertToBinaryData(voter_id_photo1)

                                # Convert data into tuple format
                                insert_blob_tuple = (name1, dob1, gender1, age1, phone_no1, aadhaar_no1, empPicture, voter_id1, empPicture1)
                                result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
                                connection.commit()

                            except mysql.connector.Error as error:
                                print("Failed inserting data into MySQL table {}".format(error))

                        insertBLOB(a,b,c,int(d),e,f,r'E:\BCA\Project\Coding\Database Retrieved Images\aadhaar_db.png',g,r'E:\BCA\Project\Coding\Database Retrieved Images\voter_db.png')
                        Thread(target=otp_verification).start()
                        
                    else :
                        messagebox.showerror('Error','Not a Valid User',parent=base)
                        base.destroy()
                        root.destroy()

            except mysql.connector.Error as error:
                print("Failed to read data from MySQL table {}".format(error))

            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()

        def verifywithdatabase():
            Lb1.insert(6,'Verifying the Entered Details & Documents with the Database.')
            Lb1.insert(7,'PLEASE WAIT FOR A MOMENT...')
            messagebox.showinfo('Verifying','Verifying the Entered Details & Documents with the Database',parent=base)
            pb1['value'] = 0
            base.update_idletasks()
            time.sleep(0.1)
            pb1['value'] += 5
            base.update_idletasks()
            time.sleep(0.1)
            a,b,c,d,e,f,g = entered_details()
            readBLOB(g, r"E:\BCA\Project\Coding\Database Retrieved Images\aadhaar_db.png", r"E:\BCA\Project\Coding\Database Retrieved Images\voter_db.png")
            

        def otp_verification():
            otp_win = Toplevel(base) 
            otp_win.title("Verification")
            otp_win.geometry("+620+350")
            root.call('wm', 'iconphoto', otp_win._w, PhotoImage(file='icons/password.png'))
            otp_win.resizable(width = False, height = False)

            otp = random.randint(100000,999999)
            print(otp)

            account_sid = 'AC4ef5fbcbd4c5b0d81d630fd11904fc47'
            auth_token = 'd74f1ed92ec68c3ad16a50593504ab1d'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                    body='Your OTP is - ' + str(otp),
                    from_='+17012053469',
                    to='+917837324670'
                )

            def verifyotp():
                x = enterotp.get()
                if(str(x)==str(otp)):
                    messagebox.showinfo('Success', 'Please proceed to vote.', parent=otp_win)
                    otp_win.destroy()
                    base.iconify()
                    votingwin = Toplevel(root)
                    votingwin.title("Vote")
                    votingwin.geometry("1920x1080")
                    votingwin.resizable(width = True, height = True)
                    votingwin.state("zoomed")
                    root.call('wm', 'iconphoto', votingwin._w, PhotoImage(file='icons/votingg.png'))
                    
                    bg1=Image.open('Labels and Backgrounds/vote2.png')
                    bg1 = bg1.resize((1555, 970), Image.ANTIALIAS)
                    bg1 = ImageTk.PhotoImage(bg1)   
                    panel = Label(votingwin, image = bg1)      
                    panel.image = bg1
                    panel.place(x=-15,y=-30)

                    bg2=Image.open('Labels and Backgrounds/choose.png')
                    bg2 = ImageTk.PhotoImage(bg2)   
                    panel = Label(votingwin, image = bg2, bg="white")      
                    panel.image = bg2
                    panel.place(x=230,y=35)

                    style = ttk.Style(votingwin)

                    def entervote():
                        vote1 = vote.get()
                        if vote1 == 0:
                            messagebox.showerror('Alert', "No Party Selected!", parent=votingwin)
                        else:
                            res = messagebox.askyesno('Prompt', 'Are you sure?', parent=votingwin) 
                            if res == True:
                                try:
                                    connection = mysql.connector.connect(
                                        host = "localhost",
                                        user = "root",
                                        passwd = "xxxxxx",
                                        database = "app_database")
                                    
                                    a,b,c,d,e,f,g = entered_details()

                                    cursor = connection.cursor()
                                    sql = "UPDATE app_user_details SET vote = %s WHERE name=%s"
                                    val = (vote1,a)
                                    result = cursor.executemany(sql,(val,))
                                    connection.commit()

                                except mysql.connector.Error as error:
                                    print("Failed inserting data into MySQL table {}".format(error))

                                messagebox.showinfo('Congratulations', "You've Successfully Voted", parent=votingwin)
                                votingwin.destroy()
                                base.destroy()
                                root.destroy()
                            else:
                                messagebox.showinfo('Alert', "Please choose the party you want to vote for", parent=votingwin)


                    vote = IntVar()

                    blank_label = Label(votingwin,text="", font=("Calibri",22), bg = "white").grid(row=0,column=0,pady=30)

                    #BJP
                    img = Image.open(r'E:\BCA\Project\Coding\logos\bjp.png')
                    img = img.resize((100, 100), Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(img)   
                    panel = Label(votingwin, image = img, bg = "white")      
                    panel.image = img
                    panel.grid(row=1,column=0,padx=70,pady=10)
                    input1 = ttk.Radiobutton(votingwin, text="Bhartiya Janata Party", variable=vote, value="1")
                    input1.grid(row=1,column=1)

                    style_name = input1.winfo_class()
                    style.configure(style_name, background="white")

                    #Bahujan
                    img = Image.open(r'E:\BCA\Project\Coding\logos\bahujan.png')
                    img = img.resize((110, 100), Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(img)   
                    panel = Label(votingwin, image = img, bg = "white")      
                    panel.image = img
                    panel.grid(row=2,column=0,pady=10)
                    input2 = ttk.Radiobutton(votingwin, text="Bahujan Samaj Party", variable=vote, value="2").grid(row=2,column=1)

                    # Lok
                    img = Image.open(r'E:\BCA\Project\Coding\logos\lok.png')
                    img = img.resize((130, 100), Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(img)   
                    panel = Label(votingwin, image = img, bg = "white")      
                    panel.image = img
                    panel.grid(row=3,column=0,pady=10)
                    input3 = ttk.Radiobutton(votingwin, text="Lok Janshakti Party", variable=vote, value="3").grid(row=3,column=1)

                    #DMK
                    img = Image.open(r'E:\BCA\Project\Coding\logos\DMK.png')
                    img = img.resize((100, 100), Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(img)   
                    panel = Label(votingwin, image = img, bg = "white")      
                    panel.image = img
                    panel.grid(row=4,column=0,pady=10)
                    input4 = ttk.Radiobutton(votingwin, text="Dravida Munnetra Kazhagam", variable=vote, value="4").grid(row=4,column=1)

                    # CPI
                    img = Image.open(r'E:\BCA\Project\Coding\logos\CPI.png')
                    img = img.resize((130, 100), Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(img)   
                    panel = Label(votingwin, image = img, bg = "white")      
                    panel.image = img
                    panel.grid(row=5,column=0,pady=10)
                    input5 = ttk.Radiobutton(votingwin, text="Communist Party of India", variable=vote, value="5").grid(row=5,column=1)

                    # COLUMN CHANGE
                    blank_label = Label(votingwin,text="", font=("Calibri",18), bg = "white").grid(row=1,column=2,padx = 50)

                    #YSR
                    img = Image.open(r'E:\BCA\Project\Coding\logos\YSR.jpg')
                    img = img.resize((150, 100), Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(img)   
                    panel = Label(votingwin, image = img, bg = "white")      
                    panel.image = img
                    panel.grid(row=1,column=3,pady=10)
                    input6 = ttk.Radiobutton(votingwin, text="Yuvajana Sramika Rythu Congress Party", variable=vote, value="6")
                    input6.grid(row=1,column=4)

                    #Congress
                    img = Image.open(r'E:\BCA\Project\Coding\logos\congress.png')
                    img = img.resize((100, 100), Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(img)   
                    panel = Label(votingwin, image = img, bg = "white")      
                    panel.image = img
                    panel.grid(row=2,column=3)
                    input7 = ttk.Radiobutton(votingwin, text="Indian National Congress", variable=vote, value="7").grid(row=2,column=4)

                    #Janata Dal
                    img = Image.open(r'E:\BCA\Project\Coding\logos\JanataDal.png')
                    img = img.resize((140, 100), Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(img)   
                    panel = Label(votingwin, image = img, bg = "white")      
                    panel.image = img
                    panel.grid(row=3,column=3,pady=10)
                    input8 = ttk.Radiobutton(votingwin, text="Janata Dal", variable=vote, value="8").grid(row=3,column=4)

                    #Shiv Sena
                    img = Image.open(r'E:\BCA\Project\Coding\logos\ShivSena.png')
                    img = img.resize((100, 100), Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(img)   
                    panel = Label(votingwin, image = img, bg = "white")      
                    panel.image = img
                    panel.grid(row=4,column=3,pady=10)
                    input9 = ttk.Radiobutton(votingwin, text="Shiv Sena", variable=vote, value="9").grid(row=4,column=4)

                    #Biju
                    img = Image.open(r'E:\BCA\Project\Coding\logos\biju.png')
                    img = img.resize((140, 100), Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(img)   
                    panel = Label(votingwin, image = img, bg = "white")      
                    panel.image = img
                    panel.grid(row=5,column=3,pady=10)
                    input10 = ttk.Radiobutton(votingwin, text="Biju Janata Dal", variable=vote, value="10").grid(row=5,column=4)

                    # COLUMN CHANGE
                    blank_label = Label(votingwin,text="", font=("Calibri",18), bg = "white").grid(row=1,column=5,padx = 30)

                    #NCP
                    img = Image.open(r'E:\BCA\Project\Coding\logos\NCP.png')
                    img = img.resize((100, 100), Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(img)   
                    panel = Label(votingwin, image = img, bg = "white")      
                    panel.image = img
                    panel.grid(row=1,column=6,pady=10)
                    input11 = ttk.Radiobutton(votingwin, text="Nationalist Congress Party", variable=vote, value="11").grid(row=1,column=7)

                    #Shiromani
                    img = Image.open(r'E:\BCA\Project\Coding\logos\shiromani.png')
                    img = img.resize((120, 100), Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(img)   
                    panel = Label(votingwin, image = img, bg = "white")      
                    panel.image = img
                    panel.grid(row=2,column=6,pady=10)
                    input12 = ttk.Radiobutton(votingwin, text="Shiromani Akali Dal", variable=vote, value="12").grid(row=2,column=7)

                    #AAP
                    img = Image.open(r'E:\BCA\Project\Coding\logos\aap.png')
                    img = img.resize((140, 100), Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(img)
                    panel = Label(votingwin, image = img, bg = "white")      
                    panel.image = img
                    panel.grid(row=3,column=6,pady=10)
                    input13 = ttk.Radiobutton(votingwin, text="AAP", variable=vote, value="13").grid(row=3,column=7)

                    # Samajwadi
                    img = Image.open(r'E:\BCA\Project\Coding\logos\samajwadi.png')
                    img = img.resize((180, 100), Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(img)   
                    panel = Label(votingwin, image = img, bg = "white")      
                    panel.image = img
                    panel.grid(row=4,column=6,pady=10)
                    input14 = ttk.Radiobutton(votingwin, text="Samajwadi Party", variable=vote, value="14").grid(row=4,column=7)

                    #AITC
                    img = Image.open(r'E:\BCA\Project\Coding\logos\AITC.png')
                    img = img.resize((150, 100), Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(img)   
                    panel = Label(votingwin, image = img, bg = "white")      
                    panel.image = img
                    panel.grid(row=5,column=6,pady=10)
                    input15 = ttk.Radiobutton(votingwin, text="All India Trinamool Congress", variable=vote, value="15").grid(row=5,column=7)

                    submit_btn = ttk.Button(votingwin, text ='Click Here to Lock Your Vote!', command = entervote)
                    submit_btn.place(x=650,y=725)
                else:
                    messagebox.showerror('Error', 'Incorrect OTP Entered.')

            enterotp = StringVar()
            Heading = Label(otp_win,text="Enter the OTP" ,font=("Calibri",14)).grid(row=0,column=0, padx = 15)
            input1 = ttk.Entry(otp_win, font=("Calibri",14), textvariable = enterotp, justify="center", width=10).grid(row=0,column=1,padx=20,pady=20)
            blank_label = Label(otp_win,text="", font=("Calibri",14),pady=15).grid(row=1,column=0)
            submit_btn = ttk.Button(otp_win, text ='Submit', command=verifyotp).place(x=110,y=80)

            messagebox.showinfo('Title', 'An OTP has been sent to your mobile number.', parent=otp_win)

            
        #BODY

        name = StringVar()  
        dob = StringVar()
        gender = StringVar()
        age = StringVar()
        phone = StringVar()
        aadhaar = StringVar()
        voter_no = StringVar()

        # Blank Label
        blank_label = Label(base,text="",bg = "#3d3a65" ,justify="right",anchor="e", font=("Calibri",14)).grid(row=0,column=0,padx=40,pady=105)

        # NAME
        FName_Label = Label(base,text="Enter Your Name", bg = "white" ,font=("Calibri",14)).grid(row=1,column=1)
        input1 = ttk.Entry(base, textvariable = name, font=("Calibri",14), justify="center")
        input1.grid(row=1,column=2,padx=20,pady=10)

        # DOB
        DateOB_Label = Label(base,text="Date of Birth (DD/MM/YYYY)" ,bg = "white" ,font=("Calibri",14)).grid(row=2,column=1)
        input2 = ttk.Entry(base, textvariable = dob, font=("Calibri",14), justify="center")
        input2.grid(row=2,column=2)

        # Gender
        Gender_Label = Label(base, text="Gender",bg = "white" ,font=("Calibri",14)).grid(row=3,column=1,pady=10)
        input3 = ttk.Radiobutton(base, text="Male", variable=gender, value="Male")
        input3.place(x=320,y=352)
        input4 = ttk.Radiobutton(base, text="Female", variable=gender, value="Female")
        input4.place(x=390,y=353)
        input9 = ttk.Radiobutton(base, text="Transgender", variable=gender, value="Transgender")
        input9.place(x=475,y=353)

        style_name = input3.winfo_class()
        style.configure(style_name, background="white")

        # Age
        Age_Label = Label(base,text="Age",bg = "white" ,font=("Calibri",14)).grid(row=4,column=1)
        input5 = ttk.Entry(base, textvariable = age, font=("Calibri",14), justify="center")
        input5.grid(row=4,column=2,pady=10)

        # Phone Number
        phone_Label = Label(base,text="Enter Your Phone Number",bg = "white" ,font=("Calibri",14)).grid(row=5,column=1)
        input6 = ttk.Entry(base, textvariable = phone, font=("Calibri",14), justify="center")
        input6.grid(row=5,column=2)

        # Aadhaar
        ad_label1 = Label(base, text="Adhaar Number \n (XXXX-XXXX-XXXX)",bg = "white" ,font=("Calibri",14)).grid(row=6,column=1)
        input7 = ttk.Entry(base, textvariable = aadhaar, font=("Calibri",14), justify="center")
        input7.grid(row=6,column=2,pady=10)
        ad_label2 = Label(base, text="Adhaar Card",bg = "white" ,font=("Calibri",14)).grid(row=7,column=1)
        ad_upload_btn = ttk.Button(base, text ="Browse", command = aadhaar_upload)
        ad_upload_btn.grid(row=7,column=2)

        # Voter ID Card
        voter_label1 = Label(base, text="Voter ID Number",bg = "white" ,font=("Calibri",14)).grid(row=8,column=1)
        input8 = ttk.Entry(base, textvariable = voter_no, font=("Calibri",14), justify="center")
        input8.grid(row=8,column=2,pady=10)
        voter_label2 = Label(base,text="Voter ID Card",bg = "white", font=("Calibri",14)).grid(row=9,column=1)
        voter_upload_btn = ttk.Button(base, text ='Browse', command = voterid_upload)
        voter_upload_btn.grid(row=9,column=2)
        
        # Upload & Submit
        Upload_btn = ttk.Button(base, text ='Upload', command = entered_details_validation)
        Upload_btn.grid(row=10,column=1,pady=25)
        submit_btn = ttk.Button(base, text ='Submit', state = DISABLED, command = Thread(target = verifywithdatabase).start)
        submit_btn.grid(row=10,column=2)

        # Progress Bar
        pb1 = ttk.Progressbar(base, orient=HORIZONTAL, length=400, mode='determinate')
        pb1.place(x=130,y=730)

        style_name = pb1.winfo_class()
        style.configure(style_name, background="white")

        # Status
        Lb1 = Listbox(base,width=55,font=("Calibri",16),bg = 'white', height =7)
        Lb1.place(x=760,y=540)

        base.mainloop()

checkbox1 = IntVar()

guidelines_label = Label(root, text="* You should be an Indian citizen.\n* You must be above 18 years of age.\n* You can cast only one vote.\n* You must have valid Voter ID & Aadhaar card authorised by\n   the Government of India.\n* Please provide correct details as per the documents.\n* Elector Detail Fields are Case Sensitive.\n* Attempts to cast multiple votes or impersonate another\n   voter during the process will attract stern action.",justify="left",bg = "#eff0f1" ,font=("Calibri",20)).place(x=170,y=190)

check_box = ttk.Checkbutton(root, text = "I confirm that I have read and agree to the guidelines written above.", variable=checkbox1, onvalue = 1, offvalue = 0).place(x=270,y=560)
enter_btn = ttk.Button(root, text ='Proceed as an Elector', command = details_win)
enter_btn.place(x=330,y=600)
admin_btn = ttk.Button(root, text ='Proceed as an Administrator', state = NORMAL, command = admin_win)
admin_btn.place(x=500,y=600)


root.mainloop()


  


from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import random,os
import tempfile
import smtplib

def main():
    win=Tk()
    app=LoginWindow(win)
    win.mainloop()

class LoginWindow:
    def __init__(self,root):
        self.root=root
        self.root.title("Login")
        self.root.geometry("1550x800+0+0")
        

        
        #Set background image
        self.background=ImageTk.PhotoImage(file=r"C:\Users\Maha Minahil\OneDrive\Desktop\Login page\loginBookshop.jpe")
        lbl_bg=Label(self.root,image=self.background)
        lbl_bg.place(x=0,y=0,relwidth=1,relheight=1)
        #Create login frame
        frame=Frame(self.root,bg="black")
        frame.place(x=910,y=140,width=340,height=450)
        #login image resize
        img1=Image.open(r"C:\Users\Maha Minahil\OneDrive\Desktop\Login page\FCClogo.png")
        img1=img1.resize((100,100),Image.ANTIALIAS)
        self.photoimage1=ImageTk.PhotoImage(img1)
        lbimg1=Label(image=self.photoimage1,bg="white",borderwidth=0)
        lbimg1.place(x=1025,y=140,width=100,height=100)

        get_str=Label(frame,text="User Login",font=("times new roman",20,"bold"),fg="white",bg="black")
        get_str.place(x=100,y=100)

        #username label
        username=lbl=Label(frame,text="Username",font=("times new roman",15,"bold"),fg="white",bg="black")
        username.place(x=40,y=155)

        self.txtuser=ttk.Entry(frame,font=("times new roman",15,"bold"))
        self.txtuser.place(x=40,y=180,width=270)

        #password label
        password=lbl=Label(frame,text="Password",font=("times new roman",15,"bold"),fg="white",bg="black")
        password.place(x=40,y=225)

        self.txtpass=ttk.Entry(frame,show="*",font=("times new roman",15,"bold"))
        self.txtpass.place(x=40,y=250,width=270)

        #login button
        loginbtn=Button(frame,command=self.login,text="Login",font=("times new roman",15,"bold"),bd=3,relief=RIDGE,fg="white",bg="grey",activeforeground="white",activebackground="grey")
        loginbtn.place(x=115,y=300,width=120,height=35)

        #forget button
        loginbtn=Button(frame,text="Forgotten password?",command=self.forgetpasswordwin,font=("times new roman",10,"bold"),borderwidth=0,fg="white",bg="black",activeforeground="white",activebackground="black")
        loginbtn.place(x=98,y=340,width=160)

        #register button
        loginbtn=Button(frame,text="Create New Account",command=self.registerwindow,font=("times new roman",15,"bold"),bd=3,relief=RIDGE,fg="white",bg="grey",activeforeground="white",activebackground="grey")
        loginbtn.place(x=80,y=370,width=200,height=35)

    def registerwindow(self):
        self.newrwin=Toplevel(self.root)
        self.app=Register(self.newrwin)
        
    def login(self):
        if self.txtuser.get()=="" or self.txtpass.get()=="":
            messagebox.showerror("Error","All fields required.",parent=self.root)
        elif self.txtuser.get()=="minahil" and self.txtpass.get()=="maha":
             messagebox.showerror("Success","Welcome to the BookShop!",parent=self.root)
        else:
            conn=mysql.connector.connect(host="localhost",user="root",password="onedirection",database="books")
            mycursor=conn.cursor()
            mycursor.execute("select * from register where email=%s and password=%s",(self.txtuser.get(),self.txtpass.get()))
            row=mycursor.fetchone()
            if row==None:
                messagebox.showerror("Error","Invalid Username and password.",parent=self.root)
            else:
                open_main=messagebox.askyesno("YesNo","Access only Shopkeeper/Manager.",parent=self.root)
                if open_main>0:
                    self.newrwin=Toplevel(self.root)
                    self.app=Product(self.newrwin)
                else:
                    if not open_main:
                        return
            conn.commit()
            conn.close()
            
            

    #reset password
    def resetpass(self):
        if self.combo_security_Q.get()=="Select":
            messagebox.showerror("Error","Select the security question.",parent=self.root2)
        elif self.txt_securityA.get()=="":
            messagebox.showerror("Error","Please enter the security answer.",parent=self.root2)
        elif self.txt_newpass.get()=="":
            messagebox.showerror("Error","Please enter the new password.",parent=self.root2)
        else:
            conn=mysql.connector.connect(host="localhost",user="root",password="onedirection",database="books")
            mycursor=conn.cursor()
            qury=("select * from register where email=%s and securityQ=%s and securityA=%s")
            val=(self.txtuser.get(),self.combo_security_Q.get(),self.txt_securityA.get(),)
            mycursor.execute(qury,val)
            row=mycursor.fetchone()
            if row==None:
                messagebox.showerror("Error","Please enter the correct answer.",parent=self.root2)
            else:
                query=("update register set password=%s where email=%s")
                value=(self.txt_newpass.get(),self.txtuser.get())
                mycursor.execute(query,value)

                conn.commit()
                conn.close()
                messagebox.showinfo("Info","Your password has been reset.",parent=self.root2)
                self.root2.destroy()
            

    #forget password window
    def forgetpasswordwin(self):
        if self.txtuser.get()=="":
            messagebox.showerror("Error","Please enter the email address to reset password.",parent=self.root)
        else:
            conn=mysql.connector.connect(host="localhost",user="root",password="onedirection",database="books")
            mycursor=conn.cursor()
            query=("select * from register where email=%s")
            value=(self.txtuser.get(),)
            mycursor.execute(query,value)
            row=mycursor.fetchone()
            #print(row)
            if row==None:
                messagebox.showerror("Error","Please enter the valid user name.",parent=self.root)
            else:
                conn.close()
                self.root2=Toplevel()
                self.root2.title("Forget Password")
                self.root2.geometry("340x450+610+170")

                l=Label(self.root2,text="Forget Password",font=("times new roman",20,"bold"),fg="black",bg="white")
                l.place(x=0,y=10,relwidth=1)

                security_Q=Label(self.root2,text="Security Question",font=("times new roman",15,"bold"),bg="white",fg="black")
                security_Q.place(x=50,y=80)
        
                self.combo_security_Q=ttk.Combobox(self.root2,font=("times new roman",15,"bold"),state="readonly")
                self.combo_security_Q["values"]=("Select","In what city were you born?","What is the name of your favourite pet?","What high school did you attend?")
                self.combo_security_Q.place(x=50,y=110,width=250)
                self.combo_security_Q.current(0)

                security_A=Label(self.root2,text="Security Answer",font=("times new roman",15,"bold"),bg="white",fg="black")
                security_A.place(x=50,y=150)

                self.txt_securityA=ttk.Entry(self.root2,font=("times new roman",15))
                self.txt_securityA.place(x=50,y=180,width=250)

                newpass=Label(self.root2,text="New Password",font=("times new roman",15,"bold"),bg="white",fg="black")
                newpass.place(x=50,y=220)

                self.txt_newpass=ttk.Entry(self.root2,font=("times new roman",15))
                self.txt_newpass.place(x=50,y=250,width=250)

                btn=Button(self.root2,text="Reset",command=self.resetpass,font=("times new roman",15,"bold"),fg="white",bg="grey")
                btn.place(x=140,y=290)
            
                                     
            

class Register:
    def __init__(self,root):
        self.root=root
        self.root.title("Register")
        self.root.geometry("1600x900+0+0")
        self.v_fname=StringVar()
        self.v_lname=StringVar()
        self.v_contact=StringVar()
        self.v_email=StringVar()
        self.v_securityQ=StringVar()
        self.v_securityA=StringVar()
        self.v_pass=StringVar()
        self.v_cpass=StringVar()
        self.v_checkb=IntVar()
        self.v_jobtitle=StringVar()
        self.v_gender=StringVar()

        #background image
        self.bg=ImageTk.PhotoImage(file=r"C:\Users\Maha Minahil\OneDrive\Desktop\Login page\registerBookshop.jpeg")
        bg_lbl=Label(self.root,image=self.bg)
        bg_lbl.place(x=0,y=0,relwidth=1,relheight=1)

        #left image
        self.bg1=ImageTk.PhotoImage(file=r"C:\Users\Maha Minahil\OneDrive\Desktop\Login page\Goodbook.jpg")
        bg_lbl=Label(self.root,image=self.bg1)
        bg_lbl.place(x=50,y=100,width=450,height=550)

        #main frame
        frame=Frame(self.root,bg="black")
        frame.place(x=500,y=100,width=800,height=550)

        register_lbl=Label(frame,text="Registeration",font=("times new roman",20,"bold"),fg="white",bg="black")
        register_lbl.place(x=20,y=20)

        #entry label
        #--ROW 1--
        fname=Label(frame,text="First Name",font=("times new roman",15,"bold"),fg="white",bg="black")
        fname.place(x=50,y=70)

        self.fname_entry=ttk.Entry(frame,textvariable=self.v_fname,font=("times new roman",15))
        self.fname_entry.place(x=50,y=100,width=250)

        l_name=Label(frame,text="Last Name",font=("times new roman",15,"bold"),fg="white",bg="black")
        l_name.place(x=370,y=70)

        self.txt_lname=ttk.Entry(frame,textvariable=self.v_lname,font=("times new roman",15))
        self.txt_lname.place(x=370,y=100,width=250)

        #-ROW 2--
        contact=Label(frame,text="Contact",font=("times new roman",15,"bold"),fg="white",bg="black")
        contact.place(x=50,y=130)

        self.txt_contact=ttk.Entry(frame,textvariable=self.v_contact,font=("times new roman",15))
        self.txt_contact.place(x=50,y=160,width=250)

        email=Label(frame,text="Email",font=("times new roman",15,"bold"),fg="white",bg="black")
        email.place(x=370,y=130)

        self.txt_email=ttk.Entry(frame,textvariable=self.v_email,font=("times new roman",15))
        self.txt_email.place(x=370,y=160,width=250)

        #__ROW 3__
        security_Q=Label(frame,text="Security Question",font=("times new roman",15,"bold"),bg="black",fg="white")
        security_Q.place(x=50,y=190)
        
        self.combo_security_Q=ttk.Combobox(frame,textvariable=self.v_securityQ,font=("times new roman",15,"bold"),state="readonly")
        self.combo_security_Q["values"]=("Select","In what city were you born?","What is the name of your favourite pet?","What high school did you attend?")
        self.combo_security_Q.place(x=50,y=220,width=250)
        self.combo_security_Q.current(0)

        security_A=Label(frame,text="Security Answer",font=("times new roman",15,"bold"),bg="black",fg="white")
        security_A.place(x=370,y=190)

        self.txt_securityA=ttk.Entry(frame,textvariable=self.v_securityA,font=("times new roman",15))
        self.txt_securityA.place(x=370,y=220,width=250)

        #__ROW 4__
        pswd=Label(frame,text="Password",font=("times new roman",15,"bold"),bg="black",fg="white")
        pswd.place(x=50,y=250)

        self.txt_pswd=ttk.Entry(frame,show="*",textvariable=self.v_pass,font=("times new roman",15))
        self.txt_pswd.place(x=50,y=280,width=250)

        cpswd=Label(frame,text="Confirm Password",font=("times new roman",15,"bold"),bg="black",fg="white")
        cpswd.place(x=370,y=250)

        self.txt_cpswd=ttk.Entry(frame,show="*",textvariable=self.v_cpass,font=("times new roman",15))
        self.txt_cpswd.place(x=370,y=280,width=250)

        #__ROW 5__
        jobtitle=Label(frame,text="Job Title",font=("times new roman",15,"bold"),bg="black",fg="white")
        jobtitle.place(x=50,y=310)
        
        self.combo_jobtitle=ttk.Combobox(frame,textvariable=self.v_jobtitle,font=("times new roman",15,"bold"),state="readonly")
        self.combo_jobtitle["values"]=("Select","Shopkeeper","Manager")
        self.combo_jobtitle.place(x=50,y=340,width=250)
        self.combo_jobtitle.current(0)

        gender=Label(frame,text="Gender",font=("times new roman",15,"bold"),bg="black",fg="white")
        gender.place(x=370,y=310)
        
        self.combo_gender=ttk.Combobox(frame,textvariable=self.v_gender,font=("times new roman",15,"bold"),state="readonly")
        self.combo_gender["values"]=("Select","Male","Female")
        self.combo_gender.place(x=370,y=340,width=250)
        self.combo_gender.current(0)

        #check button
        checkbtn=Checkbutton(frame,variable=self.v_checkb,text="I agree to the Terms and Conditions and the Privacy Policy.",font=("times new roman",10,"bold"),onvalue=1,offvalue=0)
        checkbtn.place(x=50,y=390)

        #register button
        register_btn=Button(frame,command=self.register_data,text="Sign Up",font=("times new roman",15,"bold"),bd=3,relief=RIDGE,fg="white",bg="grey",activeforeground="white",activebackground="grey")
        register_btn.place(x=250,y=450,width=200,height=35)

        #login button
        login_btn=Button(frame,text="Already have an account?",command=self.returnlogin,font=("times new roman",10,"bold"),borderwidth=0,fg="white",bg="black",activeforeground="white",activebackground="black")
        login_btn.place(x=200,y=490,width=300)

    #register function
    def register_data(self):
        if self.v_fname.get()=="" or self.v_lname.get()=="" or self.v_email.get()=="" or self.v_contact.get()=="" or self.v_securityQ.get()=="Select" or self.v_securityA.get()=="" or self.v_jobtitle.get()=="Select" or self.v_gender.get()=="Select":
            messagebox.showerror("Error","All fields are required.",parent=self.root)
        elif self.v_pass.get()!=self.v_cpass.get():
            messagebox.showerror("Error","Password and Confirm Password must be same.",parent=self.root)
        elif self.v_checkb.get()==0:
            messagebox.showerror("Error","Please agree our terms and conditions to proceed.",parent=self.root)
        else:
            conn=mysql.connector.connect(host="localhost",user="root",password="onedirection",database="books")
            mycursor=conn.cursor()
            query=("select * from register where email=%s")
            value=(self.v_email.get(),)
            mycursor.execute(query,value)
            row=mycursor.fetchone()
            if row!=None:
                messagebox.showerror("Error","User already exist,please try another email.",parent=self.root)
            else:
                mycursor.execute("insert into register values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.v_fname.get(),self.v_lname.get(),self.v_contact.get(),self.v_email.get(),self.v_securityQ.get(),self.v_securityA.get(),self.v_pass.get(),self.v_jobtitle.get(),self.v_gender.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success","Registered Successfully",parent=self.root)

    def returnlogin(self):
       self.root.destroy()


class Product:
   def __init__(self,root):
      self.root=root
      self.root.title("Bookshop Management System")
      self.root.geometry("1480x800+0+0")
     

      #Additemvariable
      self.addproduct_var=StringVar()
      self.refproduct_var=StringVar()

      #Mainvariable
      self.ref_var=StringVar()
      self.cmpName_var=StringVar()
      self.typeprod_var=StringVar()
      self.prodname_var=StringVar()
      self.lot_var=StringVar()
      self.prodqty_var=StringVar()
      self.prodprice_var=StringVar()
      
      
      
      lbltitle=Label(self.root,text="Bookshop Management System",bd=15,relief=RIDGE,bg='black',fg="white",font=("times new roman",50,"bold"),padx=2,pady=4)
      lbltitle.pack(side=TOP,fill=X)


      img1=Image.open(r"C:\Users\Maha Minahil\OneDrive\Desktop\Login page\book\blob.jpeg")
      img1=img1.resize((80,80),Image.ANTIALIAS)
      self.photoimg1=ImageTk.PhotoImage(img1)
      b1=Button(self.root,image=self.photoimg1,borderwidth=0)
      b1.place(x=70,y=20)

      #DataFrame
      DataFrame=Frame(self.root,bd=15,relief=RIDGE,padx=20,bg="black")
      DataFrame.place(x=0,y=120,width=1535,height=410)

      DataFrameLeft=LabelFrame(DataFrame,bd=10,relief=RIDGE,padx=20,text="Product Information",fg="lightblue",font=("arial",12,"bold"),bg="black")
      DataFrameLeft.place(x=0,y=5,width=740,height=300)
      

      DataFrameRight=LabelFrame(DataFrame,bd=10,relief=RIDGE,padx=20,text="Add Product department",fg="lightblue",font=("arial",12,"bold"),bg="black")
      DataFrameRight.place(x=750,y=5,width=715,height=300)

      #ButtonFrame
      ButtonFrame=Frame(self.root,bd=15,relief=RIDGE,padx=20)
      ButtonFrame.place(x=0,y=470,width=1535,height=65)

      #MainButton
      btnAddData=Button(ButtonFrame,command=self.add_data,text="Add product",font=("arial",13,"bold"),width=12,bg="black",fg="white")
      btnAddData.grid(row=0,column=0)
      
      btnUpdateBook=Button(ButtonFrame,command=self.Update,text="Update product",font=("arial",12,"bold"),width=12,bg="black",fg="white")
      btnUpdateBook.grid(row=0,column=1)

      btnDeleteBook=Button(ButtonFrame,command=self.Delete,text="Delete product",font=("arial",12,"bold"),width=12,bg="black",fg="white")
      btnDeleteBook.grid(row=0,column=2)

      btnRestBook=Button(ButtonFrame,command=self.reset,text="Reset",font=("arial",13,"bold"),width=12,bg="black",fg="white")
      btnRestBook.grid(row=0,column=3)

      #bill button
      btnExitBook=Button(ButtonFrame,command=self.Makebill,text="Make bill",font=("arial",13,"bold"),width=12,bg="black",fg="white")
      btnExitBook.grid(row=0,column=4)

      #SearchBy
      lblSearch=Label(ButtonFrame,font=("arial",17,"bold"),text="Search by",padx=2,bg="darkblue",fg="white")
      lblSearch.grid(row=0,column=5,sticky=W)

      
      #variable
      self.search_var=StringVar()
      serch_combo=ttk.Combobox(ButtonFrame,textvariable=self.search_var,width=10,font=("arial",16,"bold"),state="readonly")
      serch_combo["values"]=("Ref_no","ProdName","LotNo")
      serch_combo.grid(row=0,column=6)
      serch_combo.current(0)

      self.searchTxt_var=StringVar()
      txtSerch=Entry(ButtonFrame,textvariable=self.searchTxt_var,bd=3,relief=RIDGE,width=22,font=("arial",17,"bold"))
      txtSerch.grid(row=0,column=7)

      searchBtn=Button(ButtonFrame,command=self.search_data,text="SEARCH",font=("arial",13,"bold"),width=12,bg="black",fg="white")
      searchBtn.grid(row=0,column=8)

      showAll=Button(ButtonFrame,command=self.fetch_data,text="SHOW ALL",font=("arial",13,"bold"),width=13,bg="black",fg="white")
      showAll.grid(row=0,column=9)

      #Labelandentry
      #DataLeftFrame
      lblrefno=Label(DataFrameLeft,font=("arial",12,"bold"),text="Reference No",padx=2,bg="black",fg="white")
      lblrefno.place(x=0,y=0)

      conn=mysql.connector.connect(host="localhost",user="root",password="onedirection",database="books")
      my_cursor=conn.cursor()
      my_cursor.execute("select Ref from bookch")
      row=my_cursor.fetchall()

                                                                                 

      ref_combo=ttk.Combobox(DataFrameLeft,textvariable=self.ref_var,width=27,font=("arial",12,"bold"),state="readonly")
      ref_combo["values"]=row
      ref_combo.place(x=200,y=0)
      ref_combo.current(0)
      
      lblcompany=Label(DataFrameLeft,font=("arial",12,"bold"),text="Company/Author name",padx=2,bg="black",fg="white")
      lblcompany.place(x=2,y=30)

      txtSerch1=Entry(DataFrameLeft,textvariable=self.cmpName_var,bd=3,relief=RIDGE,width=27,font=("arial",13,"bold"))
      txtSerch1.place(x=200,y=30)

      
      lbltype=Label(DataFrameLeft,font=("arial",12,"bold"),text="Type of Product",padx=2,bg="black",fg="white")
      lbltype.place(x=2,y=62)

      ref_combo=ttk.Combobox(DataFrameLeft,textvariable=self.typeprod_var,width=27,font=("arial",12,"bold"),state="readonly")
      ref_combo["values"]=("Book","Stationery","Mobile","Uniform")
      ref_combo.place(x=200,y=62)
      ref_combo.current(0)
      
      #Additem
      lblitemname=Label(DataFrameLeft,font=("arial",12,"bold"),text="Product/Book name",padx=2,bg="black",fg="white")
      lblitemname.place(x=2,y=92)

      conn=mysql.connector.connect(host="localhost",user="root",password="onedirection",database="books")
      my_cursor=conn.cursor()
      my_cursor.execute("select ProductName from bookch")
      pro=my_cursor.fetchall()

         
      itemname_combo=ttk.Combobox(DataFrameLeft,textvariable=self.prodname_var,width=27,font=("arial",12,"bold"),state="readonly")
      itemname_combo["values"]=pro
      itemname_combo.place(x=200,y=92)
      itemname_combo.current(0)

      lbllotno=Label(DataFrameLeft,font=("arial",12,"bold"),text="Lot no",padx=2,bg="black",fg="white")
      lbllotno.place(x=2,y=122)


      txtSerch1=Entry(DataFrameLeft,textvariable=self.lot_var,bd=3,relief=RIDGE,width=27,font=("arial",13,"bold"))
      txtSerch1.place(x=200,y=122)

      lblquantity=Label(DataFrameLeft,font=("arial",12,"bold"),text="Product Qty",padx=2,bg="black",fg="white")
      lblquantity.place(x=2,y=154)

      txtSerch2=Entry(DataFrameLeft,textvariable=self.prodqty_var,bd=3,relief=RIDGE,width=27,font=("arial",13,"bold"))
      txtSerch2.place(x=200,y=154)

      lblprice=Label(DataFrameLeft,font=("arial",12,"bold"),text="Product price",padx=2,bg="black",fg="white")
      lblprice.place(x=2,y=186)

      txtSerch2=Entry(DataFrameLeft,textvariable=self.prodprice_var,bd=3,relief=RIDGE,width=27,font=("arial",13,"bold"))
      txtSerch2.place(x=200,y=186)


      img3=Image.open(r"C:\Users\Maha Minahil\OneDrive\Desktop\Login page\book\stationary.jpeg")
      img3=img3.resize((200,240),Image.ANTIALIAS)
      self.photoimg3=ImageTk.PhotoImage(img3)
      b1=Button(self.root,image=self.photoimg3,borderwidth=0)
      b1.place(x=550,y=170)
      

      #DataRightFrame
      img4=Image.open(r"C:\Users\Maha Minahil\OneDrive\Desktop\Login page\book\stationeryitem.png")
      img4=img4.resize((220,125),Image.ANTIALIAS)
      self.photoimg4=ImageTk.PhotoImage(img4)
      b1=Button(self.root,image=self.photoimg4,borderwidth=0)
      b1.place(x=1260,y=160)

      img2=Image.open(r"C:\Users\Maha Minahil\OneDrive\Desktop\Login page\book\booksbg.jpeg")
      img2=img2.resize((220,133),Image.ANTIALIAS)
      self.photoimg2=ImageTk.PhotoImage(img2)
      b1=Button(self.root,image=self.photoimg2,borderwidth=0)
      b1.place(x=1260,y=290)

      lblrefno=Label(DataFrameRight,font=("arial",12,"bold"),text="Reference No:",padx=15,pady=6,fg="white",bg="black")
      lblrefno.place(x=0,y=0)
      textrefno=Entry(DataFrameRight,textvariable=self.refproduct_var,font=("arial",12,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
      textrefno.place(x=149,y=0)

      lblitemname=Label(DataFrameRight,font=("arial",12,"bold"),text="Product Name:",fg="white",bg="black")
      lblitemname.place(x=15,y=30)
      textitemname=Entry(DataFrameRight,textvariable=self.addproduct_var,font=("arial",12,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
      textitemname.place(x=149,y=30)


      #sideframe
      side_frame=Frame(DataFrameRight,bd=4,relief=RIDGE,bg="white")
      side_frame.place(x=0,y=80,width=290,height=160)

      sc_x=ttk.Scrollbar(side_frame,orient=HORIZONTAL)
      sc_x.pack(side=BOTTOM,fill=X)
      sc_y=ttk.Scrollbar(side_frame,orient=VERTICAL)
      sc_y.pack(side=RIGHT,fill=Y)

      self.item_table=ttk.Treeview(side_frame,column=("ref","itemname"),xscrollcommand=sc_x.set,yscrollcommand=sc_y.set)
      
      sc_x.config(command=self.item_table.xview)
      sc_y.config(command=self.item_table.yview)

      self.item_table.heading("ref",text="Ref")
      self.item_table.heading("itemname",text="Product name")

      self.item_table["show"]="headings"
      self.item_table.pack(fill=BOTH,expand=1)

      self.item_table.column("ref",width=100)
      self.item_table.column("itemname",width=100)

      self.item_table.bind("<ButtonRelease-1>",self.productget_cursor)

      #ItemAddButtons
      down_frame=Frame(DataFrameRight,bd=4,relief=RIDGE,bg="darkgreen")
      down_frame.place(x=300,y=80,width=135,height=160)

      btnAdditem=Button(down_frame,text="ADD",command=self.Additem,font=("arial",12,"bold"),width=12,bg="lime",fg="white",pady=4)
      btnAdditem.grid(row=0,column=0)

      btnUpdateitem=Button(down_frame,text="UPDATE",command=self.Updateproduct,font=("arial",12,"bold"),width=12,bg="purple",fg="white",pady=4)
      btnUpdateitem.grid(row=1,column=0)

      btnDeleteitem=Button(down_frame,text="DELETE",command=self.Deleteproduct,font=("arial",12,"bold"),width=12,bg="red",fg="white",pady=4)
      btnDeleteitem.grid(row=2,column=0)

      btnCLearitem=Button(down_frame,text="CLEAR",command=self.Clearproduct,font=("arial",12,"bold"),width=12,bg="orange",fg="white",pady=4)
      btnCLearitem.grid(row=3,column=0)


      #FrameDetails
      Framedetails=Frame(self.root,bd=15,relief=RIDGE)
      Framedetails.place(x=0,y=530,width=1530,height=260)

      #Maintableandscrollbar
      Table_frame=Frame(Framedetails,bd=15,relief=RIDGE,padx=20)
      Table_frame.place(x=0,y=1,width=1500,height=230)
      
      scroll_x=ttk.Scrollbar(Table_frame,orient=HORIZONTAL)
      scroll_x.pack(side=BOTTOM,fill=X)
      scroll_y=ttk.Scrollbar(Table_frame,orient=VERTICAL)
      scroll_y.pack(side=RIGHT,fill=Y)

      self.bookshop_table=ttk.Treeview(Table_frame,column=("ref","company/authorname","type","item/bookname","lotno","itemquantity","itemprice"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
      scroll_x.pack(side=BOTTOM,fill=X)
      scroll_y.pack(side=RIGHT,fill=Y)

      scroll_x.config(command=self.bookshop_table.xview)
      scroll_y.config(command=self.bookshop_table.yview)

      self.bookshop_table["show"]="headings"

      self.bookshop_table.heading("ref",text="Reference No")
      self.bookshop_table.heading("company/authorname",text="Company/Author name")
      self.bookshop_table.heading("type",text="Type of Product")
      self.bookshop_table.heading("item/bookname",text="Product/Book name")
      self.bookshop_table.heading("lotno",text="Lot No")
      self.bookshop_table.heading("itemquantity",text="Product quantity")
      self.bookshop_table.heading("itemprice",text="Product price")
      self.bookshop_table.pack(fill=BOTH,expand=1)

      self.bookshop_table.column("ref",width=100)
      self.bookshop_table.column("company/authorname",width=100)
      self.bookshop_table.column("type",width=100)
      self.bookshop_table.column("item/bookname",width=100)
      self.bookshop_table.column("lotno",width=100)
      self.bookshop_table.column("itemquantity",width=100)
      self.bookshop_table.column("itemprice",width=100)
      self.fetch_dataproduct()
      self.fetch_data()
      self.bookshop_table.bind("<ButtonRelease-1>",self.get_cursor)



      #AddItemFunctionalityDeclaration
   def Additem(self):
         conn=mysql.connector.connect(host="localhost",user="root",password="onedirection",database="books")
         my_cursor=conn.cursor()
         my_cursor.execute("insert into bookch(Ref,ProductName) values(%s,%s)",(

                                                                                 self.refproduct_var.get(),
                                                                                 self.addproduct_var.get(),

                                                                               ))
         conn.commit()
         self.fetch_dataproduct()
         messagebox.showinfo("Sucess","Product Added",parent=self.root)
         self.productget_cursor()
         conn.close()
         

   def fetch_dataproduct(self):
         conn=mysql.connector.connect(host="localhost",user="root",password="onedirection",database="books")
         my_cursor=conn.cursor()
         my_cursor.execute("select * from bookch")
         rows=my_cursor.fetchall()
         if len(rows)!=0:
            self.item_table.delete(*self.item_table.get_children())
            for i in rows:
               self.item_table.insert("",END,values=i)
            conn.commit()
         conn.close()

   #ItemGetcursor
   def productget_cursor(self,event=""):
         cursor_row=self.item_table.focus()
         content=self.item_table.item(cursor_row)
         row=content["values"]
         self.refproduct_var.set(row[0])     #error
         self.addproduct_var.set(row[1])

   def Updateproduct(self):
        if self.refproduct_var.get()=="" or self.addproduct_var.get()=="":
           messagebox.showerror("Error","All fields are Required",parent=self.root)
        else:
           conn=mysql.connector.connect(host="localhost",user="root",password="onedirection",database="books")
           my_cursor=conn.cursor()
           my_cursor.execute("update bookch set ProductName=%s where Ref=%s",(
                                                                               self.addproduct_var.get(),
                                                                               self.refproduct_var.get(),
                                                                              ))
           conn.commit()
           self.fetch_dataproduct()
           conn.close()

           messagebox.showinfo("Success","Product Updated",parent=self.root)
   
   def Deleteproduct(self):
           conn=mysql.connector.connect(host="localhost",user="root",password="onedirection",database="books")
           my_cursor=conn.cursor()

           sql="delete from bookch where Ref=%s"
           val=(self.refproduct_var.get(),)
           my_cursor.execute(sql,val)

           conn.commit()
           self.fetch_dataproduct()
           conn.close()
           messagebox.showinfo("Success","Product Deleted",parent=self.root)

   def Clearproduct(self):
          self.refproduct_var.set("")
          self.addproduct_var.set("")

   def Makebill(self):
       open_main=messagebox.askyesno("YesNo","Access only Shopkeeper.",parent=self.root)
       if open_main>0:
           self.newwin1=Toplevel(self.root)
           self.app1=Bill_App(self.newwin1)
       else:
           if not open_main:
               return
       

   #MainTable
   def add_data(self):
         if self.ref_var.get()=="" or self.lot_var.get()=="":
            messagebox.showerror("Error","All fields are required",parent=self.root)
         else:
            conn=mysql.connector.connect(host="localhost",user="root",password="onedirection",database="books")
            my_cursor=conn.cursor()
            my_cursor.execute("insert into bookrecord values(%s,%s,%s,%s,%s,%s,%s)",(
                                                                                      self.ref_var.get(),
                                                                                      self.cmpName_var.get(),
                                                                                      self.typeprod_var.get(),
                                                                                      self.prodname_var.get(),
                                                                                      self.lot_var.get(),
                                                                                      self.prodqty_var.get(),
                                                                                      self.prodprice_var.get(),
                                                                                    ))
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Success","Data has been inserted.",parent=self.root)

   def fetch_data(self):
      conn=mysql.connector.connect(host="localhost",user="root",password="onedirection",database="books")
      my_cursor=conn.cursor()
      my_cursor.execute("select * from bookrecord")
      row=my_cursor.fetchall()
      if len(row)!=0:
         self.bookshop_table.delete(*self.bookshop_table.get_children())
         for i in row:
            self.bookshop_table.insert("",END,values=i)
         conn.commit()
      conn.close()

   def get_cursor(self,eve=""):
         cursor_row=self.bookshop_table.focus()
         content=self.bookshop_table.item(cursor_row)
         row=content["values"]
         self.ref_var.set(row[0]),
         self.cmpName_var.set(row[1]),
         self.typeprod_var.set(row[2]),
         self.prodname_var.set(row[3]),
         self.lot_var.set(row[4]),
         self.prodqty_var.set(row[5]),
         self.prodprice_var.set(row[6])

   def Update(self):
      if self.ref_var.get()=="":
           messagebox.showerror("Error","All fields are Required.",parent=self.root)
      else:
           conn=mysql.connector.connect(host="localhost",user="root",password="onedirection",database="books")
           my_cursor=conn.cursor()
           my_cursor.execute("update bookrecord set CompName=%s,Typeprod=%s,ProdName=%s,LotNo=%s,ProdQty=%s,ProdPrice=%s where Ref_no=%s",(
                                                                                                                                          
                                                                                                                                            self.cmpName_var.get(),
                                                                                                                                            self.typeprod_var.get(),
                                                                                                                                            self.prodname_var.get(),
                                                                                                                                            self.lot_var.get(),
                                                                                                                                            self.prodqty_var.get(),
                                                                                                                                            self.prodprice_var.get(),
                                                                                                                                            self.ref_var.get(),
                                                                                                                                           ))
           conn.commit()
           self.fetch_data()
           conn.close()

           messagebox.showinfo("UPDATE","Record has been Updated Successfully.",parent=self.root)

   def Delete(self):
           conn=mysql.connector.connect(host="localhost",user="root",password="onedirection",database="books")
           my_cursor=conn.cursor()

           sql="delete from bookrecord where Ref_no=%s"
           val=(self.ref_var.get(),)
           my_cursor.execute(sql,val)

           conn.commit()
           self.fetch_data()
           conn.close()

           messagebox.showinfo("Delete","Record has been deleted.",parent=self.root)

   def reset(self):
         #self.ref_var.set("")
         self.cmpName_var.set(""),
         #self.typeprod_var.set(""),
         #self.prodname_var.set(""),
         self.lot_var.set(r""),
         self.prodqty_var.set(r""),
         self.prodprice_var.set(r"")

   def search_data(self):
        conn=mysql.connector.connect(host="localhost",user="root",password="onedirection",database="books")
        my_cursor=conn.cursor()
        my_cursor.execute("select * from bookrecord where "+str(self.search_var.get())+" LIKE '%"+self.searchTxt_var.get()+"%'")

        rows=my_cursor.fetchall()
        if len(rows)!=0:
           self.bookshop_table.delete(*self.bookshop_table.get_children())
           for i in rows:
              self.bookshop_table.insert("",END,values=i)
           conn.commit()
        conn.close()

class Bill_App:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1550x800+0+0")
        self.root.title("Bookshop Billing Software")


        #Variables
        self.prodqty=StringVar()
        self.c_name=StringVar()
        self.c_phon=StringVar()
        self.bill_no=StringVar()
        z=random.randint(1000,9999)
        self.bill_no.set(z)
        self.c_email=StringVar()
        self.search_bill=StringVar()
        self.product=StringVar()
        self.prices=IntVar()
        self.qty=IntVar()
        self.sub_total=StringVar()
        self.tax_input=StringVar()
        self.total=StringVar()

        #ProductCategorieslist
        self.Category=("Select Option","Books","Stationery","Mobiles","Uniform")
        self.SubCatBooks=["Classics","History","Science Fiction","Short Stories"]
        self.Classics=["ToKillaMockingbird","PrideandPrejudice"]
        self.price_TL=500
        self.price_PA=750
    
        
        self.History=["AModernHistory","PakistanHistoryandCulture"]
        self.price_AB=1800
        self.price_PC=2500
        
        self.ScienceFiction=["Frankenstein","TheAngryEspers"]
        self.price_FS=1000
        self.price_TJ=850
        
        self.ShortStories=["TheLottery","HowtoBecomeaWriter"]
        self.price_TJ2=950
        self.price_HM=1050


        
        self.SubCatStationery=["Pencil","Pen","Eraser","Glue","Notebook"]
        self.Pencil=["Dollar","Deer","Faber-Castell"]
        self.price_DR=15
        self.price_DER=10
        self.price_FC=17
        
        self.Pen=["PIANO"]
        self.price_PO=13

        self.Eraser=["Pelikan","FaberCastell"]
        self.PN=20
        self.FCL=25

        self.Glue=["UHU","Stickoo"]
        self.price_UU=25
        self.price_SO=30


        self.Notebook=["MoonNotes"]
        self.price_MN=850
        
        
        self.SubCatMobiles=["Mobile Charger","USB Cable"]
        self.MobileCharger=["Iphonecharger","Samsungcharger"]
        self.IC=500
        self.SC=350

        self.USBcable=["Iphonecable","Samsungcable"]
        self.IE=250
        self.SG=350
        
        self.SubCatUniform=["Shirt","Pants","Sweater"]
        self.Shirt=["FCCShirt"]
        self.price_FC1=500
        self.Pants=["FCCPants"]
        self.price_FC2=800
        self.Sweater=["FCCSweater"]
        self.price_FC3=1250
        
        
        

        
        #Image1
        img=Image.open(r"C:\Users\Maha Minahil\OneDrive\Desktop\Login page\book\bookpeople.jpeg")
        img=img.resize((550,130),Image.ANTIALIAS)
        self.photoimg=ImageTk.PhotoImage(img)

        lbl_img=Label(self.root,image=self.photoimg)
        lbl_img.place(x=0,y=0,width=550,height=130)
        

        #Image2
        img_1=Image.open(r"C:\Users\Maha Minahil\OneDrive\Desktop\Login page\book\bookstore.JPG")
        img_1=img_1.resize((630,130),Image.ANTIALIAS)
        self.photoimg_1=ImageTk.PhotoImage(img_1)

        lbl_img_1=Label(self.root,image=self.photoimg_1)
        lbl_img_1.place(x=550,y=0,width=450,height=130)


        #Image3
        img_2=Image.open(r"C:\Users\Maha Minahil\OneDrive\Desktop\Login page\book\books1.jpg")
        img_2=img_2.resize((550,130),Image.ANTIALIAS)
        self.photoimg_2=ImageTk.PhotoImage(img_2)

        lbl_img_2=Label(self.root,image=self.photoimg_2)
        lbl_img_2.place(x=1000,y=0,width=530,height=130)


        lbl_title=Label(self.root,text="BOOKSHOP BILLING SECTION",font=("times new roman",35,"bold"),bg="white",fg="red")
        lbl_title.place(x=0,y=130,width=1530,height=45)

        Main_Frame=Frame(self.root,bd=5,relief=GROOVE,bg="white")
        Main_Frame.place(x=0,y=175,width=1530,height=620)


                                   

        #CustomerLabelFrame
        Cust_Frame=LabelFrame(Main_Frame,text="Customer",font=("times new roman",12,"bold"),bg="white",fg="red")
        Cust_Frame.place(x=10,y=5,width=350,height=140)

        self.lbl_mob=Label(Cust_Frame,text="Mobile No",font=("times new roman",12,"bold"),bg="white")
        self.lbl_mob.grid(row=0,column=0,sticky=W,padx=5,pady=2)

        self.entry_mob=ttk.Entry(Cust_Frame,textvariable=self.c_phon,font=("times new roman",12,"bold"),width=22)
        self.entry_mob.grid(row=0,column=1)

        self.lblCustName=Label(Cust_Frame,font=("arial",12,"bold"),bg="white",text="Customer Name",bd=4)
        self.lblCustName.grid(row=1,column=0,sticky=W,padx=5,pady=2)

        self.txtCustName=ttk.Entry(Cust_Frame,textvariable=self.c_name,font=("arial",12,"bold"),width=20)
        self.txtCustName.grid(row=1,column=1,sticky=W,padx=5,pady=2)

        self.lblEmail=Label(Cust_Frame,font=("arial",12,"bold"),bg="white",text="Email",bd=4)
        self.lblEmail.grid(row=2,column=0,sticky=W,padx=5,pady=2)

        self.txtEmail=ttk.Entry(Cust_Frame,textvariable=self.c_email,font=("arial",10,"bold"),width=24)
        self.txtEmail.grid(row=2,column=1,sticky=W,padx=5,pady=2)

        #ProductLabelFrame
        Product_Frame=LabelFrame(Main_Frame,text="Product",font=("times new roman",12,"bold"),bg="white",fg="red")
        Product_Frame.place(x=370,y=5,width=590,height=140)

        
        #Category
        self.lblCategory=Label(Product_Frame,font=("arial",12,"bold"),bg="white",text="Select Categories",bd=4)
        self.lblCategory.grid(row=0,column=0,sticky=W,padx=5,pady=2)

        self.Combo_Category=ttk.Combobox(Product_Frame,value=self.Category,font=("arial",12,"bold"),width=19,state="readonly")
        self.Combo_Category.current(0)
        self.Combo_Category.grid(row=0,column=1,sticky=W,padx=5,pady=2)
        self.Combo_Category.bind("<<ComboboxSelected>>",self.Categories)


        #SubCategory
        self.lblCategory=Label(Product_Frame,font=("arial",12,"bold"),bg="white",text="Subcategory",bd=4)
        self.lblCategory.grid(row=1,column=0,sticky=W,padx=5,pady=2)

        self.ComboSubCategory=ttk.Combobox(Product_Frame,values=[""],state="readonly",font=("arial",10,"bold"),width=24)
        self.ComboSubCategory.grid(row=1,column=1,sticky=W,padx=5,pady=2)
        self.ComboSubCategory.bind("<<ComboboxSelected>>",self.Product_add)

        #ProductName
        self.lblproduct=Label(Product_Frame,font=("arial",12,"bold"),bg="white",text="Product Name",bd=4)
        self.lblproduct.grid(row=2,column=0,sticky=W,padx=5,pady=2)

        self.ComboProduct=ttk.Combobox(Product_Frame,textvariable=self.product,state="readonly",font=("arial",10,"bold"),width=24)
        self.ComboProduct.grid(row=2,column=1,sticky=W,padx=5,pady=2)
        self.ComboProduct.bind("<<ComboboxSelected>>",self.price)


        #Price
        self.lblPrice=Label(Product_Frame,font=("arial",12,"bold"),bg="white",text="Price",bd=4)
        self.lblPrice.grid(row=0,column=2,sticky=W,padx=5,pady=2)

        self.ComboPrice=ttk.Combobox(Product_Frame,state="readonly",textvariable=self.prices,font=("arial",10,"bold"),width=19)
        self.ComboPrice.grid(row=0,column=3,sticky=W,padx=5,pady=2)
        

       
        #Qty
        self.lblQty=Label(Product_Frame,font=("arial",12,"bold"),bg="white",text="Qty",bd=4)
        self.lblQty.grid(row=1,column=2,sticky=W,padx=5,pady=2)

        self.ComboQty=ttk.Entry(Product_Frame,textvariable=self.qty,font=("arial",10,"bold"),width=21)
        self.ComboQty.grid(row=1,column=3,sticky=W,padx=5,pady=2)


        #MiddleFrame
        MiddleFrame=Frame(Main_Frame,bd=10)
        MiddleFrame.place(x=10,y=150,width=950,height=200)

        #Image1
        img12=Image.open(r"C:\Users\Maha Minahil\OneDrive\Desktop\Login page\book\SAM.JPG")
        img12=img12.resize((490,340),Image.ANTIALIAS)
        self.photoimg12=ImageTk.PhotoImage(img12)

        lbl_img12=Label(MiddleFrame,image=self.photoimg12)
        lbl_img12.place(x=0,y=0,width=490,height=230)

        #Image2
        img13=Image.open(r"C:\Users\Maha Minahil\OneDrive\Desktop\Login page\book\booksbg.jpeg")
        img13=img13.resize((490,340),Image.ANTIALIAS)
        self.photoimg13=ImageTk.PhotoImage(img13)

        lbl_img13=Label(MiddleFrame,image=self.photoimg13)
        lbl_img13.place(x=490,y=0,width=450,height=230)

        

        #Search
        Search_Frame=Frame(Main_Frame,bd=2,bg="white")
        Search_Frame.place(x=965,y=15,width=580,height=40)

        self.lblBill=Label(Search_Frame,font=("arial",12,"bold"),bg="red",fg="white",text="Bill Number")
        self.lblBill.grid(row=0,column=0,sticky=W,padx=1)

        self.txt_Entry_Search=ttk.Entry(Search_Frame,textvariable=self.search_bill,font=("arial",10,"bold"),width=42)
        self.txt_Entry_Search.grid(row=0,column=1,sticky=W,padx=2)

        self.BtnSearch=Button(Search_Frame,command=self.find_bill,text="Search",font=("arial",10,"bold"),bg="orangered",fg="white",width=15,cursor="hand2")
        self.BtnSearch.grid(row=0,column=2)

        

        #RightFrameBillArea
        RightLabelFrame=LabelFrame(Main_Frame,text="Bill Area",font=("times new roman",12,"bold"),bg="white",fg="red")
        RightLabelFrame.place(x=965,y=45,width=380,height=440)

        scroll_y=Scrollbar(RightLabelFrame,orient=VERTICAL)
        self.textarea=Text(RightLabelFrame,yscrollcommand=scroll_y.set,bg="white",fg="blue",font=("times new roman",12,"bold"))
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_y.config(command=self.textarea.yview)
        self.textarea.pack(fill=BOTH,expand=1)

        #BillCounterLabelFrame
        Bottom_Frame=LabelFrame(Main_Frame,text="Bill Counter",font=("times new roman",12,"bold"),bg="white",fg="red")
        Bottom_Frame.place(x=0,y=350,width=960,height=125)

        self.lblSubTotal=Label(Bottom_Frame,font=("arial",12,"bold"),bg="white",text="Sub Total",bd=4)
        self.lblSubTotal.grid(row=0,column=0,sticky=W,padx=5,pady=2)

        self.EntySubTotalQty=ttk.Entry(Bottom_Frame,textvariable=self.sub_total,font=("arial",10,"bold"),width=24)
        self.EntySubTotalQty.grid(row=0,column=1,sticky=W,padx=5,pady=2)


        self.lbl_tax=Label(Bottom_Frame,font=("arial",12,"bold"),bg="white",text="Gov Tax",bd=4)
        self.lbl_tax.grid(row=1,column=0,sticky=W,padx=5,pady=2)

        self.txt_tax=ttk.Entry(Bottom_Frame,textvariable=self.tax_input,font=("arial",10,"bold"),width=24)
        self.txt_tax.grid(row=1,column=1,sticky=W,padx=5,pady=2)


        self.lblAmountTotal=Label(Bottom_Frame,font=("arial",12,"bold"),bg="white",text="Total",bd=4)
        self.lblAmountTotal.grid(row=2,column=0,sticky=W,padx=5,pady=2)

        self.txtAmountTotal=ttk.Entry(Bottom_Frame,textvariable=self.total,font=("arial",10,"bold"),width=24)
        self.txtAmountTotal.grid(row=2,column=1,sticky=W,padx=5,pady=2)

        #ButtonFrame
        Btn_Frame=Frame(Bottom_Frame,bd=2,bg="white")
        Btn_Frame.place(x=350,y=0)


        self.BtnAddtoCart=Button(Btn_Frame,command=self.Additem,height=2,text="Add To Cart",font=("arial",10,"bold"),bg="orangered",fg="white",width=15,cursor="hand2")
        self.BtnAddtoCart.grid(row=0,column=0)

        self.Btngenerate_bill=Button(Btn_Frame,command=self.gen_bill,height=2,text="Generate Bill",font=("arial",10,"bold"),bg="orangered",fg="white",width=15,cursor="hand2")
        self.Btngenerate_bill.grid(row=0,column=1)

        self.BtnSave=Button(Btn_Frame,command=self.save_bill,height=2,text="Save Bill",font=("arial",10,"bold"),bg="orangered",fg="white",width=15,cursor="hand2")
        self.BtnSave.grid(row=0,column=2)

        self.BtnPrint=Button(Btn_Frame,command=self.iprint,height=2,text="Print Bill",font=("arial",10,"bold"),bg="orangered",fg="white",width=15,cursor="hand2")
        self.BtnPrint.grid(row=1,column=0)
        
        self.BtnClear=Button(Btn_Frame,command=self.clear,height=2,text="Clear",font=("arial",10,"bold"),bg="orangered",fg="white",width=15,cursor="hand2")
        self.BtnClear.grid(row=1,column=1)

        self.BtnExit=Button(Btn_Frame,command=self.root.destroy,height=2,text="Exit",font=("arial",10,"bold"),bg="orangered",fg="white",width=15,cursor="hand2")
        self.BtnExit.grid(row=1,column=2)
        self.welcome()

        self.l=[]

    #Function Declaration
        self.list1=[]
    def Additem(self):
        Tax=1
        self.n=self.prices.get()
        self.m=self.qty.get()*self.n
        self.l.append(self.m)
        if self.product.get()=="":
            messagebox.showerror("Error","Please Select the product Name.",parent=self.root)
        else:
            self.list1.append(self.product.get())
            conn=mysql.connector.connect(host="localhost",user="root",password="onedirection",database="books")
            my_cursor=conn.cursor()
            my_cursor.execute("select ProdQty from bookrecord where "+"ProdName LIKE '%"+self.product.get()+"%'")
            prodqtylist=my_cursor.fetchall()
            prodqty1=prodqtylist[0]
            prodqty2=prodqty1[0]
            calqty=int(prodqty2)-self.qty.get()
            
           

            my_cursor.execute("update bookrecord set ProdQty=%s where "+"ProdName LIKE '%"+self.product.get()+"%'",(
                                                                                                                      calqty,
          
                                                                                                                     ))
            
            conn.commit()
            conn.close()
            
            self.textarea.insert(END,f"\n {self.product.get()}\t\t\t{self.qty.get()}\t{self.m}")
            self.sub_total.set(str('Rs.%.2f'%(sum(self.l))))
            self.tax_input.set(str('Rs.%.2f'%((((sum(self.l))-(self.prices.get()))*Tax)/100)))
            self.total.set(str('Rs.%.2f'%(((sum(self.l))+((((sum(self.l))-(self.prices.get()))*Tax)/100)))))
            self.send_email()

    def send_email(self):
            conn=mysql.connector.connect(host="localhost",user="root",password="onedirection",database="books")
            my_cursor=conn.cursor()
            my_cursor.execute("select ProdQty from bookrecord where "+"ProdName LIKE '%"+self.product.get()+"%'")
            prodqtylist=my_cursor.fetchall()
            prodqty1=prodqtylist[0]
            prodqty2=prodqty1[0]
            if int(prodqty2)<3 or int(prodqty2)==3:
                server=smtplib.SMTP_SSL("smtp.gmail.com",465)
                server.login("fccbookshop@gmail.com","FCCbs123")
                message="Hello,\nPlease reorder "+self.product.get()+" as low in stock.\nThankyou."
                server.sendmail("fccbookshop@gmail.com","mahaamer2000@gmail.com",message)
                server.quit()
                messagebox.showinfo("Reorder",self.product.get()+" has been reordered.",parent=self.root)
                
                
            
            
            
    def gen_bill(self):
        if self.product.get()=="":
            messagebox.showerror("Error","Please Add To Cart Product.",parent=self.root)
        else:
            text=self.textarea.get(10.0,(10.0+float(len(self.l))))
            self.welcome()
            self.textarea.insert(END,text)
            self.textarea.insert(END,"\n =======================================")
            self.textarea.insert(END,f"\n Sub Amount:\t\t\t{self.sub_total.get()}")
            self.textarea.insert(END,f"\n Tax Amount:\t\t\t{self.tax_input.get()}")
            self.textarea.insert(END,f"\n Total Amount:\t\t\t{self.total.get()}")
            self.textarea.insert(END,"\n=======================================")

    def save_bill(self):
        op=messagebox.askyesno("Save Bill","Do you want to save the Bill.",parent=self.root)
        if op>0:
            self.bill_data=self.textarea.get(1.0,END)
            f1=open(r'bills/'+str(self.bill_no.get())+".txt",'w')
            f1.write(self.bill_data)
            op=messagebox.showinfo("Saved",f"Bill No:{self.bill_no.get()} Saved successfully.",parent=self.root)
            f1.close()

    def iprint(self):
        q=self.textarea.get(1.0,"end-1c")
        filename=tempfile.mktemp('.txt')
        open(filename,'w').write(q)
        os.startfile(filename,"print")

    def find_bill(self):
        found="no"
        for i in os.listdir(r"bills/"):
            if i.split('.')[0]==self.search_bill.get():
                f1=open(f'bills/{i}','r')
                self.textarea.delete(1.0,END)
                for d in f1:
                    self.textarea.insert(END,d)
                f1.close()
                found="yes"
        if found=='no':
            messagebox.showerror("Error","Invalid Bill No.",parent=self.root)

    def clear(self):
        self.textarea.delete(1.0,END)
        self.c_name.set("")
        self.c_phon.set("")
        self.c_email.set("")
        x=random.randint(1000,9999)
        self.bill_no.set(str(x))
        self.search_bill.set("")
        self.product.set("")
        self.prices.set(0)
        self.qty.set(0)
        self.l=[0]
        self.total.set("")
        self.sub_total.set("")
        self.tax_input.set('')
        self.welcome()
        conn=mysql.connector.connect(host="localhost",user="root",password="onedirection",database="books")
        my_cursor=conn.cursor()
        for i in self.list1:
            my_cursor.execute("select ProdQty from bookrecord where "+"ProdName LIKE '%"+i+"%'")
            prodqtylist=my_cursor.fetchall()
            prodqty1=prodqtylist[0]
            prodqty2=prodqty1[0]
            incqty=int(prodqty2)+1
            my_cursor.execute("update bookrecord set ProdQty=%s where "+"ProdName LIKE '%"+i+"%'",(
                                                                                                    incqty,
          
                                                                                                   ))
        conn.commit()
        conn.close()
            

            
            
            
            

    def welcome(self):
        self.textarea.delete(1.0,END)
        self.textarea.insert(END,"\t Welcome to FCCU Bookshop")
        self.textarea.insert(END,f"\n Bill Number:{self.bill_no.get()}")
        self.textarea.insert(END,f"\n Customer Name:{self.c_name.get()}")
        self.textarea.insert(END,f"\n Phone Number:{self.c_phon.get()}")
        self.textarea.insert(END,f"\n Email:{self.c_email.get()}")

        self.textarea.insert(END,"\n =======================================")
        self.textarea.insert(END,f"\n Products\t\t\tQTY\tPrice")
        self.textarea.insert(END,"\n =======================================\n")
        


    def Categories(self,event=""):
        if self.Combo_Category.get()=="Books":
            self.ComboSubCategory.config(value=self.SubCatBooks)
            self.ComboSubCategory.current(0)


        if self.Combo_Category.get()=="Stationery":
            self.ComboSubCategory.config(value=self.SubCatStationery)
            self.ComboSubCategory.current(0)


        if self.Combo_Category.get()=="Mobiles":
            self.ComboSubCategory.config(value=self.SubCatMobiles)
            self.ComboSubCategory.current(0)


        if self.Combo_Category.get()=="Uniform":
            self.ComboSubCategory.config(value=self.SubCatUniform)
            self.ComboSubCategory.current(0)

        #Books

    def Product_add(self,event=""):
         if self.ComboSubCategory.get()=="Classics":
             self.ComboProduct.config(value=self.Classics)
             self.ComboProduct.current(0)

         if self.ComboSubCategory.get()=="History":
             self.ComboProduct.config(value=self.History)
             self.ComboProduct.current(0)

         if self.ComboSubCategory.get()=="Science Fiction":
             self.ComboProduct.config(value=self.ScienceFiction)
             self.ComboProduct.current(0)

         if self.ComboSubCategory.get()=="Short Stories":
             self.ComboProduct.config(value=self.ShortStories)
             self.ComboProduct.current(0)


         #Stationery
         if self.ComboSubCategory.get()=="Pencil":
             self.ComboProduct.config(value=self.Pencil)
             self.ComboProduct.current(0)


         if self.ComboSubCategory.get()=="Pen":
             self.ComboProduct.config(value=self.Pen)
             self.ComboProduct.current(0)


         if self.ComboSubCategory.get()=="Eraser":
             self.ComboProduct.config(value=self.Eraser)
             self.ComboProduct.current(0)

         if self.ComboSubCategory.get()=="Glue":
             self.ComboProduct.config(value=self.Glue)
             self.ComboProduct.current(0)

         if self.ComboSubCategory.get()=="Notebook":
             self.ComboProduct.config(value=self.Notebook)
             self.ComboProduct.current(0)

         #Mobiles
         if self.ComboSubCategory.get()=="Mobile Charger":
             self.ComboProduct.config(value=self.MobileCharger)
             self.ComboProduct.current(0)

         if self.ComboSubCategory.get()=="USB Cable":
             self.ComboProduct.config(value=self.USBcable)
             self.ComboProduct.current(0)

         #Uniform
         if self.ComboSubCategory.get()=="Shirt":
             self.ComboProduct.config(value=self.Shirt)
             self.ComboProduct.current(0)

         if self.ComboSubCategory.get()=="Pants":
             self.ComboProduct.config(value=self.Pants)
             self.ComboProduct.current(0)

         if self.ComboSubCategory.get()=="Sweater":
             self.ComboProduct.config(value=self.Sweater)
             self.ComboProduct.current(0)


    def price(self,event=""):
         #Classics
         if self.ComboProduct.get()=="ToKillaMockingbird":
             self.ComboPrice.config(value=self.price_TL)
             self.ComboPrice.current(0)
             self.qty.set(1)

         if self.ComboProduct.get()=="PrideandPrejudice":
             self.ComboPrice.config(value=self.price_PA)
             self.ComboPrice.current(0)
             self.qty.set(1)


         #History
         if self.ComboProduct.get()=="AModernHistory":
             self.ComboPrice.config(value=self.price_AB)
             self.ComboPrice.current(0)
             self.qty.set(1)

         if self.ComboProduct.get()=="PakistanHistoryandCulture":
             self.ComboPrice.config(value=self.price_PC)
             self.ComboPrice.current(0)
             self.qty.set(1)

         #ScienceFiction
         if self.ComboProduct.get()=="Frankenstein":
             self.ComboPrice.config(value=self.price_FS)
             self.ComboPrice.current(0)
             self.qty.set(1)

         if self.ComboProduct.get()=="TheAngryEspers":
             self.ComboPrice.config(value=self.price_TJ)
             self.ComboPrice.current(0)
             self.qty.set(1)

         #ShortStories
         if self.ComboProduct.get()=="TheLottery":
             self.ComboPrice.config(value=self.price_TJ2)
             self.ComboPrice.current(0)
             self.qty.set(1)

         if self.ComboProduct.get()=="HowtoBecomeaWriter":
             self.ComboPrice.config(value=self.price_HM)
             self.ComboPrice.current(0)
             self.qty.set(1)

         #Pencil
         if self.ComboProduct.get()=="Dollar":
             self.ComboPrice.config(value=self.price_DR)
             self.ComboPrice.current(0)
             self.qty.set(1)

         if self.ComboProduct.get()=="Deer":
             self.ComboPrice.config(value=self.price_DER)
             self.ComboPrice.current(0)
             self.qty.set(1)

         if self.ComboProduct.get()=="Faber-Castell":
             self.ComboPrice.config(value=self.price_FC)
             self.ComboPrice.current(0)
             self.qty.set(1)

         #Pen
         if self.ComboProduct.get()=="PIANO":
             self.ComboPrice.config(value=self.price_PO)
             self.ComboPrice.current(0)
             self.qty.set(1)

             
         #Eraser
         if self.ComboProduct.get()=="Pelikan":
             self.ComboPrice.config(value=self.PN)
             self.ComboPrice.current(0)
             self.qty.set(1)

         if self.ComboProduct.get()=="FaberCastell":
             self.ComboPrice.config(value=self.FCL)
             self.ComboPrice.current(0)
             self.qty.set(1)

         #Glue
         if self.ComboProduct.get()=="UHU":
             self.ComboPrice.config(value=self.price_UU)
             self.ComboPrice.current(0)
             self.qty.set(1)

         if self.ComboProduct.get()=="Stickoo":
             self.ComboPrice.config(value=self.price_SO)
             self.ComboPrice.current(0)
             self.qty.set(1)

         #Notebook
         if self.ComboProduct.get()=="MoonNotes":
             self.ComboPrice.config(value=self.price_MN)
             self.ComboPrice.current(0)
             self.qty.set(1)

         #MobileCharger
         if self.ComboProduct.get()=="Iphonecharger":
             self.ComboPrice.config(value=self.IC)
             self.ComboPrice.current(0)
             self.qty.set(1)

         if self.ComboProduct.get()=="Samsungcharger":
             self.ComboPrice.config(value=self.SC)
             self.ComboPrice.current(0)
             self.qty.set(1)
             

         #USBCable
         if self.ComboProduct.get()=="Iphonecable":
             self.ComboPrice.config(value=self.IE)
             self.ComboPrice.current(0)
             self.qty.set(1)

         if self.ComboProduct.get()=="Samsungcable":
             self.ComboPrice.config(value=self.SG)
             self.ComboPrice.current(0)
             self.qty.set(1)

         #Shirt
         if self.ComboProduct.get()=="FCCShirt":
             self.ComboPrice.config(value=self.price_FC1)
             self.ComboPrice.current(0)
             self.qty.set(1)
             
         #Pant
         if self.ComboProduct.get()=="FCCPants":
             self.ComboPrice.config(value=self.price_FC2)
             self.ComboPrice.current(0)
             self.qty.set(1)
             
         #Sweater
         if self.ComboProduct.get()=="FCCSweater":
             self.ComboPrice.config(value=self.price_FC3)
             self.ComboPrice.current(0)
             self.qty.set(1)

            
             

        
      
      
        
        

        
if __name__=="__main__":
    main()
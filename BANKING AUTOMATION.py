#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import *
import time
from tkinter import messagebox
from tkinter.ttk import Combobox
import sqlite3
import re
try:
    conobj=sqlite3.connect(database="bank.sqlite")
    curobj=conobj.cursor()
    curobj.execute("create table acn(acn_no integer primary key autoincrement,acn_name text,acn_pass text,acn_email text,acn_mob text,acn_bal float, acn_opendate text,acn_gender text ) ")
    conobj.close()
except:
    print("something went wrong,might be table already exists")


win=Tk()
win.state('zoomed')
win.configure(bg='pink')
win.resizable(width=False,height=False)
title=Label(win,text="BANKING AUTOMATION",font=('arial',50,'bold','underline'),bg='pink')
title.pack()
dt=time.strftime("%d%b,%Y")
date=Label(win,text=dt,font=('',20),bg='pink',fg='blue')
date.place(relx=.85,rely=.1)

def main_screen():
    frm=Frame(win)
    frm.configure(bg='powder blue')
    frm.place(relx=.0,rely=.2,relwidth=1,relheight=.8)
    
    def forgot():
        frm.destroy()
        forgotpass_screen()
   
    def newuser():
        frm.destroy()
        newuser_screen()    

    def login():
        global gacn
        gacn=e_acn.get()
        pwd=e_pass.get()
        if len(gacn)==0 or len(pwd)==0:
            messagebox.showwarning("validation","Empty field are not allowed")
            return
       
        else:
            
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute("select * from acn where acn_no=? and acn_pass=?",(gacn,pwd))
            tup=curobj.fetchone()
            conobj.close()
            
            if tup==None:
                messagebox.showerror('Login','Something Went Wrong')
            
            else:
                frm.destroy()
                login_screen()
            
            
    
    def clear():
        e_acn.delete(0,'end')
        e_pass.delete(0,'end')
        e_acn.focus()
    
    lbl_acn=Label(frm,text='Account No.',font=('arial',25,'bold'),bg='powder blue')
    lbl_acn.place(relx=.22,rely=.15)
    
    e_acn=Entry(frm,font=('arial',20,'bold'),bd=4)
    e_acn.place(relx=.38,rely=.15)
    e_acn.focus()
    
    lbl_pass=Label(frm,text='Password',font=('arial',25,'bold'),bg='powder blue')
    lbl_pass.place(relx=.22,rely=.28)
    
    e_pass=Entry(frm,font=('arial',20,'bold'),bd=4,show='*')
    e_pass.place(relx=.38,rely=.28)

    btn_login=Button(frm,text="Login",font=('arial',15,'bold'),bd=4,command=login)
    btn_login.place(relx=.42,rely=.4)
    
    btn_clear=Button(frm,text="Clear",font=('arial',15,'bold'),bd=4,command=clear)
    btn_clear.place(relx=.51,rely=.4)

    btn_nu=Button(frm,width=18, text="New User",font=('arial',15,'bold'),bd=4,command=newuser)
    btn_nu.place(relx=.4,rely=.5)

    btn_fp=Button(frm,width=18, text="Forgot Password?",font=('arial',15,'bold'),bd=4,command=forgot)
    btn_fp.place(relx=.4,rely=.6)

def forgotpass_screen():
    frm=Frame(win)
    frm.configure(bg='powder blue')
    frm.place(relx=.0,rely=.2,relwidth=1,relheight=.8)    
        
    def back():
        frm.destroy
        main_screen()

    def forgotpass():
        acn=e_acn.get()
        email=e_email.get()
        mob=e_mob.get()

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute("select acn_pass from acn where acn_no=? and acn_email=? and acn_mob=?",(acn,email,mob))
        tup=curobj.fetchone()
    
        if tup==None:
            messagebox.showerror('Forgot Password','Record not found')
        else:
            messagebox.showinfo('Forgot Password',f'Your Password={tup[0]}')
        
        conobj.close()
        e_acn.delete(0,'end')
        e_email.delete(0,'end')
        e_mob.delete(0,'end')
        
    btn_back=Button(frm,text="Back",font=('arial',18,'bold'),bd=4,command=back)
    btn_back.place(relx=.01,rely=.02)

    lbl_f_acn=Label(frm,text='Account No.',font=('',18),bg='powder blue')
    lbl_f_acn.place(relx=.2,rely=.2)

    e_acn=Entry(frm,font=('arial',16,'bold'),bd=4)
    e_acn.place(relx=.32,rely=.2)
    e_acn.focus()
    
    lbl_f_email=Label(frm,text='Email',font=('',18),bg='powder blue')
    lbl_f_email.place(relx=.2,rely=.3)

    e_email=Entry(frm,font=('arial',16,'bold'),bd=4)
    e_email.place(relx=.32,rely=.3)

    lbl_f_mob=Label(frm,text='Mobile No.',font=('',18),bg='powder blue')
    lbl_f_mob.place(relx=.2,rely=.4)

    e_mob=Entry(frm,font=('arial',16,'bold'),bd=4)
    e_mob.place(relx=.32,rely=.4)

    btn_submit=Button(frm,text='Submit',font=('',15,'bold'),bd=4,command=forgotpass)
    btn_submit.place(relx=.38,rely=.5)

    

def newuser_screen():
    frm=Frame(win)
    frm.configure(bg='powder blue')
    frm.place(relx=.0,rely=.2,relwidth=1,relheight=.8)
    
    def back():
        frm.destroy()
        main_screen()

    def newuser_db():
        name=e_name.get()
        pwd=e_pass.get()
        email=e_email.get()
        mob=e_mob.get()
        gender=cb_gender.get()
        bal=0
        opendate=time.strftime("%d%b,%Y")
        
        
        match=re.fullmatch("[6-9][0-9]{9}",mob)
        if match==None:
            messagebox.showwarning("validation","Invalid format of mob")
            return

        match=re.fullmatch("[a-zA-Z0-9_]+@[a-zA-Z]+\.[a-zA-Z]+",email)
        if match==None:
            messagebox.showwarning("validation","Invalid format of email")
            return


        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("insert into acn(acn_name,acn_pass,acn_email,acn_mob,acn_gender,acn_bal,acn_opendate) values(?,?,?,?,?,?,?)",(name,pwd,email,mob,gender,bal,opendate))
        conobj.commit()
        conobj.close()

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select max(acn_no) from acn")
        tup=curobj.fetchone()
        conobj.close()

        messagebox.showinfo('New User',f'Account Created succesfully Account no:- {tup[0]}')               

        e_name.delete(0,'end')
        e_pass.delete(0,'end')
        e_email.delete(0,'end')
        e_mob.delete(0,'end')
        cb_gender.delete(0,'end')        
    
    btn_back=Button(frm,text="Back",font=('arial',18,'bold'),bd=4,command=back)
    btn_back.place(relx=.01,rely=.02)
    
    lbl_name=Label(frm,text='Name',font=('',18),bg='powder blue')
    lbl_name.place(relx=.2,rely=.2)

    e_name=Entry(frm,font=('arial',16,'bold'),bd=4)
    e_name.place(relx=.32,rely=.2)
    e_name.focus()
    
    lbl_pass=Label(frm,text='Password',font=('',18),bg='powder blue')
    lbl_pass.place(relx=.2,rely=.3)

    e_pass=Entry(frm,font=('arial',16,'bold'),bd=4)
    e_pass.place(relx=.32,rely=.3)

    lbl_email=Label(frm,text='Email',font=('',18),bg='powder blue')
    lbl_email.place(relx=.2,rely=.4)

    e_email=Entry(frm,font=('arial',16,'bold'),bd=4)
    e_email.place(relx=.32,rely=.4)

    lbl_mob=Label(frm,text='Mobile No',font=('',18),bg='powder blue')
    lbl_mob.place(relx=.2,rely=.5)

    e_mob=Entry(frm,font=('arial',16,'bold'),bd=4)
    e_mob.place(relx=.32,rely=.5)

    lbl_gender=Label(frm,text='Gender',font=('',18),bg='powder blue')
    lbl_gender.place(relx=.2,rely=.6)
    
    cb_gender=Combobox(frm, values=['---select---','Male','Female'])
    cb_gender.place(relx=.32,rely=.6)
    
    
    submit=Button(frm,text='Submit',font=('',15,'bold'),bd=4,command=newuser_db)
    submit.place(relx=.35,rely=.7)

    clear=Button(frm,text='Clear',font=('',15,'bold'),bd=4)
    clear.place(relx=.43,rely=.7)

def login_screen():
    frm=Frame(win)
    frm.configure(bg='powder blue')
    frm.place(relx=.0,rely=.2,relwidth=1,relheight=.8)

    conobj=sqlite3.connect(database='bank.sqlite')
    curobj=conobj.cursor()
    curobj.execute('select acn_name from acn where acn_no=?',(gacn))
    tup=curobj.fetchone()
    conobj.close()
    
    lbl_welcome=Label(frm,text=f'Welcome,{tup[0]}',font=('',18),bg='powder blue',fg='blue')
    lbl_welcome.place(relx=.0,rely=.0)


    
    def logout():
        frm.destroy()
        main_screen()
    
    def details():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.15,rely=.1,relwidth=.6,relheight=.48)

        lbl_details=Label(ifrm,text='This is Details screen',font=('',18),bg='white',fg='blue')
        lbl_details.pack()

        
        
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute('select acn_no,acn_name,acn_opendate,acn_email,acn_mob,acn_bal from acn where acn_no=?',(gacn))
        tup=curobj.fetchone()
        conobj.close()

        lbl_acn_no=Label(ifrm,text=f'Account no:-{tup[0]}',font=('',15),bg='white')
        lbl_acn_no.place(relx=.1,rely=.1)
        
        lbl_acn_name=Label(ifrm,text=f'Name:-{tup[1]}',font=('',15),bg='white')
        lbl_acn_name.place(relx=.1,rely=.2)

        lbl_acn_opendate=Label(ifrm,text=f'Open Date :-{tup[2]}',font=('',15),bg='white')
        lbl_acn_opendate.place(relx=.1,rely=.3)

        lbl_acn_email=Label(ifrm,text=f'Email:-{tup[3]}',font=('',15),bg='white')
        lbl_acn_email.place(relx=.1,rely=.4)

        lbl_acn_mob=Label(ifrm,text=f'Mobile:-{tup[4]}',font=('',15),bg='white')
        lbl_acn_mob.place(relx=.1,rely=.5)

        lbl_acn_bal=Label(ifrm,text=f'Balance:-{tup[5]}',font=('',15),bg='white')
        lbl_acn_bal.place(relx=.1,rely=.6)



    
    def update():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.15,rely=.1,relwidth=.6,relheight=.48)

        lbl_update=Label(ifrm,text='This is Update screen',font=('',18),bg='white',fg='blue')
        lbl_update.pack()
        
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute('select acn_name,acn_pass,acn_email,acn_mob from acn where acn_no=?',(gacn))
        tup=curobj.fetchone()
        conobj.close()
        
        lbl_name=Label(ifrm,text='Name',font=('',18),bg='white')
        lbl_name.place(relx=.1,rely=.15)
    
        e_name=Entry(ifrm,font=('arial',16,'bold'),bd=4)
        e_name.place(relx=.1,rely=.3)
        e_name.insert(0,tup[0])
        e_name.focus()
        
        lbl_pass=Label(ifrm,text='Password',font=('',18),bg='white')
        lbl_pass.place(relx=.1,rely=.45)
    
        e_pass=Entry(ifrm,font=('arial',16,'bold'),bd=4)
        e_pass.place(relx=.1,rely=.6)
        e_pass.insert(0,tup[1])
        
        lbl_email=Label(ifrm,text='Email',font=('',18),bg='white')
        lbl_email.place(relx=.45,rely=.15)
    
        e_email=Entry(ifrm,font=('arial',16,'bold'),bd=4)
        e_email.place(relx=.45,rely=.3)
        e_email.insert(0,tup[2])
        
        lbl_mob=Label(ifrm,text='Mobile No',font=('',18),bg='white')
        lbl_mob.place(relx=.45,rely=.45)
    
        e_mob=Entry(ifrm,font=('arial',16,'bold'),bd=4)
        e_mob.place(relx=.45,rely=.6)
        e_mob.insert(0,tup[3])

        def update_db():
            name=e_name.get()
            pwd=e_pass.get()
            email=e_email.get()
            mob=e_mob.get()

            conobj=sqlite3.connect('bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute('update acn set acn_name=?,acn_pass=?,acn_email=?,acn_mob=? where acn_no=?',(name,pwd,email,mob,gacn))
            conobj.commit()
            conobj.close()
            
            messagebox.showinfo('update','Sucessfully update')
            login_screen()
            
        submit_btn=Button(ifrm,text='Submit',font=('',15,'bold'),bd=4,command=update_db)
        submit_btn.place(relx=.67,rely=.77)
        
    
    def deposit():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.15,rely=.1,relwidth=.6,relheight=.48)

        lbl_deposit=Label(ifrm,text='This is Deposit screen',font=('',18),bg='white',fg='blue')
        lbl_deposit.pack()

        lbl_deposit=Label(ifrm,text='Deposit',font=('',18,'bold'),bg='white')
        lbl_deposit.place(relx=.2,rely=.2)
    
        e_deposit=Entry(ifrm,font=('arial',16,'bold'),bd=4)
        e_deposit.place(relx=.35,rely=.2)
        e_deposit.focus()
        
        def deposit_db():
            amt=e_deposit.get()

            conobj=sqlite3.connect('bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute('update acn set acn_bal=acn_bal+? where acn_no=?',(amt,gacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo('Deposit',f'{amt}Amount Deposited')
            e_deposit.delete(0,'end')
        
        deposit_btn=Button(ifrm,text='Deposit',font=('',15,'bold'),bd=4,command=deposit_db)
        deposit_btn.place(relx=.43,rely=.4)    

    
    def withdraw():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2 )
        ifrm.configure(bg='white')
        ifrm.place(relx=.15,rely=.1,relwidth=.6,relheight=.48)

        lbl_withdraw=Label(ifrm,text='This is Withdraw screen',font=('',18),bg='white',fg='blue')
        lbl_withdraw.pack()

        lbl_withdraw=Label(ifrm,text='Withdraw',font=('',18,'bold'),bg='white')
        lbl_withdraw.place(relx=.2,rely=.2)
    
        e_withdraw=Entry(ifrm,font=('arial',16,'bold'),bd=4)
        e_withdraw.place(relx=.35,rely=.2)
        e_withdraw.focus()
        
        def withdraw_db():
            amt=float(e_withdraw.get())

            conobj=sqlite3.connect('bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute('select acn_bal from acn where acn_no=?',(gacn,))
            tup=curobj.fetchone()
            amount=tup[0]
            conobj.close()

            if amount>=amt:
            
                conobj=sqlite3.connect('bank.sqlite')
                curobj=conobj.cursor()
                curobj.execute('update acn set acn_bal=acn_bal-? where acn_no=?',(amt,gacn))
                conobj.commit()
                conobj.close()
                messagebox.showinfo('Withdraw',f'{amt}Amount Withdraw')
                e_withdraw.delete(0,'end')
            
            else:
                messagebox.showerror('Withdraw','Insufficient Amount')

                
        withdraw_btn=Button(ifrm,text='Withdraw',font=('',15,'bold'),bd=4,command=withdraw_db)
        withdraw_btn.place(relx=.43,rely=.4)    
        
    def transfer():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.15,rely=.1,relwidth=.6,relheight=.48)

        lbl_transfer=Label(ifrm,text='This is Transfer screen',font=('',18),bg='white',fg='blue')
        lbl_transfer.pack()

        lbl_amt=Label(ifrm,text='Amount',font=('',18),bg='white')
        lbl_amt.place(relx=.1,rely=.15)
    
        e_amt=Entry(ifrm,font=('arial',16,'bold'),bd=4)
        e_amt.place(relx=.22,rely=.15)
        e_amt.focus()

        lbl_to=Label(ifrm,text='To',font=('',18),bg='white')
        lbl_to.place(relx=.1,rely=.35)
    
        e_to=Entry(ifrm,font=('arial',16,'bold'),bd=4)
        e_to.place(relx=.22,rely=.35)

        def transfer_db():
            amt=float(e_amt.get())
            to=e_to.get()


            conobj=sqlite3.connect('bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute('select acn_bal from acn where acn_no=?',(gacn,))
            tup=curobj.fetchone()
            cur_amt=tup[0]
            conobj.close()

            conobj=sqlite3.connect('bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute('select acn_no from acn where acn_no=?',(to,))
            tup=curobj.fetchone()
            conobj.close()

            if tup==None:
                messagebox.showwarning('Transfer','Invaild Account no')
                return
            
            if cur_amt>=amt:
                conobj=sqlite3.connect('bank.sqlite')
                curobj=conobj.cursor()
                curobj.execute('update acn set acn_bal=acn_bal+? where acn_no=?',(amt,to))
                curobj.execute('update acn set acn_bal=acn_bal-? where acn_no=?',(amt,gacn))
                conobj.commit()
                conobj.close()            
                messagebox.showinfo('Transfer',f'amount{amt}Transfer Succesfully')
        
        btn_submit=Button(ifrm,width=8,text='Submit',font=('',15,'bold'),bd=4,command=transfer_db)
        btn_submit.place(relx=.32,rely=.5)
        
    
    btn_logout=Button(frm,width=8,text='Logout',font=('',15,'bold'),bd=4,command=logout)
    btn_logout.place(relx=.91,rely=.0)

    
    btn_details=Button(frm,width=8,text='Details',font=('',15,'bold'),bd=4,command=details)
    btn_details.place(relx=.0,rely=.1)

    btn_update=Button(frm,width=8,text='Update',font=('',15,'bold'),bd=4,command=update)
    btn_update.place(relx=.0,rely=.2)

    btn_deposit=Button(frm,width=8,text='Deposit',font=('',15,'bold'),bd=4,command=deposit)
    btn_deposit.place(relx=.0,rely=.3)

    btn_withdraw=Button(frm,text='Withdraw',font=('',15,'bold'),bd=4,command=withdraw)
    btn_withdraw.place(relx=.0,rely=.4)

    btn_Transfer=Button(frm,width=8,text='Transfer',font=('',15,'bold'),bd=4,command=transfer)
    btn_Transfer.place(relx=.0,rely=.5)



main_screen()
win.mainloop()



# In[4]:


import sqlite3
conobj=sqlite3.connect(database="bank.sqlite")
curobj=conobj.cursor()
curobj.execute('select * from acn')
a=curobj.fetchone()
print(a)
conobj.close()


# In[ ]:





# In[ ]:







# In[ ]:





from flask import Flask,url_for,request,render_template,session,flash,redirect
import sqlite3
from flask_mail import Mail, Message
from random import randint,randrange
from RSA import *
from face_detection import face_register,face_reg

from datetime import datetime

app=Flask(__name__)
app.secret_key="Rudy"

mail=Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'deduplication92@gmail.com'
app.config['MAIL_PASSWORD'] = 'deduplication'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def random_with_N_digits(n):
            range_start = 10**(n-1)
            range_end = (10**n)-1
            return randint(range_start, range_end)

a=random_with_N_digits(4)

@app.route('/',methods=["GET","POST"])
def login():
    username=None
    password=None
    err=""
    if request.method=='POST':
        session['username']=request.form['uname']
        session['vid']=request.form['pwd']
        username=request.form['uname']
        password=request.form['pwd']
        val = face_reg(username)
        print(val)
        if val == 'Authorized':
            conn = sqlite3.connect("reg.db")
            r=conn.cursor()
            r.execute("select name,pwd,ema from regval2 where name=? and pwd=?",(username,password))
            rows=r.fetchall()
            print(rows)
            session['email'] = rows[0][2]
            if len(rows)!=0:
                for i in rows:
                    if i[0]=="Admin" and i[1]=="Admin":
                        return redirect(url_for('Admin'))

                    elif i[0]==username and i[1]==password:
                        return redirect(url_for('userpage'))
        else:
            
            return render_template('login.html',err=err)
    else:
        return render_template('login.html',err=err)
    return render_template('login.html')

@app.route('/reg',methods=["GET","POST"])
def reg():
    uname=None
    pwd=None
    cpwd=None
    phn=None
    ema=None
    dob=None
    msg="Register successfully"
    if request.method=='POST':
        uname=request.form['txt']
        pwd=request.form['passw']
        cpwd=request.form['cpassw']
        phn=request.form['phn']
        public_key=request.form['public_key']
        ema=request.form['ema']
        dob=request.form['dob']
        val = face_register(uname)
        if val == 'Already Registered':
            error = 'already registered'
            return render_template('registraion.html',msg=error)

        elif val =='your not allowed to register':
            error = 'already registered'
            return render_template('registraion.html',msg=error)
        elif val=='your allowed to register':
            try:
                import sqlite3
                table_name = 'regval2'
                conn = sqlite3.connect("reg.db")
                c = conn.cursor()
                c.execute('create table if not exists ' + table_name + ' (name varchar(50),pwd varchar(50) primary key,cpwd varchar(50),phn varchar(50),ema varchar(50),dob varchar(50))')
                c.execute('insert into '+table_name+'  values (?,?,?,?,?,?)',(uname,pwd,cpwd,phn,ema,dob))
                conn.commit()
                conn.close()
                flash("Register successfully")
            except:
                return "Please enter unique Voter ID"
            return render_template('registraion.html',msg=msg)
    else:
        return render_template('registraion.html')
    return render_template("registraion.html")

@app.route('/userpage',methods=["GET","POST"])
def userpage():
    voteid=session["vid"]
    dat=datetime.now().date()
    dat=dat.strftime("%d %b %Y")
    print(session['email'])

    part=None
    vname=None
    li=[]
    che=None
    final_li=[]
    text=None
    rsalist=[]
    tupe=None
    from block_chain import Block,BlockChain
    if request.method=='POST':
        vname=session["username"]
        li.append(vname)
        li.append(voteid)
        li.append(dat)
        
        
        if request.form["otp"]==str(a):
            return render_template('cast_vote.html')
        else:
            print("otp didn't match")
        return redirect(url_for('login'))

    elif request.method=='GET':
        conn = sqlite3.connect("reg.db")
        che=conn.cursor()
        che.execute("select name, voterid from final_block_chain where name=? and voterid=?",(session['username'],session['vid']))
        rows=che.fetchall()
        if len(rows)!=0:
            return "Your already voted!!!"
        else:
            msg = Message('Hello ', sender = 'deduplication92@gmail.com', recipients = [session['email']])
            msg.body = str(a)
            mail.send(msg)
            return render_template('user.html')
        return render_template('user.html')

    else:
        return render_template('user.html')
    return render_template('user.html')

@app.route('/admin',methods=["GET","POST"])
def Admin():
    admk=[]
    dmk=[]
    mnm=[]
    if request.method=='GET':
        conn = sqlite3.connect("reg.db")
        g = conn.cursor()
        g.execute("select * from RSA_table")
        rows=g.fetchall()
        return render_template("admin.html",rows=rows)
    else:
        conn=sqlite3.connect("reg.db")
        h=conn.cursor()
        h.execute("select * from Rsa_table1")
        dd=h.fetchall()
        for i in dd:
            if i[3]==("['A', 'D', 'M', 'K']"):
                admk.append(i[3])
            elif i[3]==("['D', 'M', 'K']"):
                dmk.append(i[3])
            else:
                mnm.append(i[3])
        print(len(admk))
        print(len(dmk))
        print(len(mnm))
        return render_template("admin.html",dd=dd,admkc=len(admk),dmkc=len(dmk),mnmc=len(mnm))
    return render_template("admin.html")

if __name__=='__main__':
    app.run(debug=True)

    # app = Flask(__name__)


    # @app.route('/')
    # def index():
    #     return render_template('login.html')
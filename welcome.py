from flask import Flask, render_template,request,redirect,url_for,flash
import mysql.connector
from mysql.connector import Error
from simple_code import*
from akher_forecasting import*


purchase=''
location=''
view = ''
FinishType=''
year=''
Area=''
bedroom = ''
bathroom =''
type=''
username =''
Payment=''

connection = mysql.connector.connect(host='localhost',
                                        database='thesis',
                                        user='root',
                                        password='root1234')


if connection.is_connected():

    db_Info = connection.get_server_info()
    print("Connected to MySQL Server version ", db_Info)
    cursor = connection.cursor()
    cursor.execute("select database();")
    record = cursor.fetchone()
    print("You're connected to database: ", record)


app = Flask(__name__,template_folder='../flask-server/templates')
app.config['SECRET_KEY'] = 'the random string'  

def printing():
    print('location: ',location)
    print('view: ',view)
    print('year: ',year)
    print('FinishType: ',FinishType)
    print('Area: ',Area)
    print('bedroom: ',bedroom)
    print('bathroom: ',bathroom)
    print('type: ',type)
    print('username: ',username)
    result=cursor.execute('''SELECT seller_role FROM thesis.customer where username =%s''',(username,))
    record = cursor.fetchone()[0]
    print("Srole: ",record)


@app.route('/payment', methods = ['POST', 'GET'])
def payment():
    if request.method == 'GET':
        printing()
        return render_template('payment.html')
     
    if request.method == 'POST':
        payment = request.form['payment']
        return purchase

@app.route('/houseprice', methods = ['POST', 'GET'])
def houseprice():
    if request.method == 'GET':
        cursor = connection.cursor(buffered=True)
        result=cursor.execute('''SELECT seller_role FROM thesis.customer where username =%s''',(username,))
        record = cursor.fetchone()[0]
        print("Srole: ",record)
        price=runmodel(record,type,FinishType,view,int(Area),int(year),int(bedroom),int(bathroom),Payment,location)
        
        price='{:,}'.format(price)
        return render_template('predprice.html',price=price,username=username)
     
    if request.method == 'POST':
        payment = request.form['payment']
        return purchase

@app.route('/purchase', methods = ['POST', 'GET'])
def purchase():
    if request.method == 'GET':
        printing()
        return render_template('purchase.html')
     
    if request.method == 'POST':
        purchase = request.form['purchase']
        return redirect(url_for('houseprice'))


@app.route('/aboutus', methods = ['GET'])
def Au():
    if request.method == 'GET':
        return render_template('AU.html')

@app.route('/contactus', methods = ['GET'])
def cu():
    if request.method == 'GET':
        return render_template('CU.html')
    




@app.route('/PD4', methods = ['POST', 'GET'])
def pd4():
    if request.method == 'GET':
        return render_template('pd4.html',username=username)
     
    if request.method == 'POST':
        global view
        view = request.form['view']
        global FinishType
        FinishType=request.form['FinishType']
        global year
        year=request.form['year']
        global Payment
        Payment=request.form['Payment']
        return redirect(url_for('purchase'))

@app.route('/PD3', methods = ['POST', 'GET'])
def pd3():
    if request.method == 'GET':
        return render_template('pd3.html',username=username)
     
    if request.method == 'POST':
        global location
        location = request.form['location']
        return  redirect(url_for('pd4'))


@app.route('/PD2', methods = ['POST', 'GET'])
def pd2():
    if request.method == 'GET':
        return render_template('pd2.html',username=username)
     
    if request.method == 'POST':
        global Area
        Area = request.form['area']
        return redirect(url_for('pd3'))

@app.route('/PD1', methods = ['POST', 'GET'])
def pd1():
    if request.method == 'GET':
        return render_template('pd1.html',username=username)
     
    if request.method == 'POST':
        global bedroom,bathroom
        bedroom = request.form['Bedrooms']
        bathroom = request.form['Bathrooms']
        return redirect(url_for('pd2'))

@app.route('/PD0', methods = ['POST', 'GET'])
def pd0():
    if request.method == 'GET':
        return render_template('pd0.html',username=username)
     
    if request.method == 'POST':
        global type
        type = request.form['hometype']
        return redirect(url_for('pd1'))


@app.route('/dashboard/<urn>', methods = ['GET'])
def dashboard(urn):
    if request.method == 'GET':
        global username
        username=urn
        print(urn)
        return render_template('dashboard.html', name=urn)

 
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
     
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = connection.cursor(buffered=True)
        result=cursor.execute('''SELECT *from thesis.customer where username=%s and password=%s''',(username,password))
        record = cursor.fetchone()
        if record==None:
            return redirect(url_for('login'))
        else:
            return redirect(url_for('dashboard', urn=username))


def validate_uname(uname,password):
    result=cursor.execute('''SELECT *from thesis.customer where username=%s and password=%s''',(uname,password))
    record = cursor.fetchone()
    if record!=None:
        flash("Username already taken!")
    
@app.route('/', methods = ['POST', 'GET'])
def signup():
    if request.method == 'GET':
        preparemodel()
        preparemodel2()

        return render_template('homepage.html')  

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password1 = request.form['password1']
        srole = request.form['Seller role']
        if (password!=password1):
           flash('Passwords do not match')
           return redirect(url_for('signup'))
        cursor = connection.cursor(buffered=True)

        result=cursor.execute('''SELECT *from thesis.customer where username=%s''',(username,))
        record = cursor.fetchone()
        if record!=None:
            flash("Username already taken!")
            return redirect(url_for('signup'))
        # cursor = connection.cursor()
        result=cursor.execute('''INSERT INTO thesis.customer VALUES(%s,%s,%s,%s,%s)''',(username,email,password,srole,"No subscribtion"))
        connection.commit()

        return redirect(url_for('login'))
        
@app.route('/forecast', methods = ['POST', 'GET'])
def forecast():
    if request.method == 'GET':
        return render_template('forecast.html',username=username)
     
    if request.method == 'POST':
        fprice=request.form['fprice']
        fmonth=request.form['fmonth']
        fyear=request.form['fyear']
        ffprice=runmodel2(fmonth, fyear, int(fprice))
        #ffprice = 10
        print(ffprice)
        flash('Price Forecasted :           '+str(int(ffprice))+'EGP')
        return redirect(url_for('forecast'))



if __name__ == '__main__':
   app.run(debug = True)
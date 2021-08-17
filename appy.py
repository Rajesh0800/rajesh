import mysql.connector
from datetime import datetime
mydb=mysql.connector.connect(host="localhost",user="root",password="rajesh07.b",database="food_delivery")
mycursor=mydb.cursor()
def validate_login(username,password):
    mycursor.execute("select * from customer_details where cusname like %s",(username,))
    data=mycursor.fetchall()
    print(data)
    if username==data[0][1] and password==data[0][2]:
        print("log in successfull")
        return 1
def addtocart(username):
    cgry=input("ENTER YOUR CATEGORY ----")
    cgry=cgry.lower()
    mycursor.execute("select * from stock_details where category like %s",(cgry,))
    data=mycursor.fetchall()
    for i in data:
        print("category--:",i[1])
        print("item_name--:",i[2])
        print("price--:",i[4])
        print("offer_%--:",i[5])
        print("-------------------------------------------------------------------------------------------")
    while True:
        isitemaddtocart=input("Do you want to add an item in your cart? If so, Please enter y -> yes or n -> no-----")
        isitemaddtocart=isitemaddtocart.lower()
        if isitemaddtocart=="yes":
            mycursor.execute("select * from customer_details where username like %s",(username,))
            jp=mycursor.fetchall()
            customer_id=jp[0][0]
            item_name = input('enter your item name')
            quantity = int(input('enter your item quantity'))
            mycursor.execute("select * from stock_details where item_name like %s",(item_name,))
            data=mycursor.fetchall()
            item_id=int(data[0][0])
            price=data[0][4]
            offer=data[0][5]
            off=(offer/100)
            costofone=price-(off*price)
            print(costofone)
            totalcost=costofone*quantity
            print(totalcost)
            mycursor.execute("insert into cart_details(cart_id,username,item_id,quantity,totalprice,customer_id,item_name)value(null,%s,%s,%s,%s,%s,%s)",(username,item_id,quantity,totalcost,customer_id,item_name,))
            mydb.commit()
        elif isitemaddtocart=="no":
            print("go and  place your  order \\\\\-------")
            break
    return 1
def order(username,password):
    print("DO YOU WANT TO ORDER THE IEMS?------")
    willing=input("TYPE YES ARE NO----")
    willing=willing.lower()
    if willing=="yes":
        mycursor.execute("select * from customer_details where username like %s",(username,))
        data=mycursor.fetchall()
        if username==data[0][1] and password==data[0][2]:
            customer_id=data[0][0]
        mycursor.execute("select * from cart_details where customer_id like %s",(customer_id,))
        cartdetails=mycursor.fetchall()
        for i in cartdetails:
            print("cart id=========",i[0])
            print("item_id=========",i[2])
            print("item_name=========",i[6])
            print("quantity=========",i[0])
            print("total price=========",i[0])
            print("-------------------------")
        for i in range (1):
            option=int(input("ENTER YOUR OPTION YOU LIKE RO ORDER"))
            if option!=0:
                idno= cartdetails[option-1][0]
                paymentmethod=input("enter your payment method 1.online 2.cod(cash on delivery)")
                paymentmethod=paymentmethod.lower()
                now=datetime.now()
                orderedtime=now.strftime('%Y-%m-%d %H:%M:%S')
                if paymentmethod=="online":
                    method="online"
                    accountHolderName = str(input('Enter your account holder name'))
                    accountNumber = int(input('Enter your account number'))
                    month = int(input('Enter your account valid month'))
                    year = int(input('Enter your account valid year'))
                    ccv = int(input('Enter your account valid ccv'))
                    address = str(input('Enter your address to deliver the order'))
                    recurring = str(input('want to be a recurring this order? y -> yes or n -> no'))
                    mycursor.execute("insert into order_details(order_id,cart_id,method,accountholdername,accountnumber,month,year,ccv,address,recurring,orderedtime)value(null,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(idno,accountHolderName,accountNumber,month,year,ccv,address,recurring,orderedtime,))
                    mydb.commit()
                    print("ordered successfully welcome!..............................")
                if paymentmethod=="cod":
                    method="cod"
                    address = str(input('Enter your address to deliver the order'))
                    recurring = str(input('want to be a recurring this order? y -> yes or n -> no'))
                    mycursor.execute("insert into order_details(cart_id,method,address,recurring,orderedtime)value(%s,%s,%s,%s,%s)",(idno,method,address,recurring,orderedtime,))
                    mydb.commit()
                    print("ordered successfully welcome!..............................")
                else:
                   print ("invalid option")
                   break
            else:
                break
        return    
destination=input("are u user or new_user or admin ? type your destination:")
destination=destination.lower()
if destination=="user":
    username=input("enter your user_name")
    password=input("enter your password")
    if validate_login(username,password):
        if addtocart(username):
            if order(username,password):
                print("ordered successfully welcome!..............................")
if destination=="new_user":
    username=input("ENTER YOUR USERNAME  :")
    password=input("ENTER YOUR PASSWORD  :")
    phn_no=int(input("ENTER YOUR MOBILE NO  :"))
    email=input("ENTER YOUR EMAIL ID  :")
    location=input("ENTER YOUR LOCATION")
    mycursor.execute("insert into customer_details(customer_id,username,password,phn_no,email,location) values(null,%s,%s,%s,%s,%s)",(username,password,phn_no,email,location))
    mydb.commit()
    print("resistration success, go to log in page")
    if validate_login(username,password):
        if addtocart(username):
            if order(username,password):
                print("ordered successfully welcome!..............................")

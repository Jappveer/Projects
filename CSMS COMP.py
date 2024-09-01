#_functions_
#INVENTORY#
def inventory():
    global p_type, p_brand, p_price
    p_id=random.randint(10,999)
    p_type=input("Enter Product Type:")
    p_qty=int(input("Enter Quantity:"))
    p_brand=input('Enter Brand:')
    p_price=int(input('Enter Product Price:'))
    inventory=(p_id,p_type,p_brand,p_qty,p_price)
    category=(p_id,p_type,p_brand)
    i_sql="insert into STOCK(P_ID,P_TYPE,P_BRAND,P_QTY,P_PRICE) values(%s,%s,%s,%s,%s)"
    c_sql="insert into CATEGORY(P_ID,P_CAT,P_BRAND) values(%s,%s,%s)"
    cursor.execute(i_sql,inventory)
    cursor.execute(c_sql,category)
    print('Record Successfully Added!')
    mycon.commit()

#BILLING#
def billing():
    b_code=random.randint(10,9999)
    print('RECIEPT NO.:',b_code)
    b_qty=int(input('Enter Quantity:'))
    b_disc=int(input('Enter Discount(if any):'))
    b_tax=int(input('Enter Tax:'))
    P=0
    for i in range(b_qty):
        b_item=input("Product:")
        b_brand=input('Brand:')
        b_no=int(input('Quantity:'))
        sql="select P_PRICE from STOCK where P_TYPE=%s and P_BRAND=%s"
        stock_sql="update stock set P_QTY=P_QTY- %s where P_TYPE=%s"
        inp=(b_item,b_brand)
        stock=(b_qty,b_item)
        cursor.execute(sql,inp)
        row=cursor.fetchmany(b_qty)
        pl=row[0]
        p=pl[0]
        P=P+(b_no*p)
        cursor.execute(stock_sql,stock)
    b_price=P-((b_disc*P)/100)+b_tax
    billing=(b_code,b_qty,b_disc,b_tax,b_price)
    b_sql="insert into BILLING(B_DATE,B_TIME,B_CODE,B_QTY,DISCOUNT,TAX,B_PRICE) values(curdate(),current_time(),%s,%s,%s,%s,%s)"
    cursor.execute(b_sql,billing)
    print('Record Successfully Added!')
    mycon.commit()

#DAILY_SALES
def daily_sales():
    ds_sql="select sum(B_PRICE) from billing where B_DATE=curdate()"
    cursor.execute(ds_sql)
    sales=cursor.fetchall()
    S_sales=sales[0][0]
    dsale=(S_sales,)
    s_sql="insert into DAILY_SALES(D_DATE,D_SALES) values(curdate(),%s)"
    cursor.execute(s_sql,dsale)
    print('Record Successfully Added!')
    mycon.commit()
        

#SELLERS#
def seller():
    s_id=int(input('Enter seller ID:'))
    s_name=input("Enter Seller's Name:")
    s_contact=int(input("Enter Seller's contact:"))
    seller=(s_id,s_name,s_contact)
    s_sql='insert into SELLER(S_ID,S_NAME,S_CONTACT) values(%s,%s,%s)'
    cursor.execute(s_sql,seller)
    print('Record Successfully Added!')
    mycon.commit()

#MONTHLY_SALES#
def monthly_sales():
    m=input('Enter Month Name:')
    ms_sql="select sum(D_SALES) from daily_sales where monthname(D_DATE)=%s"
    month=(m,)
    cursor.execute(ms_sql,month)
    msales=cursor.fetchall()
    M_sales=msales[0][0]
    msale=(m,M_sales)
    msql="insert into MONTHLY_SALES(M_MONTH,M_SALES) values(%s,%s)"
    cursor.execute(msql,msale)
    print('Record Successfully Added!')
    mycon.commit()        

#DISPLAY
def display(tab):
    if tab=='billing':
        sql="select * from billing"
    if tab=='daily sales':
        sql="select * from daily_sales"
    if tab=='monthly sales':
        sql="select * from monthly_sales"
    if tab=='sellers':
        sql="select * from sellers"
    if tab=='stock':
        sql="select * from stock"
    cursor.execute(sql)
    result=cursor.fetchall()
    for i in result:
        print(i)
        
    
#__main__
import random
import mysql.connector as ctor
mycon=ctor.connect(host="localhost",user='root',passwd='@Jappveer20',database='CSMS')  #connecting to MySQL
import csmslogin as login                                                           #Login
store=login.store
print('Welcome To',store,'Database')
ch=input('Press Y to continue_')
flag=0
while flag==0:
    if ch=='Y' or ch=='y':
        print('Please Login')
        user1=input('enter your username')
        pass2=input('enter your password')
        if user1==login.user and pass2==login.pass1:
            print('Signing in..')
            flag=1
        else:
            print('incorrect login details')
            flag=0
    else:
         break

if mycon.is_connected():                              
    print("Connecting to database... ... SUCCESSFULLY CONNECTED!")

    
cursor=mycon.cursor()

print()
print()
op1=0
while op1==0:
    print("_______")                                                                  
    print('MENU')
    print('1. Inventory')
    print('2. Billing')
    print('3. Seller Details')
    print('4. Sales')
    print('5. Display')
    print('6. Exit')
    op1=int(input('Enter Your Choice_'))
                                                                                 #operations based on choice
    while op1==1:                                                              
        inventory()
        op1=int(input("Press 1 to continue \nPress 0 to return to Main Menu"))
        
    while op1==2:
        billing()
        op1=int(input('Press 2 to continue \nPress 0 to return to Main Menu'))

    while op1==3:
        seller()
        op1=int(input('Press 3 to continue \nPress 0 to return to Main Menu'))

    while op1==4:
        ans=input('Press D for Daily Sales, M for Monthly Sales:')
        if ans=='d' or ans=='D':
            daily_sales()
            op1=int(input('Press 0 to return to Main Menu'))
        if ans=='m' or ans=='M':
            monthly_sales()
            op1=int(input('Press 0 to return to Main Menu'))
    while op1==5:
        tab=input('What table would you like to display?')
        display(tab)
        op1=int(input('Press 5 to continue \nPress 0 to return to Main Menu'))
    while op1==6:
        print('Exiting...')
        break


        
             
            
   







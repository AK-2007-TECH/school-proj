import mysql.connector
mydb = mysql.connector.connect(                   #ensuring python-sql connectivity
  host="localhost",
  user="root",
  password="admin",
  database='med_management'
)

mycursor = mydb.cursor()
mycursor.execute("USE Med_Management")
try:
          mycursor.execute("CREATE TABLE Medicines (Product VARCHAR(25) primary key,Quantity integer,Price float,ExpiryDate date,Manufacturer varchar(30))")
except:
          pass
try:
          mycursor.execute("CREATE TABLE Purchase_History (Product VARCHAR(25) primary key,Quantity integer,Manufacturer varchar(30))")
except:
          pass
def menu1():
          print('-------------MEDICINE SECTION-------------')
          print("""1 - Insert medicine details\n
2 - Delete a medicine\n
3 - Update a medicine\n
4 - Search a medicine\n
5 - Show the entire list\n
6 - Exit the medicine section""")
          while True:
                    choice=int(input('Enter your choice'))
                    if choice==1:
                              prod=input('Enter medicine name ')
                              Qty=int(input('Enter the quantity'))
                              ExpDate=input('Enter Expiry date')
                              Price=float(input('Enter the price'))
                              Manu=input("Enter the manufacturer's name")
                              sql="INSERT INTO MEDICINES (Product,Quantity,Price,ExpiryDate,Manufacturer) VALUES (%s,%s,%s,%s,%s)"
                              val=(prod,Qty,Price,ExpDate,Manu)
                              mycursor.execute(sql,val)
                              mydb.commit()
                              print(mycursor.rowcount," details inserted")
                    elif choice==2:
                             prod=input('Enter the medicine to delete from the table ')
                             mycursor.execute("delete from medicines where Product='"+prod+"'")
                             mydb.commit()
                             print(prod,' have been deleted')
                              
                    elif choice==3:
                              prod=input('Enter the medicine you want to update')
                              print('***Which parameter do you want to modify')
                              while True:
                                        print('***Press q for changing the quantity')
                                        print('***Press p for changing the price')
                                        print('***Press e for changing the expiry date')
                                        print('***Press m for changing the manufacturer')
                                        print('***Press 1 to exit the updation menu')
                                        ch=input('Enter q/p/e/m/1 :')
                                        if ch.upper() =='Q':
                                                  qt=int(input('Enter the new quantity '))
                                                  sql="update medicines set Quantity=%s  where Product='"+prod+"'"
                                                  val=(qt,)
                                        elif ch.upper()=='P':
                                                  pr=float(input('Enter the new price '))
                                                  sql="update medicines set Price=%s where Product='"+prod+"'"
                                                  val=(pr,)
                                        elif ch.upper()=='E':
                                                  ex=input('Enter the new Expiry date ')
                                                  sql="update medicines set ExpiryDate=%s where Product='" +prod+"'"
                                                  val=(ex,)
                                        elif ch.upper()=='M':
                                                  man=input('Enter the new manufacturer')
                                                  sql="update medicines set Manufacturer=%s where Product='"+prod+"'"
                                                  val=(man,)
                                        elif ch=='1':
                                                  break
                                        else:
                                                  print('Enter a valid choice')
                                        mycursor.execute(sql,val)
                                        mydb.commit()
                                        print('Updated.')
                    elif choice==4:
                              prod=input('Enter the product you want to search ')
                              mycursor.execute("select * from medicines where Product='"+prod+"'")
                              myresult=mycursor.fetchall()
                              for x in myresult:
                                        print(prod,'        :' ,'Quantity=',x[1],'        :', 'Price=',x[2],'          :','Expiry date=',x[3],'     :','Manufacturer=',x[4])
                              if len(myresult)==0:
                                        print("Search unsuccessful!!")
                    elif choice==5:
                              sql="select * from medicines "
                              mycursor.execute(sql)
                              myresult=mycursor.fetchall()
                              print("Medicine",'***',"Quantity",'***',"Price",'***',"Expiry date",'***',"Manufacturer")
                              for x in myresult:
                                        print(x[0],'\t','||',x[1],'\t','||',x[2],'\t','||',x[3],'\t','||',x[4])
                    elif choice==6:
                              if(input("Are you sure you want to leave the medicine section? Y/N").lower())=='y':
                                        break

def menu2():
          print('-------------SALES SECTION-------------')
          while True:
                    print('''1 - Search for a medicine\n
2 - Placing orders\n
3 - Exit Sales section ''')
                    ch=int(input('Enter your selection'))
                    if ch==1:
                              prod=input('Enter the product you want to search ')
                              mycursor.execute("select * from medicines where Product='"+prod+"'")
                              myresult=mycursor.fetchall()
                              for x in myresult:
                                        print(prod,'        :' ,'Quantity=',x[1],'        :', 'Price=',x[2],'          :','Expiry date=',x[3],'     :','Manufacturer=',x[4])
                              if len(myresult)==0:
                                        print("Search unsuccessful!!")
                    elif ch==2:
                              global AMT
                              AMT=0
                              global MEDS
                              MEDS=[]
                              global QTY
                              QTY=[]
                              while True:
                                        prod=input('Enter the product you want to purchase ')
                                        qty=int(input("Enter the quantity  you'd like to purchase "))
                                        sql="select * from medicines where Product='"+prod+"'"
                                        mycursor.execute(sql)
                                        myresult=mycursor.fetchall()
                                        if len(myresult)==0:
                                                            print("No such medicine!!")
                                        for x in myresult:
                                                  if qty>x[1]:
                                                            print('Only ',x[1],' are available!')
                                                            print('Would you like to proceed to buy ',x[1],' nos of ',prod,'? ')
                                                            ch=input("Enter Y/N")
                                                            if ch.lower()=='y':
                                                                      AMT+=(x[2]*qty)
                                                                      MEDS.append(prod)
                                                                      QTY.append(x[1])
                                                                      print('The amount is: ',x[2]*x[1])
                                                                      mycursor.execute("delete from medicines where Product='"+prod+"'")
                                                                      mydb.commit()
                                                            else:
                                                                      print('Exiting Sales Section...')
                                                                      break
                                                  else:
                                                            AMT+=(x[2]*qty)
                                                            MEDS.append(prod)
                                                            QTY.append(qty)
                                                            u=x[1]-qty
                                                            print('The amount is: ',x[2]*qty)
                                                            sql="update medicines set quantity=%s where Product=%s"
                                                            val=(u,prod)
                                                            mycursor.execute(sql,val)
                                                            mydb.commit()
                                        
                                        if (input('Do you wish to continue? Y/N ')).lower()=='n':
                                                  break
                              print("*******The total amount :",AMT)
                    elif ch==3:
                              break
def menu3():
                    print("-------------PURCHASE SECTION-------------")
                    while True:
                              print('''{1} - Purchase\n{2} - Purchase history\n{3} - Clear Purchase history\n{4} - Exit the purchase section ''')
                              ch=int(input("Enter your choice "))
                              if ch==1:
                                        prod=input("Enter the medicine you'd like to purchase ")
                                        man=input("Enter the manufacturer you'd wish to buy from ")
                                        unit=int(input("Enter the quantity you'd wish to purchase "))
                                        exp=input("Enter expiry date the order should have ")
                                        price=float(input("Enter the price per piece you're paying for the order "))
                                        print('Your order is :','\tProduct=',prod,'\tunit=',unit)
                                        if(input('Are you sure to purchase? Y/N ').lower())=='y':
                                                  print('The order has been sent to ',man)
                                                  sql="insert into purchase_history (Product,Quantity,Manufacturer) values (%s,%s,%s)"
                                                  val=(prod,unit,man)
                                                  mycursor.execute(sql,val)
                                                  mydb.commit()
                                                  sql1="insert into medicines(Product,Quantity,Price,ExpiryDate,Manufacturer) values(%s,%s,%s,%s,%s)"
                                                  val1=(prod,unit,price,exp,man)
                                                  mycursor.execute(sql1,val1)
                                                  mydb.commit()
                                                  
                                        else:
                                                  continue
                              elif ch==2:
                                        sql="SELECT * from purchase_history"
                                        mycursor.execute(sql)
                                        myresult=mycursor.fetchall()
                                        for x in myresult:
                                                  print('******',x);
                              elif ch==3:
                                        if(input("Are you sure to delete the purchase history? Y/N ")).lower()=='y':
                                                  sql="delete from purchase_history"
                                                  mycursor.execute(sql)
                                                  mydb.commit()
                                                  print("The history has been removed")
                              elif ch==4:
                                        break

def menu4():
                    print("-------------BILL SECTION-------------")
                    while True:
                              print("{1} - To review the bill\n{2} - Proceed with the payment\n{3} -  Exit the bill section")
                              ch=int(input("Enter the choice "))
                              if ch==1:
                                        name=input("Enter the customer's name")
                                        print(name)
                                        for x in range (len(MEDS)):
                                                  print('=====',x+1,')',MEDS[x],'\t\t-\t',QTY[x])
                                        print("===== Total amount =",AMT)
                                        print("===== GST=5%")
                                        print("===== Total payable amount=",AMT+0.05*AMT)
                              elif ch==2:
                                        if(input("Are you sure to proceed? Y/N ")).lower()=='y':
                                                  ch=int(input("How would you like to make the transaction?\n{1} - Cash\n{2} - Debit Card\n{3} - Credit Card\n{4} - GooglePay\n{5} - Other"))
                                                  print("Thanks for shopping from us!")
                                                  break
                              elif ch==3:
                                        print('Exiting the bill section...')
                                        break
                                        
                                                  
print("MEDICAL STORE MANAGEMENT")
while True:
          print(('''*--------------MEDICAL STORE-------------*\n
select{1} - Medicine Section \n
select{2} - Sales Section \n
select{3} - Purchase Section \n
select{4} - Report/Bill Section \n
select{5} - Exit'''))
          ch=int(input('Enter your choice'))
          if ch==1:
                    menu1()
          elif ch==2:
                    menu2()
          elif ch==3:
                    menu3()
          elif ch==4:
                    menu4()
          elif ch==5:
                    exit()
          else:
                    print("Enter a valid choice!!")

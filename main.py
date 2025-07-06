import os
import json

admin_username = "Kmitmanagement"
admin_password = "kmit123@password"
userdetails = {}
c = input("Are you a Admin?(y/n)")
if c == 'y':
    print("Welcome Admin!!")
    username = input("Enter your username : ")
    if username == admin_username :
        password = input("Ennter your poassword : ")
        if password == admin_password :
            print("Login Successful!!!")
            # choice = input("Do you want to Edit or Add New?")
            choice = int(input("Press 1 for adding category, 2 for adding item"))
            choice = 1
            if choice == 1:
                check=1
                while check==1:
                    category_name=input("Enter the name of Category : ")
                    d1={}
                    l1=[]
                    k=int(input("enter no of products you want to add : "))
                    for x in range(k):
                        dict1={}
                        dict1["product_name"]=input("Enter product name : ")
                        dict1["brand"]=input("Enter product brand : ")
                        dict1["price"]=int(input("Enter product price: "))
                        dict1["description"]=input("Enter product description : ")
                        l1.append(dict1)
                    d1[category_name+"_products"]=l1
                    with open("./categories/"+category_name+".json","w") as file:
                        json.dump(d1,file)
                    print(" to add another category press 1 \n otherwise press 0")
                    k=int(input())
                    check=k  
            elif choice == 2:
                pass
            else:
                print("Invalid Input!!")
                quit()
        else : 
            print("Invalid password!!")
            quit()
    else:
        print("Invalid username!!!")
        quit()
elif c=='n':
    username = input("Enter your name : ")
    auth = False
    temp = {}
    with open("./users/user_db.json","r") as userdb:
        userdb_dict = json.load(userdb)
        userdetails = userdb_dict
        temp = userdb_dict
        if username in userdb_dict:
            print(f"Welcome {username}!!")
            userpass = input("Enter your password : ")
            if userpass == userdb_dict[username]["password"]:
                print("Login Successful!!!")
                auth = True
            else :
                print("Invalid passwoerd.")
                quit()

        else :
            print("You are not in our database, please register to continue.")
    if auth == False:
        with open("./users/user_db.json","w") as userdb:
            userpass = input("Enter your password : ")
            temp[username] = {}
            temp[username]["password"] = userpass
            temp[username]["ph"] = input("Enter your Phone number : ")
            temp[username]["email"] = input("Enter your email : ")
            temp[username]['address']={}
            temp[username]['address']['village']=input("Enter your village : ")
            temp[username]['address']['city']=input("Enter your city : ")
            temp[username]['address']['state']=input("Enter your state : ")
            temp[username]['address']['pincode']=input("Enter your pincode : ")
            
            json.dump(temp,userdb)
            print("Registration Succesful!!!")


    print("Welcome to KMIT Shopping Mall!!!")
    print("Choose the categories from below.")
    listofcat = os.listdir("./categories")
    for x in listofcat:
        print(x[:-5])
    d={}
    d["name"] = username
    d["ph"] = userdetails[username]['ph']
    d["address"]=userdetails[username]['address']
    usercart = []
    catbool = True
    while catbool == True:
        category_selected  = input("Enter the category here : ")
        category_selected = category_selected+".json"
        with open("./categories/"+category_selected,"r") as catdata:
            catdata_dict = json.load(catdata)
            probool = True
            while probool == True:
                print("Select to view a product info : ")
                for x in catdata_dict[category_selected[:-5]+"_products"] : 
                    print(f"{x['product_name']} --- {x['price']}")
                proSel = input("Enter product name : ")
                proCount = 0
                for x in list(catdata_dict[category_selected[:-5]+"_products"]) : 
                    if proSel == x['product_name'] :
                        print(f"{x["product_name"]} Details:")
                        print(f"This product was brought to you by {x["brand"]},{x["description"]}")
                        print(f"Price : {x["price"]}")
                        proCount = int(input("Enter number of products to buy : "))
                        carted = input("Press \'c\' for add to cart \n \'b\' to checkout.")
                        if carted == 'c':
                            usercart.append({"product_name":x['product_name'],"price":x['price'],"qty":proCount,"category" : category_selected})
                            des = input("Press 1 to go select other category \n Press 2 to stay in the current category.")
                            if des == '1':
                                catbool = True
                                probool = False
                            elif des == '2':
                                probool = True
                        elif carted == 'b':
                            catbool = False
                            probool = False
                            usercart.append({"product_name":x['product_name'],"price":x['price'],"qty":proCount,"category" : category_selected})
                            ordered_products=usercart
                            d['cart']=usercart
                            bill=0
                            print("-------------------BILL------------------")
                            print(f"Name : {username} \nPhone number : {d['ph']} \nAdress : \nVillage : {d['address']['village']}\nCity : {d['address']['city']}\nState:{d['address']['state']}\nPin Code : {d['address']['pincode']}")

                            for x in ordered_products:
                                print(f"product name : {x["product_name"]},total product amount : {x["price"]*x["qty"]}")
                                bill+=int(x["price"]*x["qty"])
                            bill=float(bill)
                            gst=0.025*bill
                            totalbill=bill+gst
                            print(f"Total Amount to be paid = {totalbill}")
                            data={}
                            count = 0
                            try:
                                with open('./transactions/'+username+'.json','r') as file:
                                    data = json.load(file)
                                    print(data)
                                    print(data['noOfOrders'])
                                    count = data['noOfOrders']
                                    print(count)
                            except :
                                with open('./transactions/'+username+'.json','w') as file:
                                    json.dump({"noOfOrders" : 0},file)
                                    print("write")
                            with open('./transactions/'+username+'.json','w') as file:
                                trans_details = {str(count+1) : d}
                                for x in data:
                                    if data[x] != int :
                                        trans_details.update({x:data[x]})
                                data.update(trans_details)
                                print(trans_details)
                                data['noOfOrders'] = count+1
                                print(data)
                                json.dump(data,file)


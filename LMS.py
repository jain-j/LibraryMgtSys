#!/usr/bin/env python
# coding: utf-8

import sqlite3
from getpass import getpass
from datetime import datetime

#copy your db path here as string
db_path='''E:\Study_Material\Project Work\LMS\LMS.db'''

conn,cursor=None,None

option1,option2=0,0

#function to connect to database with given path in db_path
def connect_db():
    global conn,cursor
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    print('DB Connected')

#function to disconnect from database
def disconnect_db():
    global conn
    global cursor

    conn.commit()
    cursor.close()
    conn.close()


def get_menu(choice='option1'):

    global option1

    if choice=='option1':
        choice=option1

    menus={'main':['___________Library Management System______________','Book Info','Member Info','Author Info','Transact Book','Settings','About Me','Logout->'],
            1:['Book Information___','Show all books','Show book','Add book','Delete book','Update book','Show issued books','Back to main menu'],
            2:['Member Information___','Show all members','Show Member','Add Member','Delete Member','Update Member','Back to main menu'],
            3:['Author Information___','Show all authors','Show Author','Add Author','Delete Author','Update Author','Back to main menu'],
            4:['Transact Book___','Issue Book','Renew Book','Return Book','Calculate Fine','Collect Fine','Back to main menu'],
            5:['Settings___','Change Password','Back to main menu'],
            6:['About Me___:','Back to main menu'],
            7:['Logout___']
            }

    back_index=len(menus[choice])-1
    menu='\n___'+menus[choice][0]
    for i,label in enumerate(menus[choice]):
        if i==0:
            continue
        menu+='\n\t\t'+str(i)+'. '+label
    return menu,back_index


def get_query(login=False):

    queryDict={ 0:'''select uname,pass from User where uname=?;''',
                11:'''select * from Book;''',
                12:'''select * from Book where book_id= ?;''',
                13:'''insert into Book values(?,?,?,?,?);''',
                14:'''delete from Book where book_id=?;''',
                15:'''update Book set {0}={1} where book_id={2};''',
                16:'''select M.member_id,M.Fname,M.Lname,M.contact_no,B.book_id,B.title,B.available,br.issue_date from Member M,Book B,Borrows br where br.member_id=M.member_id and br.book_id=B.book_id and br.return_date is NULL;''',
                21:'''select * from Member;''',
                22:'''select * from Member where member_id=?;''',
                23:'''insert into Member values(?,?,?,?,?,?);''',
                24:'''delete from Member where member_id=?;''',
                25:'''update Member set {0}={1} where member_id={2};''',
                31:'''select * from Author;''',
                32:'''select * from Author where author_id= ?;''',
                33:'''insert into Author values(?,?,?);''',
                34:'''delete from Author where author_id=?;''',
                35:'''update Author set {0}={1} where author_id={2};''',
                41:['''insert into Borrows(member_id,book_id,issue_date) values(?,?,?);''',
                    '''update Book set available=available-1 where book_id=?;'''],
                42:'''update Borrows set renew_date=? where member_id=? and book_id=?;''',
                43:['''update Borrows set return_date=? where member_id=? and book_id=?;''',
                    '''update Book set available=available+1 where book_id=?;'''],
                44:'''select issue_date,renew_date,return_date from Borrows where member_id=? and book_id=?;''',
                45:'''update Borrows set fine_collected=? where member_id=? and book_id=?;''',
                51:'''update User set pass=? where pass=? and uname=? and session=1;'''
                }

    if login==True:
        return queryDict[0]
    
    global option1
    global option2

    key = int(str(option1)+str(option2))
    
    return queryDict[key]


def get_input():

    global option1,option2

    numeric_format=['book id','member id','author id','edition','available copies','contact number','collected fine']
    date_format=['renew date  (DD-MM-YYYY)','return date (DD-MM-YYYY)','issue date (DD/MM/YYYY)']
    
    numeric_attri=['book_id','member_id','author_id','edition','available','contact_no','fine_collected']
    date_attri=['issue_date','renew_date','return_date']

    key = int(str(option1)+str(option2))
    #print(key)
    
    input_dict={11:[],
                12:['book id'],
                13:['book id','title','author id','edition','available copies'],
                15:['attribute to update','update value','book id'],
                14:['book id'],
                16:[],
                21:[],
                22:['member id'],
                23:['member id','first name','last name','contact number','member type','address'],
                24:['member id'],
                25:['attribute to update','update value','member id'],
                31:[],
                32:['author id'],
                33:['author id','first name','last name'],
                34:['author id'],
                35:['attribute to update','update value','author id'],
                41:['member id','book id','issue date (DD/MM/YYYY)'],
                42:['renew date (DD/MM/YYYY)','member id','book id'],
                43:['return date (DD/MM/YYYY)','member id','book id'],
                44:['member id','book id'],
                45:['collected fine','member id','book id'],
                51:['new password','current password'],
               }

    inputs=[]
    flag=''
    for ask in input_dict[key]:
        que='\nEnter '+ask+': '
        i= getpass(que) if option1==5 else input(que)
        if ask in numeric_format:
            try:
                inputs.append(int(i))
            except:
                print('Enter valid number!!!')
        elif ask in date_format:
            try:
                inputs.append(datetime.strptime(i,'%d/%m/%Y').date())
            except:
                print('Enter valid date!!!')
        elif flag=='int':
            inputs.append(int(i))
            flag=''
        elif flag=='date':
            inputs.append(datetime.strptime(i,'%d/%m/%Y').date())
            flag=''
        elif flag=='str':
            inputs.append('"'+i+'"')
            flag=''
        elif ask=='attribute to update':
            inputs.append(i)
            if i in numeric_attri:
                flag='int'
            elif i in date_attri:
                flag='date'
            else:
                flag='str'
        else:
            inputs.append(i)
    print()
    return inputs


def get_output():
    global option1,option2
    
    key = int(str(option1)+str(option2))
    
    output_dict={12:['book id','title','author id','edition','available copies'],
                 11:['book id','title','author id','edition','available copies'],
                 16:['member id','First name','Last name','contact','book id','title','available copies','issue date'],
                 22:['member id','First name','Last name','contact','member type','Address'],
                 21:['member id','First name','Last name','contact','member type','Address'],
                 32:['author id','First name','Last name'],
                 31:['author id','First name','Last name'],
                 44:['Calculated fine']
                }
    return output_dict[key]


def Info():
    global option2
    
    while(True):
        menu,back_index=get_menu()
        print(menu,end='')
        
        try:
            option2=int(input('\t Enter Option: '))
            #print(option2)
        except ValueError as ve:
            print("\n!!!! Select Valid Option !!!!\n")
            continue

        if 0 < option2 < back_index:
            #get input & query for given choice...
            
            if option1==1 and option2==3:
                print("Note: author record should present in DB before inserting it in book's records!!!")
            
            inputs=get_input()
            query=get_query()
            
            try:
                if option2==5:
                    #print(inputs)
                    cursor.execute(query.format(*inputs))
                else:
                    cursor.execute(query,inputs)
            except sqlite3.Error as err:
                #print(err)
                print('Query execution failed due to '+str(err))
            except:
                print('Query execution failed due to Unknown error')
            else:
                result=cursor.fetchall()
                rc=cursor.rowcount
                if 'select' in query and result!=[]:
                    label=get_output()
                    print('\n') 
                    for row in result:
                        for i,value in enumerate(row):
                            print(label[i],':\t',value)
                        print('\n')

                if 'delete' in query:
                    print(rc," record deleted.")
                elif 'insert' in query:
                    print(rc," record inserted.")
                elif 'update' in query:
                    print(rc," record updated.")
                elif 'select' in query:
                    print(len(result)," records found.")
                print('Query execution successfull.')
                
        elif option2==back_index:
            break
        else:
            print("\n!!!! Select Valid Option !!!!\n")


def TransactBook():
    global option2
    
    multiple_queries_options_list=[1,3]
    
    while(True):
        menu,back_index=get_menu()
        print(menu,end='')
        
        try:
            option2=int(input('\t Enter Option: '))
            #print(option2)
        except ValueError as ve:
            print("\n!!!! Select Valid Option !!!!\n")
            continue
        
        if 0 < option2 < back_index:
            #get input & query for given choice...
            if option2==1:
                print('Note: memeber and book should be present in DB before issueing it.')
            inputs=get_input()
            query=get_query()
            
            try:
                #print(inputs)
                if option2 in multiple_queries_options_list:
                    if option2==1:
                        bid=inputs[1]
                    elif option2==3:
                        bid=inputs[2]
                    cursor.execute(query[1],[bid])
                    cursor.execute(query[0],inputs)
                else:
                    cursor.execute(query,inputs)
                rc=cursor.rowcount
            except sqlite3.Error as err:
                #print(err)
                print('Query execution failed due to '+str(err))
            except:
                print('Query execution failed due to Unknown error')
            else:
                result=cursor.fetchall()
                if 'select' in query and result!=[]:
                    
                    issue,renew,retn=result[0][0],result[0][1],result[0][2]
                    fine=0
                    
                    #if member not returned the book then retn which is return date will be None therwise it will be a date
                    if retn==None:
                        start_date=datetime.date(datetime.now())
                        
                        # if Member renewed the book then renew var will not be None
                        # if member not renwed book since issued. so, fine will be calculated since issue date.
                        
                        last_date = renew if renew!=None else issue
                        last_date=datetime.strptime(last_date,'%d/%m/%Y').date()
                            
                        diff=(start_date-last_date).days
                        fine = diff-15 if diff>15 else 0
                                
                                
                    print(get_output()[0],': ',fine)
                elif option2!=4:
                    print(rc,' record updated.')
                print('Query execution successfull.')
                
        elif option2==back_index:
            break
        else:
            print("\n!!!! Select Valid Option !!!!\n")


def Settings(usr):
    global option2

    menu,back_index=get_menu()
    print(menu,end='')
    
    while(True):
        try:
            option2=int(input('\t Enter Option: '))
            #print(option2)
        except ValueError as ve:
            print("\n!!!! Select Valid Option !!!!\n")
            continue

        if 0 < option2 < back_index:
            #get input & query for given choice...

            inputs=get_input()
            query=get_query()

            try:
                #print(inputs)
                cursor.execute(query,inputs+[usr])
                rc=cursor.rowcount
            except sqlite3.Error as err:
                #print(err)
                print('Query execution failed due to '+str(err))
            except:
                print('Query execution failed due to Unknown error')
            else:
                if rc==1:
                    print('password reset successfull.')
                print('Query execution successfull.')
        elif option2==back_index:
            break
        else:
            print("\n!!!! Select Valid Option !!!!\n")


def Login(usr):
    query=get_query(True)
    try:
        cursor.execute(query,[usr])
        r=cursor.fetchall()
    except sqlite3.Error as err:
        print('Invalid Username or password')
    except:
        print('Query execution failed due to Unknown error')

    return r[0]


def About():

    global option2

    menu,back_index=get_menu()
    print(menu,end='')
    
    print('''\n\n    Hello, I am Kuldeep Aurora. I am student of B.Tech. Computer Engineering. 
I have built this small scale library managemant system as my miniproject.
Languages used: python
database used: sqlite3''')
    
    try:
        option2=int(input('\t Enter Option: '))
    except ValueError as ve:
        print("\n!!!! Select Valid Option !!!!\n")

    if option2==back_index:
        return


def Logout():
    if 'y' == input('\nAre you sure to proceed? (y/n) :').lower():
        disconnect_db()
        print("\nDB Committed Successfully.\nDB Connection Closed.\nLogout Successfull.\n")
        return True
    else:
        return False


if __name__ == '__main__':

    connect_db()
    
    usr=input("Username: ")
    pwd=getpass("Password: ")

    u,p=Login(usr)
    
    if usr==u and p==pwd:
        print('...Welcome...')
        while(True):
            menu,back_index=get_menu('main')
            print(menu,end='')
            
            try:
                option1=int(input('\t Enter Option: '))
            except ValueError as ve:
                print("\n!!!! Select Valid Option !!!!\n")
                continue

            if 0<option1<7:
                if option1<4:
                    Info()
                else:
                    if option1==4:
                        TransactBook()
                    elif option1==5:
                        Settings(usr)
                    elif option1==6:
                        About()

            elif option1==7:
                if Logout():
                    break

            else:
                print("\n!!!! Select Valid Option !!!!\n")
                continue
    else:
        print("Invalid Username or password \nTry Again....")

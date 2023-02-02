# %%
import pywhatkit
import pandas as pd
import sys,os
import keyboard,time

# %%
filename=input('Enter the csv file name present in the same location where this program is - ')
#filename='phonenumber.csv'

# %%
def check(filename):
    try:
        dt=pd.read_csv(filename)
        return 1
    except:
        return 0

# %%
def search(other):
    if other!=None:
        try:
            df=pd.read_csv(filename)
            df.set_index('PHONENUMBER',drop=False,inplace=True)
            inp=[other]
        except:
            return 1
    else:
        try:
            df=pd.read_csv(filename)
            df.set_index('PHONENUMBER',drop=False,inplace=True)
            print('Enter the phone numbers by line space and include country code (After giving input ,press Ctrl+Z and hit enter to stop user input) - ')
            inp=sys.stdin.read().split('\n')
        except:
            print(f'ERROR,NO {filename} EXISTS OR DOES NOT CONTAIN ANY VALUES')
            print('\nPress esc key to to show menu')
            keyboard.wait('esc')
            return 0
    
    for i in inp:
        i=i.replace(' ','')
        i=i.replace('+','')
        
        if i=='':
            continue
        try:
            df.loc['a'+i]
            if other!=None:
                return 0
            print(f'{i} - Present')
        except:
            if other!=None:
                return 1
            print(f'{i} - Absent')

    print('\nPress esc key to to show menu')
    keyboard.wait('esc')

# %%
def insert():
    arr=[]
    H=False
    if not(check(filename)):
        H=True
    
    print('Enter the phone numbers by line space and include country code (After giving input ,press Ctrl+Z and hit enter to stop user input) - ')
    inp=sys.stdin.read().split('\n')
    c=0
    for i in inp:
        i=i.replace(' ','')
        i=i.replace('+','')
        if i=='':
            continue
        if search(i):
            arr.append('a'+i)
            c+=1
        else:
            print(f'{i} is ALREADY PRESENT')
    arr=list(set(arr))
    if len(arr):
        valid=[0]*c
        df=pd.DataFrame({'PHONENUMBER':arr,'CHECKSENDMSG':valid})
        df.to_csv(filename,mode='a',index=False,header=H)
        print('SUCCESS')
    
    print('\nPress esc key to to show menu')
    keyboard.wait('esc')


# %%
def update():
    curr=input('Enter the current phone number you want to update with country code - ')
    new=input('Enter the new phone number with country code - ')
    curr=curr.replace(' ','')
    new=new.replace(' ','')
    curr=curr.replace('+','')
    new=new.replace('+','')
    if curr=='' or new=='':
        print('INVALID')
        return
    
    f=1
    try:
        df=pd.read_csv(filename)
    except:
        f=0
    if f and not(search(curr)) and search(new):
        df.set_index('PHONENUMBER',drop=False,inplace=True)
        df.loc['a'+curr]='a'+new
        df.reset_index(drop=True)
        df.to_csv(filename,mode='w',index=False,header=True)
    elif search(new):
        if input('The value is not present in the database, want to insert it? (Y/N) ').lower()=='y':
            H=False
            if not(check(filename)):
                H=True
            
            df=pd.DataFrame({'PHONENUMBER':['a'+new],'CHECKSENDMSG':[0]})
            df.to_csv(filename,mode='a',index=False,header=H)
    else:
        print(f'The new number {new} is already in database')
    
    print('\nPress esc key to to show menu')
    keyboard.wait('esc')

# %%
def delete():
    print('Enter the phone numbers by line space and include country code (After giving input ,press Ctrl+Z and hit enter to stop user input) - ')
    inp=sys.stdin.read().split('\n')
    try:
        df=pd.read_csv(filename)
        df.set_index('PHONENUMBER',drop=False,inplace=True)
    except:
        print('No numbers present to delete')
        print('\nPress esc key to to show menu')
        keyboard.wait('esc')
        return
    for i in inp:
        i=i.replace(' ','')
        i=i.replace('+','')
        if i=='':
            continue
        if not(search(i)):
            df.drop(['a'+i], inplace = True)
            print(f'{i} deleted')
    df.reset_index(drop=True)
    df.to_csv(filename,mode='w',index=False,header=True)

    print('\nPress esc key to to show menu')
    keyboard.wait('esc')

# %%
def menu():
    menu='''

----------------------------------------Welcome----------------------------------------
                    '1' or 'INS'         for insert phone number
                    '2' or 'DEL'         for deleting phone number
                    '3' or 'UPD'         for update phone number
                    '4' or 'SRCH'        for searching phone number
                    '5' or 'SENDMSG'     for sending message to all
                    '6' or 'SENDIMGMSG'  for sending picture & message to all
                    '7' or 'SENDIMG'     for sending picture only to all
                    '8' or 'CHECKPREV'   for generating numbers of the previous msg where the message is not send
                    '9' or 'EXIT'        for quit
---------------------------------------------------------------------------------------

'''
    os.system('cls')
    print(menu)

# %%
def sendmessage():
    try:
        df=pd.read_csv(filename)
    except:
        print('No numbers present to send')
        print('\nPress esc key to to show menu')
        keyboard.wait('esc')
        return
    print('Enter you message here (After giving input ,press Ctrl+Z and hit enter to stop user input) - ')
    message=sys.stdin.read()
    df['CHECKSENDMSG']=0
    df.set_index('PHONENUMBER',drop=False,inplace=True)
    try:
        for i in df.index:
            pywhatkit.sendwhatmsg_instantly('+'+i.replace('a',''), message ,tab_close=True,close_time=1)
            df.loc[df.index==i,'CHECKSENDMSG']=1
            time.sleep(0.7)
    except:
        df.reset_index(drop=True)
        df.to_csv(filename,mode='w',index=False,header=True)
        print('Connection error/Whatsapp Database error')
        return
    print('Success')
    df.reset_index(drop=True)
    df.to_csv(filename,mode='w',index=False,header=True)
    print('\nPress esc key to to show menu')
    keyboard.wait('esc')

# %%
def sendimgmessage():
    try:
        df=pd.read_csv(filename)
    except:
        print('No numbers present to send')
        print('\nPress esc key to to show menu')
        keyboard.wait('esc')
        return
    path=input('Enter image path here - ')
    print('Enter you caption here (After giving input ,press Ctrl+Z and hit enter to stop user input) - ')
    message=sys.stdin.read()
    df['CHECKSENDMSG']=0
    df.set_index('PHONENUMBER',drop=False,inplace=True)
    try:
        for i in df.index:
            pywhatkit.sendwhats_image('+'+i.replace('a',''), path,message,tab_close=True,close_time=1)
            df.loc[df.index==i,'CHECKSENDMSG']=1
            time.sleep(0.7)
    except:
        df.reset_index(drop=True)
        df.to_csv(filename,mode='w',index=False,header=True)
        print('Connection error/Whatsapp Database error')
        return
    print('Success')
    df.reset_index(drop=True)
    df.to_csv(filename,mode='w',index=False,header=True)
    print('\nPress esc key to to show menu')
    keyboard.wait('esc')

# %%
def sendimg():
    try:
        df=pd.read_csv(filename)
    except:
        print('No numbers present to send')
        print('\nPress esc key to to show menu')
        keyboard.wait('esc')
        return
    path=input('Enter image path here - ')
    df['CHECKSENDMSG']=0
    df.set_index('PHONENUMBER',drop=False,inplace=True)
    try:
        for i in df.index:
            pywhatkit.sendwhats_image('+'+i.replace('a',''), path,tab_close=True,close_time=1)
            df.loc[df.index==i,'CHECKSENDMSG']=1
            time.sleep(0.7)
    except:
        df.reset_index(drop=True)
        df.to_csv(filename,mode='w',index=False,header=True)
        print('Connection error/Whatsapp Database error')
        return
    print('Success')
    df.reset_index(drop=True)
    df.to_csv(filename,mode='w',index=False,header=True)
    print('\nPress esc key to to show menu')
    keyboard.wait('esc')

# %%
def checkprev():
    try:
        df=pd.read_csv(filename)
    except:
        print('No numbers present to check')
        print('\nPress esc key to to show menu')
        keyboard.wait('esc')
        return
    df.set_index('CHECKSENDMSG',drop=False,inplace=True)
    data={}
    '''
    for i in df.index:
        if int(i)==0:
            print(df.loc[i])
            for key,value in dict(df.loc[i]).items():
                if key in data:
                    data[key].append(value)
                else:
                    data[key]=[value]'''
    for value in df.loc[0].PHONENUMBER:
        if 'PHONENUMBER' in data:
            data['PHONENUMBER'].append(value)
        else:
            data['PHONENUMBER']=[value]
    for value in df.loc[0].CHECKSENDMSG:
        if 'CHECKSENDMSG' in data:
            data['CHECKSENDMSG'].append(value)
        else:
            data['CHECKSENDMSG']=[value]
    df1 = pd.DataFrame(data)
    print(df1)
    file=open('notsendmsg.csv','w')
    file.close()
    df1.to_csv('notsendmsg.csv',mode='w',index=False,header=True)
    print('This data are saved in a file named notsendmsg.csv in the same directory, for resend the message again restart the program and enter the notsendmsg.csv filename ')
    print('\nPress esc key to to show menu')
    keyboard.wait('esc')


# %%
ans='y'
while ans=='y':
    menu()
    ch=input('Enter your choice - ')

    if ch.isalpha():
        ch.lower()
    elif ch.isdigit():
        ch=int(ch)

    if ch=='INS' or ch==1:
        insert()
    elif ch=='DEL' or ch==2:
        delete()
    elif ch=='UPD' or ch==3:
        update()
    elif ch=='SRCH' or ch==4:
        search(None)
    elif ch=='SENDMSG' or ch==5:
        sendmessage()
    elif ch=='SENDIMGMSG' or ch==6:
        sendimgmessage()
    elif ch=='SENDIMG' or ch==7:
        sendimg()
    elif ch=='CHECKPREV' or ch==8:
        checkprev()
    elif ch=='EXIT' or ch==9:
        ans='n'



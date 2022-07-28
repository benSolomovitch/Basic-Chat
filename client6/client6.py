'''
Program: Client6
Author: Ben Solomovitch
The program allows you to connect as a client to a server and receive
service from it.
In order to connect as an admin, run using an external parameter ADMIN.
'''

from socket import *
from tkinter import *
import sys
import os
from math import *
import random

entries = []
send_buttons = []
lables = []
tcpCliSock = None
button = None
entry1 = None
entry2 = None
questions=['1','2','3','4','5','6']
quiz_buttons=[]

def make_resizable(widget):
    '''
    Allowing resize of the widget
    arg=widget
    '''

    for x in range(widget.grid_size()[0]):
        widget.columnconfigure(x, weight=1)
    for y in range(widget.grid_size()[1]):
        widget.rowconfigure(y, weight=1)
    return

def back_start_screen(root):
    '''
    Connects between the menu to the home screen
    arg=root
    '''
    
    global tcpCliSock

    root.destroy()
    root1 = Tk()
    root1.geometry("330x210+400+50")
    tcpCliSock.send("QUIT".encode())
    data=tcpCliSock.recv(1024)
    w1 = Label(root1, text=data.decode(),fg="blue",height=2,width=12,
               font="normal 22")
    w1.pack(expand="YES", fill="both")
    button=Button(root1,text="Countinue",fg="blue",font="normal 18",command=
                  lambda screen=root1:start_screen([screen]))
    button.pack(expand="YES", fill="both")
    tcpCliSock.close()
    return

def manu_func(root):
    '''
    Creates and displays a menu
    arg=root
    '''
    
    menubar = Menu(root)
    enter_menu = Menu(menubar, tearoff=0)
    enter_menu.add_command(label="About", command=lambda : about_screen())
    enter_menu.add_command(label="Quit", command=lambda x=root:
                           back_start_screen(x))
    menubar.add_cascade(label="Menu", menu=enter_menu)
    root.config(menu=menubar) # displays the menu
    return

def exit_screen():
    '''
    Creates and displays a screen before exiting the program.
    '''
    
    root1 = Tk()
    root1.geometry("430x310+400+50")
    w1 = Label(root1, text="Sure you want to exit?",fg="blue",height=2,width=12,font="normal 22")
    w1.grid(row=0, column=0,columnspan=2, sticky=W+N+S+E, padx=1, pady=1)
    
    no_button=Button(root1,text="No!",fg="green",font="normal 30",command=lambda : root1.destroy())
    no_button.grid(row=1, column=0, sticky=W+N+S+E, padx=1, pady=1)
    yes_button=Button(root1,text="Yes",fg="red",font="normal 30",command=lambda : os._exit(0))
    yes_button.grid(row=1, column=1, sticky=W+N+S+E, padx=1, pady=1)
    make_resizable(root1)
    return

def conversation_screen(start_screen):
    '''
    Creates and displays the conversation screen between
    the client and the server.
    arg = start_screen
    *The function gets the start screen as a parameter
    in order to destroy it.
    '''
    
    global entries
    global send_buttons
    global lables
    global tcpCliSock
    global index
    global counter
    
    start_screen.destroy()

    send_buttons=[]
    entries=[]
    lables=[]
    index=0
    counter=0

    HOST='localhost'
    PORT=51123
    BUFSIZ=1024
    ADDR=(HOST,PORT)

    tcpCliSock=socket(AF_INET,SOCK_STREAM)
    try:
        tcpCliSock.connect(ADDR)
    except:
        root1 = Tk()
        root1.geometry("400x210+400+50")
        w1 = Label(root1, text="The server is disconnected",fg="blue",height=2,
                   width=12,font="normal 22")
        w1.pack(expand="YES", fill="both")
        sys.exit(0)
    
    root = Tk()
    root.geometry("500x500+400+50")
    entries.append(Entry(root, font='normal 18', fg='blue'))
    entries[0].grid(row=counter,column=0,sticky=W+N+S+E,padx=1, pady=1)
    send_buttons.append(Button(root,text="send",fg="blue",font="normal 18",
                           command=lambda screen=root:sending(screen)))
    send_buttons[0].grid(row=counter,column=1,padx=1, pady=1,sticky=W+S+E+N)
    lables.append(Label(root,text="",fg="blue",font="normal 18"))
    lables[0].grid(row=counter+1, column=0,sticky=W+N+S+E, padx=1, pady=1,
                   columnspan=2)
    manu_func(root)
    return

def sending(screen):
    '''
    Responsible for sending and receiving information from the server.
    Allows you to continue sending the information.
    arg = screen
    *The function gets a screen as a parameter
    in order to destroy it.
    '''
    
    global entries
    global lables
    global send_buttons
    global index
    global counter

    send_buttons[index]["state"]=DISABLED
    entries[index]["state"]=DISABLED
    
    data=entries[index].get()
    if data=="END":
        end_server_screen(screen)
    elif data=="GRAPH":
        graph_input()
    elif data=="":
        lables[index]["text"]="Echoed"
    elif data=="QUIZ":
        quiz_screen()
    else:
        try:
            tcpCliSock.send(data.encode())
            data=tcpCliSock.recv(1024)
        except:
            screen.destroy()
            root1 = Tk()
            root1.geometry("400x210+400+50")
            w1 = Label(root1, text="The server is disconnected",fg="blue",
                       height=2,width=12,font="normal 22")
            w1.pack(expand="YES", fill="both")
            sys.exit(0)
        lables[index]["text"]=data.decode()

    index+=1
    counter+=2

    #Checks if the screen is full. If so - cleans it.
    if counter==10:
        lables[0]["text"]=""
        send_buttons[0]["state"]=NORMAL
        entries[0]["state"]=NORMAL
        entries[0].delete(0, END)
        for i in range(1,len(entries),1):
            send_buttons[i].destroy()
            send_buttons[i]=None
            entries[i].destroy()
            entries[i]=None
            lables[i].destroy()
            lables[i]=None
        send_buttons=[send_buttons[0]]
        entries=[entries[0]]
        lables=[lables[0]]
        index=0
        counter=0

    #Creates a new entry and button to continue sending information.
    else:
        lables.append(Label(screen,text="",fg="blue",font="normal 18"))
        lables[index].grid(row=counter+1, column=0,sticky=W+N+S+E, padx=1,
                           pady=1,columnspan=2)
        entries.append(Entry(screen, font='normal 18', fg='blue'))
        entries[index].grid(row=counter,column=0,sticky=W+N+S+E,padx=1,pady=1)

        send_buttons.append(Button(screen,text="send",fg="blue",font="normal 18"
                                   ,command=lambda screen=screen:sending(screen)))
        send_buttons[index].grid(row=counter,column=1,padx=1, pady=1,
                                 sticky=W+S+E+N)
    return


def quiz_screen():
    '''
    Creates and displays the quiz screen.
    '''
    
    global questions
    global tcpCliSock
    global quiz_buttons
    root1 = Tk()
    root1.geometry("620x210+400+50")
    
    quest_num=questions.pop(random.randint(0,len(questions)-1))
    tcpCliSock.send(("quiz: "+quest_num).encode())
    question=tcpCliSock.recv(1024).decode()
    question_parts=question.split("\n")
    
    w1 = Label(root1, text=question_parts[0]+"\n",fg="blue",font="normal 22")
    w1.grid(row=0,column=0,sticky=W+N+S+E, padx=1, pady=1,columnspan=2)
    
    for i in range(1,5,1):
        quiz_buttons.append(Button(root1,text=question_parts[i],fg="green",
                                   font="normal 18",command=lambda screen=root1,
                                   response=question_parts[i],answer=
                                   question_parts[5]:answer_screen
                                   (screen,response,answer)))
        
        quiz_buttons[i-1].grid(row=i//3+1,column=(i+1)%2,sticky=W+N+S+E,
                               padx=1, pady=1)
    make_resizable(root1)
    return

def answer_screen(screen,response,answer):
    '''
    Checks the correctness of the answer to the question
    from the quiz and displays it on a new screen.
    arg = screen,response,answer
    '''
    
    global quiz_buttons
    quiz_buttons=[]
    root1 = Tk()
    root1.geometry("200x100+400+50")
    w1 = Label(root1, text="",fg="red",font="normal 22")
    
    screen.destroy()
    if answer==response:
        w1["text"]="Correct!"
    else: w1["text"]="Incorrect"

    w1.grid(row=1,column=0,sticky=W+N+S+E, padx=1, pady=1)
    make_resizable(root1)
    return

def graph_input():
    '''
    Creates and displays a screen for entering the function
    which will be sent to the server.
    '''
    
    global entry1
    root1 = Tk()
    root1.geometry("400x210+400+50")
    w1 = Label(root1, text="Enter a function",fg="blue",font="normal 22")
    w1.grid(row=0,column=0,sticky=W+N+S+E, padx=1, pady=1,columnspan=2)
    entry1=Entry(root1, font='normal 18', fg='blue')
    entry1.grid(row=1,column=0,sticky=W+N+S+E, padx=1, pady=1)
    button=Button(root1,text="continue",fg="blue",font="normal 18",
                  command=lambda screen=root1:graph_screen(screen))
    button.grid(row=1,column=1,sticky=W+N+S+E, padx=1, pady=1)
    return

def graph_screen(screen):
    '''
    Creates and displays a new screen in which the graph of the
    function sent to the server will be drawn.
    '''
    
    global tcpCliSock
    global entry1
    
    root1 = Tk()
    root1.geometry("500x500+400+50")
    w1 = Label(root1, text="",fg="blue",font="normal 18")
    w1.grid(row=0,column=0,sticky=W+N+S+E, padx=1, pady=1,columnspan=2)
    x=1
    formula=entry1.get()

    #Checking the integrity of the function.
    try:
        eval(formula)
        tcpCliSock.send(("graph: "+entry1.get()).encode())
        data=tcpCliSock.recv(1024)
        data+=tcpCliSock.recv(1024)
        w1["text"]=data.decode()
    except NameError:
        w1["text"]="Use only x as a parameter"
    except SyntaxError:
        w1["text"]="Make sure the function is valid"
    except ValueError:
        w1["text"]="Can't draw the function in the whole domain"
    except ZeroDivisionError:
        w1["text"]="Can't draw the function in the whole domain"
    make_resizable(root1)
    return


def end_server_screen(screen):
    '''
    Creates and displays a screen to close server activity. If the client
    is not an admin an appropriate message will be displayed.
    arg = screen
    '''
    
    root1 = Tk()
    root1.geometry("400x210+400+50")
    global entry1

    try:
        if sys.argv[1]=="ADMIN":
            w1 = Label(root1, text="Enter the password",fg="blue",
                       font="normal 22")
            w1.grid(row=0,column=0,sticky=W+N+S+E, padx=1, pady=1,columnspan=2)
            entry1=Entry(root1, font='normal 18', fg='blue')
            entry1.grid(row=1,column=0,sticky=W+N+S+E, padx=1, pady=1)
            button=Button(root1,text="continue",fg="blue",font="normal 18",
                          command=lambda screen1=screen,screen2=root1:
                          end_server(screen1,screen2))
            button.grid(row=1,column=1,sticky=W+N+S+E, padx=1, pady=1)
    except IndexError:
        w1 = Label(root1, text="You are not logged in\nas an ADMIN",fg="blue"
                   ,height=2,width=12,font="normal 22")
        w1.pack(expand="YES", fill="both")
    return

def end_server(screen1,screen2):
    '''
    Checks whether the password the admin entered is correct.
    If so it closes the server and client activity.
    '''
    
    global tcpCliSock
    global entry1
    if entry1.get()=="":
        data="Incorrect password"
    else:
        tcpCliSock.send(("check_password: "+entry1.get()).encode())
        data=(tcpCliSock.recv(1024)).decode()
        screen2.destroy()
        if "ADMIN" in data:
            screen1.destroy()
    root1 = Tk()
    root1.geometry("400x210+400+50")
    w1 = Label(root1, text=data,fg="blue",height=2,width=12,font="normal 22")
    w1.pack(expand="YES", fill="both")
    return

def confirm_password(screen):
    '''
    Creates and displays an entry and a button for password verification.
    '''
    
    global button
    global entry2
    button["state"]=DISABLED
    w2 = Label(screen, text="Confirm your password",fg="blue",font="normal 22")
    w2.grid(row=2,column=0,sticky=W+N+S+E, padx=1, pady=1,columnspan=2)
    entry2=Entry(screen, font='normal 18', fg='blue')
    entry2.grid(row=3,column=0,sticky=W+N+S+E, padx=1, pady=1)
    button=Button(screen,text="continue",fg="blue",font="normal 18",
                   command=lambda screen=screen:setting_password(screen))
    button.grid(row=3,column=1,sticky=W+N+S+E, padx=1, pady=1)
    return        


def setting_password(screen):
    '''
    Checks the password verification and then sends it to the server.
    '''
    
    global entry1
    global entry2
    global tcpCliSock
    global button
    
    button["state"]=DISABLED
    
    if (entry1.get())!=(entry2.get()):
        root1 = Tk()
        root1.geometry("400x210+400+50")
        w1 = Label(root1, text="Incorrect password verification",fg="blue",
                   height=2,width=12,font="normal 22")
        w1.pack(expand="YES", fill="both")
        button=Button(root1,text="Countinue",fg="blue",font="normal 18",
                      command=lambda screen=screen:start_screen([screen,root1]))
        button.pack(expand="YES", fill="both")
    elif(entry1.get()==""):
        root1 = Tk()
        root1.geometry("400x210+400+50")
        w1 = Label(root1, text="Invalid password",fg="blue",height=2,width=12,
                   font="normal 22")
        w1.pack(expand="YES", fill="both")
        button=Button(root1,text="Countinue",fg="blue",font="normal 18",
                      command=lambda screen=screen:start_screen([screen,root1]))
        button.pack(expand="YES", fill="both")
    else:
        HOST='192.168.1.214'
        PORT=51123
        BUFSIZ=1024
        ADDR=(HOST,PORT)
        tcpCliSock=socket(AF_INET,SOCK_STREAM)
        try:
            tcpCliSock.connect(ADDR)
            tcpCliSock.send(("set_password: "+entry1.get()).encode())
        except:
            screen.destroy()
            root1 = Tk()
            root1.geometry("400x210+400+50")
            w1 = Label(root1, text="The server is disconnected",fg="blue",
                       height=2,width=12,font="normal 22")
            w1.pack(expand="YES", fill="both")
            sys.exit(0)
        back_start_screen(screen)
    return

def admin_screen(screen):
    '''
    Creates and displays a screen for changing the password.
    If the client is not an admin an appropriate message will be displayed.
    arg = screen
    *The function gets a screen as a parameter
    in order to destroy it.
    '''
    
    global button
    global entry1
    
    button=None
    screen.destroy()
    root1 = Tk()
    root1.geometry("400x210+400+50")
    try:
        if sys.argv[1]=="ADMIN":
            w1 = Label(root1, text="Set a new password",fg="blue",
                       font="normal 22")
            w1.grid(row=0,column=0,sticky=W+N+S+E, padx=1, pady=1,columnspan=2)
            entry1=Entry(root1, font='normal 18', fg='blue')
            entry1.grid(row=1,column=0,sticky=W+N+S+E, padx=1, pady=1)
            button=Button(root1,text="continue",fg="blue",font="normal 18",
                          command=lambda screen=root1:confirm_password(screen))
            button.grid(row=1,column=1,sticky=W+N+S+E, padx=1, pady=1)
    except IndexError:
        w1 = Label(root1, text="You are not logged in\nas an ADMIN",fg="blue",
                   height=2,width=12,font="normal 22")
        w1.pack(expand="YES", fill="both")
        button=Button(root1,text="Countinue",fg="blue",font="normal 18",
                      command=lambda screen=root1:start_screen([root1]))
        button.pack(expand="YES", fill="both")
        
    make_resizable(root1)
    return


def about_screen():
    '''
    Creates and displays an explanation screen about
    the special functions.
    '''
    
    text1=""
    with open("about.txt",'r') as file:
        for line in file:
            text1=text1+(line+"\n")
    master = Tk()
    master.geometry("650x580+350+50")
    w1 = Label(master, text=text1,fg="green",font="normal 18")
    w1.pack(expand="YES", fill="both")
    make_resizable(master)
    return
    

def start_screen(screens):
    '''
    Creats and displays a home screen.
    arg = screens
    *The function gets a list of screens as a parameter
    in order to destroy them.
    '''
    
    if screens!=None:
        for screen in screens:
            screen.destroy()
            
    master = Tk()
    master.geometry("500x500+400+50")
    w1 = Label(master, text="Client's World",fg="blue",height=2,
               width=12,font="normal 40")
    w1.pack(expand="YES", fill="both")
    play_button=Button(master,text="Start!",fg="green"
                       ,font="normal 30",
                       command=lambda x=master:conversation_screen(x))
    play_button.pack(expand="YES", fill="both")
    about_button=Button(master,text="About",fg="blue"
                       ,font="normal 30",
                       command=lambda :about_screen())
    about_button.pack(expand="YES", fill="both")
    admin_button=Button(master,text="Password Settings"
                       ,fg="#%02x%02x%02x" % (255, 204, 0),
                       font="normal 30",command=
                        lambda screen=master:admin_screen(screen))
    admin_button.pack(expand="YES", fill="both")
    exit_button=Button(master,text="Exit",
                       fg="red",font="normal 30",command=lambda: exit_screen())
    exit_button.pack(expand="YES", fill="both")
    make_resizable(master)
    return

start_screen(None)

mainloop()

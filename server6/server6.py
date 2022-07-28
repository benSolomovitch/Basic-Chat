'''
Program: Server6
Author: Ben Solomovitch
The program allows you to connect with client as a server and provide
them service.
'''

import socket
import select
from datetime import datetime
from math import *
import os

MAX_MSG_LENGTH = 1024
SERVER_PORT = 51123
SERVER_IP = 'localhost'

def axis_list_func(min_axis,max_axis,amount):
    '''
    Creats a list of values for an axis. 
    arg=min_axis,max_axis,amount
    ret=axis_list,place of 0 in the list
    '''
    
    axis_list=[]
    #The difference between two consecutive values.
    delta=round((max_axis-min_axis)/amount,3)
    for i in range(0,amount+1,1):
        axis_list.append(round(min_axis,1))
        min_axis=min_axis+delta
    try:
        return axis_list,axis_list.index(0)
    except ValueError:
        #returns -1 as zero's place if it isn't in the list.
         return axis_list,-1

def symbols_x(x_min,x_max,x_list):
    '''
    Creates the string that indicates the values of the x axis.
    arg=x_min,x_max,x_list
    ret=symbol_line
    '''
    
    symbol_line=""
    for i in range(0,len(x_list),5):
        symbol_line=symbol_line+str(x_list[i])+" "*(5-(len(str(x_list[i]))))
    return symbol_line

def x_axis(x_list,x_zero):
    '''
    Creats the x axis.
    arg=x_list,x_zero
    ret=line
    '''
    
    line=""
    for j in range(len(x_list)):
        if j==x_zero:
            line=line+"+"
        elif j%5==0:
            line=line+"|"
        else: line=line+"-"
    return line

def func_paint(data):
    '''
    Responsible for creating and returning the function drawing.
    arg = data
    ret = graph
    '''
    
    formula = data
    x_min=-3
    x_max=3
    y_min=-3
    y_max=3
    graph=""
    graph+=("\tGraphing f(x)="+formula+"\n")

    x_list,x_zero=axis_list_func(x_min,x_max,70)
    y_list,y_zero=axis_list_func(y_min,y_max,24)
    delta_y=round((y_max-y_min)/24,1)
    
    for i in range(24,-1,-1):
        if i==y_zero:
            line=x_axis(x_list,x_zero)
        #Checks if the x axis has been printed in the previous line.
        elif y_zero-1==i:
            line=symbols_x(x_min,x_max,x_list)
        #Checks whether to print the y value.
        elif i%4==0:
            y=round(y_list[i],2)
            line=" "*(x_zero-1-len(str(y)))+str(y)+"-|"+(len(x_list)-x_zero)*" "
        else: line=" "*x_zero+"|"+" "*(len(x_list)-x_zero)

        for j in range(len(x_list)):
            x=x_list[j]
            try:
                y=eval(formula)
                if y_list[i]-delta_y<y<=y_list[i]:
                    #Checks whether the point of the graph can be printed
                    #(only if the axis values are not erased).
                    if line[j]=="|" or line[j]==" ":
                        graph+="*"
                    else: graph+=line[j]
                else: graph+=line[j]
            except ZeroDivisionError:
                #Asymptote
                graph+="^"
            except ValueError:
                #A domain where the function is not defined.
                graph+="^"
        graph+="\n"
    return graph


def reading_lines(file,key,lines_num):
    '''
    Opens a file to read and return specific lines
    arg=file,key,lines_num
    ret=list of the desired lines
    '''
    
    try:
        with open (file,'r') as file:
            for line in file:
                #looks for the desired content in each line.
                if key in line:
                    return [file.readline() for x in range(lines_num)]
    except FileNotFoundError:
        print("Verify the questions & reactions text files are in this folder.")
    return "Error"


def print_client_sockets(client_sockets):
    '''
    Prints all clients connected to the server.
    arg = client_sockets
    '''
    
    for c in client_sockets:
        print("\t", c.getpeername())
    return

def check_password(password,writer):
    '''
    Checking the correctness of the password received from the admin.
    If the password is correct the server will terminate its operation.
    arg = password,writer
    '''
    
    global messages_to_send
    global client_sockets
    with open("password.txt",'r') as file:
        original_password=file.readline()
    if original_password==password:
        messages_to_send.append((writer,"The server was disconnected\nby ADMIN"))
        for message in messages_to_send:
            current_socket, data = message
            if current_socket in wlist:
                current_socket.send(data.encode())
                messages_to_send.remove(message)
                client_sockets.remove(current_socket)
                current_socket.close()
        os._exit(0)
    else:
        messages_to_send.append((writer,"Incorrect password"))
    return


print("Setting up server...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
print("Listening for clients...")
client_sockets = []
messages_to_send = []

while True:
    rlist, wlist, xlist = select.select([server_socket] +
                                        client_sockets, client_sockets, [])
    for current_socket in rlist:
        if current_socket is server_socket:
            connection, client_address = current_socket.accept()
            print("New client joined!", client_address)
            client_sockets.append(connection)
            print_client_sockets(client_sockets)
        else:
            data = current_socket.recv(MAX_MSG_LENGTH).decode()
            if data == "QUIT":
                messages_to_send.append(
                    (current_socket,
                     "Hope to see you soon :)\nYour loyal server"))
            elif "set_password:" in data:
                with open ("password.txt",'w') as file:
                    file.write(data.split()[1])
            elif "check_password:" in data:
                check_password(data.split()[1],current_socket)
            elif data == "TIME":
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                messages_to_send.append((current_socket, dt_string))
            elif "graph:" in data:
                messages_to_send.append((current_socket, func_paint
                                         (data.split(" ",1)[1])))
            elif "quiz:" in data:
                question=reading_lines("questions.txt","question "
                                       +data.split(" ",1)[1],6)
                string="".join(question)
                messages_to_send.append((current_socket,string))
            else:
                messages_to_send.append((current_socket, "Echoed "+data))
                
    for message in messages_to_send:
        current_socket, data = message
        if current_socket in wlist:
            current_socket.send(data.encode())
            messages_to_send.remove(message)
            
            #Checks whether the client terminates the connection.
            if data=="Hope to see you soon :)\nYour loyal server":
                print("Connection closed")
                client_sockets.remove(current_socket)
                current_socket.close()
                print_client_sockets(client_sockets)

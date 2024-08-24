#!/usr/bin/python3					
from socket import *
from _thread import *
from datetime import *
import time
import train
import addtrains
import sys

host = ''
trainList = addtrains.trainList

userList = []

def dispTrains():
	conn.sendall("\nTrains running are\n".encode())
	for i in range(0, len(trainList)):
		temp = [trainList[i].number, trainList[i].name, trainList[i].source, trainList[i].dep, trainList[i].dest,
				trainList[i].arr]
		train_info = f"Train Number: {temp[0]}\nTrain Name: {temp[1]}\nSource: {temp[2]}\nDeparture Time: {temp[3]}\nDestination: {temp[4]}\nArrival Time: {temp[5]}\n"
		conn.sendall(train_info.encode())
		conn.sendall('\n'.encode())

	
def findTrains(src, dest):
	foundList = []
	for i in range(0, len(trainList)):
		if src in trainList[i].source and dest in trainList[i].dest:
			temp = [ trainList[i].number, trainList[i].name, trainList[i].source, trainList[i].dep, trainList[i].dest, trainList[i].arr ]
			foundList.append(temp)

	if len(foundList) == 0:
		conn.sendall("No Trains found between the given route :(".encode())
		conn.sendall('\n'.encode())
	
	else:
		conn.sendall("Trains from " + src + " to " + dest + "\n")
		for i in range(0, len(foundList)):
			conn.sendall(str(foundList[i]).encode())
			conn.sendall("\n".encode())

def trainNumIn():
	while 1:
		msg = 'Enter train number to proceed'
		conn.sendall(msg.encode())
		conn.sendall("\n".encode())
		recvd = conn.recv(1024).decode()
		if len(recvd) == 5:
			return recvd
			break
		else:
			conn.sendall("Invalid Train Number".encode())
			conn.sendall("\n".encode())

def trainInfo(number):
	temp = "null"
	for i in range(0, len(trainList)):
		if number == trainList[i].number:
			temp = [ trainList[i].number, trainList[i].name, trainList[i].source, trainList[i].dep, trainList[i].dest, trainList[i].arr ]
			conn.sendall(str(temp).encode())
			conn.sendall("\n".encode())
			break

	if temp == "null":
		conn.sendall("No train with the given number found".encode())
		conn.sendall("\n".encode())

def checkAvail(number, date, x):
	for i in range(0, len(trainList)):
		if number == trainList[i].number:
			temp = trainList[i]
			break

	res = temp.availability(date, x)
	conn.sendall(str(res).encode())

def book(number, date, travelClass, seatNum, conn, uid):
	for i in range(0, len(trainList)):
		if number == trainList[i].number:
			temp = trainList[i]
			break

	ret = temp.seatBook(date, travelClass, seatNum, conn, uid)

	if ret == -1:
		conn.sendall("Seat Not Available\n".encode())
	elif ret == 0:
		conn.sendall("Seat has been blocked by someone else, please select some other seat or try again later\n".encode())
	elif ret == 1:
		tempuser = getUser(uid)
		ticket_details = f"Ticket Details are\nName : {tempuser.uname}\tAge : {tempuser.age}\nEmail : {tempuser.email}\nPhone : {tempuser.phone}\n"
		conn.sendall(ticket_details.encode())
		conn.sendall("\n\n".encode())

def check(uid):
	# Check if user already exists
	for i in range(len(userList)):
		if uid == userList[i].uid:
			return True
def getUsername(uid):
	for i in range(len(userList)):
		if uid == userList[i].uid:
			return userList[i].uname

def welcomeinit():
	inputs = {
		'uid': None,
		'uname': None,
		'age': None,
		'gender': None,
		'email': None,
		'phone': None
	}

	while True:
		# Loop through each input field
		for field, value in inputs.items():
			# Skip if the value has already been filled
			if value is not None:
				continue

			# Prompt for input based on the field
			if field == 'uid':
				conn.sendall("Enter user id\n".encode())
			elif field == 'uname':
				conn.sendall("Enter Name\n".encode())
			elif field == 'age':
				conn.sendall("Enter age\n".encode())
			elif field == 'gender':
				conn.sendall("Enter gender (F/M/Male/Female)\n".encode())
			elif field == 'email':
				conn.sendall("Enter email\n".encode())
			elif field == 'phone':
				conn.sendall("Enter phone\n".encode())

			# Receive input from the client
			user_input = conn.recv(1024).decode()

			# Validate input based on the field
			if field == 'uid':
				if check(user_input):
					conn.sendall(("Welcome back " + getUsername(user_input) + "\n").encode())
				if not user_input.isdigit():
					conn.sendall("Error : User id must contain only digits. Please enter again.\n".encode())
					break
			elif field == 'uname':
				if not user_input.isalpha():
					conn.sendall("Error : Name must contain only alphabets. Please enter again.\n".encode())
					break
			elif field == 'age':
				if not user_input.isdigit():
					conn.sendall("Error : Age must contain only digits. Please enter again.\n".encode())
					break
			elif field == 'gender':
				gender = user_input.strip().lower()
				if gender not in ["f", "m", "male", "female"]:
					conn.sendall("Error : Invalid gender. Please enter 'F', 'M', 'Male', or 'Female'.\n".encode())
					break
			elif field == 'email':
				if "@" not in user_input or "." not in user_input:
					conn.sendall("Error : Invalid email format. Please enter again.\n".encode())
					break
			elif field == 'phone':
				if not user_input.isdigit():
					conn.sendall("Error : Phone number must contain only digits. Please enter again.\n".encode())
					break

			# Update inputs dictionary with the validated input
			inputs[field] = user_input
		else:
			# Break out of the while loop if all inputs are filled successfully
			break

	# Extract values from inputs dictionary
	uid = inputs['uid']
	uname = inputs['uname']
	age = inputs['age']
	gender = inputs['gender']
	email = inputs['email']
	phone = inputs['phone']

	# Create new user object and add to userList
	obj = train.user(uid, uname, age, gender, email, phone)
	userList.append(obj)
	return uid


def getUser(uid):
	for i in range(0, len(userList)):
		if uid == userList[i].uid:
			temp = userList[i]
			return temp

port = 2222
sock = socket(AF_INET, SOCK_STREAM)
print ('Socket created')

try:
	sock.bind((host, port))
except error as msg:
	print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
	sys.exit()

sock.listen(5)
print("Socket now Listening on port " + str(port))

def clientthread(conn):
	hellomsg = 'Hi there!, Welcome to Railway Booking System\n'
	conn.sendall(hellomsg.encode())
	uid = welcomeinit()
	while True:
		msg = 'Enter...\n1 to see all the running trains\n2 to search trains\n3 to get train info by train number\n4 to check availibilty\n5 to book a seat\n6 to visit profile\n9 to exit'
		conn.sendall(msg.encode())
		conn.sendall("\n".encode())
		data = conn.recv(1024).decode()
		# if int(data) == 9:
		# 	conn.close()
		# 	exit()
		# 	break

		if int(data) == 1:
			dispTrains()
			continue

		elif int(data) == 2:
			msg = 'Enter Source - Destination (in the given format, e.g.- Bengaluru - Mysuru)\n'
			conn.sendall((msg + "\n").encode())
			recieved = conn.recv(1024).decode()
			src,dest = recieved.strip(' ').split('-')
			findTrains(src, dest)
			conn.sendall("\nEnter..\nTrain number to check availibility for that train\n0 to go back".encode())
			conn.sendall("\n".encode())
			if int(conn.recv(1024).decode()) == 0:
				continue
			else:
				data = 4

		elif int(data) == 3:
			recvd = trainNumIn()
			trainInfo(int(recvd))
			continue


		elif int(data) == 4 or int(data) == 5:
			while True:
				try:
					trNum = trainNumIn()
					conn.sendall("Enter date and class in 'dd-mm-yyyy,c' format where c = 0 for all, 1 for sl, 2 for 3ac, 3 for 2ac, and 4 for first class".encode())
					conn.sendall("\n".encode())
					recvd = conn.recv(1024).decode()
					date, x = recvd.strip(" ").split(",")
					checkAvail(int(trNum), date, int(x))
					conn.sendall('Enter\n1 to book\n0 to return to main menu'.encode())
					conn.sendall("\n".encode())
					choice = int(conn.recv(1024).decode())

					if choice == 0:
						break
					# Inside the choice == 1 block
					elif choice == 1:
						temp = getUser(uid)
						conn.sendall('Enter Class (sl, third, second, first)\n'.encode())
						travelClass = conn.recv(1024).decode().strip().lower()

						if travelClass in ["sl", "third", "second", "first"]:
							conn.sendall('Enter seat Number to book\n'.encode())
							seatNum = conn.recv(1024).decode().strip()
							book(int(trNum), date, travelClass, int(seatNum), conn, uid)
						else:
							conn.sendall('Invalid class. Please enter sl, third, second, or first.\n'.encode())

				except Exception as e:
					print("An error occurred:", str(e).encode())
					break

       
		elif int(data) == 6:
			conn.sendall("Profile\n".encode())
			tempuser = getUser(uid)
			
			conn.sendall(("Name " + tempuser.uname + "\n").encode())
			conn.sendall(("Username " + tempuser.uid + "\n").encode())
			conn.sendall(("Age " + tempuser.age + "\n").encode())
			conn.sendall(("Email id " + tempuser.email + "\n").encode())
			conn.sendall(("Press 1 to check your booking history\n0 to go back").encode())
			resp = conn.recv(1024).decode()
			if resp == "1":
				conn.sendall("\nhere is your booking history\n".encode())
				conn.sendall((str(temp.bookings) + "\n").encode())
			elif resp == "0":
				continue
			else:
				conn.sendall("Invalid choice. Please enter either 0 or 1.\n".encode())

			
while 1:
	conn, addr = sock.accept()
	print ('Connected with ' + addr[0] + ':' + str(addr[1]))
	start_new_thread(clientthread ,(conn,))
		

sock.close()
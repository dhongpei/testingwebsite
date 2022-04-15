#chmod +x index.py
#!/usr/bin/python
print('Content-type: text/html\r\n\r')

import pyodbc
import pandas as pd
import smtplib

import random

# Reset Passcodes on daily restart, attemptRegistration
# Stop functions if disabled, remove (?) accounts if query finds odd quantity
# Account lockout and login location notification
# Check given email is an email, formatting, etc.

#	myconn = pyodbc.connect('Driver='{SQL Server}',host='', database='',user='',password='', Trusted connection='yes')
#	query = """SELECT *;"""

# connectionString="data source=powers.cacsumj2zjkc.us-east-1.rds.amazonaws.com,1433;initial catalog=powerseimain;user id=admin;password=powers123;MultipleActiveResultSets=True"

ADMIN_ACCESS = -1
USER_ACCESS = 0
MANAGER_ACCESS = 1
MASTER_ACCESS = 2
 



####################################################################################################
## Server Control
####################################################################################################

# Send when adding or changing text/email notifictions
def sendTestSMS(phoneNumber):
	return 1


def sendTestEmail(connection, emailAddress):
	# smtplib
	cursor = connection.cursor()
	cursor.execute("select * from X")
	remail = "sendto@gmail.com"
	smtpObj = smtplib.SMTP('smtp-outlook.com', 587)
	smtpObj.ehlo()
	smtpObj.starttls()
	smtpObj.login('from@gmail.com','PASSWORD')
	smtpObj.sendmail('from@gmail.com', remail, 'Subject:Query results \n' +df.to_string())
	smtpObj.quit()


# Auto call when a payment update is made to Disable table
# Only updates the next payment date based on newly inputted current payment date
def updatePayment(companyName):
	return 1


# Run at server restart, daily preferred
def updateDisable():
	return 1
	# Updates expiration status for all rows, doesn't change any other columns


def sendInspectionNotif(emailAddress, companyName, tankName, locationName, reportType, lastReport, nextReport, powersNotes):
	return 1
	# WIP: How often to send message, and how early (2y/1y6m/1y/9m/6m/4m/2m/1m/0)
	# Send email to our team for phone call notifications
	# "If any information regarding this tank seems off/you need information regarding this tank, please contact at:..."


def sendLoginNotif(emailAddress):
	return 1
	# WIP: Need system to monitor login location and login attempt count

# WIP: Need functions to send notifications regarding recommended repairs
# WIP: Need functions to send notifications regarding routine checks by company ground workers


# WIP: Either transfer the file for a standard PDF view or have a built-in viewer to prevent unauthorized viewership
def transferFile(fileName, companyName, tankName):
	return 1


# WIP: Send message for bad input or further instructions (ex. during account registration)




####################################################################################################
## Base Account (0)
## 
## Basic functions for login and table access. Also checks for permissions, without feedback.
## Default for all registered accounts.
####################################################################################################


# createCode found in YYY via createTempCode
def attemptRegistration(connection, emailAddress, userName, password, companyName, phoneNumber, phoneExt, emailNotif, phoneNotif, createCode):
	cursor = connection.cursor()
	try:
		checkLogins = cursor.execute("select EmailAddress, Username from Login where EmailAddress=\'" + emailAddress + "\' or Username=\'" + userName + "\';").fetchall()
		isDisabled = isCompanyDisabled(companyName)
		checkCode = cursor.execute("select XXX, Company from YYY where Company=\'" + companyName + "\' and XXX=\'" + createCode + "\';").fetchall()

		if len(checkLogins) > 0 and checkLogins[0][0] == emailAddress:
			print("There is already an account with that email address.")
		elif len(checkLogins) > 0 and checkLogins[0][1] == userName:
			print("Username unavailable or already in use.")
		elif isDisabled == True or isDisabled == None:
			print("Could not find an active company with that name. Please contact Powers Engineering to check your subscription status.")
		elif len(checkCode == 0):
			print("That access code has not been setup. Please double-check or recontact the main account for another code.")
		else:
			cursor.execute("insert into Login values(\'" + emailAddress + "\', \'" + companyName + "\', \'" + userName + "\', \'" + password + "\', \'" + phoneNumber + "\', \'" + phoneExt + "\', \'" + emailNotif + "\', \'" + phoneNotif + "\', 0);")
			cursor.execute("delete from YYY where Company=\'" + companyName + "\' and XXX=\'" + createCode + "\';")
			print("Account created successfully. Return to the login page to sign into your account.")
			connection.commit()
	except pyodbc.Error as err:
		print("Could not create an account using these parameters. Please contact Powers Engineering for assistance or try again later.")
	finally:
		if cursor != None:
			cursor.close()

	return


def attemptLogin(connection, emailAddress, userName, password):
	cursor = connection.cursor()
	try:
		checkLogin = cursor.execute("select Company from Login where EmailAddress=\'" + emailAddress + "\' and Username=\'" + userName + "\' and Password=\'" + password + "\';").fetchall()

		if len(checkLogin) != 1:
			print("Could not locate account.")
		else:
			if isCompanyDisabled(checkLogin[0][0]) == False:
				print("Login successful. Please wait while we load your information.")
			else:
				print("Your company's subscription has expired and your account is temporarily disabled. Please contact Powers Engineering to renew your subscription.")
	except pyodbc.Error as err:
		print("Could not login using the provided login information. Please contact Powers Engineering if you believe this to be incorrect.")
	finally:
		if cursor != None:
			cursor.close()

	return


def updateLoginInfo(connection, emailAddress, userName, columnName, value):
	cursor = connection.cursor()
	try:
		checkAccount = cursor.execute("select * from Login where Username=\'" + userName + "\' and EmailAddress=\'" + emailAddress + "\';").fetchall()
		if checkAccount != 1:
			print("Could not locate account.")
			return

		cursor.execute("update Login set " + columnName + "=\'" + value + "\' where Username=\'" + userName + "\' and EmailAddress=\'" + emailAddress + "\';")
		connection.commit()
		print("Successfully updated account info.")
	except pyodbc.Error as err:
		print("Error making changes to account.")
	finally:
		if cursor != None:
			cursor.close()

	return


def isCompanyDisabled(connection, companyName):
	if isCompanyDisabled(connection, companyName) == True:
		print("Could not find an active company with that name. Please contact Powers Engineering to check your subscription status.")
		return

	cursor = connection.cursor()
	disabled = None
	try:
		checkDisabled = cursor.execute("select Expired from Disable where Company=\'" + companyName + "\';").fetchall()
		if len(checkDisabled) > 0:
			disabled = len([1 for entry in checkDisabled if entry[0] == 'Y']) == 0
	except pyodbc.Error as err:
		print("Could not access company status.")
	finally:
		if cursor != None:
			cursor.close()

	return disabled


def getAccountPermissions(connection, userName):
	cursor = connection.cursor()
	perms = None
	try:
		checkPerms = cursor.execute("select GroupID from Permissions where Username=\'" + userName + "\';").fetchall()
		if len(perms) > 0:
			perms = [entry[0] for entry in checkPerms]
		else:
			print("Successfully pulled account permissions.")
	except pyodbc.Error as err:
		print("Could not retrieve permissions for that account.")
	finally:
		if cursor != None:
			cursor.close()

	return perms


def isAccountPermitted(connection, userName, groupID):
	cursor = connection.cursor()
	permitted = None
	try:
		checkPerms = cursor.execute("select * from Permissions where Username=\'" + userName + "\' and GroupID=\'" + groupID + "\';").fetchall()
		permitted = len(checkPerms) > 0
	except pyodbc.Error as err:
		print("Could not retrieve permissions for that account.")
	finally:
		if cursor != None:
			cursor.close()

	return permitted


def getTankDefault(connection, userName, companyName):
	if isCompanyDisabled(connection, companyName) == True:
		print("Could not find an active company with that name. Please contact Powers Engineering to check your subscription status.")
		return

	cursor = connection.cursor()
	tankInfo = None
	try:
		perms = getAccountPermissions(userName)
		tankInfo = cursor.execute("select * from Tank where Company=\'" + companyName + "\' and GroupID in \'" + perms + "\';")
		if tankInfo == None:
			print("Could not find any tanks for this account.")
		else:
			print("Successfully pulled tank information.")
	except pyodbc.Error as err:
		print("Error loading default tank information.")
	finally:
		if cursor != None:
			cursor.close()

	return tankInfo




####################################################################################################
## Manager Level Account (1)
##
## Heightened access to files and alter table access.
## Requires Master Access or higher to promote.
####################################################################################################


def getTankFiles(connection, companyName, tankName, location, accessLevel) :
	if accessLevel < MANAGER_ACCESS:
		print("Your account doesn't have access to this feature. Request a permission upgrade from your company's master account.")
		return None
	elif isCompanyDisabled(connection, companyName) == True:
		print("Could not find an active company with that name. Please contact Powers Engineering to check your subscription status.")
		return

	cursor = connection.cursor()
	files = None
	try:
		filePaths = cursor.execute("select FileName from files where Company=\'" + companyName + "\' and TankNo=\'" + tankName + "\' and Location=\'" + location + "\';")
		files = [entry[0] for entry in filePaths]
		if files == []:
			print("Could not find any files related to that tank.")
		else:
			print("Successfully located relevant files.")
	except pyodbc.Error as err:
		print("Error retrieving tank files.")
	finally:
		if cursor != None:
			cursor.close()

	return files


def showTankFiles(connection, fileName, accessLevel):
	if accessLevel < MANAGER_ACCESS:
		print("Your account doesn't have access to this feature. Request a permission upgrade from your company's master account.")
		return None
	
	cursor = connection.cursor()
	fileString = None
	try:
		file = open(fileName)
		if file == None:
			print("Error opening that file.")
			return
		else:
			fileString = file.read()
			file.close()
	except pyodbc.Error as err:
		print("Error retrieving the desired file.")
	finally:
		if cursor != None:
			cursor.close()

	return fileString




####################################################################################################
## Company Master Access (2)
##
## Permission access to all accounts and tables with like company relationships.
## Maximum for standard subscription users. One account per company (required and max).
####################################################################################################


def getCompanyAccounts(connection, companyName, accessLevel):
	if accessLevel < MASTER_ACCESS:
		print("Your account doesn't have access to this feature. Request a permission upgrade from your company's master account.")
		return None
	elif isCompanyDisabled(connection, companyName) == True:
		print("Could not find an active company with that name. Please contact Powers Engineering to check your subscription status.")
		return

	cursor = connection.cursor()
	accounts = None
	try:
		search = cursor.execute("select Username, EmailAddress from Login where Company=\'" + companyName + "\';").fetchall()
		accounts = [(entry[0], entry[1]) for entry in search]
		print("Successfully retrieved related accounts.")
	except pyodbc.Error as err:
		print("Error retrieving accounts.")
	finally:
		if cursor != None:
			cursor.close()

	return accounts


def alterAccount(connection, companyName, userName, accessLevel, columnName, value):
	if accessLevel < MASTER_ACCESS:
		print("Your account doesn't have access to this feature. Request a permission upgrade from your company's master account.")
		return
	elif isCompanyDisabled(connection, companyName) == True:
		print("Could not find an active company with that name. Please contact Powers Engineering to check your subscription status.")
		return

	cursor = connection.cursor()
	try:
		checkUser = cursor.execute("select * from Login where Company=\'" + companyName + "\' and Username=\'" + userName + "\';").fetchall()
		if len(checkUser) != 1:
			print("That account could not be located.")
			return

		cursor.execute("update Login set " + columnName + "=\'" + value + "\' where Company=\'" + companyName + "\' and Username=\'" + userName + "\';")
		connection.commit()
		print("Successfully updated account column.")
	except pyodbc.Error as err:
		print("Error making changes to account.")
	finally:
		if cursor != None:
			cursor.close()

	return


def createTempCode(connection, companyName, accessLevel):
	# Create table and use random function to generate unique codes paired per company
	if accessLevel < MASTER_ACCESS:
		print("Your account doesn't have access to this feature. Request a permission upgrade from your company's master account.")
		return
	elif isCompanyDisabled(connection, companyName) == True:
		print("Could not find an active company with that name. Please contact Powers Engineering to check your subscription status.")
		return

	cursor = connection.cursor()
	try:
		checkLimit = cursor.execute("select Code from Passcodes where Company=\'" + companyName + "\';")
		if len(checkLimit) >= 20:
			print("You have reached the passcode limit for today. Please use an existing code or wait for some to expire.")
			return

		newCode = random.randint(10000000, 99999999)
		while len([1 for entry in checkLimit if entry[0] == newCode]) > 0 :
			newCode = random.randint(10000000, 99999999)

		cursor.execute("insert into (Company, Code) values (\'" + companyName + "\', \'" + newCode + "\');")
		connection.commit()
		print("Successfully created registration passcode.")
	except pyodbc.Error as err:
		print("Error creating registration passcode.")
	finally:
		if cursor != None:
			cursor.close()

	return


def grantAccountAccessLevel(connection, userName, masterName, accessLevel):
	if accessLevel < MASTER_ACCESS:
		print("Your account doesn't have access to this feature. Request a permission upgrade from your company's master account.")
		return

	cursor = connection.cursor()
	try:
		companyName = cursor.execute("select Company from Login where Username=\'" + masterName + "\';").fetchall()
		hasAccess = cursor.execute("select Company from Login where Username=\'" + userName + "\' or Username=\'" + masterName + "\';").fetchall()
		if len(hasAccess) < 2 or hasAccess[0][0] != hasAccess[1][0]:
			print("You do not have access to that account.")
		else:
			cursor.execute("update Login set AccountAccess=1 where Username=\'" + userName + "\';")
			connection.commit()
			print("Successfully promoted account.")
	except pyodbc.Error as err:
		print("Error granting heightened access to account.")
	finally:
		if cursor != None:
			cursor.close()

	return


def updateTankDefault(connection, tankName, companyName, accessLevel, columnName, value):
	if accessLevel < MASTER_ACCESS:
		print("Your account doesn't have access to this feature. Request a permission upgrade from your company's master account.")
		return
	elif isCompanyDisabled(connection, companyName) == True:
		print("Could not find an active company with that name. Please contact Powers Engineering to check your subscription status.")
		return

	cursor = connection.cursor()
	try:
		checkTank = cursor.execute("select * from Tank where Company=\'" + companyName + "\' and TankNo=\'" + tankName + "\';").fetchall()
		if len(checkTank) != 1:
			print("A tank with that name could not be located.")
			return

		cursor.execute("update Tank set " + columnName + "=\'" + value + "\' where TankNo=\'" + tankName + "\' and Company=\'" + companyName + "\';")
		connection.commit()
		print("Successfully updated tank column.")
	except pyodbc.Error as err:
		print("Could not make changes to that tank.")
	finally:
		if cursor != None:
			cursor.close()

	return


def createTGroup(connection, companyName, accessLevel, groupName):
	if accessLevel < MASTER_ACCESS:
		print("Your account doesn't have access to this feature. Request a permission upgrade from your company's master account.")
		return
	elif isCompanyDisabled(connection, companyName) == True:
		print("Could not find an active company with that name. Please contact Powers Engineering to check your subscription status.")
		return

	cursor = connection.cursor()
	try:
		checkGroup = cursor.execute("select * from TGroup where Company=\'" + companyName + "\' and GroupID=\'" + groupName + "\';").fetchall()
		if len(checkGroup) > 0:
			print("That group name already exists for your company.")
			return

		cursor.execute("insert into TGroup (Company, GroupID) values (\'" + companyName + "\', \'" + groupName + "\');")
		connection.commit()
		print("Successfully created new group.")
	except pyodbc.Error as err:
		print("Could not create group.")
	finally:
		if cursor != None:
			cursor.close()

	return


def deleteTGroup(connection, companyName, accessLevel, groupName):
	if accessLevel < MASTER_ACCESS:
		print("Your account doesn't have access to this feature. Request a permission upgrade from your company's master account.")
		return
	elif isCompanyDisabled(connection, companyName) == True:
		print("Could not find an active company with that name. Please contact Powers Engineering to check your subscription status.")
		return

	cursor = connection.cursor()
	try:
		checkGroup = cursor.execute("select * from TGroup where Company=" + companyName + " and GroupID=" + groupName + ";").fetchall()
		if len(checkGroup) == 0:
			print("A group with that name doesn't exist.")
			return

		tanks = cursor.execute("select TankNo from Tank where Company=\'" + companyName + "\' and GroupID=\'" + groupName + "\';")
		for tEntry in tanks:
			removeTankFromTGroup(connection, companyName, tEntry[0], accessLevel, groupName)

		accounts = cursor.execute("select Username from Permissions where Company=\'" + companyName + "\' and GroupID=\'" + groupName + "\';")
		for aEntry in accounts:
			dropAccountFromTGroup(connection, aEntry[0], companyName, accessLevel, groupName)

		cursor.execute("delete from TGroup where Company=\'" + companyName + "\' and GroupID=\'" + groupName + "\';")

		connection.commit()
		print("Successfully removed tank group.")
	except pyodbc.Error as err:
		print("Error removing that group. Check with Powers Engineering to restore any lost data.")
	finally:
		if cursor != None:
			cursor.close()

	return


def addTankToTGroup(connection, companyName, tankName, location, accessLevel, groupName):
	if accessLevel < MASTER_ACCESS:
		print("Your account doesn't have access to this feature. Request a permission upgrade from your company's master account.")
		return
	elif isCompanyDisabled(connection, companyName) == True:
		print("Could not find an active company with that name. Please contact Powers Engineering to check your subscription status.")
		return

	cursor = connection.cursor()
	try:
		checkGroup = cursor.execute("select * from TGroup where Company=\'" + companyName + "\' and GroupID=\'" + groupName + "\';").fetchall()
		if len(checkGroup) == 0:
			print("That group name does not exist for your company.")
			return

		checkTank = cursor.execute("select TankNo from Tank where Company=\'" + companyName + "\' and TankNo=\'" + tankName + "\' and Location=\'" + location + "\';").fetchall()
		if len(checkTank) == 0:
			print("Could not locate that tank.")
			return

		cursor.execute("update Tank set GroupID=\'" + groupName + "\' where Company=\'" + companyName + "\' and TankNo=\'" + tankName + "\' and Location=\'" + location + "\';")
		connection.commit()
		print("Successfully added tank to group.")
	except pyodbc.Error as err:
		print("Could not assign tank to group.")
	finally:
		if cursor != None:
			cursor.close()

	return


def removeTankFromTGroup(connection, companyName, tankName, accessLevel, groupName):
	if accessLevel < MASTER_ACCESS:
		print("Your account doesn't have access to this feature. Request a permission upgrade from your company's master account.")
		return
	elif isCompanyDisabled(connection, companyName) == True:
		print("Could not find an active company with that name. Please contact Powers Engineering to check your subscription status.")
		return

	cursor = connection.cursor()
	try:
		checkGroup = cursor.execute("select * from TGroup where Company=\'" + companyName + "\' and GroupID=\'" + groupName + "\';").fetchall()
		if len(checkGroup) == 0:
			print("The group with that name does not exist for your company.")
			return

		checkTank = cursor.execute("select TankNo from Tank where Company=\'" + companyName + "\' and TankNo=\'" + tankName + "\' and GroupID=\'" + groupName + "\';").fetchall()
		if len(checkTank) == 0:
			print("Could not locate that tank.")
			return

		cursor.execute("update Tank set GroupID=NULL where Company=\'" + companyName + "\' and TankNo=\'" + tankName + "\' and GroupID=\'" + groupName + "\';")
		connection.commit()
		print("Successfully removed tank from group.")
	except pyodbc.Error as err:
		print("Could not remove tank from group.")
	finally:
		if cursor != None:
			cursor.close()

	return


def addAccountToTGroup(connection, userName, companyName, accessLevel, groupName):
	if accessLevel < MASTER_ACCESS:
		print("Your account doesn't have access to this feature. Request a permission upgrade from your company's master account.")
		return
	elif isCompanyDisabled(connection, companyName) == True:
		print("Could not find an active company with that name. Please contact Powers Engineering to check your subscription status.")
		return

	cursor = connection.cursor()
	try:
		checkUser = cursor.execute("select * from Login where Username=\'" + userName + "\' and Company=\'" + companyName + "\';").fetchall()
		if len(checkUser) != 1:
			print("An account with that username does not exist.")
			return

		checkGroup = cursor.execute("select * from TGroup where Company=\'" + companyName + "\' and GroupID=\'" + groupName + "\';").fetchall()
		if len(checkGroup) == 0:
			print("That group name does not exist for your company.")
			return

		checkPermExists = cursor.execute("select * from Permissions where Username=\'" + userName + "\' and Company=\'" + companyName + "\' and GroupID=\'" + groupName + "\';").fetchall()
		if len(checkPermExists) > 0:
			print("That account already has access to that group.")
			return

		cursor.execute("insert into Permissions (Company, Username, GroupID) values (\'" + companyName + "\', \'" + userName + "\', \'" + groupName + "\');")
		connection.commit()
		print("Successfully added account to group.")
	except pyodbc.Error as err:
		print("Could not add account to group.")
	finally:
		if cursor != None:
			cursor.close()

	return


def dropAccountFromTGroup(connection, userName, companyName, accessLevel, groupName):
	if accessLevel < MASTER_ACCESS:
		print("Your account doesn't have access to this feature. Request a permission upgrade from your company's master account.")
		return
	elif isCompanyDisabled(connection, companyName) == True:
		print("Could not find an active company with that name. Please contact Powers Engineering to check your subscription status.")
		return

	cursor = connection.cursor()
	try:
		checkPerm = cursor.execute("select * from Permissions where Username=\'" + userName + "\' and Company=\'" + companyName + "\' and GroupID=\'" + groupName + "\';").fetchall()
		if len(checkPerm) == 0:
			print("That account doesn't have access to that group.")
			return

		cursor.execute("delete from Permissions where Company=\'" + companyName + "\' and Username=\'" + userName + "\' and GroupID=\'" + groupName + "\';")
		connection.commit()
		print("Successfully removed account access to group.")
	except pyodbc.Error as err:
		print("Could not remove account from group.")
	finally:
		if cursor != None:
			cursor.close()

	return
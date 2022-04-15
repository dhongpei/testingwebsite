# Admin scripts (0): insert Tank, update LastPayment (update NextPayment, update Expired), update Disable (check/update Expired), upload file, delete Login (heavy gating), recommendations
# Executive 	(1): add group perm, check Disable, request Login termination
# Manager	    (2): get file (direct copy/pdf view), update basic info (warning message, edit all or just update date info?)
# Base		    (3): get basic info (from tables), attempt Login, register acocunt, edit self contact/login

# File conversion
# Format selected rows when printing
# Get table names
# Update Disable to server restart

# Delete
# Insert seems fine, but still doesn't insert

import pyodbc
import pandas as pd


def server_connect(hostName, dbName, userName, userPassword):
    connection = None
    print("Attempting server login...")
    try:
        connection = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server="
                                    + hostName + ";Database=" + dbName + ";UID="
                                    + userName + ";PWD=" + userPassword)
        print("SQL Database connection successful.")
    except pyodbc.Error as err:
        print("Couldn't connect to server with error: '{err}'")

    return connection


def query(connection, queryStr):
    cursor = connection.cursor()
    records = None
    try:
        records = cursor.execute(queryStr).fetchall()
        connection.commit()
    except pyodbc.Error as err:
        return records, err
    finally:
        if cursor != None:
            cursor.close()

    return records, None


def createTable(connection):
    print("Creating new table...")
    cmd = input("\tDo you want to enter the full query now? ").lower()
    if cmd in ["yes", "y"]:
        records, err = query(connection, input("\t\tEnter query now: "))
        if err != None:
            print("\t\tError creating table.", err)
        else:
            print("\t\tTable created successfully.")
    else:
        qStr = "create table " + input("\t\tEnter table name: ") + " ("
        start = True
        while(input("\t\tDo you want to enter another column or constraint? ").lower() in ["yes", "y"]):
            if not start:
                qStr += ", "
            else:
                start = False

            qStr += input("\t\t\tEnter column or constraint now: ")

        records, err = query(connection, qStr + ");")
        if err != None:
            print("\tError creating table.")
        else:
            print("\tTable created successfully.")


def importData(connection):
    print("Importing data from exterior file...")
    cmd = input("\tDo you want to enter the full query now? ").lower()
    if cmd in ["yes", "y"]:
        #do you need to convert a file?
        records, err = query(connection, input("\t\tEnter query now: "))
        if err != None:
            print("\t\tError importing data.")
        else:
            print("\t\tData successfully imported.")
    else:
        fileName = input("\t\tEnter file path (tdv only): ")
        qStr = "bulk insert " + input("\t\tEnter table name: ") + " from \'" + fileName

        try:
            file = open(fileName)
        except Error as err:
            print("\t\tCouldn't open file with name " + filename + ". Cancelling import...")
            return

        # Take csv, xlsx -> tab-sv (quotes take priority over commas) -> Replace all quotes

        qStr += "\' with (firstrow = 2, fieldterminator = \'\t\', rowterminator = \'\n\', tablock);"
        records, err = query(connection, qStr)
        if err != None:
            print("\tError importing data.")
        else:
            print("\tTable created successfully.")


def alterTable(connection):
    #Do something
    print("\tBroken for now, try again later.")

def insertRow(connection):
    cmd = input("\tDo you want to enter the full query now? ").lower()
    if cmd in ["yes", "y"]:
        records, err = query(connection, input("\t\tEnter query now: "))
        if err != None:
            print("\tError inserting row.")
        else:
            print("\tRow successfully inserted.")
    else:
        tableName = input("\t\tEnter table name: ")
        qStr = "insert into " + tableName + " values("
        columns, errCol = query(connection, "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N\'" + tableName + "\';")
        if errCol != None:
            print("\t\tError getting column information.")
            return
        
        isFirst = True
        for colName in columns:
            colType, errType = query(connection, "SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N\'" + tableName + "\' AND COLUMN_NAME = N\'" + colName[0] + "\';")
            if errType != None:
                print("\t\tError getting column type.")
                return

            if not isFirst:
                qStr += ", "

            isFirst = False
            if colType[0][0].lower() in ["char", "varchar", "text", "nchar", "nvarchar", "ntext", "binary", "varbinary", "image", "datetime", "datetime2", "smalldatetime", "date", "time", "datetimeoffset, timestamp"]:
                qStr += "\'" + input("\t\t\tEnter value for \'" + colName[0] + "\' column: ") + "\'"
            else:
                qStr += input("\t\t\tEnter value for \'" + colName[0] + "\' column: ")

        records, errIns = query(connection, qStr + ");")
        if errIns != None:
            print("\tError inserting row.")
        else:
            print("\tRow successfully inserted.")


def dropTable(connection):
    qStr = "drop table " + input("\tEnter table name: ") + ";"
    records, err = query(connection, qStr)
    if err != None:
        print("\tError deleting table.")
    else:
        print("\tTable successfully deleted.")


def selectRows(connection):
    tableName = input("\tEnter table name: ")
    qStr = "select top(" + input("\tHow many rows? ") + ") * from " + tableName + ";"
    columns, errCol = query(connection, "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N\'" + tableName + "\';")
    if errCol != None:
        print("\tError getting column information.")
        return

    rows, errRow = query(connection, qStr)
    if errRow != None:
        print("\tError getting row information.")
        return
    #Do column formatting for printed rows
    for colName in columns:
        print(colName[0], "\t", end='')

    print()
    for row in rows:
        for cell in row:
            print(cell, "\t", end='')

        print()


def main():
    hostName = "testing-server.database.windows.net"
    dbName = "NoLedger"
    userName = "powersadmin"
    userPassword = "cr@yonstastel1kemelon"
    connection = server_connect(hostName, dbName, userName, userPassword)

    validCommands = ["quit", "q", "create", "c", "new", "populate", "pop", "p", "fill", "drop", "d", "delete", "remove", "insert", "ins", "i", "add", "get", "g", "retrieve", "modify", "m", "alter"]
    cmd = ""
    while cmd != None:
        cmd = input("Enter a keyword: ").lower()
        if cmd in ["quit", "q"]:
            cmd = input("\tAre you sure? ").lower()
            if cmd in ["yes", "y", "quit", "q"]:
                break;
        elif cmd in ["create", "c", "new"]:
            createTable(connection)
        elif cmd in ["populate", "pop", "p", "fill"]:
            importData(connection)
        elif cmd in ["drop", "d", "delete", "remove"]:
            dropTable(connection)
        elif cmd in ["insert", "ins", "i", "add"]:
            insertRow(connection)
        elif cmd in ["get", "g", "retrieve"]:
            selectRows(connection)
        elif cmd in ["modify", "m", "alter"]:
            alterTable(connection)
        else:
            similar = []
            for word in validCommands:
                if cmd in word or cmd[0] == word[0]:
                    similar.append(word)
                else:
                    common = 0
                    for letter in cmd:
                        if letter in word:
                            common += 1

                    if (common/len(cmd) >= 0.9):
                        similar.append(word)

            if similar == []:
                similar = validCommands
                print("Bad query entered. Available commands: ", end='')
            else :
                print("Bad query entered. Did you mean: ", end='')

            for word in similar:
                print(word, end='')
                if word != similar[-1]:
                    print(", ", end='')

            print()

        print()

    if (connection != None):
        print("\nDisconnecting from database.")
        connection.close()


main()



# C:\Users\riced\Desktop\Powers\Customer Database\Testing\TankDataSample.txt
# create table TGroup (Company varchar(30) not null, GroupID varchar(15) not null, constraint PK_Group primary key (Company,GroupID));
# insert into Test values('HELCO', 'Honolulu, Hawaii, US', '712893', 'Aboveground Vertical', 'Bolted', 'Cone', 'Aluminum', 'Bolted', 'Asphalt', 'Av Gas', 100, 100, 100);

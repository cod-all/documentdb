#! /usr/bin/python3

# import MongoClient class
import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# ask for varialbes
defaultHost = "127.0.0.1"
MongoHost = input ("MongoDB host connection details (default 127.0.0.1): ")
if not MongoHost:
    MongoHost = defaultHost

defaultPort = 27017
MongoPort = int(input("MongoDB host port (default 27017): ") or defaultPort)

MongoUser = input ("MongoDB admin user: ")
while len(MongoUser)==0:
    MongoUser=input("Admin user required - please enter MongoDB admin user: ")

MongoPass = input ("MongoDB password: ")
while len(MongoPass)==0:
    MongoPass=input("Password is required - please enter MongoDB password: ")

print("Attempting to connect to MongoDB instance" + " " + MongoHost)

def connMongo():
    try:
        # create an instance of MongoClient()
        conn = MongoClient(host = MongoHost + ":" + str(MongoPort),
                             serverSelectionTimeoutMS = 5000, # 5 second timeout
                             username = MongoUser,
                             password = MongoPass)
                             
        conn.server_info()
    
    except (pymongo.errors.ConnectionFailure, pymongo.errors.NetworkTimeout, pymongo.errors.OperationFailure) as e:   
        print ("Error connecting to server: %s" % e)
        return
    
    return conn

def getUsers(client = connMongo()):

    if client is None:
        return

    try:
        # authenticating against the admin databse to get user credentials
        db = client.admin
        userInfo = db.command('usersInfo')
        
        # creating the output file
        print("Creating results file")
        f = open("user_output.txt", "w+")
        print("use admin", file=f)

        # iterate through the results of users and output their dbs and roles to the output file
        print("Collecting user information")
        for document in userInfo['users']:
            roleCount = len(document['roles'])
            for i in range(roleCount):
                print ("db.createUser({user:" + '"' + document['user'] + '",pwd:' + '"{REPLACE THIS VALUE WITH YOUR PASSWORD}",roles:[{"db":"' + document['roles'][i]['db'] +'","role":"' + document['roles'][i]['role'] + '"}]})', file=f)
        
        f.close()
        print("User collection successful.")
        
    except:
        print ("No host found - check host name")
        
getUsers()

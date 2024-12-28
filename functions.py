import os
import ast
import pickle
from pymongo import MongoClient
cluster="mongodb://mongo:WNsrSjDuaLpLoKAMZosADdAHTbhJrZFG@autorack.proxy.rlwy.net:42448/?retryWrites=true&w=majority"
client=MongoClient(cluster)
db=client.Users
profs=db.profiles
lists=db.listings
def signUp(user, passwd):
    j=profs.find_one({user: {'$exists': True}})
    if j==None:
        c={user:passwd,
           "wood":50,
           "steel":{"type1":0, "type2":0, "type3":0},
           "plants":{"cotton":0, "wool":0, "silk":0, "bamboo":0, "tomato":0, "onion":0},
           "metal":{"iron":0, "tungsten":0, "copper":0},
           "plastic":0,
           "money":10000}
        l=profs.insert_one(c)
        lists.insert_one({"material":[]})
        return "Done!"
    else:
        return "User exists!"

def passChange(user,oldPasswd,newPasswd):
    r=profs.find_one({user: {'$exists': True}})
    if r!=None:
        if profs.find_one({user:oldPasswd}):
            profs.update_one({user:oldPasswd},{"$set":{user: newPasswd}})
            return "password changed"
        else:
            return "wrong current password"
    else:
        return "no user"

def login(user, passwd):
    f=profs.find_one({user: {'$exists': True}})
    if f==None:
        return "User not found!"
    else:
        if profs.distinct(user)==[passwd]:
            print(profs.distinct(user))
            print(type(profs.distinct(user)))
            return "correct!"
        else:
            print(profs.distinct(user))
            print(type(profs.distinct(user)))
            return "incorrect!"

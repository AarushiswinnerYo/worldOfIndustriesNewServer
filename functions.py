import os
import ast
import pickle

def signUp(user, passwd):
    os.chdir("users")
    j=os.path.isfile(f"{user}.profile")
    if not j:
        with open(f"{user}.profile", "wb") as newUser:
            c={"passwd":passwd,
               "wood":50,
               "steel":{"type1":0, "type2":0, "type3":0},
               "plants":{"cotton":0, "wool":0, "silk":0, "bamboo":0, "tomato":0, "onion":0},
               "metal":{"iron":0, "tungsten":0, "copper":0},
               "plastic":0,
               "money":10000}
            pickle.dump(c, newUser)
        os.chdir("..")
        os.chdir("listings")
        with open(f"{user}.listings", "w") as newUserListings:
            newUserListings.write('{"material":[]}')
        os.chdir('..')
        return "Done!"
    else:
        os.chdir("..")
        return "User exists!"

def passChange(user,oldPasswd,newPasswd):
    os.chdir("users")
    r=os.path.isfile(f"{user}.profile")
    if r:
        with open(f"{user}.profile","rb") as changePass:
            f=pickle.load(changePass)
        if oldPasswd==f["passwd"]:
            f["passwd"]=newPasswd
            with open(f"{user}.profile", "wb") as newPass:
                pickle.dump(f, newPass)
            os.chdir("..")
            return "password changed"
        else:
            os.chdir("..")
            return "wrong current password"
    else:
        os.chdir("..")
        return "no user"

def login(user, passwd):
    os.chdir("users")
    f=os.path.isfile(f"{user}.profile")
    if not f:
        os.chdir("..")
        return "User not found!"
    else:
        with open(f"{user}.profile", "rb") as s:
            x=pickle.load(s)
        os.chdir("..")
        if passwd==x['passwd']:
            return "correct!"
        else:
            return "incorrect!"
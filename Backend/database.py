from pymongo.mongo_client import MongoClient
import cipher
import HardwareSet

uri = "mongodb+srv://resulovezov:zTXelEryJEzsz6N8@cluster0.ieiqobl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


# Consts
CIPHER_N = 5
CIPHER_D = 1
SIGN_UP_SUCCESSFUL = 1
SIGN_UP_USER_EXISTS = 0
LOGIN_FAILED = 0
LOGIN_SUCCESS = 1
DB_ERROR = -1
PROJECT_ADD_SUCCESS = 1
PROJECT_ADD_FAILURE = 0


# CALL THIS ONLY ONCE. THIS HAS BEEN CALLED ALREADY SO DO NOT CALL IT AGAIN
def DATABASE_CREATE_HARDWARE():
    client = MongoClient(uri)
    db = client["HardwareSet"]
    collection = db["Universe"]
    laser = HardwareSet.HardwareSet(name="Laser Cutter", capacity=1000, availability=1000, checked={})
    print3D = HardwareSet.HardwareSet(name="3D Printer", capacity=1000, availability=1000, checked={})
    gpu = HardwareSet.HardwareSet(name="GPU", capacity=1000, availability=1000, checked={})
    collection.insert_one(laser.to_dict())
    collection.insert_one(print3D.to_dict())
    collection.insert_one(gpu.to_dict())
    client.close()

# This function adds a project, call only after loging in or signing in
# This function adds the projectID to the user's projects list
# Then it creates the project with the given values
# This only happens if the User exists and the the project does not already exist
# Input: userID (username), name (string), id (project id), description (string), hardwareSets (list of HardSet objects)
# Output  if successful return PROJECT_ADD_SUCCESS
# if error then DB_ERROR
# if user already exists PROJECT_ADD_FAILURE
def database_add_project(userid, name, id, description):
    try:
        client = MongoClient(uri)
        db = client["Projects"]
        collection = db["Universe"]
        userDB = client["Users"]
        userCollection = userDB["Universe"]
        filter = {"userid": userid}
        userProjectList = userCollection.find_one({"userid": userid}, {"projects": 1, "_id": 0})
        if userProjectList is None:
            client.close()
            return PROJECT_ADD_FAILURE
        else:
            userProjectList = userProjectList.get("projects")
        projectToAdd = collection.find_one({"ID": id})
        if projectToAdd is None:
            set = {
                    "Name": name,
                    "ID": id,
                    "Description": description,
                    "Users": [userid]
                }
            userProjectList.append(id)
            update_statement = {"$set": {"projects": userProjectList}}
            result = userCollection.update_one(filter, update_statement)
            if result.modified_count > 0:
                collection.insert_one(set)
                client.close()
                return PROJECT_ADD_SUCCESS
            else:
                client.close()
                return PROJECT_ADD_FAILURE
        else:
            client.close()
            return PROJECT_ADD_FAILURE
    except Exception as e:
        client.close()
        print(e)
        return DB_ERROR

# Function joins a user to a project, ie updates their list to include the id
# Input: userid (username), projectid (projectid)
# Output: Same stuff
def database_join_project(userid, projectid):
    try:
        client = MongoClient(uri)
        db = client["Projects"]
        collection = db["Universe"]
        userDB = client["Users"]
        userCollection = userDB["Universe"]
        filter = {"userid": userid}
        filterProject = {"ID": projectid}
        userProjectList = userCollection.find_one({"userid": userid}, {"projects": 1, "_id": 0})
        if userProjectList is None:
            client.close()
            return PROJECT_ADD_FAILURE
        else:
            userProjectList = userProjectList.get("projects")
        projectUserList = collection.find_one({"ID": projectid}, {"Users": 1, "_id": 0})
        if projectUserList is not None:
            if projectid not in userProjectList:
                userProjectList.append(projectid)
                update_statement = {"$set": {"projects": userProjectList}}
                result = userCollection.update_one(filter, update_statement)
                if result.modified_count > 0:
                    projectUserList = projectUserList.get("Users")
                    projectUserList.append(userid)
                    update_statement = {"$set": {"Users": projectUserList}}
                    collection.update_one(filterProject, update_statement)
                    client.close()
                    return PROJECT_ADD_SUCCESS
                else:
                    client.close()
                    return PROJECT_ADD_FAILURE
            else:
                client.close()
                return PROJECT_ADD_FAILURE
        else:
            client.close()
            return PROJECT_ADD_FAILURE
    except Exception as e:
        client.close()
        print(e)
        return DB_ERROR

# Function returns the list of projects the user has
# Input userid
# Output if successful list of projects
# if error occurs then returns None
def database_get_user_projects(userid):
    try:
        projectList = []
        client = MongoClient(uri)
        db = client["Projects"]
        collection = db["Universe"]
        userDB = client["Users"]
        userCollection = userDB["Universe"]
        userProjectList = userCollection.find_one({"userid": userid}, {"projects": 1, "_id": 0})
        if userProjectList is None:
            client.close()
            return None
        else:
            userProjectList = userProjectList.get("projects")
        
        for projectID in userProjectList:
            project = collection.find_one({"ID": projectID}, {"_id": 0})
            if project is None:
                client.close()
                return None
            else:
                projectList.append(project)
        return projectList
    except Exception as e:
        client.close()
        print(e)
        return None

# This function adds a new user to the database
# Input: userid (username), password
# Output  if successful return SIGN_UP_SUCCESSFUL
# if error in try and except then DB_ERROR
# if user already exists SIGN_UP_USER_EXISTS
def database_sign_up(userid, password):
    try:
        client = MongoClient(uri)
        db = client["Users"]
        collection_name = "Universe"
        collection = db[collection_name]
        user = collection.find_one({"userid": userid})
        if user is None:
            encrypted_password = cipher.encrypt(password, CIPHER_N, CIPHER_D)
            new_user = {
                    "userid": userid,
                    "password": encrypted_password,
                    "projects": []
                }
            collection.insert_one(new_user)
            client.close()
            return SIGN_UP_SUCCESSFUL
        else:
            client.close()
            return SIGN_UP_USER_EXISTS
    except Exception as e:
        print(e)
        client.close()
        return DB_ERROR


# This function logs in a user
# Input: userid (username), password
# Output  if successful return LOGIN_SUCCESSFUL
# if error then DB_ERROR
# if user does not exist LOGIN_FAILED
# if password is incorrect LOGIN_FAILED
def database_login(userid, password):
    try:
        client = MongoClient(uri)
        db = client["Users"]
        collection_name = "Universe"
        collection = db[collection_name]
        user = collection.find_one({"userid": userid})
        if user is None:
            client.close()
            return LOGIN_FAILED
        else:
            dbPassword = cipher.decrypt(collection.find_one({"userid": userid}, {"password": 1, "_id": 0}).get("password"), CIPHER_N, CIPHER_D)
            if (dbPassword == password):
                client.close()
                return LOGIN_SUCCESS
            else:
                client.close()
                return LOGIN_FAILED
    except Exception as e:
        client.close()
        print(e)
        return DB_ERROR


def database_check_out(hardwareName, userID, qty):
    client = MongoClient(uri)
    db = client["HardwareSet"]
    collection = db["Universe"]
    document = collection.find_one({"hardware_name": hardwareName})
    if document is not None:
        filter = {"hardware_name": hardwareName}
        hardwareObj = HardwareSet.HardwareSet.from_dict(document)
        hardwareObj.check_out(qty, userID)
        collection.replace_one(filter, hardwareObj.to_dict())

def database_check_in(hardwareName, userID, qty):
    client = MongoClient(uri)
    db = client["HardwareSet"]
    collection = db["Universe"]
    document = collection.find_one({"hardware_name": hardwareName})
    if document is not None:
        filter = {"hardware_name": hardwareName}
        hardwareObj = HardwareSet.HardwareSet.from_dict(document)
        if(hardwareObj.check_in(qty, userID) == 0):
            collection.replace_one(filter, hardwareObj.to_dict())

def database_get_hardwareSets():
    client = MongoClient(uri)
    db = client["HardwareSet"]
    collection = db["Universe"]
    documents = collection.find({}, {"_id": 0})
    hardwareList = []
    for doc in documents:
        hardwareList.append(doc)
    return hardwareList

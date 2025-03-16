import hashlib
from datetime import datetime
import re
import json
from Classes import Customer, Driver
    
def openFile(TableFile):
    try:
        # Try to open the file, if it doesn't exist, an exception will be raised
        with open(TableFile, "r") as file:
            try:
                FileContents = json.load(file)  # Attempt to load the existing data on file
                return FileContents
            except json.JSONDecodeError:
                FileContents = []  # If the file is empty, it returns an empty list
                return FileContents
    except FileNotFoundError:
        return False
    
def closeFile(TableFile, FileContents):
    try:
        # Writes the updated list into the file, if an error occurs, it returns the exception
        with open(TableFile, "w") as file:
            json.dump(FileContents, file, indent=4)
        return True
    except Exception:
        return False
    
def hashPassword(Password):
    return hashlib.sha256(Password.encode()).hexdigest()

def validateFutureDate(Date):
    # Validate if the given date is in the correct format and is today or in the future.
    Regex = r"^(?:(?:31[- /.](0[13578]|1[02]))|(?:30[- /.](0[13-9]|1[0-2]))|(?:29[- /.]02[- /.](?:(?:19|20)(?:[02468][048]|[13579][26])|2000))|(?:0[1-9]|1\d|2[0-8])[- /.](0[1-9]|1[0-2]))[- /.](19|20)\d\d$"
    # Check format
    if not re.match(Regex, Date):
        return False, "Invalid date format or impossible date."

    # Convert to datetime object
    try:
        DateStruct = datetime.strptime(Date, "%d/%m/%Y")
    except ValueError:
        return False, "Invalid date format."

    # Get current date
    Today = datetime.today()

    # Ensure date is later than today
    if DateStruct > Today:
        return True, "Valid future date."
    else:
        return False, "Date must be in the future."

def searchUser(UserType, userID):
    if UserType == "customers":
        customers = openFile("customers.json")
        for customer in customers:
            if customer["custID"] == userID:
                UserDetails = Customer(customer["custID"], 
                                    customer["Firstname"], 
                                    customer["Lastname"], 
                                    customer["Email"], 
                                    customer["Password"], 
                                    customer["Phone Number"], 
                                    customer["Street"], 
                                    customer["City"], 
                                    customer["Postcode"])
                return UserDetails
            else:
                return False
    else:
        drivers = openFile("drivers.json")
        for driver in drivers:
            if driver["driverID"] == userID:
                UserDetails = Driver(driver["driverID"], 
                                    driver["Firstname"], 
                                    driver["Lastname"], 
                                    driver["Email"], 
                                    driver["Password"], 
                                    driver["Phone Number"], 
                                    driver["Street"], 
                                    driver["City"], 
                                    driver["Postcode"],
                                    driver["Car Reg"], 
                                    driver["Car Model"], 
                                    driver["Wallet"])
                return UserDetails
            else:
                return False
            
def updateCustomerDetails(UserDetails, key, newValue):
    customers = openFile("customers.json")
    for customer in customers:
        if customer["custID"] == UserDetails.getCustID():
            customer[key] = newValue
            break
    closeFile("customers.json", customers)
    
def updateDriverDetails(UserDetails, key, newValue):
    drivers = openFile("drivers.json")
    for driver in drivers:
        if driver["driverID"] == UserDetails.getDriverID():
            driver[key] = newValue
            break
    closeFile("drivers.json", drivers)
    
def updateMultipliers(key, newValue):
    multipliers = openFile("multipliers.json")
    multipliers[key] = float(newValue)
    closeFile("multipliers.json", multipliers)
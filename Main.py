# Imports required modules module
import re
import pygame
import sys
from Classes import Button, Customer, Driver, Admin
import User_Detail_Processes
import Price_Calculator
import time
import datetime    
# Initialize Pygame to display a Screen
pygame.init()

# Creates the window
Width, Height = 800, 1000
Screen = pygame.display.set_mode((Width, Height), pygame.RESIZABLE)
pygame.display.set_caption("TaxiCo Booking and Management System")

# Creates the different Fonts (Different Font sizes)
pygame.font.init()
TitleFont = pygame.font.Font(None, 72)
SubtitleFont = pygame.font.Font(None, 36)
button_Font = pygame.font.Font(None, 32)
ErrorFont = pygame.font.SysFont(None, 18)
Font = pygame.font.SysFont(None, 24)
       
def custLogin():
    InputBoxes = [pygame.Rect(250, 160 + i * 80, 300, 40) for i in range(2)]
    Labels = ["Email:", "Password:"]
    Inputs = ["", ""]
    ActiveIndex = 0
    ErrorMessage = ""
    LastCursorTime = time.time()  # To track the blink timing
    CursorVisible = True  # To toggle caret visibility
    
    def ValidateCustLogin(Email, Password):
        Users = User_Detail_Processes.openFile("customers.json")
        if Users == False:
            return False
        # Hashes Password to compare it to what is on the database
        Password = User_Detail_Processes.hashPassword(Password)
        for User in Users:
            if User["Email"].lower() == Email.lower() and User["Password"] == Password:
                UserDetails = Customer(User["custID"], 
                                       User["Firstname"], 
                                       User["Lastname"], 
                                       User["Email"], 
                                       User["Password"], 
                                       User["Phone Number"], 
                                       User["Street"], 
                                       User["City"], 
                                       User["Postcode"])
                return UserDetails
        return False

    Running = True
    while Running:
        Screen.fill((0, 0, 0))
        
        # Draws title background
        TitleBgRect = pygame.Rect(0, 0, Width, Height // 15)
        pygame.draw.rect(Screen, (0, 153, 0), TitleBgRect)

        # Renders title
        TitleSurface = TitleFont.render("TBMS", True, (0, 0, 0))
        TitleRect = TitleSurface.get_rect(center=(Width // 2, Height // 25))
        Screen.blit(TitleSurface, TitleRect)
        
        # Displays the name of the screen "Customer Login"
        SubtitleSurface = TitleFont.render("Customer Login", True, (255, 255, 255))
        Screen.blit(SubtitleSurface, (Width // 2 - SubtitleSurface.get_width() // 2, 80))
        
        for i, label in enumerate(Labels):
            LabelSurface = Font.render(label, True, (255, 255, 255))
            Screen.blit(LabelSurface, (250, 130 + i * 80))
            pygame.draw.rect(Screen, (255, 255, 255), InputBoxes[i], 2)
            InputSurface = Font.render(Inputs[i], True, (255, 255, 255))
            Screen.blit(InputSurface, (InputBoxes[i].x + 5, InputBoxes[i].y + 10))
            
            # Toggle cursor visibility based on time
            if time.time() - LastCursorTime > 0.5:
                CursorVisible = not CursorVisible
                LastCursorTime = time.time()

            # Draw the blinking cursor if it's visible and if the field is active
            if CursorVisible and ActiveIndex == i:  # Active index matches the current label
                CursorX = InputBoxes[i].x + 5 + Font.size(Inputs[i])[0]
                CursorY = InputBoxes[i].y + 10
                pygame.draw.line(Screen, (255, 255, 255), (CursorX, CursorY), (CursorX, CursorY + 15), 2)

        if ErrorMessage:
            ErrorSurface = Font.render(ErrorMessage, True, (255, 0, 0))
            Screen.blit(ErrorSurface, (250, 320))
        
        # Creates and displays the "Login" button
        LoginButton = Button("Login", (Width // 2 - 60, Height - 200, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), ValidateCustLogin)
        LoginButton.draw(Screen, pygame.mouse.get_pos())
        
        # Creates and displays the "Exit" button
        ExitButton = Button("Exit", (Width // 2 - 60, Height - 100, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), mainMenu)
        ExitButton.draw(Screen, pygame.mouse.get_pos())        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    Inputs[ActiveIndex] = Inputs[ActiveIndex][:-1]
                elif event.key == pygame.K_TAB:
                    ActiveIndex = (ActiveIndex + 1) % 2
                elif event.key == pygame.K_RETURN:
                    UserDetails = ValidateCustLogin(Inputs[0], Inputs[1])
                    if UserDetails:
                        return custMenu(UserDetails)
                    else:
                        ErrorMessage = "Invalid email or password. Try again."
                else:
                    Inputs[ActiveIndex] += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(InputBoxes):
                    if rect.collidepoint(event.pos):
                        ActiveIndex = i
                if LoginButton.rect.collidepoint(event.pos):
                    UserDetails = ValidateCustLogin(Inputs[0], Inputs[1])
                    if UserDetails:
                        return custMenu(UserDetails)
                    else:
                        ErrorMessage = "Invalid email or password. Try again."
                elif ExitButton.rect.collidepoint(event.pos):
                    MousePosition = pygame.mouse.get_pos()
                    ExitButton.check_click(MousePosition)
        
        pygame.display.flip()
         
def driverLogin():
    InputBoxes = [pygame.Rect(250, 160 + i * 80, 300, 40) for i in range(2)]
    Labels = ["Email:", "Password:"]
    Inputs = ["", ""]
    ActiveIndex = 0
    ErrorMessage = ""
    LastCursorTime = time.time()  # To track the blink timing
    CursorVisible = True  # To toggle caret visibility
    
    def validateDriverLogin(Email, Password):
        # Pulls user data from database
        Users = User_Detail_Processes.openFile("drivers.json")
        if Users == False: # If the file is empty, it returns False
            return False
        # Hashes Password to compare it to what is on the database
        Password = User_Detail_Processes.hashPassword(Password)
        for User in Users: # Cycles through every user 
            if User["Email"].lower() == Email.lower() and User["Password"] == Password:
                # Puts all driver details into an object from Driver class
                UserDetails = Driver(User["driverID"], 
                                     User["Firstname"], 
                                     User["Lastname"], 
                                     User["Email"], 
                                     User["Password"], 
                                     User["Phone Number"], 
                                     User["Street"], 
                                     User["City"], 
                                     User["Postcode"],
                                     User["Car Reg"], 
                                     User["Car Model"], 
                                     User["Wallet"])
                return UserDetails
        return False # Returns False if no Email and Password is matched

    Running = True
    while Running:
        Screen.fill((0, 0, 0))
        
        # Draws title background
        TitleBgRect = pygame.Rect(0, 0, Width, Height // 15)
        pygame.draw.rect(Screen, (0, 153, 0), TitleBgRect)

        # Renders title
        TitleSurface = TitleFont.render("TBMS", True, (0, 0, 0))
        TitleRect = TitleSurface.get_rect(center=(Width // 2, Height // 25))
        Screen.blit(TitleSurface, TitleRect)
        
        # Displays the name of the screen "Driver Login"
        SubtitleSurface = TitleFont.render("Driver Login", True, (255, 255, 255))
        Screen.blit(SubtitleSurface, (Width // 2 - SubtitleSurface.get_width() // 2, 80))
        
        for i, label in enumerate(Labels): # Cycles through all the values in Labels
            LabelSurface = Font.render(label, True, (255, 255, 255))
            Screen.blit(LabelSurface, (250, 130 + i * 80)) # Creates Label
            pygame.draw.rect(Screen, (255, 255, 255), InputBoxes[i], 2)
            # Draws input surcface
            InputSurface = Font.render(Inputs[i], True, (255, 255, 255))
            Screen.blit(InputSurface, (InputBoxes[i].x + 5, InputBoxes[i].y + 10)) 
        
            # Toggle cursor visibility based on time
            if time.time() - LastCursorTime > 0.5:
                CursorVisible = not CursorVisible
                LastCursorTime = time.time()

            # Draw the blinking cursor if it's visible and if the field is active
            if CursorVisible and ActiveIndex == i:  # Active index matches the current label
                CursorX = InputBoxes[i].x + 5 + Font.size(Inputs[i])[0]
                CursorY = InputBoxes[i].y + 10
                pygame.draw.line(Screen, (255, 255, 255), (CursorX, CursorY), (CursorX, CursorY + 15), 2)

        if ErrorMessage: # Displays ErrorMessage if not empty
            ErrorSurface = Font.render(ErrorMessage, True, (255, 0, 0))
            Screen.blit(ErrorSurface, (250, 320))
        
        # Creates and displays the "Login" button
        LoginButton = Button("Login", (Width // 2 - 60, Height - 200, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), validateDriverLogin)
        LoginButton.draw(Screen, pygame.mouse.get_pos())
        
        # Creates and displays the "Exit" button
        ExitButton = Button("Exit", (Width // 2 - 60, Height - 100, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), mainMenu)
        ExitButton.draw(Screen, pygame.mouse.get_pos())        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If window exit button is clicked it closes application
                Running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN: # For all the keyboard presses
                if event.key == pygame.K_BACKSPACE: # If backspace is presses, removes the last letter in the input box
                    Inputs[ActiveIndex] = Inputs[ActiveIndex][:-1] 
                elif event.key == pygame.K_TAB: # If TAB is pressed, it switches to next input box
                    ActiveIndex = (ActiveIndex + 1) % 2 
                elif event.key == pygame.K_RETURN: # If Enter is pressed, submits user details for validation
                    UserDetails = validateDriverLogin(Inputs[0], Inputs[1]) # Validates inputs
                    if UserDetails:
                        return driverMenu(UserDetails) 
                    else:
                        ErrorMessage = "Invalid email or password. Try again."
                else:
                    Inputs[ActiveIndex] += event.unicode # Enters character into input box
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # For all left mouse clicks
                for i, rect in enumerate(InputBoxes):
                    if rect.collidepoint(event.pos):
                        ActiveIndex = i
                if LoginButton.rect.collidepoint(event.pos): # Login Button Collision
                    UserDetails = validateDriverLogin(Inputs[0], Inputs[1]) # Validates inputs
                    if UserDetails:
                        return driverMenu(UserDetails)
                    else:
                        ErrorMessage = "Invalid email or password. Try again."
                elif ExitButton.rect.collidepoint(event.pos): # Exit Button collision
                    MousePosition = pygame.mouse.get_pos()
                    ExitButton.check_click(MousePosition)
                    
        pygame.display.flip()

def adminLogin():
    InputBoxes = [pygame.Rect(250, 160 + i * 80, 300, 40) for i in range(2)]
    Labels = ["AdminID:", "Password:"]
    Inputs = ["", ""]
    ActiveIndex = 0
    ErrorMessage = ""
    LastCursorTime = time.time()  # To track the blink timing
    CursorVisible = True  # To toggle caret visibility
        
    def validateAdminLogin(AdminID, Password):
        # Pulls user data from database
        Users = User_Detail_Processes.openFile("admins.json")
        try:
            AdminID = int(AdminID)
        except Exception:
            return False
        # Hashes Password to compare it to what is on the database
        Password = User_Detail_Processes.hashPassword(Password)
        
        # AdminID and Password checked against all admin users to see if login details are valid
        if Users == False:
            return False # If the file is empty, it returns False
        for User in Users:
            if User["adminID"] == AdminID and User["Password"] == Password:
                # Puts all driver details into an object from Driver class
                UserDetails = Admin(User["adminID"], 
                                    User["Firstname"], 
                                    User["Lastname"], 
                                    User["Email"], 
                                    User["Password"], 
                                    User["Phone Number"], 
                                    User["Street"], 
                                    User["City"], 
                                    User["Postcode"])
                return UserDetails
        return False # Returns False if no Email and Password is matched

    Running = True
    while Running:
        Screen.fill((0, 0, 0))
        
        # Draws title background
        TitleBgRect = pygame.Rect(0, 0, Width, Height // 15)
        pygame.draw.rect(Screen, (0, 153, 0), TitleBgRect)

        # Renders title
        TitleSurface = TitleFont.render("TBMS", True, (0, 0, 0))
        TitleRect = TitleSurface.get_rect(center=(Width // 2, Height // 25))
        Screen.blit(TitleSurface, TitleRect)
        
        # Displays the name of the screen "Administrator Login"
        SubtitleSurface = TitleFont.render("Administrator Login", True, (255, 255, 255))
        Screen.blit(SubtitleSurface, (Width // 2 - SubtitleSurface.get_width() // 2, 80))
        
        for i, label in enumerate(Labels): # Cycles through all the values in Labels
            LabelSurface = Font.render(label, True, (255, 255, 255))
            Screen.blit(LabelSurface, (250, 130 + i * 80)) # Creates Label
            pygame.draw.rect(Screen, (255, 255, 255), InputBoxes[i], 2)
            # Draws input surcface
            InputSurface = Font.render(Inputs[i], True, (255, 255, 255))
            Screen.blit(InputSurface, (InputBoxes[i].x + 5, InputBoxes[i].y + 10))
            
            # Toggle cursor visibility based on time
            if time.time() - LastCursorTime > 0.5:
                CursorVisible = not CursorVisible
                LastCursorTime = time.time()

            # Draw the blinking cursor if it's visible and if the field is active
            if CursorVisible and ActiveIndex == i:  # Active index matches the current label
                CursorX = InputBoxes[i].x + 5 + Font.size(Inputs[i])[0]
                CursorY = InputBoxes[i].y + 10
                pygame.draw.line(Screen, (255, 255, 255), (CursorX, CursorY), (CursorX, CursorY + 15), 2)
        
        if ErrorMessage: # Displays ErrorMessage if not empty
            ErrorSurface = Font.render(ErrorMessage, True, (255, 0, 0))
            Screen.blit(ErrorSurface, (250, 320))
        
        # Creates and displays the "Login" button
        LoginButton = Button("Login", (Width // 2 - 60, Height - 200, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), validateAdminLogin)
        LoginButton.draw(Screen, pygame.mouse.get_pos())
        
        # Creates and displays the "Exit" button
        ExitButton = Button("Exit", (Width // 2 - 60, Height - 100, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), mainMenu)
        ExitButton.draw(Screen, pygame.mouse.get_pos())        
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If window exit button is clicked it closes application
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN: # For all the keyboard presses
                if event.key == pygame.K_BACKSPACE: # If backspace is presses, removes the last letter in the input box
                    Inputs[ActiveIndex] = Inputs[ActiveIndex][:-1]
                elif event.key == pygame.K_TAB: # If TAB is pressed, it switches to next input box
                    ActiveIndex = (ActiveIndex + 1) % 2
                elif event.key == pygame.K_RETURN: # If Enter is pressed, submits user details for validation
                    UserDetails = validateAdminLogin(Inputs[0], Inputs[1]) # Validates inputs
                    if UserDetails:
                        return adminMenu(UserDetails)
                    else:
                        ErrorMessage = "Invalid AdminID or password. Try again."
                else:
                    Inputs[ActiveIndex] += event.unicode # Enters character into input box
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # For all left mouse clicks
                for i, rect in enumerate(InputBoxes):
                    if rect.collidepoint(event.pos):
                        ActiveIndex = i
                if LoginButton.rect.collidepoint(event.pos): # Login Button Collision
                    UserDetails = validateAdminLogin(Inputs[0], Inputs[1]) # Validates inputs
                    if UserDetails:
                        return adminMenu(UserDetails)
                    else:
                        ErrorMessage = "Invalid AdminID or password. Try again."
                elif ExitButton.rect.collidepoint(event.pos): # Exit Button collision
                    MousePosition = pygame.mouse.get_pos()
                    ExitButton.check_click(MousePosition)
        
        pygame.display.flip()

def createAccount():
        # Initialises fields for customer to input details
    Fields = [
        {"label": "Firstname:", "text": "", "valid": False, "error": ""},
        {"label": "Lastname:", "text": "", "valid": False, "error": ""},
        {"label": "Email:", "text": "", "valid": False, "error": ""},
        {"label": "Password:", "text": "", "valid": False, "error": ""},
        {"label": "Phone Number:", "text": "", "valid": False, "error": ""},
        {"label": "Street:", "text": "", "valid": False, "error": ""},
        {"label": "City:", "text": "", "valid": False, "error": ""},
        {"label": "Postcode:", "text": "", "valid": False, "error": ""},
    ]
    
    ActiveIndex = 0  # Tracks the currently active input field
    message = ""
    MessageColour = (255, 0, 0)
    LastCursorTime = time.time()  # For flashing cursor (start time)
    CursorVisible = True  # Initially, the cursor is visible

    def saveCustDetails():
        # Validate all fields
        for i, field in enumerate(Fields):
            text = field["text"].strip() # Removes any spaces before and after input

            if i == 0:  # Firstname validation
                field["valid"] = text.isalpha() and len(text) > 0
                field["error"] = "" if field["valid"] else "First name must be letters and not blank"
            
            elif i == 1:  # Lastname validation
                field["valid"] = text.isalpha() and len(text) > 0
                field["error"] = "" if field["valid"] else "Last name must be letters and not blank"
            
            elif i == 2:  # Email validation
                text = text.lower()
                field["text"] = text
                field["valid"] = bool(re.match(r"^(?![.])[A-Za-z0-9!#$%&'*+/=?^_`{|}~.-]+(?<![.])@([A-Za-z0-9.-]+)\.([A-Za-z]{2,})$", text))
                field["error"] = "" if field["valid"] else "Invalid email format"
            
            elif i == 3:  # Password validation
                field["valid"] = len(text) >= 8 and any(c.isdigit() for c in text) and any(c.isupper() for c in text)
                field["error"] = "" if field["valid"] else "Password must contain at least 8 characters, one number and one uppercase letter"
            
            elif i == 4:  # Phone validation
                field["valid"] = text.isdigit() and len(text) == 11
                field["error"] = "" if field["valid"] else "Phone number must be 11 digits"

            elif i == 5:  # Street validation
                field["valid"] = len(text) > 0
                field["error"] = "" if field["valid"] else "Street can't be empty"
            
            elif i == 6:  # City validation
                field["valid"] = len(text) > 0
                field["error"] = "" if field["valid"] else "City can't be empty"
            
            elif i == 7:  # Postcode validation
                field["valid"] = bool(re.match(r"^([A-Za-z][A-Ha-hJ-Yj-y]?[0-9][A-Za-z0-9]? ?[0-9][A-Za-z]{2}|[Gg][Ii][Rr] ?0[Aa]{2})$", text))
                field["error"] = "" if field["valid"] else "Postcode is not in a valid format"
                
        # If all fields are valid, save customer data
        if all(field["valid"] for field in Fields):
            customers = User_Detail_Processes.openFile("customers.json")
            if customers == False: # Handles errors returned by User_Detail_Processes.openFile function
                return False, "Error locating customer database.", (255, 0, 0)

            # Check if email is already in use
            EmailInput = Fields[2]["text"].strip()  # Get the email field
            if any(customer["Email"] == EmailInput for customer in customers):
                return False, "Email is already in use.", (255, 0, 0)
        
            # Generate new customer ID
            if customers:  # If there are existing customers in the array
                LastCustID = max(customer["custID"] for customer in customers) # Finds the last custID on the array
                CustID = LastCustID + 1 
            else:
                CustID = 1 # If the array is empty, it makes the new custID = 1

            # Replaces the Password with a hashed version of the password
            for field in Fields:
                if field["label"] == "Password:":
                    PasswordText = field["text"]
                    break
            HashedPassword = User_Detail_Processes.hashPassword(PasswordText)
            for field in Fields:
                if field["label"] == "Password:":
                    field["text"] = HashedPassword
                    break

            # Combine all fields
            CustData = {field["label"][:-1]: field["text"] for field in Fields}
            CustData["custID"] = CustID  # Assign the generated customer ID

            # Append the new customer data to the array
            customers.append(CustData)
            Changes = User_Detail_Processes.closeFile("customers.json", customers)
            if Changes == True:
                return True, "Account Created Successfully!", (0, 200, 0)
            else:
                print("Error saving customer data.")
                return False, "Error saving customer data.", (255, 0, 0) # Handles errors returned by User_Detail_Processes.closeFile function

        return False, "Please fill out all fields correctly.", (255, 0, 0) # If any fields are invalid

    AccountCreated = False  # Flag to track if account has been created
    # Creates a list of pygame rectangles which will be input fields
    InputBoxes = [pygame.Rect(250, 160 + i * 80, 300, 40) for i in range(len(Fields))] 
        
    while True:
        Screen.fill((0, 0, 0))

        # Draws title background
        TitleBgRect = pygame.Rect(0, 0, Width, Height // 15)
        pygame.draw.rect(Screen, (0, 153, 0), TitleBgRect)

        # Renders title
        TitleSurface = TitleFont.render("TBMS", True, (0, 0, 0))
        TitleRect = TitleSurface.get_rect(center=(Width // 2, Height // 25))
        Screen.blit(TitleSurface, TitleRect)
        
        # Displays the name of the screen "Create Account"
        SubtitleSurface = TitleFont.render("Create Account", True, (255, 255, 255))
        Screen.blit(SubtitleSurface, (Width // 2 - SubtitleSurface.get_width() // 2, 80))
        
        # Draws each input box and label
        for i, field in enumerate(Fields):
            LabelSurface = Font.render(field["label"], True, (255, 255, 255))
            Screen.blit(LabelSurface, (250, 100 + i * 80 + 40))  # Label position above the input box
            pygame.draw.rect(Screen, (255, 255, 255), InputBoxes[i], 2)  # Input box
            InputSurface = Font.render(field["text"], True, (255, 255, 255)) # Input surface where the text is displayed
            Screen.blit(InputSurface, (InputBoxes[i].x + 5, InputBoxes[i].y + 5))
            
            # Error message for invalid fields
            if not field["valid"] and field["error"]:
                ErrorSurface = ErrorFont.render(field["error"], True, (255, 0, 0))
                Screen.blit(ErrorSurface, (InputBoxes[i].x + 5, InputBoxes[i].y + 45))

            # Draw the flashing cursor if it's the active field
            if ActiveIndex == i:
                # Determine position of the cursor (where the text is currently)
                TextWidth = Font.size(field["text"])[0]
                CursorX = InputBoxes[i].x + 5 + TextWidth
                CursorY = InputBoxes[i].y + 5

                # Toggle cursor visibility based on time
                if time.time() - LastCursorTime > 0.5:
                    CursorVisible = not CursorVisible
                    LastCursorTime = time.time()

                # Draw the cursor if it's visible
                if CursorVisible:
                    pygame.draw.line(Screen, (255, 255, 255), (CursorX, CursorY), (CursorX, CursorY + 15), 2)
                    
        # Display the message if there is an error or success
        MessageSurface = Font.render(message, True, MessageColour)
        Screen.blit(MessageSurface, (Width // 2 - MessageSurface.get_width() // 2, Height - 120))
        
        # Creates and displays the "Enter" button
        EnterButton = Button("Enter", (Width // 2 - 60, Height - 200, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), saveCustDetails)
        EnterButton.draw(Screen, pygame.mouse.get_pos())
        
        # Creates and displays the "Exit1" button
        ExitButton = Button("Exit", (Width // 2 - 60, Height - 100, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), mainMenu)
        ExitButton.draw(Screen, pygame.mouse.get_pos())
        
        # Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    Fields[ActiveIndex]["text"] = Fields[ActiveIndex]["text"][:-1]  # Remove last character
                elif event.key == pygame.K_RETURN:
                    # Attempt to save details when "Enter" key is pressed
                    valid, message, MessageColour = saveCustDetails()
                    if valid:
                        # Show confirmation of account created and reset fields
                        AccountCreated = True
                        Fields = [{**field, "text": "", "valid": False, "error": ""} for field in Fields]
                    else:
                        MessageColour = (255, 0, 0)
                elif event.key == pygame.K_TAB:
                    # Move to the next field if Tab key pressed (or previous field if Shift + Tab)
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        ActiveIndex = (ActiveIndex - 1) % len(Fields)
                    else:
                        ActiveIndex = (ActiveIndex + 1) % len(Fields)
                else:
                    Fields[ActiveIndex]["text"] += event.unicode  # Add character to the active field

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Detects a mouse click to select a field
                for i, rect in enumerate(InputBoxes):
                    if rect.collidepoint(event.pos):  # Check if the mouse click is inside the box
                        ActiveIndex = i  # Set the clicked box as active
                        break
             # Check if the "Enter" button is clicked
                if EnterButton.rect.collidepoint(event.pos):
                    valid, message, MessageColour = saveCustDetails()
                    if valid:
                        AccountCreated = True
                        Fields = [{**field, "text": "", "valid": False, "error": ""} for field in Fields]
                    else:
                        MessageColour = (255, 0, 0)
                elif ExitButton.rect.collidepoint(event.pos):
                    MousePosition = pygame.mouse.get_pos()
                    ExitButton.check_click(MousePosition)
                    
        # If account is created, show the confirmation message and transition back to the main menu
        if AccountCreated:

            # Transition to the success Screen
            Screen.fill((0, 0, 0))

            # Displays success message
            SuccessMessage = Font.render("Account Created Successfully!", True, (0, 200, 0))
            Screen.blit(SuccessMessage, (Width // 2 - SuccessMessage.get_width() // 2, Height // 2 - 20))

            pygame.display.update()

            # Wait for 2 seconds
            pygame.time.wait(2000)

            # Transition back to the main menu
            break

        pygame.display.update()

def exit():
    pygame.quit()
    sys.exit()

def custMenu(UserDetails):
    # Buttons for the Customer Menu
    buttons = [
        Button("Create Booking", (150, 200, 200, 50), (211, 211, 211), (64, 64, 64), (0, 0, 0), lambda: createBooking(UserDetails)),
        Button("Edit Account Details", (450, 200, 200, 50), (211, 211, 211), (64, 64, 64), (0, 0, 0), lambda: editCustDetails(UserDetails)),
        Button("View My bookings", (150, 300, 200, 50), (211, 211, 211), (64, 64, 64), (0, 0, 0), lambda: viewCustBookings(UserDetails)),
        Button("Logout", (450, 300, 200, 50), (211, 211, 211), (64, 64, 64), (0, 0, 0), lambda: logout()),
        ]
    
    global Width, Height
    running = True
    
    while running:
        Screen.fill((99, 99, 99))  # Screen is filled with grey background
        MousePosition = pygame.mouse.get_pos() # Gets position of the cursor
        
        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                Width, Height = event.w, event.h
                pygame.display.set_mode((Width, Height), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    button.check_click(MousePosition)
                    
        # Draws title background
        TitleBgRect = pygame.Rect(0, 0, Width, Height // 15)
        pygame.draw.rect(Screen, (0, 153, 0), TitleBgRect)

        # Renders title
        TitleSurface = TitleFont.render("TBMS", True, (0, 0, 0))
        TitleRect = TitleSurface.get_rect(center=(Width // 2, Height // 25))
        Screen.blit(TitleSurface, TitleRect)
        
        # Displays the name of the screen "Customer Login"
        SubtitleSurface = TitleFont.render("Customer Menu", True, (255, 255, 255))
        Screen.blit(SubtitleSurface, (Width // 2 - SubtitleSurface.get_width() // 2, 80))
        
        NameSurface = SubtitleFont.render(f"Hello {UserDetails.getFirstname()}!", True, (255, 255, 255))
        Screen.blit(NameSurface, (Width // 2 - NameSurface.get_width() // 2, 130))
        
        # Adjust button positions and sizes dynamically
        buttons[0].rect.update(50, Height // 2 - 80, Width // 2 - 100, 50)
        buttons[1].rect.update(Width // 2 + 50, Height // 2 - 80, Width // 2 - 100, 50)
        buttons[2].rect.update(50, Height // 2 + 20, Width // 2 - 100, 50)
        buttons[3].rect.update(Width // 2 + 50, Height // 2 + 20, Width // 2 - 100, 50)
        
        # Draw buttons
        for button in buttons:
            button.draw(Screen, MousePosition)
    
        # Updates the Screen by redrawing it every iteration
        pygame.display.flip()
        
def createBooking(UserDetails):
     # Initialises fields for customer to input booking details
    Fields = [
        {"label": "Pickup Postcode:", "text": "", "valid": False, "error": ""},
        {"label": "Pickup Address:", "text": "", "valid": False, "error": ""},
        {"label": "Dropoff Postcode:", "text": "", "valid": False, "error": ""},
        {"label": "Dropoff Address:", "text": "", "valid": False, "error": ""},
        {"label": "Date (DD/MM/YYYY):", "text": "", "valid": False, "error": ""},
        {"label": "Time (24hr):", "text": "", "valid": False, "error": ""}
    ]
    
    ActiveIndex = 0  # Tracks the currently active input field
    message = ""
    MessageColour = (255, 0, 0)
    LastCursorTime = time.time()  # For flashing cursor (start time)
    CursorVisible = True  # Initially, the cursor is visible
    
    def bookingOptions(Fields):
        global Width, Height
        
        try:
            Results = Price_Calculator.priceCalculator(Fields[0]["text"], Fields[2]["text"], Fields[5]["text"])
            if Results == False:
                # Fills screen black
                Screen.fill((0, 0, 0))

                # Displays error message
                ErrorMessage = Font.render("Error occured during booking process. Please try again later.", True, (255, 0, 0))
                Screen.blit(ErrorMessage, (Width // 2 - ErrorMessage.get_width() // 2, Height // 2 - 20))

                pygame.display.update()

                # Wait for 2 seconds
                pygame.time.wait(2000)
                # Transition back to the Customer Menu
                custMenu(UserDetails)
            else:
                Four = Results[0]
                Five = Results[1]
                Seven = Results[2]
        except Exception as e:
            print(f"Error running priceCalculator function {e}")   
            # Fills screen black
            Screen.fill((0, 0, 0))

            # Displays error message
            ErrorMessage = Font.render("Error occured during booking process. Please try again later.", True, (255, 0, 0))
            Screen.blit(ErrorMessage, (Width // 2 - ErrorMessage.get_width() // 2, Height // 2 - 20))

            pygame.display.update()

            # Wait for 2 seconds
            pygame.time.wait(2000)
            # Transition back to the Customer Menu
            custMenu(UserDetails)
        # Buttons for the Customer Menu
        buttons = [
            Button(f"1-4 Passenger: £{Four}", (150, 200, 200, 50), (211, 211, 211), (64, 64, 64), (0, 0, 0), action = None),
            Button(f"5-6 Passenger: £{Five}", (450, 200, 200, 50), (211, 211, 211), (64, 64, 64), (0, 0, 0), action = None),
            Button(f"7-8 Passenger: £{Seven}", (150, 300, 200, 50), (211, 211, 211), (64, 64, 64), (0, 0, 0), action = None),
            Button("Cancel", (450, 300, 200, 50), (211, 211, 211), (64, 64, 64), (0, 0, 0), lambda: custMenu(UserDetails)),
            ]
        
        running = True
        
        while running:
            Screen.fill((99, 99, 99))  # Screen is filled with grey background
            MousePosition = pygame.mouse.get_pos() # Gets position of the cursor
            
            # Event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    Width, Height = event.w, event.h
                    pygame.display.set_mode((Width, Height), pygame.RESIZABLE)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if buttons[0].rect.collidepoint(event.pos):
                        return Four, "1-4 Passengers"
                    elif buttons[1].rect.collidepoint(event.pos):
                        return Five, "5-6 Passengers"
                    elif buttons[2].rect.collidepoint(event.pos):
                        return Seven, "7-8 Passengers"
                    elif buttons[3].rect.collidepoint(event.pos):
                        MousePosition = pygame.mouse.get_pos()
                        buttons[3].check_click(MousePosition)
            # Draws title background
            TitleBgRect = pygame.Rect(0, 0, Width, Height // 15)
            pygame.draw.rect(Screen, (0, 153, 0), TitleBgRect)

            # Renders title
            TitleSurface = TitleFont.render("TBMS", True, (0, 0, 0))
            TitleRect = TitleSurface.get_rect(center=(Width // 2, Height // 25))
            Screen.blit(TitleSurface, TitleRect)
            
            # Displays the name of the screen "Taxi Options"
            SubtitleSurface = TitleFont.render("Taxi Options", True, (255, 255, 255))
            Screen.blit(SubtitleSurface, (Width // 2 - SubtitleSurface.get_width() // 2, 80))
            
            # Adjust button positions and sizes dynamically
            buttons[0].rect.update(50, Height // 2 - 80, Width // 2 - 100, 50)
            buttons[1].rect.update(Width // 2 + 50, Height // 2 - 80, Width // 2 - 100, 50)
            buttons[2].rect.update(50, Height // 2 + 20, Width // 2 - 100, 50)
            buttons[3].rect.update(Width // 2 + 50, Height // 2 + 20, Width // 2 - 100, 50)
            
            # Draw buttons
            for button in buttons:
                button.draw(Screen, MousePosition)
        
            # Updates the Screen by redrawing it every iteration
            pygame.display.flip()        
        
    def saveBookingDetails():
        # Validate all fields
        for i, field in enumerate(Fields):
            text = field["text"].strip() # Removes any spaces before and after input

            if i == 0:  # Pickup Postcode validation
                field["valid"] = bool(re.match(r"^([A-Za-z][A-Ha-hJ-Yj-y]?[0-9][A-Za-z0-9]? ?[0-9][A-Za-z]{2}|[Gg][Ii][Rr] ?0[Aa]{2})$", text))
                field["error"] = "" if field["valid"] else "Invalid postcode!"
            
            elif i == 1:  # Pickup Address validation
                field["valid"] = len(text) > 0
                field["error"] = "" if field["valid"] else "Cannot be blank!"
            
            elif i == 2:  # Dropoff Postcode validation
                field["valid"] = bool(re.match(r"^([A-Za-z][A-Ha-hJ-Yj-y]?[0-9][A-Za-z0-9]? ?[0-9][A-Za-z]{2}|[Gg][Ii][Rr] ?0[Aa]{2})$", text))
                field["error"] = "" if field["valid"] else "Invalid postcode!"
            
            elif i == 3:  # Dropoff Address validation
                field["valid"] = len(text) > 0
                field["error"] = "" if field["valid"] else "Cannot be blank!"
            
            elif i == 4:  # Date validation
                Valid, Message = User_Detail_Processes.validateFutureDate(text)
                field["valid"] = Valid
                field["error"] = "" if field["valid"] else Message

            elif i == 5:  # Time validation
                field["valid"] = bool(re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", text))
                field["error"] = "" if field["valid"] else "Time is not valid"
                
        # If all fields are valid, save customer data
        if all(field["valid"] for field in Fields):
            Price, TaxiType = bookingOptions(Fields)
            bookings = User_Detail_Processes.openFile("bookings.json")
            if bookings == False: # Handles errors returned by User_Detail_Processes.openFile function
                return False, "Error locating booking database.", (255, 0, 0)
        
            # Generate new bookingID
            if bookings:  # If there are existing bookings in the array
                LastBookingID = max(booking["bookingID"] for booking in bookings) # Finds the last bookingID on the array
                BookingID = LastBookingID + 1 
            else:
                BookingID = 1 # If the array is empty, it makes the new bookingID = 1

            # Calculate Driver Cut
            Multipliers = User_Detail_Processes.openFile("multipliers.json")
            # Combine all fields 
            BookingData = {field["label"][:-1]: field["text"] for field in Fields}
            BookingData["bookingID"] = BookingID  # Assign the generated customer ID
            BookingData["TaxiType"] = TaxiType
            BookingData["Price"] = Price
            BookingData["Driver Cut"] = Price * (Multipliers["DriverCut"])
            BookingData["Status"] = "Unassigned"
            BookingData["custID"] = UserDetails.getCustID()
            BookingData["driverID"] = "N/A"
            
            # Append the new Booking data to the array
            bookings.append(BookingData)
            Changes = User_Detail_Processes.closeFile("bookings.json", bookings)
            if Changes == True:
                return True, "Booking Created Successfully!", (0, 200, 0)
            else:
                print("Error saving Booking data.")
                return False, "Error saving Booking data.", (255, 0, 0) # Handles errors returned by User_Detail_Processes.closeFile function

        return False, "Please fill out all fields correctly.", (255, 0, 0) # If any fields are invalid

    BookingCreated = False  # Flag to track if Booking has been created
    # Creates a list of pygame rectangles which will be input fields
    InputBoxes = [pygame.Rect(250, 160 + i * 80, 300, 40) for i in range(len(Fields))] 
    running = True    
    while running:
        Screen.fill((0, 0, 0))

        # Draws title background
        TitleBgRect = pygame.Rect(0, 0, Width, Height // 15)
        pygame.draw.rect(Screen, (0, 153, 0), TitleBgRect)

        # Renders title
        TitleSurface = TitleFont.render("TBMS", True, (0, 0, 0))
        TitleRect = TitleSurface.get_rect(center=(Width // 2, Height // 25))
        Screen.blit(TitleSurface, TitleRect)
        
        # Displays the name of the screen "Create Booking"
        SubtitleSurface = TitleFont.render("Create Booking", True, (255, 255, 255))
        Screen.blit(SubtitleSurface, (Width // 2 - SubtitleSurface.get_width() // 2, 80))
        
        # Draws each input box and label
        for i, field in enumerate(Fields):
            LabelSurface = Font.render(field["label"], True, (255, 255, 255))
            Screen.blit(LabelSurface, (250, 100 + i * 80 + 40))  # Label position above the input box
            pygame.draw.rect(Screen, (255, 255, 255), InputBoxes[i], 2)  # Input box
            InputSurface = Font.render(field["text"], True, (255, 255, 255)) # Input surface where the text is displayed
            Screen.blit(InputSurface, (InputBoxes[i].x + 5, InputBoxes[i].y + 5))
            
            # Error message for invalid fields
            if not field["valid"] and field["error"]:
                ErrorSurface = ErrorFont.render(field["error"], True, (255, 0, 0))
                Screen.blit(ErrorSurface, (InputBoxes[i].x + 5, InputBoxes[i].y + 45))
            # Draw the flashing cursor if it's the active field
            if ActiveIndex == i:
                # Determine position of the cursor (where the text is currently)
                TextWidth = Font.size(field["text"])[0]
                CursorX = InputBoxes[i].x + 5 + TextWidth
                CursorY = InputBoxes[i].y + 5

                # Toggle cursor visibility based on time
                if time.time() - LastCursorTime > 0.5:
                    CursorVisible = not CursorVisible
                    LastCursorTime = time.time()

                # Draw the cursor if it's visible
                if CursorVisible:
                    pygame.draw.line(Screen, (255, 255, 255), (CursorX, CursorY), (CursorX, CursorY + 15), 2)

        # Display the message if there is an error or success
        MessageSurface = Font.render(message, True, MessageColour)
        Screen.blit(MessageSurface, (Width // 2 - MessageSurface.get_width() // 2, Height - 120))
        
        # Creates and displays the "Enter" button
        EnterButton = Button("Enter", (Width // 2 - 60, Height - 200, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), saveBookingDetails)
        EnterButton.draw(Screen, pygame.mouse.get_pos())
        
        # Creates and displays the "Exit" button
        ExitButton = Button("Exit", (Width // 2 - 60, Height - 100, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), lambda: custMenu(UserDetails))
        ExitButton.draw(Screen, pygame.mouse.get_pos())
        
        # Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    Fields[ActiveIndex]["text"] = Fields[ActiveIndex]["text"][:-1]  # Remove last character
                elif event.key == pygame.K_RETURN:
                    # Attempt to save details when "Enter" key is pressed
                    valid, message, MessageColour = saveBookingDetails()
                    if valid:
                        # Show confirmation of account created and reset fields
                        BookingCreated = True
                        Fields = [{**field, "text": "", "valid": False, "error": ""} for field in Fields]
                    else:
                        MessageColour = (255, 0, 0)
                elif event.key == pygame.K_TAB:
                    # Move to the next field if Tab key pressed (or previous field if Shift + Tab)
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        ActiveIndex = (ActiveIndex - 1) % len(Fields)
                    else:
                        ActiveIndex = (ActiveIndex + 1) % len(Fields)
                else:
                    Fields[ActiveIndex]["text"] += event.unicode  # Add character to the active field

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Detects a mouse click to select a field
                for i, rect in enumerate(InputBoxes):
                    if rect.collidepoint(event.pos):  # Check if the mouse click is inside the box
                        ActiveIndex = i  # Set the clicked box as active
                        break
             # Check if the "Enter" button is clicked
                if EnterButton.rect.collidepoint(event.pos):
                    valid, message, MessageColour = saveBookingDetails()
                    if valid:
                        BookingCreated = True
                        Fields = [{**field, "text": "", "valid": False, "error": ""} for field in Fields]
                    else:
                        MessageColour = (255, 0, 0)
                elif ExitButton.rect.collidepoint(event.pos):
                    MousePosition = pygame.mouse.get_pos()
                    ExitButton.check_click(MousePosition)
                    
        # If account is created, show the confirmation message and transition back to the customer menu
        if BookingCreated:

            # Transition to the success Screen
            Screen.fill((0, 0, 0))

            # Displays success message
            SuccessMessage = Font.render("Booking Created Successfully!", True, (0, 200, 0))
            Screen.blit(SuccessMessage, (Width // 2 - SuccessMessage.get_width() // 2, Height // 2 - 20))

            pygame.display.update()

            # Wait for 2 seconds
            pygame.time.wait(2000)
            running = False
            # Transition back to the Customer Menu
            custMenu(UserDetails)

        pygame.display.update()
    
def editCustDetails(UserDetails):
    options = [
        "Firstname", 
        "Lastname", 
        "Password", 
        "Phone Number", 
        "Street", "City", "Postcode"
    ]
    message = ""
    MessageColour = (255, 0, 0)

    # Runs when user data is successfully appended
    def displaySuccessMessage(successMessage):
        Screen.fill((0, 0, 0))
        SuccessSurface = TitleFont.render(successMessage, True, (0, 255, 0))
        Screen.blit(SuccessSurface, (Width // 2 - SuccessSurface.get_width() // 2, Height // 2 - 20))
        pygame.display.flip()
        pygame.time.wait(2000) # Waits two seconds before returning to customer menu
        custMenu(UserDetails)

    # Input screen that comes after user clicks on an option button.
    def getInputScreen(Label, validationFunction, updateKey):
        InputText = ""
        active = True
        nonlocal message, MessageColour
        LastCursorTime = time.time()  # To track the blink timing
        CursorVisible = True  # To toggle caret visibility
    
        while active:
            Screen.fill((0, 0, 0))
            # Draws title background
            TitleBgRect = pygame.Rect(0, 0, Width, Height // 15)
            pygame.draw.rect(Screen, (0, 153, 0), TitleBgRect)
            # Renders title
            TitleSurface = TitleFont.render("TBMS", True, (0, 0, 0))
            TitleRect = TitleSurface.get_rect(center=(Width // 2, Height // 25))
            Screen.blit(TitleSurface, TitleRect)
            # The screen subtitle is the chosen option
            SubtitleSurface = TitleFont.render(f"Change {Label}", True, (255, 255, 255))
            Screen.blit(SubtitleSurface, (Width // 2 - SubtitleSurface.get_width() // 2, 80))

            InputBox = pygame.Rect(250, 200, 300, 40)
            pygame.draw.rect(Screen, (255, 255, 255), InputBox, 2)
            # Creates input box for the user to enter input for selected option
            InputSurface = Font.render(InputText, True, (255, 255, 255))
            Screen.blit(InputSurface, (InputBox.x + 5, InputBox.y + 10))

            # Toggle cursor visibility based on time
            if time.time() - LastCursorTime > 0.5:
                CursorVisible = not CursorVisible
                LastCursorTime = time.time()

            if CursorVisible:
                CursorX = InputBox.x + 5 + Font.size(InputText)[0]
                CursorY = InputBox.y + 10
                pygame.draw.line(Screen, (255, 255, 255), (CursorX, CursorY), (CursorX, CursorY + 20), 2)

            MessageSurface = Font.render(message, True, MessageColour)
            if Label == "Password":
                Screen.blit(MessageSurface, (Width // 2 - 250, 400))
            else:
                Screen.blit(MessageSurface, (Width // 2 - 80, 400))

            EnterButton = Button("Enter", (Width // 2 - 60, Height - 200, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), action=None)
            ExitButton = Button("Exit", (Width // 2 - 60, Height - 100, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), lambda: editCustDetails(UserDetails))

            EnterButton.draw(Screen, pygame.mouse.get_pos())
            ExitButton.draw(Screen, pygame.mouse.get_pos())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: # validates user input
                        valid, errorMsg = validationFunction(InputText)
                        if valid:
                            if updateKey == 'Password': # Hashes the input if the Password is being updated
                                InputText = User_Detail_Processes.hashPassword(InputText)
                            User_Detail_Processes.updateCustomerDetails(UserDetails, updateKey, InputText)
                            if updateKey == 'Firstname':
                                UserDetails.firstname = InputText
                            displaySuccessMessage(f"{Label} updated successfully!")
                            return
                        else:
                            message, MessageColour = errorMsg, (255, 0, 0)
                    elif event.key == pygame.K_BACKSPACE: 
                        InputText = InputText[:-1]
                    else:
                        InputText += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if EnterButton.rect.collidepoint(event.pos): # validates user input
                        valid, errorMsg = validationFunction(InputText)
                        if valid:
                            if updateKey == 'Password': # Hashes the input if the Password is being updated
                                InputText = User_Detail_Processes.hashPassword(InputText)
                            User_Detail_Processes.updateCustomerDetails(UserDetails, updateKey, InputText)
                            if updateKey == 'Firstname':
                                UserDetails.firstname = InputText
                            displaySuccessMessage(f"{Label} updated successfully!")
                            return
                        else:
                            message, MessageColour = errorMsg, (255, 0, 0)
                    elif ExitButton.rect.collidepoint(event.pos):
                        ExitButton.action()

            pygame.display.flip()

    def validateText(InputText):
        return (len(InputText.strip()) > 0, "Field cannot be empty")
    def validatePhone(InputText):
        return (InputText.isdigit() and len(InputText) == 11, "Invalid Phone Number")
    def validatePasswordField(InputText):
        return (len(InputText) >= 8 and any(c.isdigit() for c in InputText) and any(c.isupper() for c in InputText), "Password must be at least 8 characters with a number and uppercase letter")
    def validatePostcode(InputText):
        return (bool(re.match (r"^([A-Za-z][A-Ha-hJ-Yj-y]?[0-9][A-Za-z0-9]? ?[0-9][A-Za-z]{2}|[Gg][Ii][Rr] ?0[Aa]{2})$", InputText)), "Invalid postcode format")

    validators = {
        "Firstname": validateText,
        "Lastname": validateText,
        "Password": validatePasswordField,
        "Phone Number": validatePhone,
        "Street": validateText,
        "City": validateText,
        "Postcode": validatePostcode,
    }

    while True:
        Screen.fill((0, 0, 0))
        
        # Draws title background
        TitleBgRect = pygame.Rect(0, 0, Width, Height // 15)
        pygame.draw.rect(Screen, (0, 153, 0), TitleBgRect)
        
        # Renders title
        TitleSurface = TitleFont.render("TBMS", True, (0, 0, 0))
        TitleRect = TitleSurface.get_rect(center=(Width // 2, Height // 25))
        Screen.blit(TitleSurface, TitleRect)
                
        SubtitleSurface = TitleFont.render("Edit Customer Details", True, (255, 255, 255))
        Screen.blit(SubtitleSurface, (Width // 2 - SubtitleSurface.get_width() // 2, 80))

        Buttons = []
        for i, option in enumerate(options):
            Buttons.append(Button(option, (250, 160 + i * 60, 300, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), None))
            Buttons[i].draw(Screen, pygame.mouse.get_pos())

        MessageSurface = Font.render(message, True, MessageColour)
        Screen.blit(MessageSurface, (250, 700))

        ExitButton = Button("Exit", (Width // 2 - 60, Height - 100, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), lambda: custMenu(UserDetails))
        ExitButton.draw(Screen, pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, button in enumerate(Buttons):
                    if button.rect.collidepoint(event.pos):
                        getInputScreen(options[i], validators[options[i]], options[i])
                if ExitButton.rect.collidepoint(event.pos):
                    ExitButton.action()
                    break
        pygame.display.flip()

def viewCustBookings(UserDetails):
    def getDriverDetails(DriverID):
        Drivers = User_Detail_Processes.openFile("drivers.json")
        for Driver in Drivers:
            if Driver["driverID"] == DriverID:
                return Driver
        return None

    def getCustomerBookings(Future):
        Bookings = User_Detail_Processes.openFile("bookings.json")
        CustomerBookings = []
        CurrentDate = datetime.datetime.now()

        for Booking in Bookings:
            if Booking["custID"] == UserDetails.getCustID():
                BookingDateTime = datetime.datetime.strptime(
                    f"{Booking['Date (DD/MM/YYYY)']} {Booking['Time (24hr)']}", "%d/%m/%Y %H:%M"
                )
                if (Future and BookingDateTime >= CurrentDate) or (not Future and BookingDateTime < CurrentDate):
                    CustomerBookings.append(Booking)
        return CustomerBookings

    def displayBookingDetails(Booking, Future):
        DriverDetails = None
        if Booking["driverID"] != "N/A":
            DriverDetails = getDriverDetails(Booking["driverID"])

        Viewing = True
        while Viewing:
            Screen.fill((0, 0, 0))
            MousePosition = pygame.mouse.get_pos()
            Details = [
                f"Pickup Postcode: {Booking['Pickup Postcode']}",
                f"Pickup Address: {Booking['Pickup Address']}",
                f"Dropoff Postcode: {Booking['Dropoff Postcode']}",
                f"Dropoff Address: {Booking['Dropoff Address']}",
                f"Date: {Booking['Date (DD/MM/YYYY)']}",
                f"Time: {Booking['Time (24hr)']}",
                f"Taxi Type: {Booking['TaxiType']}",
                f"Price: £{Booking['Price']}",
                f"Status: {Booking['Status']}"
            ]
            if DriverDetails:
                Details.extend([
                    f"Driver: {DriverDetails['Firstname']} {DriverDetails['Lastname']}",
                    f"Car Reg: {DriverDetails['Car Reg']}",
                    f"Car Model: {DriverDetails['Car Model']}",
                    f"Phone: {DriverDetails['Phone Number']}"
                ])

            for I, Line in enumerate(Details):
                DetailSurface = Font.render(Line, True, (255, 255, 255))
                Screen.blit(DetailSurface, (50, 50 + I * 30))

            ExitButton = Button("Exit", (Width // 2 - 60, Height - 100, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), lambda: setViewingFalse())
            ExitButton.draw(Screen, MousePosition)
            # Show "Cancel Booking" button only if it's a future booking
            if Future and Booking["Status"] not in ["Cancelled", "Completed"]:
                CancelButton = Button("Cancel Booking", (Width // 2 - 100, Height - 150, 200, 40), (200, 0, 0), (255, 0, 0), (255, 255, 255), lambda: confirmCancelBooking(Booking))
                CancelButton.draw(Screen, MousePosition)
            
            def setViewingFalse():
                nonlocal Viewing
                Viewing = False
            
            def confirmCancelBooking(Booking):
                Confirmation = showConfirmationDialog("Are you sure you want to cancel this booking?")
                if Confirmation:  
                    # Load all bookings
                    AllBookings = User_Detail_Processes.openFile("bookings.json")
                    print(AllBookings)
                    for B in AllBookings:
                        if B["custID"] == Booking["custID"] and B["Date (DD/MM/YYYY)"] == Booking["Date (DD/MM/YYYY)"] and B["Time (24hr)"] == Booking["Time (24hr)"]:
                            B["Status"] = "Cancelled"
                            break
                    # Save the updated bookings
                    User_Detail_Processes.closeFile("bookings.json", AllBookings)
                # Refresh the screen after cancellation and return to the customer menu
                setViewingFalse()
                viewCustBookings(UserDetails) 

            for Event in pygame.event.get(): # Event handling
                if Event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif Event.type == pygame.MOUSEBUTTONDOWN and Event.button == 1:
                    if ExitButton.rect.collidepoint(Event.pos):
                        setViewingFalse()
                    if Future and Booking["Status"] not in ["Cancelled", "Completed"]:
                        if CancelButton.rect.collidepoint(Event.pos):
                            CancelButton.action()
            pygame.display.flip()

    def displayBookings(Future):
        Bookings = getCustomerBookings(Future)
        Running = True
        while Running:
            Screen.fill((0, 0, 0))
            MousePosition = pygame.mouse.get_pos()
            # Draws title background
            TitleBgRect = pygame.Rect(0, 0, Width, Height // 15)
            pygame.draw.rect(Screen, (0, 153, 0), TitleBgRect)
            # Renders title
            TitleSurface = TitleFont.render("TBMS", True, (0, 0, 0))
            TitleRect = TitleSurface.get_rect(center=(Width // 2, Height // 25))
            Screen.blit(TitleSurface, TitleRect)
            SubtitleSurface = TitleFont.render("Bookings", True, (255, 255, 255))
            Screen.blit(SubtitleSurface, (Width // 2 - SubtitleSurface.get_width() // 2, 80))

            if not Bookings: # If there are no bookings returned, it presents the message below
                NoBookingsText = "No bookings found." if Future else "No past bookings found."
                NoBookingsSurface = TitleFont.render(NoBookingsText, True, (255, 0, 0))
                Screen.blit(NoBookingsSurface, (Width // 2 - NoBookingsSurface.get_width() // 2, Height // 2))
            else:
                BookingButtons = []
                for I, Booking in enumerate(Bookings):
                    RowText = f"{Booking['Pickup Postcode']} to {Booking['Dropoff Postcode']} | {Booking['Time (24hr)']} | {Booking['Date (DD/MM/YYYY)']}"
                    RowButton = Button(RowText, ((Width - 500) // 2, 150 + I * 50, 500, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), lambda b=Booking: displayBookingDetails(b, Future))
                    RowButton.draw(Screen, MousePosition)
                    BookingButtons.append(RowButton)
            ExitButton = Button("Exit", (Width // 2 - 60, Height - 100, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), lambda: viewCustBookings(UserDetails))
            ExitButton.draw(Screen, MousePosition)

            for Event in pygame.event.get(): # Event handler
                if Event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif Event.type == pygame.MOUSEBUTTONDOWN and Event.button == 1:
                    if Bookings:
                        for RowButton in BookingButtons:
                            if RowButton.rect.collidepoint(Event.pos):
                                RowButton.action()
                    if ExitButton.rect.collidepoint(Event.pos):
                        viewCustBookings(UserDetails)
            pygame.display.flip()

    def showConfirmationDialog(Message):
        Running = True
        while Running:
            Screen.fill((0, 0, 0))

            ConfirmationSurface = Font.render(Message, True, (255, 255, 255))
            Screen.blit(ConfirmationSurface, (Width // 2 - ConfirmationSurface.get_width() // 2, Height // 2 - 50))

            YesButton = Button("Yes", 
                               (Width // 2 - 120, Height // 2 + 20, 100, 50), (0, 153, 0), (0, 200, 0), (255, 255, 255), lambda: setRunningFalse(True))
            NoButton = Button("No", (Width // 2 + 20, Height // 2 + 20, 100, 50), (200, 0, 0), (255, 0, 0), (255, 255, 255), lambda: setRunningFalse(False))

            MousePosition = pygame.mouse.get_pos()
            YesButton.draw(Screen, MousePosition)
            NoButton.draw(Screen, MousePosition)

            for Event in pygame.event.get():
                if Event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif Event.type == pygame.MOUSEBUTTONDOWN and Event.button == 1:
                    if YesButton.rect.collidepoint(Event.pos):
                        Running = False
                        return True
                    elif NoButton.rect.collidepoint(Event.pos):
                        Running = False
                        return False

            pygame.display.flip()
    
    def setRunningFalse():
            nonlocal Running
            Running = False
            
    Running = True
    while Running:
        Screen.fill((0, 0, 0))
        MousePosition = pygame.mouse.get_pos()
        # Draws title background
        TitleBgRect = pygame.Rect(0, 0, Width, Height // 15)
        pygame.draw.rect(Screen, (0, 153, 0), TitleBgRect)
        # Renders title
        TitleSurface = TitleFont.render("TBMS", True, (0, 0, 0))
        TitleRect = TitleSurface.get_rect(center=(Width // 2, Height // 25))
        Screen.blit(TitleSurface, TitleRect)
        
        # Displays the name of the screen "View Your Bookings"
        SubtitleSurface = TitleFont.render("View Your Bookings", True, (255, 255, 255))
        Screen.blit(SubtitleSurface, (Width // 2 - SubtitleSurface.get_width() // 2, 80))
        # Array containing all the buttons required for this screen
        Buttons = [Button("Future Bookings", 
                          ((Width // 2) - 220, 200, 200, 50), (99, 99, 99), (64, 64, 64), (255, 255, 255), 
                          lambda: displayBookings(True)), 
                   Button("Past Bookings", 
                          ((Width // 2) + 20, 200, 200, 50), (99, 99, 99), (64, 64, 64), (255, 255, 255), 
                          lambda: displayBookings(False)),
                   Button("Exit", 
                          (Width // 2 - 60, Height - 100, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), 
                          lambda: custMenu(UserDetails))]
        for button in Buttons: # Draws each button within Buttons array
            button.draw(Screen, MousePosition)
            
        for Event in pygame.event.get(): # Event handler
            if Event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif Event.type == pygame.MOUSEBUTTONDOWN and Event.button == 1:
                for button in Buttons:
                    button.check_click(MousePosition)
        pygame.display.flip()
    
def logout():
    # Buttons for the Main menu
    LogoutButton = Button("Logout", (150, 200, 200, 50), (211, 211, 211), (64, 64, 64), (0, 0, 0), mainMenu)
    BackButton = Button("Back", (450, 200, 200, 50), (211, 211, 211), (64, 64, 64), (0, 0, 0), action=None)
    global Width, Height

    running = True
    while running:
        Screen.fill((0, 0, 0)) # Screen is filled with Black background
        MousePosition = pygame.mouse.get_pos() # Gets position of the cursor

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                Width, Height = event.w, event.h
                pygame.display.set_mode((Width, Height), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if BackButton.rect.collidepoint(event.pos):
                    running = False
                elif LogoutButton.rect.collidepoint(event.pos):
                    MousePosition = pygame.mouse.get_pos()
                    LogoutButton.check_click(MousePosition)
                
        # Draws title background
        TitleBgRect = pygame.Rect(0, 0, Width, Height // 15)
        pygame.draw.rect(Screen, (0, 153, 0), TitleBgRect)

        # Renders title
        TitleSurface = TitleFont.render("TBMS", True, (0, 0, 0))
        TitleRect = TitleSurface.get_rect(center=(Width // 2, Height // 25))
        Screen.blit(TitleSurface, TitleRect)

        # Renders subtitle
        SubtitleSurface = SubtitleFont.render("Are you sure you would like to logout?", True, (255, 255, 255))
        SubtitleRect = SubtitleSurface.get_rect(center=(Width // 2, Height // 10))
        Screen.blit(SubtitleSurface, SubtitleRect)    
        
        # Adjust button positions and sizes dynamically
        LogoutButton.rect.update(50, Height // 2 - 80, Width // 2 - 100, 50)
        BackButton.rect.update(Width // 2 + 50, Height // 2 - 80, Width // 2 - 100, 50)
        # Draw buttons
        LogoutButton.draw(Screen, MousePosition)
        BackButton.draw(Screen, MousePosition)
        # Updates the Screen by redrawing it every iteration
        pygame.display.flip()
            
def adminMenu(UserDetails):
    # Buttons for the Administrator Menu
    buttons = [
        Button("View Issues", (150, 200, 200, 50), (211, 211, 211), (64, 64, 64), (0, 0, 0), lambda: viewReportedIssues(UserDetails)),
        Button("Edit User Details", (450, 200, 200, 50), (211, 211, 211), (64, 64, 64), (0, 0, 0), lambda: editUserDetails(UserDetails)),
        Button("View all bookings", (150, 300, 200, 50), (211, 211, 211), (64, 64, 64), (0, 0, 0), lambda: allBookings(UserDetails)),
        Button("Alter Pricing", (450, 300, 200, 50), (211, 211, 211), (64, 64, 64), (0, 0, 0), lambda: alterPricing(UserDetails)),
        Button("Logout", (300, 100, 250, 50), (211, 211, 211), (64, 64, 64), (0, 0, 0), lambda: logout()),
        ]
    
    global Width, Height
    running = True 
    while running:
        Screen.fill((99, 99, 99))  # Screen is filled with grey background
        MousePosition = pygame.mouse.get_pos() # Gets position of the cursor
        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                Width, Height = event.w, event.h
                pygame.display.set_mode((Width, Height), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    button.check_click(MousePosition)     
        # Draws title background
        TitleBgRect = pygame.Rect(0, 0, Width, Height // 15)
        pygame.draw.rect(Screen, (0, 153, 0), TitleBgRect)
        # Renders title
        TitleSurface = TitleFont.render("TBMS", True, (0, 0, 0))
        TitleRect = TitleSurface.get_rect(center=(Width // 2, Height // 25))
        Screen.blit(TitleSurface, TitleRect)
        # Displays the name of the screen "Administrator Menu"
        SubtitleSurface = TitleFont.render("Administrator Menu", True, (255, 255, 255))
        Screen.blit(SubtitleSurface, (Width // 2 - SubtitleSurface.get_width() // 2, 80))
        NameSurface = SubtitleFont.render(f"Hello {UserDetails.getFirstname()}!", True, (255, 255, 255))
        Screen.blit(NameSurface, (Width // 2 - NameSurface.get_width() // 2, 130))
        
        # Adjust button positions and sizes dynamically
        buttons[0].rect.update(50, Height // 2 - 80, Width // 2 - 100, 50)
        buttons[1].rect.update(Width // 2 + 50, Height // 2 - 80, Width // 2 - 100, 50)
        buttons[2].rect.update(50, Height // 2 + 20, Width // 2 - 100, 50)
        buttons[3].rect.update(Width // 2 + 50, Height // 2 + 20, Width // 2 - 100, 50)
        buttons[4].rect.update(Width // 2 - (Width // 5), Height // 2 + 120, Width // 2 - 100, 50)
        # Draw buttons
        for button in buttons:
            button.draw(Screen, MousePosition)
        # Updates the Screen by redrawing it every iteration
        pygame.display.flip()

def allBookings(UserDetails):
    print("View All Bookings button clicked...")

def viewReportedIssues(UserDetails):
    print("View Reported Issues button clicked...")
    
def alterPricing(UserDetails):
    # Array containing all the alterable multipliers
    options = ["1-4 Passenger", "5-6 Passenger", "7-8 Passenger", "Night", "DriverCut"]
    message = ""
    MessageColour = (255, 0, 0)

    def displaySuccessMessage(successMessage): 
        Screen.fill((0, 0, 0))
        SuccessSurface = TitleFont.render(successMessage, True, (0, 255, 0))
        Screen.blit(SuccessSurface, (Width // 2 - SuccessSurface.get_width() // 2, Height // 2 - 20))
        pygame.display.flip()
        pygame.time.wait(2000)
        adminMenu(UserDetails)

    def getInputScreen(Label):
        InputText = ""
        active = True
        nonlocal message, MessageColour
        LastCursorTime = time.time()  # To track the blink timing
        CursorVisible = True  # To toggle caret visibility
        while active:
            Screen.fill((0, 0, 0))
            SubtitleSurface = TitleFont.render(f"Change {Label}", True, (255, 255, 255))
            Screen.blit(SubtitleSurface, (Width // 2 - SubtitleSurface.get_width() // 2, 80))
            InputBox = pygame.Rect(250, 200, 300, 40) # Creates input box for the new multiplier
            pygame.draw.rect(Screen, (255, 255, 255), InputBox, 2)
            InputSurface = Font.render(InputText, True, (255, 255, 255))
            Screen.blit(InputSurface, (InputBox.x + 5, InputBox.y + 10))
            # Toggle cursor visibility based on time
            if time.time() - LastCursorTime > 0.5:
                CursorVisible = not CursorVisible
                LastCursorTime = time.time()
            if CursorVisible:
                CursorX = InputBox.x + 5 + Font.size(InputText)[0]
                CursorY = InputBox.y + 10
                pygame.draw.line(Screen, (255, 255, 255), (CursorX, CursorY), (CursorX, CursorY + 20), 2)

            MessageSurface = Font.render(message, True, MessageColour)
            Screen.blit(MessageSurface, (250, 400))
            # Submits user input
            EnterButton = Button("Enter", (Width // 2 - 60, Height - 200, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), None)
            ExitButton = Button("Exit", (Width // 2 - 60, Height - 100, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), action=None)
            EnterButton.draw(Screen, pygame.mouse.get_pos())
            ExitButton.draw(Screen, pygame.mouse.get_pos())

            for event in pygame.event.get(): # Event Handler
                if event.type == pygame.QUIT:
                    active = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: # Validates user input 
                        valid, errorMsg = validateFloat(InputText)
                        if valid: # Updates multipliers and displays success message
                            User_Detail_Processes.updateMultipliers(Label, InputText)
                            displaySuccessMessage(f"Multiplier updated successfully!")
                            message = ""
                            return
                        else: # Display's error message if invalid input
                            message, MessageColour = errorMsg, (255, 0, 0)
                    elif event.key == pygame.K_BACKSPACE:
                            InputText = InputText[:-1]
                    else:
                        InputText += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if EnterButton.rect.collidepoint(event.pos): # Validates user input 
                        valid, errorMsg = validateFloat(InputText)
                        if valid: # Updates multipliers and displays success message
                            User_Detail_Processes.updateMultipliers(Label, InputText)
                            displaySuccessMessage(f"Multiplier updated successfully!")
                            message = ""
                            return
                        else: # Display's error message if invalid input
                            message, MessageColour = errorMsg, (255, 0, 0)
                    elif ExitButton.rect.collidepoint(event.pos):
                        message = ""
                        active = False
            pygame.display.flip()

    def validateFloat(InputText):
        try:
            Value = float(InputText)  # Attempt to convert to float
            return ((Value >= 0), "Cannot be negative")
        except ValueError:
             # Return False if value is not a float
            return (False , "Has to be a decimal value") 
        
    while True:
        Screen.fill((0, 0, 0))
        # Draws title background
        TitleBgRect = pygame.Rect(0, 0, Width, Height // 15)
        pygame.draw.rect(Screen, (0, 153, 0), TitleBgRect)
        # Renders title
        TitleSurface = TitleFont.render("TBMS", True, (0, 0, 0))
        TitleRect = TitleSurface.get_rect(center=(Width // 2, Height // 25))
        Screen.blit(TitleSurface, TitleRect)  
        SubtitleSurface = TitleFont.render("Edit Multpliers", True, (255, 255, 255))
        Screen.blit(SubtitleSurface, (Width // 2 - SubtitleSurface.get_width() // 2, 80))

        Buttons = [] # Array that will hold buttons for all possible multipliers
        for i, option in enumerate(options):
            Buttons.append(Button(option, (250, 160 + i * 60, 300, 40), 
                                  (99, 99, 99), (64, 64, 64), (255, 255, 255), None))
            Buttons[i].draw(Screen, pygame.mouse.get_pos())
            
        MessageSurface = Font.render(message, True, MessageColour)
        Screen.blit(MessageSurface, (250, 700)) # Display's any error messages (or others)
        
        ExitButton = Button("Exit", (Width // 2 - 60, Height - 100, 120, 40), 
                            (99, 99, 99), (64, 64, 64), (255, 255, 255), 
                            lambda: adminMenu(UserDetails))
        ExitButton.draw(Screen, pygame.mouse.get_pos())
        for event in pygame.event.get(): # Event handler
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, button in enumerate(Buttons):
                    if button.rect.collidepoint(event.pos): 
                        # Displays input screen for selected multiplier
                        getInputScreen(options[i])
                if ExitButton.rect.collidepoint(event.pos):
                    ExitButton.action()
        pygame.display.flip()
   
def editUserDetails(UserDetails):
    def checkUserID(UserID, UserType):
        try:
            int(UserID)
        except Exception:
            return False, "Invalid UserID entered"
        User = User_Detail_Processes.searchUser(UserType, int(UserID))
        if User == False:
            return False, "Invalid UserID entered"
        else:
            return True, User
    def getUserInput(UserType):
        ErrorMessage = ""
        InputText = ""
        active = True
        LastCursorTime = time.time()
        CursorVisible = True
        
        while active:
            Screen.fill((0, 0, 0))
            TitleBgRect = pygame.Rect(0, 0, Width, Height // 15) # Draws title background 
            pygame.draw.rect(Screen, (0, 153, 0), TitleBgRect)
            # Renders title
            TitleSurface = TitleFont.render("TBMS", True, (0, 0, 0))
            TitleRect = TitleSurface.get_rect(center=(Width // 2, Height // 25))
            Screen.blit(TitleSurface, TitleRect)
            SubtitleSurface = TitleFont.render("Enter User ID:", True, (255, 255, 255))
            Screen.blit(SubtitleSurface, (Width // 2 - SubtitleSurface.get_width() // 2, 80))
            
            InputBox = pygame.Rect(250, 200, 300, 40) # Renders input box and input surface
            pygame.draw.rect(Screen, (255, 255, 255), InputBox, 2)
            InputSurface = Font.render(InputText, True, (255, 255, 255))
            Screen.blit(InputSurface, (InputBox.x + 5, InputBox.y + 10))
            
            if ErrorMessage: # Error message is displayed (if there is a false input)
                ErrorSurface = Font.render(ErrorMessage, True, (255, 0, 0))
                Screen.blit(ErrorSurface, (Width // 2 - ErrorSurface.get_width() // 2, 320))
            
            # Creates and displays the "Enter" button
            EnterButton = Button("Enter", (Width // 2 - 60, Height - 200, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), None)
            EnterButton.draw(Screen, pygame.mouse.get_pos())
            # Creates and displays the "Exit" button
            ExitButton = Button("Exit", (Width // 2 - 60, Height - 100, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), lambda: editUserDetails(UserDetails))
            ExitButton.draw(Screen, pygame.mouse.get_pos()) 
        
            if time.time() - LastCursorTime > 0.5: # Creates Navigator Caret
                CursorVisible = not CursorVisible
                LastCursorTime = time.time()
            if CursorVisible:
                CursorX = InputBox.x + 5 + Font.size(InputText)[0]
                CursorY = InputBox.y + 10
                pygame.draw.line(Screen, (255, 255, 255), (CursorX, CursorY), (CursorX, CursorY + 20), 2)
            
            for event in pygame.event.get(): # Event Hanlder
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: # Checks if user input is valid
                        Valid, User = checkUserID(InputText.strip(), UserType)
                        if Valid: # Directs user to the correct UserType section
                             editAllCustDetails(User) if UserType == "customers" else editDriverDetails(User)
                        else:
                            ErrorMessage = User
                    elif event.key == pygame.K_BACKSPACE:
                        InputText = InputText[:-1]
                    else:
                        InputText += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if ExitButton.rect.collidepoint(event.pos): # Exit Button collision
                        MousePosition = pygame.mouse.get_pos()
                        ExitButton.check_click(MousePosition)
                    elif EnterButton.rect.collidepoint(event.pos): # Checks if user input is valid
                        Valid, User = checkUserID(InputText.strip(), UserType)
                        if Valid: # Directs user to the correct UserType section
                             editAllCustDetails(User) if UserType == "customers" else editDriverDetails(User)
                        else:
                            ErrorMessage = User
            pygame.display.flip()
    
    UserType = None
    while UserType not in ["customers", "drivers"]:
        Screen.fill((0, 0, 0))
        # Draws title background
        TitleBgRect = pygame.Rect(0, 0, Width, Height // 15)
        pygame.draw.rect(Screen, (0, 153, 0), TitleBgRect)
        # Renders title
        TitleSurface = TitleFont.render("TBMS", True, (0, 0, 0))
        TitleRect = TitleSurface.get_rect(center=(Width // 2, Height // 25))
        Screen.blit(TitleSurface, TitleRect)
        SubtitleSurface = TitleFont.render("Choose User Type:", True, (255, 255, 255))
        Screen.blit(SubtitleSurface, (Width // 2 - SubtitleSurface.get_width() // 2, 80))
        # Creates and displays the "Customer" button
        CustomerButton = Button("Customer", (250, 200, 300, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), action=None)
        CustomerButton.draw(Screen, pygame.mouse.get_pos())
        # Creates and displays the "Driver" button
        DriverButton = Button("Driver", (250, 300, 300, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), action=None)
        DriverButton.draw(Screen, pygame.mouse.get_pos())
        # Creates and displays the "Exit" button
        ExitButton = Button("Exit", (Width // 2 - 60, Height - 100, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), 
                            lambda: adminMenu(UserDetails))
        ExitButton.draw(Screen, pygame.mouse.get_pos()) 
        
        for event in pygame.event.get(): # Event Handler
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if CustomerButton.rect.collidepoint(event.pos): # Checks usertype selected
                    UserType = "customers"
                elif DriverButton.rect.collidepoint(event.pos):
                    UserType = "drivers"
                elif ExitButton.rect.collidepoint(event.pos): # Exit Button collision
                    MousePosition = pygame.mouse.get_pos()
                    ExitButton.check_click(MousePosition)
        pygame.display.flip() 
    getUserInput(UserType)
        
def editAllCustDetails(UserDetails):
    options = ["Firstname", "Lastname", "Email", "Password", "Phone Number", "Street", "City", "Postcode"]
    message = ""
    MessageColour = (255, 0, 0)

    def getInputScreen(Label, validationFunction, updateKey):
        InputText = ""
        active = True
        nonlocal message, MessageColour
        LastCursorTime = time.time()  # To track the blink timing
        CursorVisible = True  # To toggle caret visibility
    
        while active:
            Screen.fill((0, 0, 0))
            # Draws title background
            TitleBgRect = pygame.Rect(0, 0, Width, Height // 15)
            pygame.draw.rect(Screen, (0, 153, 0), TitleBgRect)
            # Renders title
            TitleSurface = TitleFont.render("TBMS", True, (0, 0, 0))
            TitleRect = TitleSurface.get_rect(center=(Width // 2, Height // 25))
            Screen.blit(TitleSurface, TitleRect)
            SubtitleSurface = TitleFont.render(f"Change {Label}", True, (255, 255, 255))
            Screen.blit(SubtitleSurface, (Width // 2 - SubtitleSurface.get_width() // 2, 80))
            
            InputBox = pygame.Rect(250, 200, 300, 40)
            pygame.draw.rect(Screen, (255, 255, 255), InputBox, 2)
            InputSurface = Font.render(InputText, True, (255, 255, 255))
            Screen.blit(InputSurface, (InputBox.x + 5, InputBox.y + 10))

            # Toggle cursor visibility based on time
            if time.time() - LastCursorTime > 0.5:
                CursorVisible = not CursorVisible
                LastCursorTime = time.time()
            if CursorVisible:
                CursorX = InputBox.x + 5 + Font.size(InputText)[0]
                CursorY = InputBox.y + 10
                pygame.draw.line(Screen, (255, 255, 255), (CursorX, CursorY), (CursorX, CursorY + 20), 2)

            MessageSurface = Font.render(message, True, MessageColour)
            if Label == "Password":
                Screen.blit(MessageSurface, (Width // 2 - 250, 400))
            else:
                Screen.blit(MessageSurface, (Width // 2 - 80, 400))

            EnterButton = Button("Enter", (Width // 2 - 60, Height - 200, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), None)
            ExitButton = Button("Exit", (Width // 2 - 60, Height - 100, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), None)
            EnterButton.draw(Screen, pygame.mouse.get_pos())
            ExitButton.draw(Screen, pygame.mouse.get_pos())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        valid, errorMsg = validationFunction(InputText)
                        if valid:
                            User_Detail_Processes.updateCustomerDetails(UserDetails, updateKey, User_Detail_Processes.hashPassword(InputText) if updateKey == 'Password' else InputText)
                            Screen.fill((0, 0, 0))
                            SuccessSurface = TitleFont.render(f"{Label} updated successfully!", True, (0, 255, 0))
                            Screen.blit(SuccessSurface, (Width // 2 - SuccessSurface.get_width() // 2, Height // 2 - 20))
                            pygame.display.flip()
                            pygame.time.wait(2000)
                            message = ""
                            return
                        else:
                            message, MessageColour = errorMsg, (255, 0, 0)
                    elif event.key == pygame.K_BACKSPACE:
                        InputText = InputText[:-1]
                    else:
                        InputText += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if EnterButton.rect.collidepoint(event.pos):
                        valid, errorMsg = validationFunction(InputText)
                        if valid:
                            User_Detail_Processes.updateCustomerDetails(UserDetails, updateKey, User_Detail_Processes.hashPassword(InputText) if updateKey == 'Password' else InputText)
                            Screen.fill((0, 0, 0))
                            SuccessSurface = TitleFont.render(f"{Label} updated successfully!", True, (0, 255, 0))
                            Screen.blit(SuccessSurface, (Width // 2 - SuccessSurface.get_width() // 2, Height // 2 - 20))
                            pygame.display.flip()
                            pygame.time.wait(2000)
                            message = ""
                            return
                        else:
                            message, MessageColour = errorMsg, (255, 0, 0)
                    elif ExitButton.rect.collidepoint(event.pos):
                        message = ""
                        return
            pygame.display.flip()

    def validateText(InputText):
        return (len(InputText.strip()) > 0, "Field cannot be empty")
    def validatePhone(InputText):
        return (InputText.isdigit() and len(InputText) == 11, "Phone number must be 11 digits")
    def validatePasswordField(InputText):
        return (len(InputText) >= 8 and any(c.isdigit() for c in InputText) and any(c.isupper() for c in InputText), "Password must be at least 8 characters with a number and uppercase letter")
    def validatePostcode(InputText):
        import re
        return (bool(re.match(r"^([A-Za-z][A-Ha-hJ-Yj-y]?[0-9][A-Za-z0-9]? ?[0-9][A-Za-z]{2}|[Gg][Ii][Rr] ?0[Aa]{2})$", InputText)), "Invalid postcode format")
    def validateEmail(InputText):
        return (bool(re.match(r"^(?![.])[A-Za-z0-9!#$%&'*+/=?^_`{|}~.-]+(?<![.])@([A-Za-z0-9.-]+)\.([A-Za-z]{2,})$", InputText)), "Invalid Email format")
    
    validators = {
        "Firstname": validateText,
        "Lastname": validateText,
        "Email" : validateEmail,
        "Password": validatePasswordField,
        "Phone Number": validatePhone,
        "Street": validateText,
        "City": validateText,
        "Postcode": validatePostcode,
    }

    while True:
        Screen.fill((0, 0, 0))
        # Draws title background
        TitleBgRect = pygame.Rect(0, 0, Width, Height // 15)
        pygame.draw.rect(Screen, (0, 153, 0), TitleBgRect)
        # Renders title
        TitleSurface = TitleFont.render("TBMS", True, (0, 0, 0))
        TitleRect = TitleSurface.get_rect(center=(Width // 2, Height // 25))
        Screen.blit(TitleSurface, TitleRect)  
        SubtitleSurface = TitleFont.render(f"Edit Customer {UserDetails.getFirstname()}'s Details", True, (255, 255, 255))
        Screen.blit(SubtitleSurface, (Width // 2 - SubtitleSurface.get_width() // 2, 80))

        Buttons = []
        for i, option in enumerate(options):
            Buttons.append(Button(option, (250, 160 + i * 60, 300, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), None))
            Buttons[i].draw(Screen, pygame.mouse.get_pos())

        MessageSurface = Font.render(message, True, MessageColour)
        Screen.blit(MessageSurface, (250, 700))
        ExitButton = Button("Exit", (Width // 2 - 60, Height - 100, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), None)
        ExitButton.draw(Screen, pygame.mouse.get_pos())

        for event in pygame.event.get(): # Event handler
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, button in enumerate(Buttons): # Checks collision for each option 
                    if button.rect.collidepoint(event.pos): # Runs the getInputScreen function for the selected button 
                        getInputScreen(options[i], validators[options[i]], options[i])
                if ExitButton.rect.collidepoint(event.pos):
                    return
        pygame.display.flip()

def editDriverDetails(UserDetails):
    options = [ "Firstname", "Lastname", "Email", "Password", "Phone Number", "Street", "City", "Postcode", "Car Reg", "Car Model", "Taxi Type", "Wallet"]
    message = ""
    MessageColour = (255, 0, 0)

    def getInputScreen(Label, validationFunction, updateKey):
        InputText = ""
        active = True
        nonlocal message, MessageColour
        LastCursorTime = time.time()  # To track the blink timing
        CursorVisible = True  # To toggle caret visibility
    
        while active:
            Screen.fill((0, 0, 0))
            # Draws title background
            TitleBgRect = pygame.Rect(0, 0, Width, Height // 15)
            pygame.draw.rect(Screen, (0, 153, 0), TitleBgRect)
            # Renders title
            TitleSurface = TitleFont.render("TBMS", True, (0, 0, 0))
            TitleRect = TitleSurface.get_rect(center=(Width // 2, Height // 25))
            Screen.blit(TitleSurface, TitleRect)
            SubtitleSurface = TitleFont.render(f"Change {Label}", True, (255, 255, 255))
            Screen.blit(SubtitleSurface, (Width // 2 - SubtitleSurface.get_width() // 2, 80))
            
            InputBox = pygame.Rect(250, 200, 300, 40)
            pygame.draw.rect(Screen, (255, 255, 255), InputBox, 2)
            InputSurface = Font.render(InputText, True, (255, 255, 255))
            Screen.blit(InputSurface, (InputBox.x + 5, InputBox.y + 10))

            # Toggle cursor visibility based on time
            if time.time() - LastCursorTime > 0.5:
                CursorVisible = not CursorVisible
                LastCursorTime = time.time()
            if CursorVisible:
                CursorX = InputBox.x + 5 + Font.size(InputText)[0]
                CursorY = InputBox.y + 10
                pygame.draw.line(Screen, (255, 255, 255), (CursorX, CursorY), (CursorX, CursorY + 20), 2)

            MessageSurface = Font.render(message, True, MessageColour)
            Screen.blit(MessageSurface, (250, 400))
            EnterButton = Button("Enter", (Width // 2 - 60, Height - 200, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), None)
            ExitButton = Button("Exit", (Width // 2 - 60, Height - 100, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), None)
            EnterButton.draw(Screen, pygame.mouse.get_pos())
            ExitButton.draw(Screen, pygame.mouse.get_pos())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        valid, errorMsg = validationFunction(InputText)
                        if valid:
                            if Label == "Wallet":
                                InputText = float(InputText)
                            User_Detail_Processes.updateDriverDetails(UserDetails, updateKey, User_Detail_Processes.hashPassword(InputText) if updateKey == 'Password' else InputText)
                            Screen.fill((0, 0, 0))
                            SuccessSurface = TitleFont.render(f"{Label} updated successfully!", True, (0, 255, 0))
                            Screen.blit(SuccessSurface, (Width // 2 - SuccessSurface.get_width() // 2, Height // 2 - 20))
                            pygame.display.flip()
                            pygame.time.wait(2000)
                            message = ""
                            return
                        else:
                            message, MessageColour = errorMsg, (255, 0, 0)
                    elif event.key == pygame.K_BACKSPACE:
                            InputText = InputText[:-1]
                    else:
                        InputText += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if EnterButton.rect.collidepoint(event.pos):
                        valid, errorMsg = validationFunction(InputText)
                        if valid:
                            if Label == "Wallet":
                                InputText = float(InputText)
                            User_Detail_Processes.updateDriverDetails(UserDetails, updateKey, User_Detail_Processes.hashPassword(InputText) if updateKey == 'Password' else InputText)
                            Screen.fill((0, 0, 0))
                            SuccessSurface = TitleFont.render(f"{Label} updated successfully!", True, (0, 255, 0))
                            Screen.blit(SuccessSurface, (Width // 2 - SuccessSurface.get_width() // 2, Height // 2 - 20))
                            pygame.display.flip()
                            pygame.time.wait(2000)
                            message = ""
                            return
                        else:
                            message, MessageColour = errorMsg, (255, 0, 0)
                    elif ExitButton.rect.collidepoint(event.pos):
                        message = ""
                        return
            pygame.display.flip()

    def validateText(InputText):
        return (len(InputText.strip()) > 0, "Field cannot be empty")
    def validatePhone(InputText):
        return (InputText.isdigit() and len(InputText) == 11, "Phone number must be 11 digits")
    def validatePasswordField(InputText):
        return (len(InputText) >= 8 and any(c.isdigit() for c in InputText) and any(c.isupper() for c in InputText), "Password must be at least 8 characters with a number and uppercase letter")
    def validatePostcode(InputText):
        return (bool(re.match(r"^([A-Za-z][A-Ha-hJ-Yj-y]?[0-9][A-Za-z0-9]? ?[0-9][A-Za-z]{2}|[Gg][Ii][Rr] ?0[Aa]{2})$", InputText)), "Invalid postcode format")
    def validateEmail(InputText):
        return (bool(re.match(r"^(?![.])[A-Za-z0-9!#$%&'*+/=?^_`{|}~.-]+(?<![.])@([A-Za-z0-9.-]+)\.([A-Za-z]{2,})$", InputText)), "Invalid Email format")
    def validateCarReg(InputText):
        return (bool(re.match(r"^(?:[A-Z]{2}\d{2} [A-Z]{3}|[A-Z]\d{1,3} [A-Z]{3}|[A-Z]{3} \d{1,3} [A-Z]|[A-Z]{3} \d{1,4}|\d{1,4} [A-Z]{3}|[A-Z]{1,3}\d{1,4})$", InputText)), "Invalid Car Registration format")
    def validateTaxiType(InputText):
        return ((InputText.strip() in ["1-4 Passenger", "5-6 Passenger", "7-8 Passenger"]), "Can only accept taxi types as: 1-4 Passenger, 5-6 Passenger, 7-8 Passenger ")
    def validateWallet(InputText):
        try:
            value = float(InputText)  # Attempt to convert to float
            return ((value >= 0), "Cannot be negative")
        except ValueError:
             # Return False if value is not a float
            return (False , "Has to be a decimal value") 
    
    validators = {
        "Firstname": validateText,
        "Lastname": validateText,
        "Email" : validateEmail,
        "Password": validatePasswordField,
        "Phone Number": validatePhone,
        "Street": validateText,
        "City": validateText,
        "Postcode": validatePostcode,
        "Car Reg" : validateCarReg,
        "Car Model" : validateText,
        "Taxi Type" : validateTaxiType,
        "Wallet" : validateWallet
    }

    while True:
        Screen.fill((0, 0, 0))
        # Draws title background
        TitleBgRect = pygame.Rect(0, 0, Width, Height // 15)
        pygame.draw.rect(Screen, (0, 153, 0), TitleBgRect)
        # Renders title
        TitleSurface = TitleFont.render("TBMS", True, (0, 0, 0))
        TitleRect = TitleSurface.get_rect(center=(Width // 2, Height // 25))
        Screen.blit(TitleSurface, TitleRect)     
        SubtitleSurface = TitleFont.render(f"Edit Driver {UserDetails.getFirstname()}'s Details", True, (255, 255, 255))
        Screen.blit(SubtitleSurface, (Width // 2 - SubtitleSurface.get_width() // 2, 80))

        Buttons = []
        for i, option in enumerate(options):
            Buttons.append(Button(option, (250, 160 + i * 60, 300, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), None))
            Buttons[i].draw(Screen, pygame.mouse.get_pos())
        MessageSurface = Font.render(message, True, MessageColour)
        Screen.blit(MessageSurface, (250, 700))
        ExitButton = Button("Exit", (Width // 2 - 60, Height - 100, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), None)
        ExitButton.draw(Screen, pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, button in enumerate(Buttons):
                    if button.rect.collidepoint(event.pos):
                        getInputScreen(options[i], validators[options[i]], options[i])
                if ExitButton.rect.collidepoint(event.pos):
                    return
        pygame.display.flip()
        
def driverMenu(UserDetails):
    # Buttons for the DriverMenu
    buttons = [
        Button("View Available Bookings", (150, 200, 200, 50), (211, 211, 211), (64, 64, 64), (0, 0, 0), lambda: viewAvailableBookings(UserDetails)),
        Button("View Assigned Bookings", (450, 200, 200, 50), (211, 211, 211), (64, 64, 64), (0, 0, 0), lambda: viewAssignedBookings(UserDetails)),
        Button("View past bookings", (150, 300, 200, 50), (211, 211, 211), (64, 64, 64), (0, 0, 0), lambda: viewPastBooking(UserDetails)),
        Button("Report Issue", (450, 300, 200, 50), (211, 211, 211), (64, 64, 64), (0, 0, 0), lambda: reportIssue(UserDetails)),
        Button("Logout", (300, 100, 250, 50), (211, 211, 211), (64, 64, 64), (0, 0, 0), lambda: logout())
        ]
    
    global Width, Height
    running = True
    while running:
        Screen.fill((99, 99, 99))  # Screen is filled with grey background
        MousePosition = pygame.mouse.get_pos() # Gets position of the cursor
        
        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                Width, Height = event.w, event.h
                pygame.display.set_mode((Width, Height), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    button.check_click(MousePosition)
                    
        # Draws title background
        TitleBgRect = pygame.Rect(0, 0, Width, Height // 15)
        pygame.draw.rect(Screen, (0, 153, 0), TitleBgRect)
        # Renders title
        TitleSurface = TitleFont.render("TBMS", True, (0, 0, 0))
        TitleRect = TitleSurface.get_rect(center=(Width // 2, Height // 25))
        Screen.blit(TitleSurface, TitleRect)
        # Displays the name of the screen "Customer Login"
        SubtitleSurface = TitleFont.render("Driver Menu", True, (255, 255, 255))
        Screen.blit(SubtitleSurface, (Width // 2 - SubtitleSurface.get_width() // 2, 80))
        
        NameSurface = SubtitleFont.render(f"Hello {UserDetails.getFirstname()}!", True, (255, 255, 255))
        Screen.blit(NameSurface, (Width // 2 - NameSurface.get_width() // 2, 130))
        
        # Adjust button positions and sizes dynamically
        buttons[0].rect.update(50, Height // 2 - 80, Width // 2 - 100, 50)
        buttons[1].rect.update(Width // 2 + 50, Height // 2 - 80, Width // 2 - 100, 50)
        buttons[2].rect.update(50, Height // 2 + 20, Width // 2 - 100, 50)
        buttons[3].rect.update(Width // 2 + 50, Height // 2 + 20, Width // 2 - 100, 50)
        buttons[4].rect.update(Width // 2 - (Width // 5), Height // 2 + 120, Width // 2 - 100, 50)
        # Draw buttons
        for button in buttons:
            button.draw(Screen, MousePosition)
        pygame.display.flip()
    
def viewPastBooking(UserDetails):
    print("View Past Bookings button clicked…")
    
def reportIssue(UserDetails):
    print("Report Issue button clicked…")
    
def viewAvailableBookings(UserDetails):
    def getAvailableBookings():
        Bookings = User_Detail_Processes.openFile("bookings.json")
        AvailableBookings = []
        CurrentDate = datetime.datetime.now()
        for Booking in Bookings:
            if Booking["Status"] == "Unassigned":
                BookingDateTime = datetime.datetime.strptime(
                    f"{Booking['Date (DD/MM/YYYY)']} {Booking['Time (24hr)']}", "%d/%m/%Y %H:%M"
                )
                if (BookingDateTime >= CurrentDate):
                    AvailableBookings.append(Booking)
        return AvailableBookings

    def displayBookingDetails(Booking):
        Viewing = True
        while Viewing:
            Screen.fill((0, 0, 0))
            MousePosition = pygame.mouse.get_pos()
            Details = [
                f"Pickup Postcode: {Booking['Pickup Postcode']}",
                f"Pickup Address: {Booking['Pickup Address']}",
                f"Dropoff Postcode: {Booking['Dropoff Postcode']}",
                f"Dropoff Address: {Booking['Dropoff Address']}",
                f"Date: {Booking['Date (DD/MM/YYYY)']}",
                f"Time: {Booking['Time (24hr)']}",
                f"Taxi Type: {Booking['TaxiType']}",
                f"Price: £{Booking['Price']}",
                f"Driver Cut: £{Booking['Driver Cut']}",
                f"Status: {Booking['Status']}"
            ]
            for I, Line in enumerate(Details):
                DetailSurface = Font.render(Line, True, (255, 255, 255))
                Screen.blit(DetailSurface, (50, 50 + I * 30))
            ExitButton = Button("Exit", (Width // 2 - 60, Height - 100, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), lambda: setViewingFalse())
            ExitButton.draw(Screen, MousePosition)

            # Show "Assign Booking" button 
            if Booking["Status"] not in ["Assigned", "Completed", "Cancelled"]:
                AssignButton = Button("Assign Booking", (Width // 2 - 100, Height - 150, 200, 40), (200, 0, 0), (255, 0, 0), (255, 255, 255), lambda: confirmAssignBooking(Booking))
                AssignButton.draw(Screen, MousePosition)
            def setViewingFalse():
                nonlocal Viewing
                Viewing = False
            def confirmAssignBooking(Booking):
                Confirmation = showConfirmationDialog("Are you sure you want to assign this booking?")
                if Confirmation:  
                    # Load all bookings
                    AllBookings = User_Detail_Processes.openFile("bookings.json")
                    for B in AllBookings:
                        if B["bookingID"] == Booking["bookingID"]:
                            B["Status"] = "Assigned"
                            B["driverID"] = UserDetails.getDriverID()
                            break
                    # Save the updated bookings
                    User_Detail_Processes.closeFile("bookings.json", AllBookings)
                # Refresh the screen after assigning the booking and return to the Driver Menu
                setViewingFalse()
                driverMenu(UserDetails)  
            for Event in pygame.event.get():
                if Event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif Event.type == pygame.MOUSEBUTTONDOWN and Event.button == 1:
                    if ExitButton.rect.collidepoint(Event.pos):
                        setViewingFalse()
                    if Booking["Status"] not in ["Assigned", "Cancelled"]:
                        if AssignButton.rect.collidepoint(Event.pos):
                            AssignButton.action()
            pygame.display.flip()
    
            
    def showConfirmationDialog(Message):
        Running = True
        while Running:
            Screen.fill((0, 0, 0))
            ConfirmationSurface = Font.render(Message, True, (255, 255, 255))
            Screen.blit(ConfirmationSurface, (Width // 2 - ConfirmationSurface.get_width() // 2, Height // 2 - 50))

            YesButton = Button("Yes", (Width // 2 - 120, Height // 2 + 20, 100, 50), (0, 153, 0), (0, 200, 0), (255, 255, 255), lambda: setRunningFalse(True))
            NoButton = Button("No", (Width // 2 + 20, Height // 2 + 20, 100, 50), (200, 0, 0), (255, 0, 0), (255, 255, 255), lambda: setRunningFalse(False))

            MousePosition = pygame.mouse.get_pos()
            YesButton.draw(Screen, MousePosition)
            NoButton.draw(Screen, MousePosition)

            for Event in pygame.event.get():
                if Event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif Event.type == pygame.MOUSEBUTTONDOWN and Event.button == 1:
                    if YesButton.rect.collidepoint(Event.pos):
                        Running = False
                        return True
                    elif NoButton.rect.collidepoint(Event.pos):
                        Running = False
                        return False

            pygame.display.flip()
    
    def setRunningFalse():
        nonlocal Running
        Running = False
      
    Bookings = getAvailableBookings()
    Running = True
    while Running:
        Screen.fill((0, 0, 0))
        MousePosition = pygame.mouse.get_pos()
        # Draws title background
        TitleBgRect = pygame.Rect(0, 0, Width, Height // 15)
        pygame.draw.rect(Screen, (0, 153, 0), TitleBgRect)
        # Renders title
        TitleSurface = TitleFont.render("TBMS", True, (0, 0, 0))
        TitleRect = TitleSurface.get_rect(center=(Width // 2, Height // 25))
        Screen.blit(TitleSurface, TitleRect)
        SubtitleSurface = TitleFont.render("Available Bookings", True, (255, 255, 255))
        Screen.blit(SubtitleSurface, (Width // 2 - SubtitleSurface.get_width() // 2, 80))

        if not Bookings: # If no bookings are returned, it presents the message below
            NoBookingsText = "No bookings available."
            NoBookingsSurface = TitleFont.render(NoBookingsText, True, (255, 0, 0))
            Screen.blit(NoBookingsSurface, (Width // 2 - NoBookingsSurface.get_width() // 2, Height // 2))
        else:
            BookingButtons = [] # Each booking in Bookings is displayed as a button
            for I, Booking in enumerate(Bookings):
                RowText = f"{Booking['Pickup Postcode']} to {Booking['Dropoff Postcode']} | {Booking['Time (24hr)']} | {Booking['Date (DD/MM/YYYY)']}"
                RowButton = Button(RowText, ((Width - 500) // 2, 150 + I * 50, 500, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), lambda b=Booking: displayBookingDetails(b))
                RowButton.draw(Screen, MousePosition)
                BookingButtons.append(RowButton)

        ExitButton = Button("Exit", (Width // 2 - 60, Height - 100, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), lambda: driverMenu(UserDetails))
        ExitButton.draw(Screen, MousePosition)

        for Event in pygame.event.get(): # Event handler
            if Event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif Event.type == pygame.MOUSEBUTTONDOWN and Event.button == 1:
                if Bookings:
                    for RowButton in BookingButtons:
                        if RowButton.rect.collidepoint(Event.pos):
                            RowButton.action()
                if ExitButton.rect.collidepoint(Event.pos):
                    ExitButton.action()
        pygame.display.flip()
    
def viewAssignedBookings(UserDetails):
    def getAvailableBookings():
        Bookings = User_Detail_Processes.openFile("bookings.json")
        AssignedBookings = []
        CurrentDate = datetime.datetime.now()
        for Booking in Bookings:
            if Booking["Status"] in ["Assigned", "Cancelled"] and Booking["driverID"] == UserDetails.getDriverID():
                BookingDateTime = datetime.datetime.strptime(
                    f"{Booking['Date (DD/MM/YYYY)']} {Booking['Time (24hr)']}", "%d/%m/%Y %H:%M"
                )
                if (BookingDateTime >= CurrentDate):
                    AssignedBookings.append(Booking)
        return AssignedBookings

    def displayBookingDetails(Booking):
        Viewing = True
        while Viewing:
            Screen.fill((0, 0, 0))
            MousePosition = pygame.mouse.get_pos()
            Details = [
                f"Pickup Postcode: {Booking['Pickup Postcode']}",
                f"Pickup Address: {Booking['Pickup Address']}",
                f"Dropoff Postcode: {Booking['Dropoff Postcode']}",
                f"Dropoff Address: {Booking['Dropoff Address']}",
                f"Date: {Booking['Date (DD/MM/YYYY)']}",
                f"Time: {Booking['Time (24hr)']}",
                f"Taxi Type: {Booking['TaxiType']}",
                f"Price: £{Booking['Price']}",
                f"Driver Cut: £{Booking['Driver Cut']}",
                f"Status: {Booking['Status']}"
            ]
            for I, Line in enumerate(Details):
                DetailSurface = Font.render(Line, True, (255, 255, 255))
                Screen.blit(DetailSurface, (50, 50 + I * 30))
            
            ExitButton = Button("Exit", (Width // 2 - 60, Height - 100, 120, 40), 
                                (99, 99, 99), (64, 64, 64), (255, 255, 255), lambda: setViewingFalse())
            ExitButton.draw(Screen, MousePosition)
            if Booking["Status"] not in ["Unassigned", "Completed", "Cancelled"]:
                RemoveButton = Button("Unassign Booking", (Width // 2 - 100, Height - 150, 200, 40), (200, 0, 0), (255, 0, 0), (255, 255, 255), lambda: confirmRemoveBooking(Booking))
                RemoveButton.draw(Screen, MousePosition)
                CompleteButton = Button("Complete Booking", (Width // 2 - 100, Height - 200, 200, 40), (0, 153, 0), (0, 200, 0), (255, 255, 255), lambda: completeBooking(Booking))
                CompleteButton.draw(Screen, MousePosition)
            
            def completeBooking(Booking):
                Confirmation = showConfirmationDialog("Are you sure you want to mark this booking as completed?")
                if Confirmation:  
                    # Load all bookings
                    AllBookings = User_Detail_Processes.openFile("bookings.json")
                    for B in AllBookings:
                        if B["bookingID"] == Booking["bookingID"]:
                            B["Status"] = "Completed"
                            break
                    # Save the updated bookings
                    User_Detail_Processes.closeFile("bookings.json", AllBookings)
                    # Updates Driver Wallet
                    NewWallet = UserDetails.wallet + Booking['Driver Cut']
                    User_Detail_Processes.updateDriverDetails(UserDetails, "Wallet", NewWallet)
                # Refresh the screen and return to the Driver Menu
                setViewingFalse()
                driverMenu(UserDetails)  
            
            def setViewingFalse():
                nonlocal Viewing
                Viewing = False
            def confirmRemoveBooking(Booking):
                Confirmation = showConfirmationDialog("Are you sure you want to remove this booking?")
                if Confirmation:  
                    # Load all bookings
                    AllBookings = User_Detail_Processes.openFile("bookings.json")
                    for B in AllBookings:
                        if B["bookingID"] == Booking["bookingID"]:
                            B["Status"] = "Unassigned"
                            B["driverID"] = "N/A"
                            break
                    # Save the updated bookings
                    User_Detail_Processes.closeFile("bookings.json", AllBookings)
                # Refresh the screen after cancellation and return to the Driver Menu
                setViewingFalse()
                driverMenu(UserDetails)  
            for Event in pygame.event.get():
                if Event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif Event.type == pygame.MOUSEBUTTONDOWN and Event.button == 1:
                    if ExitButton.rect.collidepoint(Event.pos):
                        setViewingFalse()
                    # Only checks RemoveButton click if the button is displayed (only by these conditions is it displayed)
                    if Booking["Status"] not in ["Unassigned", "Completed", "Cancelled"]:
                        if RemoveButton.rect.collidepoint(Event.pos):
                            RemoveButton.action()
                        if CompleteButton.rect.collidepoint(Event.pos):
                            CompleteButton.action()
            pygame.display.flip()

    def showConfirmationDialog(Message):
        Running = True
        while Running:
            Screen.fill((0, 0, 0))
            ConfirmationSurface = Font.render(Message, True, (255, 255, 255))
            Screen.blit(ConfirmationSurface, (Width // 2 - ConfirmationSurface.get_width() // 2, Height // 2 - 50))
            YesButton = Button("Yes", (Width // 2 - 120, Height // 2 + 20, 100, 50), (0, 153, 0), (0, 200, 0), (255, 255, 255), lambda: setRunningFalse(True))
            NoButton = Button("No", (Width // 2 + 20, Height // 2 + 20, 100, 50), (200, 0, 0), (255, 0, 0), (255, 255, 255), lambda: setRunningFalse(False))
            MousePosition = pygame.mouse.get_pos()
            YesButton.draw(Screen, MousePosition)
            NoButton.draw(Screen, MousePosition)

            for Event in pygame.event.get():
                if Event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif Event.type == pygame.MOUSEBUTTONDOWN and Event.button == 1:
                    if YesButton.rect.collidepoint(Event.pos):
                        Running = False
                        return True
                    elif NoButton.rect.collidepoint(Event.pos):
                        Running = False
                        return False

            pygame.display.flip()

    Bookings = getAvailableBookings()
    Running = True

    while Running:
        Screen.fill((0, 0, 0))
        MousePosition = pygame.mouse.get_pos()
        # Draws title background
        TitleBgRect = pygame.Rect(0, 0, Width, Height // 15)
        pygame.draw.rect(Screen, (0, 153, 0), TitleBgRect)
        # Renders title
        TitleSurface = TitleFont.render("TBMS", True, (0, 0, 0))
        TitleRect = TitleSurface.get_rect(center=(Width // 2, Height // 25))
        Screen.blit(TitleSurface, TitleRect)
        SubtitleSurface = TitleFont.render("Assigned Bookings", True, (255, 255, 255))
        Screen.blit(SubtitleSurface, (Width // 2 - SubtitleSurface.get_width() // 2, 80))

        if not Bookings:
            NoBookingsText = "No bookings assigned to your account."
            NoBookingsSurface = SubtitleFont.render(NoBookingsText, True, (255, 0, 0))
            Screen.blit(NoBookingsSurface, (Width // 2 - NoBookingsSurface.get_width() // 2, Height // 2))
        else:
            BookingButtons = []
            for I, Booking in enumerate(Bookings):
                RowText = f"{Booking['Pickup Postcode']} to {Booking['Dropoff Postcode']} | {Booking['Time (24hr)']} | {Booking['Date (DD/MM/YYYY)']}"
                RowButton = Button(RowText, ((Width - 500) // 2, 150 + I * 50, 500, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), lambda b=Booking: displayBookingDetails(b))
                RowButton.draw(Screen, MousePosition)
                BookingButtons.append(RowButton)

        ExitButton = Button("Exit", (Width // 2 - 60, Height - 100, 120, 40), (99, 99, 99), (64, 64, 64), (255, 255, 255), lambda: setRunningFalse())
        ExitButton.draw(Screen, MousePosition)
        def setRunningFalse():
            nonlocal Running
            Running = False
        for Event in pygame.event.get():
            if Event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif Event.type == pygame.MOUSEBUTTONDOWN and Event.button == 1:
                if Bookings:
                    for RowButton in BookingButtons:
                        if RowButton.rect.collidepoint(Event.pos):
                            RowButton.action()
                if ExitButton.rect.collidepoint(Event.pos):
                    setRunningFalse()
        pygame.display.flip()
    driverMenu(UserDetails)
    
def mainMenu():
    # Main loop
    buttons = [ # Buttons for the Main menu
        Button("Customer Login", (150, 200, 200, 50), (211, 211, 211), (64, 64, 64), (0, 0, 0), custLogin),
        Button("Driver Login", (450, 200, 200, 50), (211, 211, 211), (64, 64, 64), (0, 0, 0), driverLogin),
        Button("Create Account", (150, 300, 200, 50), (211, 211, 211), (64, 64, 64), (0, 0, 0), createAccount),
        Button("Admin Login", (450, 300, 200, 50), (211, 211, 211), (64, 64, 64), (0, 0, 0), adminLogin),
        Button("Close Program", (300, 100, 250, 50), (211, 211, 211), (64, 64, 64), (0, 0, 0), exit),
    ]
    global Width, Height

    running = True
    while running:
        Screen.fill((99, 99, 99)) # Screen is filled with grey background
        MousePosition = pygame.mouse.get_pos() # Gets position of the cursor

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                Width, Height = event.w, event.h
                pygame.display.set_mode((Width, Height), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    button.check_click(MousePosition)
                
        # Draws title background
        TitleBgRect = pygame.Rect(0, 0, Width, Height // 15)
        pygame.draw.rect(Screen, (0, 153, 0), TitleBgRect)
        # Draws subtitle background
        SubtitleBgRect = pygame.Rect(0, Height // 15, Width, Height // 15)
        pygame.draw.rect(Screen, (0, 153, 0), SubtitleBgRect)
        # Renders title
        TitleSurface = TitleFont.render("TBMS", True, (0, 0, 0))
        TitleRect = TitleSurface.get_rect(center=(Width // 2, Height // 25))
        Screen.blit(TitleSurface, TitleRect)

        # Renders subtitle
        SubtitleSurface = SubtitleFont.render("TaxiCo Booking and Management System", True, (0, 0, 0))
        SubtitleRect = SubtitleSurface.get_rect(center=(Width // 2, Height // 10))
        Screen.blit(SubtitleSurface, SubtitleRect)    
        
        # Adjust button positions and sizes dynamically
        buttons[0].rect.update(50, Height // 2 - 80, Width // 2 - 100, 50)
        buttons[1].rect.update(Width // 2 + 50, Height // 2 - 80, Width // 2 - 100, 50)
        buttons[2].rect.update(50, Height // 2 + 20, Width // 2 - 100, 50)
        buttons[3].rect.update(Width // 2 + 50, Height // 2 + 20, Width // 2 - 100, 50)
        buttons[4].rect.update(Width // 2 - (Width // 5), Height // 2 + 120, Width // 2 - 100, 50)

        # Draw buttons
        for button in buttons:
            button.draw(Screen, MousePosition)
        # Updates the Screen by redrawing it every iteration
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    mainMenu()
    
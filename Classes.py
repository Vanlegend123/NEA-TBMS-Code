import pygame


class Button:
    def __init__(self, Text, rect, Colour, HoverColour, TextColour, action):
        self.Text = Text
        self.rect = pygame.Rect(rect)
        self.Colour = Colour
        self.HoverColour = HoverColour
        self.TextColour = TextColour
        self.action = action

    # Method to draw the button object
    def draw(self, screen, mouse_pos):
        # Changes the colour that the button is drawn with to show that the curser is over said button
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.HoverColour, self.rect)
        else:
            pygame.draw.rect(screen, self.Colour, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Border

        # Renders the text on the button
        pygame.font.init()
        ButtonFont = pygame.font.Font(None, 32)
        TextSurface = ButtonFont.render(self.Text, True, self.TextColour)
        Textrect = TextSurface.get_rect(center=self.rect.center)
        screen.blit(TextSurface, Textrect)

    # Checks if the button has been clicked
    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.action()
            
class User:
    def __init__(self, firstname, lastname, email, password, phone, street, city, postcode):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password  
        self.phone = phone
        self.street = street
        self.city = city
        self.postcode = postcode

    def getFirstname(self):
        return self.firstname
    
    def getLastname(self):
        return self.lastname
    
    def getEmail(self):
        return self.email
    
    def getPhone(self):
        return self.phone
    
    def getAddress(self):
        return f"{self.street}, {self.city}, {self.postcode}"


class Customer(User):
    def __init__(self, custID, firstname, lastname, email, password, phone, street, city, postcode):
        super().__init__(firstname, lastname, email, password, phone, street, city, postcode)
        self.custID = custID
    
    def getCustID(self):
        return self.custID


class Driver(User):
    def __init__(self, driverID, firstname, lastname, email, password, phone, street, city, postcode, car_reg, car_model, wallet):
        super().__init__(firstname, lastname, email, password, phone, street, city, postcode)
        self.driverID = driverID
        self.car_reg = car_reg
        self.car_model = car_model
        self.wallet = wallet
    
    def getDriverID(self):
        return self.driverID
    
    def getCarDetails(self):
        return f"{self.car_model} ({self.car_reg})"
    
    def getWallet(self):
        return self.wallet


class Admin(User):
    def __init__(self, adminID, firstname, lastname, email, password, phone, street, city, postcode):
        super().__init__(firstname, lastname, email, password, phone, street, city, postcode)
        self.adminID = adminID
    
    def getAdminID(self):
        return self.adminID
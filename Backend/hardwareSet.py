

class hardwareSet:

    def __init__(self):
        self.__capacity = 0
        self.__availability = 0
        self.__checked_out = {}
        self.__hardware_name = ""
    
    def initialize_capacity(self,qty):
        self.__capacity = qty
        self.__availability = qty
        self.__checked_out = {}

    def initialize_name(self, name):
        self.__hardwareName = name

    def get_availability(self):
        return self.__availability
    
    def get_hardware_name(self):
        return self.__hardware_name

    def get_capacity(self):
        return self.__capacity
    
    def check_out(self, qty, userName):
        self.handle_userName(userName)
        if qty > self.__availability:
            self.__checked_out[userName] += self.__availability
            self.__availability = 0
            return -1
        else:
            self.__checked_out[userName] += qty
            self.__availability -= qty
            return 0
        
    def check_in(self, qty, userName):
        self.handle_userName(userName)
        checkoutQTY = self.__checked_out[userName]
        print(checkoutQTY)
        if qty > checkoutQTY:
            return -1
        else:
            self.__checked_out[userName] -= qty
            self.__availability += qty
            return 0
        
    def handle_userName(self, userName):
        if userName not in self.__checked_out:
            self.__checked_out[userName] = 0
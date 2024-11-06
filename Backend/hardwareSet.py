

class HardwareSet:


    def __init__(self, name, capacity, availability, checked):
        self.__capacity = capacity
        self.__availability = availability
        self.__checked_out = checked
        self.__hardware_name = name

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
        if qty > checkoutQTY:
            return -1
        else:
            self.__checked_out[userName] -= qty
            self.__availability += qty
            return 0
        
    def handle_userName(self, userName):
        if userName not in self.__checked_out:
            self.__checked_out[userName] = 0
    
    def to_dict(self):
        return {
            "hardware_name": self.__hardware_name,
            "capacity": self.__capacity,
            "availability": self.__availability,
            "checked_out": self.__checked_out
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(name=data["hardware_name"], capacity=data["capacity"], availability=data["availability"], checked=data["checked_out"])

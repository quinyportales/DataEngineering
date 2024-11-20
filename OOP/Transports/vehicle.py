
class Vehicle():
    """Parent class representing type of transport"""
    manufacture_year = None  
    is_operational = True    

    def __init__(self):
        self.manufacture_year = Vehicle.manufacture_year
        self.is_operational = Vehicle.is_operational
      
    @classmethod
    def set_common_attributes(cls, manufacture_year, is_operational):
        """Set manufacture_year and fuel_type for all instances of this class or subclasses."""
        cls.manufacture_year = manufacture_year
        cls.is_operational = is_operational

    @classmethod
    def get_common_attributes(cls):
            """Retrieve the common attributes of the class."""
            return f"Manufacture Year: {cls.manufacture_year}, Is Operational Status {cls.is_operational}"

    def __str__(self):
            return (f"Manufacture Year: {self.manufacture_year}, Is Operational: {self.is_operational}")
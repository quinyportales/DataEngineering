"""Module defining various types of transport using inheritance and abstraction."""

from abc import ABC, abstractmethod
from vehicle import Vehicle


class Transport(ABC, Vehicle):
    '''Parent class representing type of transport'''
    _has_engine = True
    vehicles_created = 0

    def __init__(self,max_speed, max_capacity ):
        super().__init__()
        self.max_speed = max_speed
        self.max_capacity = max_capacity
        Transport.vehicles_created += 1

    @staticmethod
    def get_total_vehicles():
        """Return the total number of vehicles created."""
        return f'Total vehicles created: {Transport.vehicles_created}'


    #overiding the magic methods
    def __str__(self):
        """String representation of the transport object."""
        return f'{self.transport_type} {self.max_speed}'

    def __len__(self):
        return self.max_capacity

    def __call__(self, message):
        return f"Transport says: {message}"

    @staticmethod
    def print_class_hierarchy(instance):
        """Print out the class hierarchy"""
        class_name = type(instance).__name__
        base_classes = [base.__name__ for base in type(instance).__bases__]
        print(f'Instance name: {instance}')
        print(f'Instance of class: {class_name}')
        print(' ---> Parent class:', ' ---> '.join(base_classes))
        print('\n')

    @property
    @abstractmethod
    def transport_type(self):
        """Abstract property to ensure child classes define a transport type."""

    @abstractmethod
    def get_transport_type(self):
        'return the transport type'

    @abstractmethod
    def get_max_speed(self):
        'return the max speed'



class Car(Transport):
    '''Class representing a car'''
    transport_type = 'road transport'
    def __init__(self, max_speed, max_capacity, model, brand):
        super().__init__( max_speed, max_capacity)
        self.vehicle = 'Car'
        self.model = model
        self.brand = brand
        self._wheel_number = 4

    def get_transport_type(self):
        return f'{Car.transport_type}'

    def get_max_speed(self):
        return f'{self.max_speed}'

    #overiding magic method
    def __add__(self, other):
        """Add two transport objects to combine their capacity."""
        combined_capacity = self.max_speed + other.max_speed
        return combined_capacity

    def __str__(self):
        return (f'This is a {self.vehicle} {self.model} {self.brand}\n'
                 f'max capacity {self.max_capacity} persons to transport\n'
                 f'max speed {self.get_max_speed()} km/h \n'
                 f'type of transport {self.get_transport_type()}')

    @property
    def wheel_number(self):
        'returns the non-public wheel_number'
        return self._wheel_number

class ElectricCar(Car):
    '''Class representing an electric car'''
    def __init__(self, max_speed, model, brand, battery_voltage, max_capacity=4):
        super().__init__(max_speed, max_capacity, model, brand)
        self.battery_voltage = battery_voltage

    def __str__(self):
        return (f'This is an Electric Car {self.model} {self.brand} \n'
                f' with a battery of {self.battery_voltage}V max speed {self.max_speed} km/h \n'
                f'max capacity {self.max_capacity}'
                )


class Ship(Transport):
    '''Class representing an ship'''
    transport_type = 'water transport'

    def __init__(self, max_speed, max_capacity, type_of_ship):
        super().__init__(max_speed, max_capacity)
        self.type_of_ship = type_of_ship

    def __str__(self):
        return (f'This is ship,  {self.get_transport_type()}\n'
                f'max speed {self.get_max_speed()}')

    def get_transport_type(self):
        return (f'Type {Ship.transport_type} with a max'
        f'capacity of {self.max_capacity} persons to transport')

    def get_max_speed(self):
        return f'{self.max_speed} km/h'

class Train(Transport):
    '''Class representing a train'''
    transport_type = 'rail transport'

    def __init__(self, max_speed, max_capacity,type_of_train, stations):
        super().__init__(max_speed, max_capacity)
        self.type_of_train = type_of_train
        self.stations = stations

    def __str__(self):
        return (f'This is a Train, {self.get_transport_type()}, model {self.type_of_train}\n'
                f'Train Stations: {self.stations} \n'
                f'max speed {self.get_max_speed()}, max capacity {self.max_capacity}'
                )
    def __contain__(self, station):
        return station in self.stations

    def get_transport_type(self):
        return f'It is a {Train.transport_type} train'

    def get_max_speed(self):
        return f'{self.max_speed} km/h'



class Plane(Transport):
    '''Class representing a plane'''
    transport_type = 'air transport'
    def __init__(self, max_speed, max_capacity, type_of_plane):
        super().__init__(max_speed, max_capacity)
        self.type_of_plane = type_of_plane

  #overiding the magic methods
    def __str__(self):
        return (f'This is a plane {self.transport_type}, type of {self.type_of_plane}'
                f'with a max capacity of {self.max_capacity} persons to transport \n'
                f'Max speed {self.get_max_speed()}')

    def __eq__(self, other):
        return self.type_of_plane == other.type_of_plane

    def get_transport_type(self):
        return (f'{self.transport_type} with a max capacity of'
                f'{self.max_capacity} persons to transport \n')

    def get_max_speed(self):
        return f'{self.max_speed} km/h'

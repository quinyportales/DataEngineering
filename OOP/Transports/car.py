"""Module contains the class Transport"""
from transports import Transport

class Car(Transport):
    '''Class representing a car'''
    transport_type : str = 'road transport'

    def __init__(self, max_speed: float, max_capacity: int, model: str, brand: str):
        """Initialize a Car instance.

        Args:
            max_speed: float - Maximum speed of the car in km/h.
            max_capacity: int - Maximum number of people the car can transport.
            model: str - Model of the car.
            brand: str - Brand of the car.
        """
        super().__init__( max_speed, max_capacity)
        self.vehicle: str = 'Car'
        self.model : str = model
        self.brand : str = brand
        self._wheel_number : int = 4

    def get_transport_type(self) -> str :
        """Return the transport type of the car."""
        return f'{Car.transport_type}'

    def get_max_speed(self) -> float :
        """Return the maximum speed of the car."""
        return f'{self.max_speed}'

    #overiding magic method
    def __add__(self, other : Transport) -> float:
        """Add two transport objects to combine their capacities.

        Args:
            other: Transport - Another instance of transport class.

        Returns:
            float: Combined maximum speed of both transport objects.
        """

        combined_capacity = self.max_speed + other.max_speed
        return combined_capacity

    def __str__(self) -> str :
        """String representation of the Car instance."""
        return (f'This is a {self.vehicle} {self.model} {self.brand}\n'
                 f'max capacity {self.max_capacity} persons to transport\n'
                 f'max speed {self.get_max_speed()} km/h \n'
                 f'type of transport {self.get_transport_type()}')

    @property
    def wheel_number(self) -> int :
        """Returns the non-public attribute _wheel_number."""
        return self._wheel_number


class ElectricCar(Car):
    """Class representing an electric car."""


    def __init__(self, max_speed: float, model: str, brand : str, 
                 battery_voltage : float, max_capacity: int = 4):
        """Initialize an ElectricCar instance.

        Args:
            max_speed: float - Maximum speed of the electric car in km/h.
            model: str - Model of the electric car.
            brand: str - Brand of the electric car.
            battery_voltage: float - Voltage of the electric car's battery.
            max_capacity: int, optional - Maximum capacity of the electric car. Defaults to 4.
        """
        super().__init__(max_speed, max_capacity, model, brand)
        self.battery_voltage : float = battery_voltage

    def __str__(self) -> str :
        """String representation of the ElectricCar instance."""
        return (f'This is an Electric Car {self.model} {self.brand} \n'
                f' with a battery of {self.battery_voltage}V max speed {self.max_speed} km/h \n'
                f'max capacity {self.max_capacity}'
                )

"""Module contains the class Transport"""
from abc import ABC, abstractmethod
from vehicle import Vehicle


class Transport(ABC, Vehicle):
    """Parent class representing type of transport"""
    _has_engine: bool = True
    vehicles_created: int = 0

    def __init__(self,max_speed: float, max_capacity: int ) -> None:
        """
        Initialize a Transport instance.
        
        Args:
            max_speed: float - Maximum speed of the transport in km/h.
            max_capacity : int - Maximum capacity of the transport.
            manufacture_year : int, optional - Year of manufacture. Defaults to None.
            is_operational : bool, optional - Operational status. Defaults to None.
        """
        super().__init__()
        self.max_speed: float = max_speed
        self.max_capacity: int = max_capacity
        Transport.vehicles_created += 1

    @staticmethod
    def get_total_vehicles() -> int :
        """Returns the total number of vehicles created."""
        return f'Total vehicles created: {Transport.vehicles_created}'


    #overiding the magic methods
    def __str__(self) -> str :
        """String representation of the transport object."""
        return f'{self.transport_type} {self.max_speed}'

    def __len__(self) -> int :
        return self.max_capacity

    def __call__(self, message) -> str :
        return f"Transport says: {message}"

    @staticmethod
    def print_class_hierarchy(instance: Vehicle) -> None:
        """Print out the class hierarchy"""
        class_name = type(instance).__name__
        base_classes = [base.__name__ for base in type(instance).__bases__]
        print(f'Instance name: {instance}')
        print(f'Instance of class: {class_name}')
        print(' ---> Parent class:', ' ---> '.join(base_classes))
        print('\n')

    @property
    @abstractmethod
    def transport_type(self) -> None :
        """Abstract property to ensure child classes define a transport type."""

    @abstractmethod
    def get_transport_type(self) -> None :
        'return the transport type'

    @abstractmethod
    def get_max_speed(self) -> None :
        'return the max speed'

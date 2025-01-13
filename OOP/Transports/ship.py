"""Module contains the  class Ship"""
from transports import Transport

class Ship(Transport):
    """Class representing a ship."""
    transport_type : str = 'water transport'

    def __init__(self, max_speed : float, max_capacity: int, type_of_ship: str) -> None:
        """Initialize a Ship instance.

        Args:
            max_speed : float - Maximum speed of the ship in km/h.
            max_capacity: int - Maximum number of people the ship can transport.
            type_of_ship: str - Type of ship  (e.g., motorboat, yate).
        """
        super().__init__(max_speed, max_capacity)
        self.type_of_ship : str = type_of_ship

    # Overriding the magic methods
    def __str__(self) -> str:
        """String representation of the Ship instance."""
        return (f'This is ship,  {self.get_transport_type()}\n'
                f'max speed {self.get_max_speed()}')

    def get_transport_type(self) -> str :
        """Return the transport type and capacity of the train."""
        return (f'Type {Ship.transport_type} with a max'
        f'capacity of {self.max_capacity} persons to transport')

    def get_max_speed(self) -> str :
        """Return the maximum speed of the ship."""
        return f'{self.max_speed} km/h'

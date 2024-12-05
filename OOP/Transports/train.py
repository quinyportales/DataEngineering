"""Module contains the  class Train"""
from transports import Transport

class Train(Transport):
    """Class representing a train."""

    transport_type : str = 'rail transport'

    def __init__(self, max_speed : float , max_capacity : int ,
                 type_of_train : str , stations : list[str]) -> None:
        """Initialize a Train instance.

        Args:
            max_speed : float - Maximum speed of the train in km/h.
            max_capacity: int - Maximum number of people or the cargo capacity 
            that the train can transport.
            type_of_train: str - Type of train (e.g., passenger train, cargo trains)
            stations: list(str) - List of stations the train serves.
        """
        super().__init__(max_speed, max_capacity)
        self.type_of_train : str = type_of_train
        self.stations : list[str] = stations

    def __str__(self) -> str :
        """String representation of the Train instance."""
        return (f'This is a Train, {self.get_transport_type()}, model {self.type_of_train}\n'
                f'Train Stations: {self.stations} \n'
                f'max speed {self.get_max_speed()}, max capacity {self.max_capacity}'
                )

    def __contains__(self, station: str) -> bool:
        """Check if a station is in the list of train stations.

        Args:
            station (str): Station to check.
        Returns:
            bool: True if the station is served by the train, False otherwise."""
        return station in self.stations

    def get_transport_type(self) -> str :
        """Returns the transport type of the train."""
        return f'It is a {Train.transport_type} train'

    def get_max_speed(self) -> str :
        """Return the maximum speed of the train."""
        return f'{self.max_speed} km/h'

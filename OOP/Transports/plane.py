"""Module contains the class Plane."""
from transports import Transport

class Plane(Transport):
    """Class representing a plane."""

    transport_type: str = 'air transport'

    def __init__(self, max_speed: float, max_capacity: int, type_of_plane: str) -> None:
        """Initialize a Plane instance.

        Args:
            max_speed : float - Maximum speed of the plane in km/h.
            max_capacity: int - Maximum number of people the plane can transport.
            type_of_plane: str - Type of aerial transport (e.g., plane, helicopter).
        """
        super().__init__(max_speed, max_capacity)
        self.type_of_plane: str = type_of_plane

    # Overriding the magic methods
    def __str__(self) -> str:
        """String representation of the Plane instance."""
        return (f"This is a {self.type_of_plane}, a type of {self.transport_type}.\n"
                f"Max capacity: {self.max_capacity} persons.\n"
                f"Max speed: {self.get_max_speed()}.")

    def __eq__(self, other_plane: 'Plane') -> bool:
        """Check equality based on type_of_plane.
        Returns: True if the type_of_plane is the same; False otherwise.
        """
        return self.type_of_plane == other.type_of_plane

    def get_transport_type(self) -> str:
        """Return the transport type and capacity of the plane."""
        return (f"{self.transport_type} with a max capacity of "
                f"{self.max_capacity} persons.")

    def get_max_speed(self) -> str:
        """Return the maximum speed of the plane."""
        return f"{self.max_speed} km/h"

"""Module contains the super class Vehicle"""

class Vehicle:
    class Vehicle:
        """ 
        Base class representing a generic vehicle.
        """

    _class_manufacture_year: int = None
    _class_is_operational : bool = True

    def __init__(self, manufacture_year=None, is_operational=None) -> None:
        """
        Initialize a Vehicle instance.

        Args:
            manufacture_year: int, optional - Year of manufacture. Defaults to class-level value.
            is_operational : bool, optional - Operational status. Defaults to class-level value.
        """
        self._manufacture_year : int = manufacture_year or Vehicle._class_manufacture_year
        self._is_operational : bool = is_operational if is_operational is not None else Vehicle._class_is_operational
    

    @property
    def manufacture_year(self) -> int:
        """get the instance-level property for _manufacture_year """
        return self._manufacture_year

    @manufacture_year.setter
    def manufacture_year(self, year: int) -> None:
        """_manufacture_year setter"""
        self._manufacture_year = year

    @property
    def is_operational(self) -> bool:
        """get the instance-level property for _is_operational """
        return self._is_operational

    @is_operational.setter
    def is_operational(self, status: bool) -> None:
        """is_operational setter"""
        self._is_operational = status

    
    def __str__(self) -> str:
        """String representation of the vehicle object."""
        return (f"Manufacture Year: {self.manufacture_year}, "
                f'Is Operational: {self.is_operational}')


    @classmethod
    def set_common_attributes(cls, manufacture_year: int, is_operational: bool) -> None:
        """
        Set class-level manufacture_year and is_operational for all future instances.

        Args:
            manufacture_year: int, optional - Year of manufacture.
            is_operational : bool, optional - Operational status.
        """
        cls._class_manufacture_year = manufacture_year
        cls._class_is_operational = is_operational

    @classmethod
    def get_common_attributes(cls) -> str:
        """
        Retrieve the common attributes set at the class level.
        """
        return (f"Class Manufacture Year: {cls._class_manufacture_year}, "
                f"Class Is Operational: {cls._class_is_operational}")
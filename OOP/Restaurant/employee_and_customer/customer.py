"""Module Contains classes Customer """

class Customer:
    """Models a customer in a restaurant system with unique IDs and order history."""
    #initializing the uniques id's

    _id_counter : int = 1

    def __init__(self,name: str,address: str,phone: str) -> None:
        """
        Initialize a Customer instance.

        Parameters:
        name: str - Name of the customer.
        address: str - Address of the customer.
        phone: str - Phone number of the customer.
        """
        self.name: str =name
        self.address: str =address
        self.phone: str =phone

        #auto increment ID for every customer
        self._cust_id: int = Customer._id_counter
        Customer._id_counter += 1

        self._historial: list[dict[str, str]]= []

    @property
    def cust_id(self) -> int:
        """getter for _cust_id"""
        return self._cust_id

    @property
    def historial(self) -> list [dict [str, str]]:
        """getter for _historial"""
        return self._historial

    def __str__(self) -> str:
        """Returns the string representation for the Customer instance."""
        return(f'ID: {self.cust_id}\n'
            f'Name: {self.name.title()}\n'
            f'Address:{self.address}\n'
            f'Phone: {self.phone} \n')

    def add_to_historial(self, item_date: str, item_name: str)-> None:
        """
        Add elements to the customer's history.

        Parameters:
        item_date: str - Date of the order.
        item_name: str - Name of the item ordered.
        """
        self._historial.append({'date': item_date,'ordered item': item_name})

    def show_historial(self) -> None:
        """
        Prints out the customer's order history.
        """
        print(f'{self.name.title()} order history:')
        for i in self.historial:
            print(f"Date: {i['date']}\n"
                  f"Ordered Items: {i['ordered item']}"
                  )

"""Module Contains classes Table and Menu"""


class Table:
    """Details for each table on restaurant"""
    #initializing the uniques id's

    _id_counter: int = 1

    def __init__(self, capacity: int, available: bool=True) -> None:
        """
        Initialize a Table instance.

        Parameters:
        capacity: int - Max number of seats for this table.
         available: bool - False if the table has been assigned to a customer
        """
        self.capacity: int = capacity
        self.available: bool = available
        self.assigned_customer: int = None
        #auto increment ID for every table
        self._table_id: int = Table._id_counter
        Table._id_counter+=1

    @property
    def table_id(self):
        """table_id getter"""
        return self._table_id

    def __str__(self)-> str:
        return f"Table {self.table_id} - Available: {self.available} - Capacity: {self.capacity}"

    def __repr__(self) -> str:
        return self.__str__()

    def assign_table(self, customer: int) -> None:
        """Associates a table with a customer and updates its availability"""
        if self.available:
            self.assigned_customer=customer
            self.available=False
            print(f'Table {self.table_id} sucessfully assigned to Customer ID: {customer}')
            return
        print('This table is taken, please assign a different table')


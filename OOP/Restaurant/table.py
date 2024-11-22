"""Module Contains classes Table and Menu"""

class Table:
    """Details for each table on restaurant"""
    #initializing the uniques id's
    _id_counter = 1 
    def __init__(self, capacity, available=True) -> None:

        self.capacity=capacity
        self.available=available
        self.assigned_customer=None

        #auto increment ID for every table
        self._table_id=Table._id_counter
        Table._id_counter+=1
    @property
    def table_id(self):
        """table_id getter"""
        return self._table_id

    def __str__(self):
        return f"Table {self.table_id} - Available: {self.available} - Capacity: {self.capacity}"

    def __repr__(self):
        return self.__str__()

    def assign_table(self, customer):
        """Associates a table with a customer and updates its availability"""
        if self.available != None:
            self.assigned_customer=customer
            self.available=False
            print(f'Table {self.table_id} sucessfully assigned to Customer ID: {customer}')
            return
        print('This table is taken, please assign a different table')

    def get_table_status(self):
        """return if the table is available"""
        return self.available



class Menu:
    """This class contain all the items and their categuries from the menu"""
    def __init__(self) -> None:
        self.menu_items ={}

    def add_menu (self, dic_items):
        """add multiple items to menu"""
        for category,item in dic_items.items():
            if category in self.menu_items:
                self.menu_items[category].update(item)
            else:
                self.menu_items[category]=item

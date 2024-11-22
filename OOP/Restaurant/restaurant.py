"""Module Contains classes Restaurant, Customer classes"""

class Restaurant:
    """Manages the restaurant and its clases as Menu, Employees, Tables and Stock"""
    def __init__(self, name, address, menu, stock) -> None:
        self.name=name
        self.address=address
        self.menu=menu
        self.stock=stock
        self.employees=[]
        self.tables=[]


    def add_employees(self, employees):
        """Take a dictionary of employees and added to Restaurant staff"""
        self.employees.extend(employees)

    def show_employees(self):
        """Show the details for each employee"""
        for employee in self.employees:
            print(f'Employee ID {employee.employee_id}\n'
                  f'Employee Name {employee.name.title()}\n'
                  f'Employee Salary: {employee.salary}\n')

    def add_tables(self, tables):
        """Take a dictionary of tables and added to restaurant"""
        self.tables.extend(tables)

    def show_tables(self):
        """Show the details for each table on restaurant"""
        for table in self.tables:
            print(f'Table ID {table.table_id} '
                  f'Capacity: {table.capacity} '
                  f'Available: {table.available} ')
            if table.available==False:
                print(f'Assigned to Customer ID: {table.assigned_customer}\n')

    def show_menu(self):
        """Display the menu with its categories, items, prices"""
        for category in self.menu.menu_items:
            print(f'Category: {category.title()}')
            for item in self.menu.menu_items[category]:
                print(f'Item: {item.title()}')

    def show_stock(self):
        """Shows the available quatities per item"""
        for item, qty in self.stock.inventory.items():
            print(f'Item: {item} ---> Quantity: {qty}')


class Customer:
    """Contains the data for customers restaurant"""
    #initializing the uniques id's
    _id_counter = 1

    def __init__(self,name,address,phone) -> None:
        self.name=name
        self.address=address
        self.phone=phone

        #auto increment ID for every customer
        self._cust_id=Customer._id_counter
        Customer._id_counter += 1

        self._historial=[]

    @property
    def cust_id(self):
        """getter for _cust_id"""
        return self._cust_id

    @property
    def historial(self):
        """getter for _hist_id"""
        return self._historial

    def add_to_historial(self,item):
        """Add elements to customer historial
        Element: dictionary item: order date
        """
        self._historial.append({'date': item.date,'ordered item': item.item_name})

    def show_customer(self):
        """Prints out the detais for a single customer"""
        print(f'ID: {self.cust_id}\n'
            f'Name: {self.name.title()}\n'
            f'Address:{self.address}\n'
            f'Phone: {self.phone} \n')

    def show_historial(self):
        """Prints out the customer order history"""
        print(f'{self.name.title()} order history:')
        for i in self.historial:
            print(f"Date: {i['date']}\n"
                  f"Ordered Items: {i['ordered item']}"
                  )

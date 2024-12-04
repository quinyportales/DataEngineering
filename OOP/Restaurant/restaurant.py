"""Module Contains the Restaurant class"""
from table_and_mobiliary.table import Table
from employee_and_customer.employee import Employee
from menu.stock import Stock
from menu.menu_class import Menu


class Restaurant:
    """Manages the restaurant and its clases as Menu, Employees, Tables and Stock"""

    def __init__(self, name: str, address: str, menu: Menu, stock: Stock) -> None:
        """
        Initialize a Restaurant instance.

        Parameters:
        name: str - Name of the Restaurant.
        address: str - Address of the Restaurant.
        menu: Menu - Instance of the class Menu.
        stock: Stock - Instance of the class Stock.

        """
        self.name: str = name
        self.address: str = address
        self.menu: Menu = menu
        self.stock: Stock = stock
        self.employees: list [Employee] = []
        self.tables: list[Table] = []

    def add_employees(self, employees: list[Employee]) -> None:
        """Take a dictionary of employees and added to Restaurant staff"""
        self.employees.extend(employees)

    def show_employees(self) -> None:
        """Show the details for each employee"""
        for employee in self.employees:
            print(f'{employee}\n')

    def add_tables(self, tables: list[Table ]) -> None:
        """Take a list of tables and added to restaurant"""
        self.tables.extend(tables)

    def show_tables(self)-> None:
        """Show the details for each table on restaurant"""
        for table in self.tables:
            print(f'Table ID {table.table_id} '
                  f'Capacity: {table.capacity} '
                  f'Available: {table.available} ')
            if table.available is False:
                print(f'Assigned to Customer ID: {table.assigned_customer}\n')

    def show_menu(self) -> None:
        """Display the menu with its categories, items, prices"""
        for category, items in self.menu.menu_items.items():
            print(f'Category: {category.title()}')
            for item_name, price in items.items():
                print(f'{item_name.title()}, Price: HUF{price:}')

    def show_stock(self) -> None:
        """Shows the available quatities per item"""
        for item, qty in self.stock.inventory.items():
            print(f'Item: {item} ---> Quantity: {qty}')

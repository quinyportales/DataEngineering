"""This module implements the classes for a restaurant representation"""

from restaurant import Restaurant, Customer
from employee import Employee
from table import Table, Menu
from item import Delivery, Item, OrderedItem, Payment, Stock, Order

if __name__=='__main__':

    #instanciating Customer
    customer1=Customer('customer1', 'Street 1', '12345678', )

    #Instantiating Employee
    employee1=Employee('employee1', 'waiter', 1000)
    employee2=Employee('employee2', 'delivery driver', 1500)
    employee3=Employee('employee3', 'chef', 2000)


    #instantiating Table
    table1=Table(capacity=4)
    table2=Table(capacity=4)

    #instantiating Menu
    menu=Menu()

    #instantiating Stock
    stock=Stock()

    #instatiating Item
    item1=Item('entrance','item 1', 100)
    item2=Item('entrance','item 2', 200)
    item3=Item('main course','item 3', 300)
    item4=Item('main course','item 4', 400)
    item5=Item('dessert','item 5', 100)
    item6=Item('dessert','item 6', 200)

    #adding the items to menu
    item1.add_item(menu)
    item2.add_item(menu)
    item3.add_item(menu)
    item4.add_item(menu)
    item5.add_item(menu)
    item6.add_item(menu)

    #adding the items to stock
    stock.add_stock(item1.item_name, 5)
    stock.add_stock(item2.item_name, 10)
    stock.add_stock(item3.item_name, 15)
    stock.add_stock(item4.item_name, 5)
    stock.add_stock(item5.item_name, 10)
    stock.add_stock(item6.item_name, 15)

    #instantiating Restaurant
    restaurant=Restaurant('Great Restaurant', 'Budapest', menu, stock )
    restaurant.add_employees([employee1,employee2, employee3])
    restaurant.add_tables([table1, table2])
    print('\n *************PRINTING Restaurant INFO************** \n')
    print('**EMPLOYEES**')
    restaurant.show_employees()
    print('**TABLES**')
    restaurant.show_tables()
    print('**MENU**')
    restaurant.show_menu()
    print('**STOCK**')
    restaurant.show_stock()

    #Assigning tables
    print(f'Table {table1.table_id} is assigned to {table1.assigned_customer}')
    table1.assign_table(customer1.cust_id)

    #ORDER FLOW

    #instatiating ordered item
    print('\n ***ORDERING ITEMS***')

    ordered_item1= OrderedItem("2024-11-20",item1, 2, customer1)
    ordered_item1.show_details()
    ordered_item2= OrderedItem("2024-11-22",item5, 5, customer1)
    ordered_item2.show_details()

    #instatiating orders
    order1 = Order(customer1)
    order1.add_item(ordered_item1)
    order1.add_item(ordered_item2)
    order1.show_details()
    #processing payment
    payment = Payment(order1, 'Credit Card')
    payment.process_payment()

    #updating stock and customer history
    print('-->updating stock')
    stock.deduct_item(ordered_item1)
    stock.deduct_item(ordered_item2)

    print('-->Customer historial')
    customer1.add_to_historial(ordered_item1)
    customer1.add_to_historial(ordered_item2)
    customer1.show_historial()

    print('\n ***Showing delivery details***')
    #Instantiating the delivery
    delivery=Delivery(order1, employee2, customer1)
    delivery.start_delivery()
    delivery.show_delivery_details()
    print('-->Completing the delivery')
    delivery.complete_delivery()


"""Implement the transport clases"""
from vehicle  import Vehicle
from transports  import Transport
from car import Car, ElectricCar 
from ship import Ship 
from train import Train
from plane import Plane

if __name__ == '__main__':

    instances_list = []
    # Creating the instances
    car1 = Car(180, 4, 'Camry', 'Toyota')
    ship1 = Ship(50, 10, 'Motorboat')
    train1 = Train(160, 100, 'Passenger Train', ['Nyugaty', 'Keleti' ])
    plane1 = Plane(150, 2, 'Helicopter')
    plane2 = Plane(200, 100, 'Airplane')
    elec_car1 = ElectricCar(120, "Model S", "Tesla", 800)

    #printing the classes and super classes
    instances_list.extend([car1, ship1, train1, plane1, plane2, elec_car1])
    for instance in instances_list:
        Transport.print_class_hierarchy(instance)

    #checking the ancestor classes
    print(f'printing MRO for Electric Car Class {ElectricCar.mro()}\n')

    #Total of transports created
    print(Transport.get_total_vehicles())

    #Checking  the magic method
    print ('\n Printing the len for car1 and train1:\n')
    print (f'Len of car 1 {len(car1)}')
    print (f'Len of train 1 {len(train1)}\n')

    print ('Are plane1 and plane2 equals?')
    print (plane1 == plane2)
    print(f'Comparing {plane1.type_of_plane} with {plane2.type_of_plane}\n')

    print(elec_car1('I am an electric car and I was called as a function \n'))

    print(f'Adding car1 and elec_car1 velocities {car1+elec_car1} km/h')

    print('Checking if train stops at Nyugaty station')
    print('Nyugaty' in train1.stations)


    #testing the class methods
    print('\n***Testing the class methods***')
     # setting the attributes at the class level
    Vehicle.set_common_attributes(2015, False)
    print(Vehicle.get_common_attributes()) 

    #creating an instance using the default values
    car_def = Vehicle()
    print(car_def)

    # Changing the instance attributes
    car_def.manufacture_year = 2020
    car_def.is_operational = True
    print(car_def)
    # Now testing creating another instance
    # this one will be created with the attributes set it by
    # Vehicle.set_common_attributes(2015, False)
    bike_def = Vehicle()
    print(bike_def)

    

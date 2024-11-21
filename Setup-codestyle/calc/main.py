"""Implementing the class Calculator"""

from calc import Calculator

if __name__=='__main__':

    num=list(range(3,8))
    calc1=Calculator()

    #Checking additon
    print(f'The consecutive sum of {num} is equal to {calc1.addition(*num)}\n')

    #Checking substraction
    print(f'The consecutive rest of {num} is equal to {calc1.subtraction(*num)}\n')

    #Checkin the multiplication
    print(f'The consecutive multiplication of {num} is equal to {calc1.multiplication(*num)}\n')

    #Checking the division
    print(f'The result of division {num[-1]} / {num[0]} is {calc1.division(num[-1],num[0])} \n')
    print(f'If I try a cero division'
          f'{calc1.division(num[-1],0)}')

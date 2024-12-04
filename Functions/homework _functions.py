"""
1. You need to write a function that will convert the specified number to the specified number system.
The function takes two arguments as input: a number and a number system.

Expected output:
    B13
    101100010011
"""

from functools import reduce
from math import remainder
from typing import Union
import time


def convert_to(num: int, base: int) -> Union[str, int]:
    if base >= 2 and base <= 16:
        # Range to represent any numerical system
        digits = "0123456789ABCDEF"
        division = num
        converted = ''
        
        while division > 0:
            remainder = division % base
            converted = digits[remainder] + converted
            # Floor division 
            division //= base  
            
        return converted
    else:
        print("Base must be a number between 2 and 16")

print(convert_to(2835, 16))
print(convert_to(2835, 2))

"""
2. You need to write a function of recursion list sum.
The function takes a list as input.

Expected output:
    30
"""


def sum_recursive_list(data: list) -> int:
    total = 0
    for elem in data:
        if isinstance(elem, list):
            #calling itself
            total += sum_recursive_list(elem)
        else:
            total += elem
    return total
  

print(sum_recursive_list([1, 2, [3, 4], [5, 6, [2, 3, 4]]]))

"""
3. You need to write a Python program to find the greatest common divisor (gcd) of two integers.
The function takes two integer values as input.

Expected output:
    2
    5
    25
"""


def calculate_gcd(a: int, b: int) -> int:
    #Euclides algorithm
    while b != 0:
        a, b = b, a % b
    return a

print(calculate_gcd(12, 14))
print(calculate_gcd(15, 25))
print(calculate_gcd(75, 25))

"""
4. You need to write a function that returns the first n rows of Pascal's triangle.
Each number is the two numbers above it added together.
The function takes the number of triangle rows.

Expected output:
    [
        [1],
        [1, 1],
        [1, 2, 1],
        [1, 3, 3, 1],
        [1, 4, 6, 4, 1],
        [1, 5, 10, 10, 5, 1],
    ]
"""


def get_pascal_triangle(n: int) -> list:
    triangle = []

    for i in range(n):
        row = [1]
        if i > 0:
            for j in range(1, i):
                row.append(triangle[i-1][j-1] + triangle[i-1][j])
            row.append(1)
        triangle.append(row)

    return triangle

print(get_pascal_triangle(6))

"""
5. You need to write a program to find whether a given string starts with a given character using Lambda.
The function takes a word and a letter as input.

Expected output:
    True
    False
"""

starts_with = lambda word,char: word[0]==char 
print(starts_with('Python', 'P'))
print(starts_with('Java', 'P'))

"""
6. You need to write a program to create Fibonacci series upto n using Lambda and reduce. It's a hard task.
The function takes as input the number of Fibonacci numbers to be calculated.

Expected output:
    [0, 1, 1, 2, 3, 5]
"""

from functools import reduce

#base condition [0, 1]
fib_series =  lambda n: reduce(lambda acc, _: acc + [acc[-1] + acc[-2]], range(n - 2), [0, 1])
'''n=6:
init: 
acc=[0,1]
first iter: [0,1,1] (0+1)
sec iter: [0,1,1,2] (1+1)
third iter : [0,1,1,2, 3] (1+2)...
'''

print(fib_series(6))

"""
7. You need to write a program to find intersection of two given arrays using Lambda and filter.
You are given two lists, the result will be a list-intersection of the given ones.

Expected output:
    [1, 2, 8, 9]
"""

first = [1, 2, 3, 5, 7, 8, 9, 10]
second = [1, 2, 4, 8, 9]
result = list(filter(lambda i: i in first, second))
print(result)

"""
8. You need write a program to find palindromes in a given list of strings using Lambda and filter.
According Wikipedia - A palindromic number or numeral palindrome is a number that remains the same
when its digits are reversed. Like 16461, for example, it is "symmetrical".

Expected output:
    ['php', 'sagas', 'repaper', 'madam', 'level']
"""

words = ["php", "sagas", "Python", "abcdefg", "Java", "repaper", "madam", "level"]
result = list(filter(lambda word: word[-1::-1]==word,words))
#print(result)

"""
9.  You need write a Python program to add three given lists using Python map and lambda.
You are given three lists, the result will be a list with numbers that are the sum of 
the first values of the given lists, the second values, the third...

Expected output:
    [12, 15, 18]
"""

nums_1 = [1, 2, 3] #x
nums_2 = [4, 5, 6] #y
nums_3 = [7, 8, 9] #z
result = list(map(lambda x,y,z: x+y+z, nums_1, nums_2,nums_3))
print(result)

"""
10. You need a program to make a chain of function decorators (bold, italic, underline etc.).
Apply the string formatting that is given as input to the function.

Expected output:
    <b><i><u>Hello world</u></i></b>
"""


def make_bold(func):
    def wrapper():
        result=func()
        return ('<b>'+ result+ '</b>')
    return wrapper



def make_italic(func):
    def wrapper():
        result=func()
        return ('<i>'+ result+ '</i>')
    return wrapper

def make_underline(func):
    def wrapper():
        result=func()
        return ('<u>'+ result+ '</u>')
    return wrapper


@make_bold
@make_italic
@make_underline
def hello():
    return "Hello world"


print(hello())


"""
11. You need to implement a decorator that calculates the execution time of the function.

Expected output:
    sum_linear_progression finished in 0:00:28.791659 (*here is your time)
    500000000500000000
    sum_constant_progression finished in 0:00:00
    500000000500000000
"""


def timeit(fun):
    def wrapper(*args, **kwargs):
        time_ini = time.time()
        fun(*args, **kwargs)
        time_fin = time.time()
        exec_time= time_fin - time_ini
        print(f'{fun} finished in {exec_time}')
        return fun(*args, **kwargs)
    return wrapper


# OR


class Timeit:
    def __init__(self, fun):
        self.fun= fun
    def __call__(self, *args, **kwds):
        self.time_ini = time.time() #when class is called this is initialized
        self.time_fin = time.time() #fun ran, we got the time
        print(f'{self.fun} finished in {self.time_fin - self.time_ini}')
        return self.fun(*args, **kwds)
        

@timeit
def sum_linear_progression(n):
    return sum(range(n + 1))

'''
@Timeit
def sum_linear_progression(n):
    return sum(range(n + 1))
'''

@timeit
def sum_linear_progression(n):
    return sum(range(n + 1))


@timeit
def sum_constant_progression(n):
    return n * (n + 1) // 2


print(sum_linear_progression(100_000_000))
print(sum_constant_progression(100_000_000))

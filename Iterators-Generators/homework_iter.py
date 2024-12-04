"""
1. You need to implement the class MyEnumerate in such a way
that the result of passing through the loop gives the expected value.
The class constructor accepts a value as a character string.
You need to iterate over the characters and output the result like <character index> : <character>

Expected output:
    0 : a
    1 : b
    2 : c
    3 : d
    4 : f
"""


class MyEnumerate:
    def __init__(self, data: str) -> None:
        self.data = data
        self.index = 0 

    def __iter__(self) -> iter:
        #iterators return themselves
        return self  

    def __next__(self) -> tuple[int, str]:
        #it will only iterate while we have elements
        if self.index < len(self.data):  
            result = (self.index, self.data[self.index])  
            self.index += 1  
            return result
        else:
            raise StopIteration 


for index, letter in MyEnumerate('abcdf'):
    print(f'{index} : {letter}')


"""
2. You need to implement the classes CircleIterator and Circle in such a way
that the result of passing through the loop gives the expected value.
Circle class constructor accepts a value as a string of characters and the number of characters in the resulting list.
You need to loop through the symbols until you reach the maximum number of symbols.

Expected output:
    ['a', 'b', 'c', 'a', 'b']
"""


class CircleIterator:
    def __init__(self, data: str, max_times: int) -> None:
        self.max_time = max_times
        self.data =data
        self.index = 0

        if self.max_time> len(self.data):
            extend = self.max_time - len(self.data)
            self.data_extended = self.data + self.data[0: extend]

    def __next__(self) -> tuple[int, str]:
        if self.index< self.max_time:
            result = self.data_extended[self.index]
            self.index += 1
            return result

        else:
            raise StopIteration


class Circle:
    def __init__(self, data: str, max_times: int) -> None:
        self.data = data
        self.max_times = max_times
            
    def __iter__(self) -> iter:
        return CircleIterator(self.data, self.max_times)



c = Circle('abc', 5)
print(list(c))

"""
3. You need to create a generator function that iterates over prime numbers up to the limit.
The function takes as input an integer value, up to which we will go by prime numbers.

Expected output:
    2 3 5 7
"""


def gen_primes(limit: int):
    primes = []  
    for num in range(2, limit + 1):
        for prime in primes:
            if num % prime == 0:
                #if it's divisible by a prime is not prime
                break
        else:
            primes.append(num)  
            yield num


for i in gen_primes(10):
    print(i)

"""
4. You need to use the list comprehension to connect the numbers separated by commas.
(There is a better solution without list comprehension, find it.)

Expected output:
    0,1,2,3,4,5,6,7,8,9,10,11,12,13,14
"""

numbers = range(15)

def gen_num(numbers: list[int]) -> None:
    result = ','.join(str(i) for i in numbers)
    print(result)

gen_num(numbers)

"""
5. You need to use the list comprehension to take the numbers separated by spaces from the string and sum them up.
Expected output:
    Sum: 100
"""


numbers = '10 abc 20 de44 30 55fg 40'

def sum_str(numbers: str) -> None:
    total = sum([int(num) for num in numbers.split() if num.isnumeric()==True])
    print(f'Sum: {total}')

sum_str(numbers)

"""
6. You need to use the list comprehension to swap keys and values in a dictionary.
Expected output:
    {1: 'a', 2: 'b', 3: 'c'}
"""


d = {'a': 1, 'b': 2, 'c': 3}

def flipped_dic(d: dict[str, int]) -> None:
    flipped_d = dict([(b,a) for (a,b) in d.items()])
    print(flipped_d)

flipped_dic(d)


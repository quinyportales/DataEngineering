"""
Calculator class : addition, subtraction, multiplication, and division.
"""

class Calculator:

    """
    Methods:
    addition: Returns the sum of multiple numbers.
    subtraction: Returns the difference between multiple numbers.
    multiplication: Returns the product of multiple numbers.
    division: Returns the quotient of two numbers, raises an exception for division by zero.
    """

    def addition(self, *args):
        """
        Addition of any number of arguments.

        Parameters:
        *args (float): Numbers to add.

        Returns:
        float: The sum of all provided numbers.
        """
        return sum(args)

    def subtraction(self, *args):
        """
        Subtraction of any number of arguments.

        Parameters:
        *args (float): Subtracting the second number and onwards from the first.

        Returns:
        float: The result of subtracting all the provided numbers in sequence.
        """
        if len(args) < 2:
            raise ValueError("At least two numbers are required for subtraction.")
        result = args[0]
        for num in args[1:]:
            result -= num
        return result

    def multiplication(self, *args):
        """
        Multiplication of any number of arguments.

        Parameters:
        *args (float): Numbers to multiply.

        Returns:
        float: The product of all provided numbers.
        """
        if len(args) == 0:
            raise ValueError("At least one number is required for multiplication.")
        result = 1
        for num in args:
            result *= num
        return result

    def division(self, num1, num2):
        """
        Perform division of two numbers.

        Parameters:
        num1 (float): Numerator.
        num2 (float): Denominator.

        Returns:
        float: The result of num1 divided by num2.

        Raises:
        ZeroDivisionError: If num2 is zero.
        """
        if num2 == 0:
            raise ZeroDivisionError("You cannot divide by zero.")
        return num1 / num2

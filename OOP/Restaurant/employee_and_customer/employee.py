"""Module Contains classes Employee """


class Employee:
    """
    Models an employee in a restaurant system with unique IDs, job role, and salary.
    """
    #initializing the uniques id's

    _id_counter: int = 1

    def __init__(self, name: str, job_role: str, salary: float) -> None:
        """
        Initialize an Employee instance.

        Parameters:
        name: str - Name of the employee.
        job_role: str - Role or position of the employee.
        salary: float - Monthly pay
        """
        self.name: str = name
        self.job_role: str = job_role
        self.salary: float = salary

        #auto increment ID for every employee
        self._employee_id: int = Employee._id_counter
        Employee._id_counter += 1

    @property
    def employee_id(self) -> int:
        """Getter for the employee's unique ID."""
        return self._employee_id

    def __str__(self) -> str:
        """Returns the string representation for the Employee instance."""
        return(
            f'ID: {self.employee_id}\n'
            f'Name: {self.name.title()}\n'
            f'Job Role: {self.job_role}\n'
            f'Salary: {self.salary}'
            )

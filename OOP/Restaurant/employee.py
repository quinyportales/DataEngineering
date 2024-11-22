"""Module Contains Employee class"""

class Employee:
    """Single employee details"""
    #initializing the uniques id's
    _id_counter = 1
    employees_list=[]
    def __init__(self,name,job_role, salary) -> None:
        self.name=name
        self.job_role=job_role
        self.salary=salary

        #auto increment ID for every employee
        self._employee_id = Employee._id_counter
        Employee._id_counter += 1

    @property
    def employee_id(self):
        """employe_id getter"""
        return self._employee_id

    def show_employee(self):
        """prints out the details for a single employee"""
        print(
            f'ID: {self.employee_id}\n'
            f'Name: {self.name.title()}\n'
            f'Job Role: {self.job_role}\n'
            f'Salary: {self.salary}'
            )

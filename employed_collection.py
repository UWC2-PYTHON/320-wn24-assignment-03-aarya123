from peewee import IntegrityError, DoesNotExist

from models import JobTable, EmployedPersonTable


# A base class that will also contain the database
class BaseCollection:
    def __init__(self, database):
        self.database = database


class JobCollection(BaseCollection):
    def add(self, name, min_wage, max_wage):
        try:
            # Start a transaction that ends when we leave the with function
            with self.database.transaction():
                # Create the object
                result = JobTable.create(
                    name=name,
                    min_wage=float(min_wage),
                    max_wage=float(max_wage),
                )
                # Save it in the db
                result.save()
            return True
        # Catch any errors with duplicate keys (name)
        except IntegrityError:
            return False

    def search(self, name):
        try:
            with self.database.transaction():
                # Find jobs with the same name
                result = JobTable.get(JobTable.name == name)
            return result
        # Catches any errors not finding this record
        except DoesNotExist:
            return None

    def remove(self, name):
        try:
            with self.database.transaction():
                # Find jobs with the same name
                result = JobTable.get(JobTable.name == name)
                # Deletes it
                result.delete_instance()
            return True
        # Catches any errors not finding this record
        except DoesNotExist:
            return False

    def update_wages(self, name, min_wage, max_wage):
        try:
            with self.database.transaction():
                # Find the job
                result = JobTable.get(JobTable.name == name)
                # Update fields
                result.min_wage = min_wage
                result.max_wage = max_wage
                # Save it in the db
                result.save()
            return True
        # Catches any errors not finding this record
        except DoesNotExist:
            return False


# Everything thing here is effectively a duplicate of JobCollection
class EmployedPersonCollection(BaseCollection):
    def add(self, first_name, last_name, job):
        try:
            with self.database.transaction():
                result = EmployedPersonTable.create(
                    first_name=first_name,
                    last_name=last_name,
                    job=job,
                )
                result.save()
            return True
        except IntegrityError:
            return False

    def search(self, first_name):
        try:
            with self.database.transaction():
                result = EmployedPersonTable.get(
                    EmployedPersonTable.first_name == first_name
                )
            return result
        except DoesNotExist:
            return None

    def remove(self, first_name):
        try:
            with self.database.transaction():
                result = EmployedPersonTable.get(
                    EmployedPersonTable.first_name == first_name
                )
                result.delete_instance()
            return True
        except DoesNotExist:
            return False

    def update_job(self, first_name, job):
        try:
            with self.database.transaction():
                result = EmployedPersonTable.get(
                    EmployedPersonTable.first_name == first_name
                )
                result.job = job
                result.save()
            return True
        except DoesNotExist:
            return False

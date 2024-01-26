from unittest import TestCase

from peewee import SqliteDatabase

from employed_collection import JobCollection, EmployedPersonCollection
from models import EmployedPersonTable, JobTable


class TestPeopleCollection(TestCase):
    def setUp(self):
        # Don't use a real database, instead, let's use an in-memory version that gets thrown away once tests are done
        self.database = SqliteDatabase(":memory:", pragmas={"foreign_keys": 1})
        # Bind our tables to this one instead of our people.db file
        self.database.bind([EmployedPersonTable, JobTable])
        # Connect and create tables
        self.database.connect()
        self.database.create_tables([EmployedPersonTable, JobTable])
        # Seeding data
        self.job_collection_instance = JobCollection(self.database)
        self.job_collection_instance.add("lecturer", 10.00, 15.00)
        lecturer = self.job_collection_instance.search("lecturer")
        self.job_collection_instance.add("assistant", 5.00, 10.00)
        assistant = self.job_collection_instance.search("assistant")
        self.employed_person_collection_instance = EmployedPersonCollection(
            self.database
        )
        self.employed_person_collection_instance.add("Anubhaw", "Arya", lecturer)
        self.employed_person_collection_instance.add("John", "Doe", assistant)

    def tearDown(self):
        self.database.drop_tables([EmployedPersonTable, JobTable])
        self.database.close()

    def test_add_job_happy(self):
        name = "student"
        min_wage = 0
        max_wage = 0
        self.assertTrue(self.job_collection_instance.add(name, min_wage, max_wage))
        result = self.job_collection_instance.search(name)
        self.assertIsNotNone(result)
        self.assertEqual(result.name, name)
        self.assertEqual(result.min_wage, min_wage)
        self.assertEqual(result.max_wage, max_wage)

    def test_add_person_happy(self):
        first_name = "Jane"
        last_name = "Smith"
        job = self.job_collection_instance.search("assistant")
        self.assertTrue(
            self.employed_person_collection_instance.add(first_name, last_name, job)
        )
        result = self.employed_person_collection_instance.search(first_name)
        self.assertIsNotNone(result)
        self.assertEqual(result.first_name, first_name)
        self.assertEqual(result.last_name, last_name)
        self.assertEqual(result.job, job)
        job_holders_with_first_name = [
            holder for holder in job.job_holders if holder.first_name == first_name
        ]
        self.assertTrue(len(job_holders_with_first_name) == 1)
        self.assertEqual(job_holders_with_first_name[0], result)

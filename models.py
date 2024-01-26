from peewee import SqliteDatabase, Model, CharField, DoubleField, ForeignKeyField

# Connect to SQLite and ensure foreign_keys are enforced
database = SqliteDatabase("people.db", pragmas={"foreign_keys": 1})
database.connect()


# This base class will automatically bind our models to the sqlite database we're creating
class BaseModel(Model):
    class Meta:
        database = database


class PersonTable(BaseModel):
    # https://docs.peewee-orm.com/en/latest/peewee/models.html?#fields
    first_name = CharField(primary_key=True, max_length=32)
    last_name = CharField(max_length=32)
    position = CharField(max_length=32)


class JobTable(BaseModel):
    name = CharField(primary_key=True, max_length=32)
    min_wage = DoubleField()
    max_wage = DoubleField()


class EmployedPersonTable(BaseModel):
    first_name = CharField(primary_key=True, max_length=32)
    last_name = CharField(max_length=32)
    # This field will refer to a record in the JobTable. A record in the JobTable will also now contain a field called
    # job_holders that contains a list of people that hold this job. Additionally, whenever a job is deleted, the people
    # will also be deleted
    job = ForeignKeyField(JobTable, backref="job_holders", on_delete="CASCADE")


# Creates the table
database.create_tables([PersonTable, EmployedPersonTable, JobTable])
database.close()

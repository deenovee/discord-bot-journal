import sqlalchemy as db
from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData, Float, Insert
from sqlalchemy_utils import database_exists, create_database

class Journal_DB:
    def __init__(self):
        self.engine = create_engine('sqlite:///journal.db')

        if not database_exists(self.engine.url):
            create_database(self.engine.url)

        self.metadata = MetaData()
        self.timekeeper_table = db.Table('timekeeper', self.metadata,
                            Column('id', Integer, primary_key=True, autoincrement=True),
                            Column('date', DateTime),
                            Column('minutes', Integer),
                            Column('description', String),
                            Column('category', Integer)
                            )

        self.journal_table = db.Table('journal', self.metadata,
                        Column('id', Integer, primary_key=True, autoincrement=True),
                        Column('date', DateTime),
                        Column('productivity', Integer),
                        Column('journal', String)
                        )

        self.exercise_table = db.Table('exercise', self.metadata,
                            Column('id', Integer, primary_key=True, autoincrement=True),
                            Column('date', DateTime),
                            Column('exercise_type', Integer),
                            Column('duration', String),
                            Column('effort', Integer),
                            Column('reps', Integer),
                            Column('weight', Float),
                            Column('distance', Float),
                            Column('description', String)
                            )

        self.sleep_table = db.Table('sleep', self.metadata,
                            Column('id', Integer, primary_key=True, autoincrement=True),
                            Column('time_start', DateTime),
                            Column('time_end', DateTime),
                            Column('hours', Float),
                            Column('quality', Integer),
                            Column('nap', String)
                            )

        self.nutrition_table = db.Table('nutrition', self.metadata,
                            Column('id', Integer, primary_key=True, autoincrement=True),
                            Column('date', DateTime),
                            Column('calories', Integer),
                            Column('protein', Integer),
                            Column('carbs', Integer),
                            Column('fat', Integer),
                            Column('pints', Integer),
                            Column('alcohol', Integer),
                            Column('food_type', Integer)
                            )
        
        self.metadata.create_all(self.engine)
        self.table_mapping = self.get_table_mapping()

    def get_table_mapping(self):
        return {
            'timekeeper': self.timekeeper_table,
            'journal': self.journal_table,
            'exercise': self.exercise_table,
            'sleep': self.sleep_table,
            'nutrition': self.nutrition_table
        }
    
    def insert(self, table_name, **kwargs):
        table = self.table_mapping.get(table_name)
        print(table)
        print(kwargs)
        if table is not None:
            with self.engine.connect() as connection:
                ins = Insert(table).values(**kwargs)
                connection.execute(ins)
                connection.commit()
        else:
            raise ValueError(f"Table {table_name} does not exist")

    #view 5 previous records
    def view(self, table_name):
        table = self.table_mapping.get(table_name)
        if table is not None:
            with self.engine.connect() as connection:
                query = table.select().order_by(table.c.id.desc()).limit(5)
                result = connection.execute(query)
                return result.fetchall()
        else:
            raise ValueError(f"Table {table_name} does not exist")
        
    def update(self, table_name, id, **kwargs):
        table = self.table_mapping.get(table_name)
        if table is not None:
            with self.engine.connect() as connection:
                query = table.update().where(table.c.id == id).values(**kwargs)
                connection.execute(query)
                connection.commit()
        else:
            raise ValueError(f"Table {table_name} does not exist")
        
    def delete(self, table_name, id):
        table = self.table_mapping.get(table_name)
        if table is not None:
            with self.engine.connect() as connection:
                query = table.delete().where(table.c.id == id)
                connection.execute(query)
                connection.commit()
        else:
            raise ValueError(f"Table {table_name} does not exist")
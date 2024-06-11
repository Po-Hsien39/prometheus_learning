from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()
engine = None

class Todo(Base):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(String(255), nullable=False)

def get_engine(user, password, host, database=None):
    database_url = f"{user}:{password}@{host}"
    if database:
        database_url += f"/{database}"
    url = f"mysql+mysqlconnector://{database_url}"
    
    # Use connection pooling
    engine = create_engine(
        url,
        echo=False,  # Turn off echo to reduce logging
        future=True,
        pool_size=10,  # Number of connections to keep open in the pool
        max_overflow=20,  # Number of additional connections to open if the pool is full
        pool_timeout=30,  # Timeout in seconds for getting a connection from the pool
        pool_recycle=3600,  # Time in seconds to recycle a connection (avoid stale connections)
    )
    return engine

def initialize_database():
    global engine
    if engine is None:
        print("Initializing database...")
        engine = get_engine("root", "1234", "127.0.0.1", "MySQL_Database")
        Base.metadata.create_all(engine)
    return engine

initialize_database()
Session = scoped_session(sessionmaker(bind=engine))

def add_task(task):
    session = Session()
    try:
        new_task = Todo(task=task)
        session.add(new_task)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

def get_all_tasks():
    session = Session()
    try:
        tasks = session.query(Todo).all()
        return tasks
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

def delete_task(task_id):
    session = Session()
    try:
        task_to_delete = session.query(Todo).filter(Todo.id == task_id).first()
        if task_to_delete:
            session.delete(task_to_delete)
            session.commit()
            print(f"Task with ID: {task_id} has been deleted.")
        else:
            print(f"No task found with ID: {task_id}.")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

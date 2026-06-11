from sqlmodel import SQLModel, create_engine, Session

# define the database file location
sqlite_file_name="ctf_lab.db"
sqlite_url=f"sqlite:///{sqlite_file_name}" #tell SQLModel to create a local file name

#config
connect_args={"check_same_thread": False}
engine= create_engine(sqlite_url, connect_args=connect_args)# tlanslates python commands to SQL

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
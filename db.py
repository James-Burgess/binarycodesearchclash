import sqlalchemy
import databases


DATABASE_URL = "sqlite:///./db.sqlite3"
metadata = sqlalchemy.MetaData()


def load_db():
    database = databases.Database(DATABASE_URL)

    engine = sqlalchemy.create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
    metadata.create_all(engine)
    return database


games = sqlalchemy.Table(
    "games",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),

    sqlalchemy.Column("user", sqlalchemy.String),
    sqlalchemy.Column("game", sqlalchemy.String),
    sqlalchemy.Column("time", sqlalchemy.String),
    sqlalchemy.Column("language", sqlalchemy.String),
    sqlalchemy.Column("code", sqlalchemy.String),
    sqlalchemy.Column("success", sqlalchemy.Boolean),
)

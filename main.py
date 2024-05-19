from orm.database import engine, Base
from orm.crud import upsert


data = [
    {
        "id": 1,
        "username": "admin",
        "email": "test@gmail.com",
        "password": "admin",
        "is_active": True,
        "is_superuser": True
    }
]


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    upsert(data, "users", "public", engine)

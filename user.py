import uuid
import datetime

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


db_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    gender = db.Column(db.Text)
    email = db.Column(db.Text)
    birthdate = db.Column(db.Text)
    height = db.Column(db.Text)


def connect_db():
    
    engine = db.create_engine(db_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def request_data():
    
    print("Привет! Я запишу твои данные!")
    first_name = input("Введите своё имя: ")
    last_name = input("И фамилию: ")
    email = input("Адрес электронной почты: ")
    gender = input("Пол Male / Female: ")
    birthdate = input("Дату рождения в формате ГГГГ-ММ-ДД: ")
    height = input("Рост м.cм: ")
    
    user_id = str(uuid.uuid4())
    user = User(
        id=user_id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        gender=gender,
        birthdate=birthdate,
        height=height
    )
    
    return user

def print_users_list(cnt, user_ids, last_seen_log):
    if user_ids:
        print("Найдено пользователей: ", cnt)
        print("Идентификатор пользвоателя - дата его последней активности")
        for user_id in user_ids:
            last_seen = last_seen_log[user_id]
            print("{} - {}".format(user_id, last_seen))
    else:
        print("Пользователей с таким именем нет.")

def main():
    session = connect_db()
    user = request_data()
    session.add(user)
    session.commit()
    print("Спасибо, данные сохранены!")


if __name__ == "__main__":
    main()
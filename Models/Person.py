from Models.DBConnection import db, connection

class Person:

    @staticmethod
    def create_table():
        db.execute("""--sql
            CREATE TABLE IF NOT EXISTS "Person" (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name TEXT NOT NULL,
                location TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES User(telegram_id) ON DELETE CASCADE
            );
        """)

    @staticmethod
    def create_person(name: str, location: str, telegram_id: int):
        db.execute("""--sql
            INSERT INTO "Person" (name, location, user_id, created_at)
            VALUES
                ( ?, ?, ?, datetime('now') );
        """,
        ( name, location, telegram_id ))
        connection.commit()

    @staticmethod
    def exists(id: int):
        result = Person.findByPk(id)
        return True if result else False
    
    @staticmethod
    def findByPk(id: int):
        result = db.execute("SELECT * FROM 'Person' WHERE id = ?", (id,)).fetchone()
        return result[0]
    
    @staticmethod
    def find_by_name(person_name: int):
        result = db.execute("SELECT * FROM 'Person' WHERE id = ?", (person_name,)).fetchone()
        return result
    
    @staticmethod
    def get_all_persons_by_telegram_id(telegram_id: int) -> list[tuple[str]]:
        result: list = db.execute("""SELECT id, name, location FROM 'Person' WHERE user_id = ?;""", (telegram_id,)).fetchall()
        return result
    
    def get_person_id_by_name_from_telegram_id(telegram_id: int, name: str) -> str:
        result: list = db.execute("""SELECT id FROM 'Person' WHERE user_id = ? AND name = ?;""", (telegram_id, name)).fetchone()
        return result
    
    @staticmethod
    def edit_person_name_by_pk(id: int, location: str, name: str):
        db.execute("UPDATE Person SET name = ?, location = ? WHERE id = ?", (name, location, id))
        connection.commit()

    @staticmethod
    def delete_person_by_name_from_telegram_id(id: int, name: str):
        db.execute("DELETE FROM Person WHERE name = ? AND user_id = ?", (name, id))
        connection.commit()

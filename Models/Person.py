from Models.DBConnection import db, connection

class Person:

    def create_table():
        db.execute("""--sql
            CREATE TABLE IF NOT EXISTS "Person" (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES User(telegram_id) ON DELETE CASCADE
            );
        """)

    def create_person(name: str, telegram_id: int):
        db.execute("""--sql
            INSERT INTO "Person" (name, user_id, created_at)
            VALUES
                ( ?, ?, datetime('now') );
        """,
        ( name, telegram_id ))
        connection.commit()

    def exists(id: int):
        result = Person.findByPk(id)
        return True if result else False
    
    def findByPk(id: int):
        result = db.execute("SELECT * FROM 'Person' WHERE id = ?", (id,)).fetchone()
        return result[0]
    
    def get_all_persons_by_telegram_id(telegram_id: int):
        result: list = db.execute("""SELECT name FROM 'Person' WHERE user_id = ?;""", (telegram_id,)).fetchall()
        return result
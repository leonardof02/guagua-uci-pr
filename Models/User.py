from Models.DBConnection import connection, db

class User:

    @staticmethod
    def create_table():
        db.execute("""--sql
            CREATE TABLE IF NOT EXISTS "User" (
                telegram_id INTEGER PRIMARY KEY NOT NULL,
                full_name TEXT,
                created_at TIMESTAMP
            );
        """)

    @staticmethod
    def create_user(telegram_id: int, full_name: str,):
        db.execute("""--sql
            INSERT INTO "User" (telegram_id, full_name, created_at)
            VALUES
                ( ?, ?, datetime('now') );
        """,
        ( telegram_id, full_name ))
        connection.commit()


    @staticmethod
    def exists(user_id):
        result = User.findByPk(user_id);
        return True if result else False
    
    @staticmethod
    def findByPk(user_id):
        result = db.execute("SELECT * FROM User WHERE telegram_id = ?", (user_id,)).fetchone();
        return result
    
    @staticmethod
    def get_all_users_chat_id():
        result: list = db.execute("""SELECT telegram_id FROM 'User';""").fetchall()
        return result
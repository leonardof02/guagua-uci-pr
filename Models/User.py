from Models.DBConnection import connection, db

class User:

    def create_table():
        db.execute("""--sql
            CREATE TABLE IF NOT EXISTS "User" (
                telegram_id INTEGER PRIMARY KEY NOT NULL,
                username TEXT NOT NULL,
                full_name TEXT,
                created_at TIMESTAMP
            );
        """)

    def create_user(telegram_id: int, username: str, full_name: str):
        db.execute("""--sql
            INSERT INTO "User" (telegram_id, username, full_name, created_at)
            VALUES
                ( ?, ?, ?, datetime('now') );
        """,
        ( telegram_id, username, full_name ))
        connection.commit()

    def exists(user_id):
        result = User.findByPk(user_id);
        return True if result else False
    
    def findByPk(user_id):
        result = db.execute("SELECT * FROM User WHERE telegram_id = ?", (user_id,)).fetchone();
        return result

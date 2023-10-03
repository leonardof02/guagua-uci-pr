from Models.DBConnection import connection, db

class Reservation:

    def create_table():
        db.execute("""--sql
            CREATE TABLE IF NOT EXISTS "Reservation" (
                reservation_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                'order' INTEGER,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES User(telegram_id)
            );
        """)

    def create_reservation(telegram_id: int):
        db.execute("""--sql
            INSERT INTO "Reservation" (telegram_id, order, created_at)
            VALUES
                ( ROWID, ?, datetime('now') );
        """, (telegram_id,))
        connection.commit()

    def exists(reservation_id):
        result = Reservation.findByPk(reservation_id);
        return True if result else False
    
    def existsByUserId(telegram_id):
        result = Reservation.findByUserId(telegram_id)
        return True if result else False
    
    def findByUserId(telegram_id):
        result = db.execute("SELECT 'order' FROM 'Reservation' WHERE user_id = ?", (telegram_id,))
        return result
    
    def findByPk(reservation_id):
        result = db.execute("SELECT * FROM 'Reservation' WHERE telegram_id = ?", (reservation_id,)).fetchone();
        print(result)
        return result


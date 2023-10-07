from Models.DBConnection import connection, db

class Reservation:

    def create_table():
        db.execute("""--sql
            CREATE TABLE IF NOT EXISTS "Reservation" (
                reservation_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                user_id INTEGER NOT NULL,
                person_id INTEGER NOT NULL,
                created_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES User(telegram_id),
                FOREIGN KEY (person_id) REFERENCES Person(id)
            );
        """)

    def create_reservation(telegram_id: int):
        db.execute("""--sql
            INSERT INTO "Reservation" (user_id, created_at)
            VALUES
                ( ?, datetime('now') );
        """, (telegram_id,))
        connection.commit()

    def exists(reservation_id):
        result = Reservation.findByPk(reservation_id);
        return True if result else False
    
    def existsByUserId(telegram_id):
        result = Reservation.findByUserId(telegram_id)
        return True if result else False
    
    def findByUserId(telegram_id):
        result = db.execute("SELECT 'order' FROM 'Reservation' WHERE user_id = ?", (telegram_id,)).fetchone()
        return result
    
    def findByPk(reservation_id):
        result = db.execute("SELECT * FROM 'Reservation' WHERE telegram_id = ?", (reservation_id,)).fetchone();
        print(result)
        return result
    
    def getArrivalOrderByUser(telegram_id):
        result = db.execute("""--sql
            SELECT arrival_order FROM 
            (SELECT user_id, ROW_NUMBER() OVER(ORDER BY created_at ASC) AS arrival_order FROM "Reservation")
            WHERE user_id = ?
        """, (telegram_id,)).fetchone();
        return result[0]
    
    def get_all_by_user_id(user_id: int):
        result = db.execute("""--sql
            SELECT * FROM Reservation WHERE user_id = ? 
        """, (user_id,)).fetchall();
    
    def deleteByUserId(telegram_id):
        db.execute("DELETE FROM 'Reservation' WHERE user_id = ?", (telegram_id,))
        connection.commit()



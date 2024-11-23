from Models.DBConnection import connection, db

class Reservation:

    @staticmethod
    def create_table():
        db.execute("""--sql
            CREATE TABLE IF NOT EXISTS "Reservation" (
                reservation_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                user_id INTEGER NOT NULL,
                person_ci INTEGER NOT NULL,
                created_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES User(telegram_id),
                FOREIGN KEY (person_ci) REFERENCES Person(ci)
            );
        """)
        connection.commit()

    @staticmethod
    def get_all_reservations():
        result = db.execute("""--sql
            SELECT ROW_NUMBER() OVER( ORDER BY created_at ASC) as arrival_order, name, location, reservado_por
                FROM (
                    SELECT Person.name, Reservation.created_at, Person.location, User.telegram_id, User.full_name as reservado_por
                        FROM Reservation
                        INNER JOIN Person ON Person.ci = Reservation.person_ci
                        INNER JOIN "User" ON User.telegram_id = Reservation.user_id
                )
        """)
        return result
    
    @staticmethod
    def get_all_reservations_by_telegram_id(telegram_id: int):
        result = db.execute("""--sql
            SELECT reservation_id, arrival_order, name FROM (
                SELECT ROW_NUMBER() OVER( ORDER BY created_at ASC) as arrival_order, name, created_at, reservado_por, telegram_id, reservation_id
                FROM (
                    SELECT Reservation.reservation_id, Person.name, Reservation.created_at, User.telegram_id, User.full_name as reservado_por
                        FROM Reservation
                        INNER JOIN Person ON Person.ci = Reservation.person_ci
                        INNER JOIN "User" ON User.telegram_id = Reservation.user_id
                )) WHERE telegram_id = ?
        """, (telegram_id,)).fetchall()
        return result
    
    @staticmethod
    def get_reservation_by_id(reservation_id: int):
        result = db.execute("""--sql
            SELECT reservation_id, arrival_order, name FROM (
                SELECT ROW_NUMBER() OVER( ORDER BY created_at ASC) as arrival_order, name, created_at, reservado_por, telegram_id, reservation_id
                FROM (
                    SELECT Reservation.reservation_id, Person.name, Reservation.created_at, User.telegram_id, User.full_name as reservado_por
                        FROM Reservation
                        INNER JOIN Person ON Person.ci = Reservation.person_ci
                        INNER JOIN "User" ON User.telegram_id = Reservation.user_id
                )) WHERE reservation_id = ?
        """, (reservation_id,)).fetchone()
        return result

    @staticmethod
    def create_reservation(telegram_id: int, person_ci: int):
        db.execute("""--sql
            INSERT INTO "Reservation" (user_id, person_ci, created_at)
            VALUES
                ( ?, ?, datetime('now') );
        """, (telegram_id, person_ci))
        connection.commit()

    @staticmethod
    def get_reservation_by_user_id_and_name(telegram_id: int, person_name: str):
        result = db.execute("""--sql
            SELECT reservation_id, arrival_order, name FROM (
                SELECT ROW_NUMBER() OVER( ORDER BY created_at ASC) as arrival_order, name, created_at, reservado_por, telegram_id, reservation_id
                    FROM (
                        SELECT Reservation.reservation_id, Person.name, Reservation.created_at, User.telegram_id, User.full_name as reservado_por
                            FROM Reservation
                            INNER JOIN Person ON Person.ci = Reservation.person_ci
                            INNER JOIN "User" ON User.telegram_id = Reservation.user_id
                    )) WHERE telegram_id = ? AND name = ?
        """, (telegram_id, person_name)).fetchone()
        return result

    def get_all_locations():
        result = db.execute("SELECT Person.location FROM Reservation INNER JOIN Person ON id = person_ci GROUP BY Person.location").fetchall()
        return result
    
    @staticmethod
    def clean():
        print("Clearing db...")
        db.execute("DELETE FROM Reservation")
        connection.commit()

    @staticmethod
    def exists(reservation_id: int) -> bool:
        result = Reservation.findByPk(reservation_id);
        return True if result else False

    @staticmethod
    def exist_person(person_ci: int) -> bool:
        result = db.execute("""SELECT person_ci, full_name, user_id as name FROM Reservation INNER JOIN User ON User.telegram_id = Reservation.user_id WHERE person_ci = ?""", (person_ci,)).fetchone()
        return result
    
    @staticmethod
    def existsByUserId(telegram_id: int):
        result = Reservation.findByUserId(telegram_id)
        return True if result else False
    
    @staticmethod
    def find_by_id(telegram_id: int):
        result = db.execute("SELECT 'order' FROM 'Reservation' WHERE user_id = ?", (telegram_id,)).fetchone()
        return result
    
    @staticmethod
    def findByPk(reservation_id: int):
        result = db.execute("SELECT * FROM 'Reservation' WHERE telegram_id = ?", (reservation_id,)).fetchone();
        print(result)
        return result
    
    @staticmethod
    def get_all_by_user_id(user_id: int):
        result = db.execute("""--sql
            SELECT * FROM Reservation WHERE user_id = ? 
        """, (user_id,)).fetchall();
    
    @staticmethod
    def delete_by_id(id: int):
        db.execute("DELETE FROM 'Reservation' WHERE reservation_id = ?", (id,))
        connection.commit()



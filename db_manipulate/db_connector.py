import mysql.connector

class DBFetcher:
    def __init__(self, host: str, database: str, user: str, password: str):
        self.db_object = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
        )

        self.db_cursor = self.db_object.cursor()

        self.week = {
                1: 'monday',
                2: 'tuesday',
                3: 'wednesday',
                4: 'thursday',
                5: 'friday',
                6: 'saturday'
        }
        
        self.TABLE_TEACHERS_NAME = 'teachers'
        self.TABLE_TEACHERS_TIMETABLE_NAME = 'teachers_timetable'
        self.TABLE_STUDENTS_NAME = 'students'
        self.MAX_LESSON_NUM = 6
        
    def close_db(self):
        self.db_object.close()

    def send_query(self, query: str) -> list | None:
        if type(query) is not str or not query:
            return None
        
        try:
            self.db_cursor.execute(query)
            result = self.db_cursor.fetchall()

        except mysql.connector.errors.ProgrammingError:
            return None

        except mysql.connector.errors.InternalError:
            self.db_cursor.fetchall()
            self.db_cursor.execute(query)
            result = self.db_cursor.fetchall()

        return result

class DBEditor(DBFetcher):
    def save_changes(self) -> bool:
        try:
            self.db_object.commit()
        except AttributeError:
            return False

        return True


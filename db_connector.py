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

    def save_changes(self) -> bool:
        try:
            self.db_object.commit()
        except AttributeError:
            return False

        return True

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

    #def formalize_row_result(self, fetch_row_result: list) -> tuple:

    def get_subclasses_in_class(self, class_num: int) -> tuple:
        pass

    def get_info_subject(self, week_day: int, lesson_number: int, class_number: int, subclass: str) -> str | None:
        try:
            week_day = int(week_day)
            week_day = self.week[week_day]
            
            lesson_number = int(lesson_number)
            class_number = int(class_number)

            if type(subclass) is not str or len(subclass) != 1:
                return None

            if lesson_number < 1 or lesson_number > self.MAX_LESSON_NUM:
                return None

            if class_number < 1 or class_number > 11:
                return None

        except (ValueError, KeyError):
            return None

        self.db_cursor.execute('SELECT {} FROM {} WHERE lesson_number = {} AND class = {} AND subclass = "{}"'.format(
                week_day,
                self.TABLE_TEACHERS_TIMETABLE_NAME,
                lesson_number,
                class_number,
                subclass
            )
        )
        
        result = self.db_cursor.fetchone()
        
        if result:
            result = result[0]

        return result


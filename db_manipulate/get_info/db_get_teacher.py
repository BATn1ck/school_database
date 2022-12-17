import db_manipulate.db_connector as db_connector

def get_school_lessons(DBReader) -> list | None: 
    if type(DBReader) is not db_connector.DBFetcher:
        return None

    lessons_list = DBReader.send_query(
        "SELECT DISTINCT subject FROM {}".format(
            DBReader.TABLE_TEACHERS_NAME
        )
    )

    return lessons_list

def get_all_subclasses(DBReader) -> list | None:
    if type(DBReader) is not db_connector.DBFetcher:
        return None

    subclasses_list = DBReader.send_query(
        "SELECT DISTINCT subclass FROM {}".format(
            DBReader.TABLE_TEACHERS_NAME
        )
    )

    return subclasses_list

def get_teacher_info(DBReader) -> tuple | None:
    teacher_lessons = get_school_lessons(DBReader)
    teacher_subclasses = get_all_subclasses(DBReader)

    if teacher_lessons:
        teacher_lessons = list(map(lambda x: x[0], teacher_lessons))

    if teacher_subclasses:
        teacher_subclasses = list(map(lambda x: x[0], teacher_subclasses))

    return (teacher_lessons, teacher_subclasses)

def handle_teacher(values_dict: dict, session, DBReader) -> str | None:
    result = None

    get_session_variable = lambda session_variable: \
            session[session_variable] if session_variable in session.keys() else None

    if type(values_dict) is not dict or \
            type(DBReader) is not db_connector.DBFetcher:
        return result

    if "teacher_lesson" in values_dict.keys() and \
            type(values_dict["teacher_lesson"]) is str:
        if get_session_variable("teacher_lesson") != values_dict["teacher_lesson"]:
            session["teacher_lesson"] = values_dict["teacher_lesson"]
            session["teacher_class"] = 0
            session["teacher_subclasses"] = []
            session["teacher_subclass"] = ''

            query = \
                '''
                SELECT class FROM {}
                WHERE subject = "{}"
                '''.format(
                    DBReader.TABLE_TEACHERS_NAME,
                    get_session_variable('teacher_lesson')
                )

            classes = DBReader.send_query(query)
            classes = list(map(lambda x: x[0] if x else '', classes))
            temp_arr = []
            
            for cl in classes:
                if cl not in temp_arr:
                    temp_arr.append(cl)
            
            temp_arr.sort()
            session["teacher_classes"] = temp_arr

    if "teacher_class" in values_dict.keys() and \
            get_session_variable("teacher_lesson") and \
            type(values_dict["teacher_class"]) is str:
        if get_session_variable("teacher_class") != values_dict["teacher_class"]:
            session["teacher_class"] = values_dict["teacher_class"]
            session["teacher_subclass"] = ''

            query = \
                '''
                SELECT subclass FROM {}
                WHERE subject = "{}"
                AND class = {}
                '''.format(
                    DBReader.TABLE_TEACHERS_NAME,
                    get_session_variable('teacher_lesson'),
                    get_session_variable('teacher_class')
                )

            subclasses = DBReader.send_query(query)
            subclasses = list(map(lambda x: str(x[0]) if x else '', subclasses))
            temp_arr = []
            
            for cl in subclasses:
                if cl not in temp_arr:
                    temp_arr.append(cl)
            
            temp_arr.sort()
            session["teacher_subclasses"] = subclasses

    if "teacher_subclass" in values_dict.keys() and \
            get_session_variable("teacher_lesson") and \
            get_session_variable("teacher_class") and \
            type(values_dict["teacher_subclass"]) is str and \
            len(values_dict["teacher_subclass"]) == 1:

            session['teacher_subclass'] = values_dict['teacher_subclass']

    if "teacher_get" in values_dict.keys() and \
            get_session_variable("teacher_lesson") and \
            get_session_variable("teacher_class") and \
            get_session_variable("teacher_subclass"):

            query = \
                """
                SELECT first_name,second_name,third_name FROM {}
                WHERE subject = '{}' 
                AND class = {}
                AND subclass = '{}'
                """.format(
                    DBReader.TABLE_TEACHERS_NAME,
                    get_session_variable('teacher_lesson'),
                    get_session_variable('teacher_class'),
                    get_session_variable('teacher_subclass')
                )

            result = DBReader.send_query(query)

            if result:
                result = ' '.join([i for i in result[0]])

    return result

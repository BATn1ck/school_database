import db_manipulate.db_connector as db_connector

def handle_subject(values_dict: dict, session, DBReader) -> str | None:
    result = None

    if type(values_dict) is not dict or \
            type(DBReader) is not db_connector.DBFetcher:
        return result

    get_session_variable = lambda session_variable: \
            session[session_variable] if session_variable in session.keys() else None
    
    def get_subject_classes() -> list | None:
        nonlocal DBReader, session
        if not get_session_variable("subject_day_week") or \
                not get_session_variable("subject_lesson_num") or \
                type(DBReader) is not db_connector.DBFetcher:
            return None
        
        classes_list = DBReader.send_query(
                "SELECT DISTINCT class FROM {} WHERE {} IS NOT NULL AND lesson_number = {}".format(
                    DBReader.TABLE_TEACHERS_TIMETABLE_NAME,
                    DBReader.week[get_session_variable("subject_day_week")],
                    get_session_variable("subject_lesson_num")
                )
        )

        if classes_list:
            classes_list = [cl[0] for cl in classes_list]

        return classes_list

    if "subject_day_week" in values_dict.keys():
        try:
            subject_day_week = int(values_dict["subject_day_week"])
            
            if subject_day_week < 7 and subject_day_week > 0:
                if get_session_variable("subject_day_week") and \
                        get_session_variable("subject_day_week") != subject_day_week:
                    session['subject_lesson_num'] = 0
                    session['subject_classes'] = []
                    session['subject_class'] = 0
                    session["subject_subclasses"] = []
                    session["subject_subclass"] = ''
                    session["taked_subject"] = ''

                session["subject_day_week"] = subject_day_week

        except ValueError: # if "subject_day_week" is not int
            pass

    if "subject_lesson_num" in values_dict.keys():
        try:
            subject_lesson_num = int(values_dict["subject_lesson_num"])
            
            if subject_lesson_num <= DBReader.MAX_LESSON_NUM and subject_lesson_num > 0:
                if get_session_variable("subject_lesson_num") and \
                        get_session_variable("subject_lesson_num") != subject_lesson_num:
                    session['subject_classes'] = []
                    session['subject_class'] = 0
                    session["subject_subclasses"] = []
                    session["subject_subclass"] = ''
                    session["taked_subject"] = ''

                session["subject_lesson_num"] = subject_lesson_num

                classes_list = get_subject_classes()
                if classes_list:
                    session['subject_classes'] = classes_list

        except ValueError: # if "subject_lesson_num" is not int
            pass

    
    if "subject_class" in values_dict.keys():
        try:
            subject_class = int(values_dict["subject_class"])

            if subject_class > 0 and subject_class < 12:
                if get_session_variable("subject_class") and \
                        get_session_variable("subject_class") != subject_class:
                    session['subject_subclasses'] = []
                    session['subject_subclass'] = ''

                session["subject_class"] = subject_class
                subclasses_list = DBReader.send_query("SELECT DISTINCT subclass FROM {} WHERE {} IS NOT NULL AND lesson_number = {} AND class = {}".format(
                        DBReader.TABLE_TEACHERS_TIMETABLE_NAME,
                        DBReader.week[get_session_variable("subject_day_week")],
                        get_session_variable("subject_lesson_num"),
                        get_session_variable("subject_class")
                    )
                )
                
                if subclasses_list:
                    subclasses_list = [subclass[0] for subclass in subclasses_list]
                    session["subject_subclasses"] = subclasses_list

        except ValueError:
            pass

    if "subject_subclass" in values_dict.keys():
        if type(values_dict["subject_subclass"]) is str and \
                len(values_dict["subject_subclass"]) == 1:
            session["subject_subclass"] = values_dict["subject_subclass"]

    if "subject_get" in values_dict.keys():
        if get_session_variable("subject_day_week") and \
                get_session_variable("subject_lesson_num") and \
                get_session_variable("subject_class") and \
                get_session_variable("subject_subclass"):

            subject_query = \
            '''
            SELECT {} FROM {}
            WHERE lesson_number = {} AND class = {} AND subclass = "{}" 
            AND {} IS NOT NULL
            '''.format(
                    DBReader.week[get_session_variable("subject_day_week")],
                    DBReader.TABLE_TEACHERS_TIMETABLE_NAME,
                    get_session_variable("subject_lesson_num"),
                    get_session_variable("subject_class"),
                    get_session_variable("subject_subclass"),
                    DBReader.week[get_session_variable("subject_day_week")]
            )

            result = DBReader.send_query(subject_query)

            if result: # if result is not empty list or None
                result = result[0][0]

    return result

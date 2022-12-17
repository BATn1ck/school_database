import db_manipulate.db_connector as db_connector

def handle_timetable_class(values_dict: dict, session, DBReader) -> list:
    result = []

    if type(values_dict) is not dict or \
            type(DBReader) is not db_connector.DBFetcher:
        return result

    get_session_variable = lambda session_variable: \
            session[session_variable] if session_variable in session.keys() else None

    if "timetable_class_day_week" in values_dict.keys():
        try:
            timetable_class_day_week = int(values_dict["timetable_class_day_week"])
            
            if timetable_class_day_week < 7 and timetable_class_day_week > 0:
                if get_session_variable("timetable_class_day_week") and \
                        get_session_variable("timetable_class_day_week") != timetable_class_day_week:
                    session['timetable_class_classes'] = []
                    session['timetable_class_class'] = 0
                    session["timetable_class_subclasses"] = []
                    session["timetable_class_subclass"] = ''
                    session["taked_timetable_class"] = ''

                query = \
                    '''
                    SELECT DISTINCT class FROM {}
                    WHERE {} IS NOT NULL
                    '''.format(
                        DBReader.TABLE_TEACHERS_TIMETABLE_NAME,
                        DBReader.week[timetable_class_day_week]
                    )

                classes = DBReader.send_query(query)
                
                if classes:
                    classes = [cl[0] for cl in classes]

                session["timetable_class_day_week"] = timetable_class_day_week
                session['timetable_class_classes'] = classes

        except (ValueError, TypeError): # if "timetable_class_day_week" is not int or None
            pass

    if "timetable_class_class" in values_dict.keys() and \
            get_session_variable("timetable_class_day_week"):
        try:
            timetable_class_class = int(values_dict["timetable_class_class"])
            
            if timetable_class_class < 12 and timetable_class_class > 0:
                if get_session_variable("timetable_class_class") and \
                        get_session_variable("timetable_class_class") != timetable_class_class:
                    session["timetable_class_subclasses"] = []
                    session["timetable_class_subclass"] = ''
                    session["taked_timetable_class"] = ''
                
                query = \
                    '''
                    SELECT DISTINCT subclass FROM {}
                    WHERE class = {}
                    '''.format(
                        DBReader.TABLE_TEACHERS_TIMETABLE_NAME,
                        timetable_class_class
                    )

                subclasses = DBReader.send_query(query)

                if subclasses:
                    subclasses = [subc[0] for subc in subclasses]

                session["timetable_class_class"] = timetable_class_class
                session["timetable_class_subclasses"] = subclasses

        except (ValueError, TypeError): # if "timetable_class_class" is not int or None
            pass

    if "timetable_class_subclass" in values_dict.keys() and \
            get_session_variable("timetable_class_day_week") and \
            get_session_variable("timetable_class_class"):
        if values_dict["timetable_class_subclass"] and \
                type(values_dict["timetable_class_subclass"]) is str and \
                len(values_dict["timetable_class_subclass"]) == 1:
            session["timetable_class_subclass"] = values_dict["timetable_class_subclass"]

    if "timetable_class_get" in values_dict.keys() and \
            get_session_variable("timetable_class_day_week") and \
            get_session_variable("timetable_class_class") and \
            get_session_variable("timetable_class_subclass"):
        timetable_class_query = \
            '''
            SELECT lesson_number,{} FROM {}
            WHERE class = {}
            AND subclass = "{}"
            ORDER BY lesson_number
            '''.format(
                DBReader.week[get_session_variable("timetable_class_day_week")],
                DBReader.TABLE_TEACHERS_TIMETABLE_NAME,
                get_session_variable("timetable_class_class"),
                get_session_variable("timetable_class_subclass")
            )

        timetable_class = DBReader.send_query(timetable_class_query)
        
        if timetable_class:
            for lesson_num, lesson in timetable_class:
                result.append("{}) {}".format(lesson_num, '-' if not lesson else lesson))

    return result

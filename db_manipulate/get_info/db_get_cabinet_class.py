import db_manipulate.db_connector as db_connector

def handle_cabinet_class(values_dict: dict, session, DBReader) -> str | None:
    get_session_variable = lambda session_variable: \
            session[session_variable] if session_variable in session.keys() else None

    result = None

    if type(values_dict) is not dict or \
            type(DBReader) is not db_connector.DBFetcher:
        return result

    if "cabinet_class_day_week" in values_dict.keys():
        try:
            cabinet_class_day_week = int(values_dict["cabinet_class_day_week"])
            
            if cabinet_class_day_week < 7 and cabinet_class_day_week > 0:
                if get_session_variable("cabinet_class_day_week") and \
                        get_session_variable("cabinet_class_day_week") != cabinet_class_day_week:
                    session['cabinet_class_lesson_num'] = 0
                    session['cabinet_class_classes'] = []
                    session['cabinet_class_class'] = 0
                    session["cabinet_class_subclasses"] = []
                    session["cabinet_class_subclass"] = ''
                    session["taked_cabinet_class"] = ''

                session["cabinet_class_day_week"] = cabinet_class_day_week

        except ValueError: # if "cabinet_class_day_week" is not int
            pass

    if "cabinet_class_lesson_num" in values_dict.keys() and \
            get_session_variable("cabinet_class_day_week"):
        try:
            cabinet_class_lesson_num = int(values_dict["cabinet_class_lesson_num"])
            
            if cabinet_class_lesson_num <= DBReader.MAX_LESSON_NUM and cabinet_class_lesson_num > 0:
                if get_session_variable("cabinet_class_lesson_num") != cabinet_class_lesson_num:
                    session['cabinet_class_classes'] = []
                    session['cabinet_class_class'] = 0
                    session["cabinet_class_subclasses"] = []
                    session["cabinet_class_subclass"] = ''
                    session["taked_cabinet_class"] = ''
                    session["cabinet_class_lesson_num"] = cabinet_class_lesson_num

                    query = \
                        '''
                        SELECT class FROM {}
                        WHERE {} IS NOT NULL
                        AND lesson_number = {}
                        '''.format(
                            DBReader.TABLE_TEACHERS_TIMETABLE_NAME,
                            DBReader.week[get_session_variable('cabinet_class_day_week')],
                            get_session_variable('cabinet_class_lesson_num')
                        )

                    classes_list = DBReader.send_query(query)

                    if classes_list:
                        classes_list = [cl[0] for cl in classes_list]

                    session['cabinet_class_classes'] = classes_list

        except ValueError: # if "cabinet_class_lesson_num" is not int
            pass

    
    if "cabinet_class_class" in values_dict.keys() and \
            get_session_variable("cabinet_class_day_week") and \
            get_session_variable('cabinet_class_lesson_num'):
        try:
            cabinet_class_class = int(values_dict["cabinet_class_class"])

            if cabinet_class_class > 0 and cabinet_class_class < 12:
                if get_session_variable("cabinet_class_class") and \
                        get_session_variable("cabinet_class_class") != cabinet_class_class:
                    session['cabinet_class_subclasses'] = []
                    session['cabinet_class_subclass'] = ''

                session["cabinet_class_class"] = cabinet_class_class
                query = \
                        """
                        SELECT DISTINCT subclass FROM {} 
                        WHERE {} IS NOT NULL 
                        AND lesson_number = {} 
                        AND class = {}
                        """.format(
                            DBReader.TABLE_TEACHERS_TIMETABLE_NAME,
                            DBReader.week[get_session_variable("cabinet_class_day_week")],
                            get_session_variable("cabinet_class_lesson_num"),
                            get_session_variable("cabinet_class_class")
                    )

                subclasses_list = DBReader.send_query(query)
                
                if subclasses_list:
                    subclasses_list = [subclass[0] for subclass in subclasses_list]
                    session["cabinet_class_subclasses"] = subclasses_list

        except ValueError:
            pass

    if "cabinet_class_subclass" in values_dict.keys() and \
            get_session_variable("cabinet_class_day_week") and \
            get_session_variable('cabinet_class_lesson_num') and \
            get_session_variable('cabinet_class_class'):
        if type(values_dict["cabinet_class_subclass"]) is str and \
                len(values_dict["cabinet_class_subclass"]) == 1:
            session["cabinet_class_subclass"] = values_dict["cabinet_class_subclass"]

    if "cabinet_class_get" in values_dict.keys():
        if get_session_variable("cabinet_class_day_week") and \
                get_session_variable("cabinet_class_lesson_num") and \
                get_session_variable("cabinet_class_class") and \
                get_session_variable("cabinet_class_subclass"):

            cabinet_class_query = \
            '''
            SELECT classroom FROM {}
            WHERE lesson_number = {}
            AND class = {}
            AND subclass = "{}" 
            AND {} IS NOT NULL
            '''.format(
                    DBReader.TABLE_TEACHERS_TIMETABLE_NAME,
                    get_session_variable("cabinet_class_lesson_num"),
                    get_session_variable("cabinet_class_class"),
                    get_session_variable("cabinet_class_subclass"),
                    DBReader.week[get_session_variable("cabinet_class_day_week")]
            )

            result = DBReader.send_query(cabinet_class_query)

            if result: # if result is not empty list or None
                result = result[0][0]

    return result

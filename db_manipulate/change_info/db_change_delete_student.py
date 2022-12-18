import db_manipulate.db_connector as db_connector

def delete_student(values_dict: dict, session, DBWriter: db_connector.DBEditor) -> bool:
    result = False

    get_session_variable = lambda session_variable: \
                        session[session_variable] if session_variable in session.keys() else None

    if type(values_dict) is not dict or \
            type(DBWriter) is not db_connector.DBEditor or \
            not session:
        return result

    if 'student_delete_class' in values_dict.keys():
        try:
            stud_class = int(values_dict['student_delete_class'])

            if get_session_variable('student_delete_class') != stud_class:
                session['student_delete_class'] = stud_class
                session['student_delete_subclasses'] = []
                session['student_delete_subclass'] = ''
                session['student_delete_first_names'] = []
                session['student_delete_first_name'] = ''
                session['student_delete_second_names'] = []
                session['student_delete_second_name'] = ''
                session['student_delete_third_names'] = []
                session['student_delete_third_name'] = ''

            query = \
                '''
                SELECT DISTINCT subclass FROM {}
                WHERE class = {}
                '''.format(
                    DBWriter.TABLE_STUDENTS_NAME,
                    stud_class
                )

            subclasses = DBWriter.send_query(query)

            if subclasses:
                subclasses = [subcl[0] for subcl in subclasses]
            
            session['student_delete_subclasses'] = subclasses

        except (ValueError, TypeError):
            pass

    if 'student_delete_subclass' in values_dict.keys():
        subclass = values_dict['student_delete_subclass']

        if get_session_variable('student_delete_class') and \
                 subclass in get_session_variable('student_delete_subclasses'):

            if get_session_variable('student_delete_subclass') != subclass:
                session['student_delete_subclass'] = subclass
                session['student_delete_first_names'] = []
                session['student_delete_first_name'] = ''
                session['student_delete_second_names'] = []
                session['student_delete_second_name'] = ''
                session['student_delete_third_names'] = []
                session['student_delete_third_name'] = ''

            query = \
                '''
                SELECT DISTINCT first_name FROM {}
                WHERE class = {}
                AND subclass = "{}"
                '''.format(
                    DBWriter.TABLE_STUDENTS_NAME,
                    get_session_variable('student_delete_class'),
                    get_session_variable('student_delete_subclass')
                )

            first_names = DBWriter.send_query(query)

            if first_names:
                first_names = [fn[0] for fn in first_names]

            session['student_delete_first_names'] = first_names

    if 'student_delete_first_name' in values_dict.keys():
        first_name = values_dict['student_delete_first_name']

        if get_session_variable('student_delete_class') and \
                get_session_variable('student_delete_subclass') and \
                first_name in get_session_variable('student_delete_first_names'):

            if get_session_variable('student_delete_first_name') != first_name:
                session['student_delete_first_name'] = first_name
                session['student_delete_second_names'] = []
                session['student_delete_second_name'] = ''
                session['student_delete_third_names'] = []
                session['student_delete_third_name'] = ''

            query = \
                '''
                SELECT DISTINCT second_name FROM {}
                WHERE class = {}
                AND subclass = "{}"
                AND first_name = "{}"
                '''.format(
                    DBWriter.TABLE_STUDENTS_NAME,
                    get_session_variable('student_delete_class'),
                    get_session_variable('student_delete_subclass'),
                    get_session_variable('student_delete_first_name')
                )

            second_names = DBWriter.send_query(query)

            if second_names:
                second_names = [fn[0] for fn in second_names]

            session['student_delete_second_names'] = second_names

    if 'student_delete_second_name' in values_dict.keys():
        second_name = values_dict['student_delete_second_name']

        if get_session_variable('student_delete_class') and \
                get_session_variable('student_delete_subclass') and \
                get_session_variable('student_delete_first_name') and \
                second_name in get_session_variable('student_delete_second_names'):

            if get_session_variable('student_delete_second_names') != second_name:
                session['student_delete_second_name'] = second_name
                session['student_delete_third_names'] = []
                session['student_delete_third_name'] = ''

            query = \
                '''
                SELECT DISTINCT third_name FROM {}
                WHERE class = {}
                AND subclass = "{}"
                AND first_name = "{}"
                AND second_name = "{}"
                '''.format(
                    DBWriter.TABLE_STUDENTS_NAME,
                    get_session_variable('student_delete_class'),
                    get_session_variable('student_delete_subclass'),
                    get_session_variable('student_delete_first_name'),
                    get_session_variable('student_delete_second_name')
                )

            third_names = DBWriter.send_query(query)

            if third_names:
                third_names = [tn[0] if tn[0] else '(нет)' for tn in third_names]

            session['student_delete_third_names'] = third_names

    if 'student_delete_third_name' in values_dict.keys():
        third_name = values_dict['student_delete_third_name']

        if get_session_variable('student_delete_class') and \
                get_session_variable('student_delete_subclass') and \
                get_session_variable('student_delete_first_name') and \
                get_session_variable('student_delete_second_name') and \
                third_name in get_session_variable('student_delete_third_names'):

            if get_session_variable('student_delete_third_names') != third_name:
                session['student_delete_third_name'] = third_name

    if 'student_delete' in values_dict.keys():
        stud = values_dict['student_delete']

        if get_session_variable('student_delete_class') and \
                get_session_variable('student_delete_subclass') and \
                get_session_variable('student_delete_first_name') and \
                get_session_variable('student_delete_second_name') and \
                get_session_variable('student_delete_third_name'):

            query = \
                '''
                DELETE FROM {}
                WHERE class = {}
                AND subclass = "{}"
                AND first_name = "{}"
                AND second_name = "{}"
                AND third_name {}
                '''.format(
                    DBWriter.TABLE_STUDENTS_NAME,
                    get_session_variable('student_delete_class'),
                    get_session_variable('student_delete_subclass'),
                    get_session_variable('student_delete_first_name'),
                    get_session_variable('student_delete_second_name'),
                    'IS NULL' if get_session_variable('student_delete_third_name') == '(нет)' \
                            else '= "{}"'.format(get_session_variable('student_delete_third_name'))
                )

            DBWriter.send_query(query)
            if DBWriter.save_changes():
                result = True

            session['student_delete_class'] = ''
            session['student_delete_subclasses'] = []
            session['student_delete_subclass'] = ''
            session['student_delete_first_names'] = []
            session['student_delete_first_name'] = ''
            session['student_delete_second_names'] = []
            session['student_delete_second_name'] = ''
            session['student_delete_third_names'] = []
            session['student_delete_third_name'] = ''

    return result

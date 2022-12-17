import db_manipulate.db_connector as db_connector

def get_teachers_first_names(DBReader) -> list | None:
    query = \
        '''
        SELECT DISTINCT first_name FROM {}
        '''.format(
            DBReader.TABLE_TEACHERS_NAME
        )

    first_names = DBReader.send_query(query)

    if first_names:
        first_names = [fn[0] for fn in first_names]

    return first_names

def handle_teacher_classes(values_dict: dict, session, DBReader) -> str | None:
    result = None

    if type(values_dict) is not dict or \
            type(DBReader) is not db_connector.DBFetcher:
        return result

    get_session_variable = lambda session_variable: \
            session[session_variable] if session_variable in session.keys() else None

    if "teacher_classes_first_name" in values_dict.keys():
        first_name = values_dict["teacher_classes_first_name"]

        if first_name and type(first_name) is str and \
                get_session_variable('teacher_classes_first_name') != first_name:
            session['teacher_classes_first_name'] = first_name
            session['teacher_classes_second_name'] = ''
            session['teacher_classes_third_name'] = ''
            session['teacher_classes_subject'] = []

            query = \
                '''
                SELECT DISTINCT second_name FROM {}
                WHERE first_name = "{}"
                '''.format(
                    DBReader.TABLE_TEACHERS_NAME,
                    first_name
                )

            second_names_list = DBReader.send_query(query)

            if second_names_list:
                second_names_list = [sn[0] for sn in second_names_list]

            session['teacher_classes_second_names'] = second_names_list

    if "teacher_classes_second_name" in values_dict.keys() and \
            get_session_variable('teacher_classes_first_name'):
        second_name = values_dict["teacher_classes_second_name"]

        if second_name and type(second_name) is str and \
                get_session_variable('teacher_classes_second_name') != second_name:
            session['teacher_classes_second_name'] = second_name
            session['teacher_classes_third_name'] = ''
            session['teacher_classes_subject'] = []
            query = \
                '''
                SELECT DISTINCT third_name FROM {}
                WHERE first_name = "{}"
                AND second_name = "{}"
                '''.format(
                    DBReader.TABLE_TEACHERS_NAME,
                    get_session_variable('teacher_classes_first_name'),
                    second_name
                )

            third_names_list = DBReader.send_query(query)

            if third_names_list:
                third_names_list = [tn[0] if tn[0] else '(нет)' for tn in third_names_list]

            session['teacher_classes_third_names'] = third_names_list

    if "teacher_classes_third_name" in values_dict.keys() and \
            get_session_variable('teacher_classes_first_name') and \
            get_session_variable('teacher_classes_second_name'):
        third_name = values_dict["teacher_classes_third_name"]

        if third_name and type(third_name) is str and \
                get_session_variable('teacher_classes_third_name') != third_name:
            session['teacher_classes_third_name'] = third_name
            session['teacher_classes_subject'] = []
            query = \
                '''
                SELECT DISTINCT subject FROM {}
                WHERE first_name = "{}"
                AND second_name = "{}"
                AND third_name {}
                '''.format(
                    DBReader.TABLE_TEACHERS_NAME,
                    get_session_variable('teacher_classes_first_name'),
                    get_session_variable('teacher_classes_second_name'),
                    'IS NULL' if third_name == '(нет)' else '= "%s"' % third_name
                )

            subjects_list = DBReader.send_query(query)

            if subjects_list:
                subjects_list = [s[0] for s in subjects_list]
            
            session["teacher_classes_subjects"] = subjects_list

    if "teacher_classes_subject" in values_dict.keys() and \
            get_session_variable('teacher_classes_first_name') and \
            get_session_variable('teacher_classes_second_name') and \
            get_session_variable('teacher_classes_third_name'):
        subject = values_dict['teacher_classes_subject']

        if subject and type(subject) is str and \
                get_session_variable('teacher_classes_subject') != subject:
            session['teacher_classes_subject'] = subject

    if "teacher_classes_get" in values_dict.keys() and \
            get_session_variable('teacher_classes_first_name') and \
            get_session_variable('teacher_classes_second_name') and \
            get_session_variable('teacher_classes_third_name') and \
            get_session_variable('teacher_classes_subject'):

            query = \
                '''
                SELECT DISTINCT class,subclass FROM {}
                WHERE first_name = "{}"
                AND second_name = "{}"
                AND third_name {}
                AND subject = "{}"
                '''.format(
                    DBReader.TABLE_TEACHERS_NAME,
                    get_session_variable('teacher_classes_first_name'),
                    get_session_variable('teacher_classes_second_name'),
                    'IS NULL' if get_session_variable('teacher_classes_third_name') == '(нет)' else \
                            '= "%s"' % get_session_variable('teacher_classes_third_name'),
                    get_session_variable('teacher_classes_subject')
                )

            classes_list = DBReader.send_query(query)

            if classes_list:
                classes_list = [ ''.join(list(map(str, cl))) for cl in classes_list ]
                result = ' '.join(classes_list)

    return result

import db_manipulate.db_connector as db_connector

def change_grade(values_dict: dict, session, DBWriter) -> bool:
    result = False

    get_session_variable = lambda session_variable: \
                        session[session_variable] if session_variable in session.keys() else None

    if type(values_dict) is not dict or \
            type(DBWriter) is not db_connector.DBEditor or \
            not session:
        return result

    if 'student_grade_class' in values_dict.keys():
        try:
            stud_class = int(values_dict['student_grade_class'])

            if get_session_variable('student_grade_class') != stud_class:
                session['student_grade_class'] = stud_class
                session['student_grade_subclasses'] = []
                session['student_grade_subclass'] = ''
                session['student_grade_first_names'] = []
                session['student_grade_first_name'] = ''
                session['student_grade_second_names'] = []
                session['student_grade_second_name'] = ''
                session['student_grade_third_names'] = []
                session['student_grade_third_name'] = ''
                session['student_grade_subjects'] = []
                session['student_grade_subject'] = ''
                session['student_grade_grade'] = 0

            query = \
                '''
                SELECT DISTINCT subclass FROM {}
                WHERE class = {}
                '''.format(
                    DBWriter.TABLE_STUDENTS_NAME,
                    get_session_variable('student_grade_class')
                )

            subclasses = DBWriter.send_query(query)

            if subclasses:
                subclasses = [subcl[0] for subcl in subclasses]
            
            session['student_grade_subclasses'] = subclasses

        except (ValueError, TypeError):
            pass

    if 'student_grade_subclass' in values_dict.keys():
        subclass = values_dict['student_grade_subclass']

        if get_session_variable('student_grade_class') and \
                 subclass in get_session_variable('student_grade_subclasses'):

            if get_session_variable('student_grade_subclass') != subclass and \
                    get_session_variable('student_grade_class'):
                session['student_grade_subclass'] = subclass
                session['student_grade_first_names'] = []
                session['student_grade_first_name'] = ''
                session['student_grade_second_names'] = []
                session['student_grade_second_name'] = ''
                session['student_grade_third_names'] = []
                session['student_grade_third_name'] = ''
                session['student_grade_subjects'] = []
                session['student_grade_subject'] = ''
                session['student_grade_grade'] = 0

            query = \
                '''
                SELECT DISTINCT first_name FROM {}
                WHERE class = {}
                AND subclass = "{}"
                '''.format(
                    DBWriter.TABLE_STUDENTS_NAME,
                    get_session_variable('student_grade_class'),
                    get_session_variable('student_grade_subclass')
                )
            
            first_names = DBWriter.send_query(query)

            if first_names:
                first_names = [fn[0] for fn in first_names]

            session['student_grade_first_names'] = first_names

    if 'student_grade_first_name' in values_dict.keys():
        first_name = values_dict['student_grade_first_name']

        if get_session_variable('student_grade_first_name') != first_name and \
                get_session_variable('student_grade_class') and \
                get_session_variable('student_grade_subclass'):
            session['student_grade_first_name'] = first_name
            session['student_grade_second_names'] = []
            session['student_grade_second_name'] = ''
            session['student_grade_third_names'] = []
            session['student_grade_third_name'] = ''
            session['student_grade_subjects'] = []
            session['student_grade_subject'] = ''
            session['student_grade_grade'] = 0

        query = \
            '''
            SELECT DISTINCT second_name FROM {}
            WHERE class = {}
            AND subclass = "{}"
            AND first_name = "{}"
            '''.format(
                DBWriter.TABLE_STUDENTS_NAME,
                get_session_variable('student_grade_class'),
                get_session_variable('student_grade_subclass'),
                get_session_variable('student_grade_first_name')
            )

        second_names = DBWriter.send_query(query)

        if second_names:
            second_names = [sn[0] for sn in second_names]

        session['student_grade_second_names'] = second_names

    if 'student_grade_second_name' in values_dict.keys():
        second_name = values_dict['student_grade_second_name']

        if get_session_variable('student_grade_second_name') != second_name and \
                get_session_variable('student_grade_class') and \
                get_session_variable('student_grade_subclass') and \
                get_session_variable('student_grade_first_name'):
            session['student_grade_second_name'] = second_name
            session['student_grade_third_names'] = []
            session['student_grade_third_name'] = ''
            session['student_grade_subjects'] = []
            session['student_grade_subject'] = ''
            session['student_grade_grade'] = 0

        query = \
            '''
            SELECT DISTINCT third_name FROM {}
            WHERE class = {}
            AND subclass = "{}"
            AND first_name = "{}"
            AND second_name = "{}"
            '''.format(
                DBWriter.TABLE_STUDENTS_NAME,
                get_session_variable('student_grade_class'),
                get_session_variable('student_grade_subclass'),
                get_session_variable('student_grade_first_name'),
                get_session_variable('student_grade_second_name')
            )

        third_names = DBWriter.send_query(query)

        if third_names:
            third_names = [tn[0] if tn[0] else '(нет)' for tn in third_names]

        session['student_grade_third_names'] = third_names

    if 'student_grade_third_name' in values_dict.keys():
        third_name = values_dict['student_grade_third_name']

        if get_session_variable('student_grade_third_name') != third_name and \
                get_session_variable('student_grade_class') and \
                get_session_variable('student_grade_subclass') and \
                get_session_variable('student_grade_first_name') and \
                get_session_variable('student_grade_second_name'):
            session['student_grade_third_name'] = third_name
            session['student_grade_subjects'] = []
            session['student_grade_subject'] = ''
            session['student_grade_grade'] = 0

        query = \
            '''
            DESC {}
            '''.format(
                DBWriter.TABLE_STUDENTS_NAME
            )

        subjects = DBWriter.send_query(query)

        if subjects:
            subjects = [
                    sub[0][:sub[0].index('_grade')] for sub in subjects \
                    if sub[0] and sub[0].endswith('_grade')
            ]

        session['student_grade_subjects'] = subjects

    if 'student_grade_subject' in values_dict.keys():
        subject = values_dict['student_grade_subject']
        
        if get_session_variable('student_grade_subject') != subject and \
                get_session_variable('student_grade_class') and \
                get_session_variable('student_grade_subclass') and \
                get_session_variable('student_grade_first_name') and \
                get_session_variable('student_grade_second_name') and \
                subject in get_session_variable('student_grade_subjects'):
            session['student_grade_subject'] = subject
            session['student_grade_grade'] = 0

    if 'student_grade_grade' in values_dict.keys():
        grade = values_dict['student_grade_grade']

        if get_session_variable('student_grade_grade') != grade and \
                get_session_variable('student_grade_class') and \
                get_session_variable('student_grade_subclass') and \
                get_session_variable('student_grade_first_name') and \
                get_session_variable('student_grade_second_name') and \
                get_session_variable('student_grade_subject'):
            try:
                grade = int(grade)

                if grade >= 1 and grade <= 5:
                    session['student_grade_grade'] = grade

            except (ValueError, TypeError):
                pass

    if 'student_grade_change' in values_dict.keys():
        if get_session_variable('student_grade_grade') and \
                get_session_variable('student_grade_class') and \
                get_session_variable('student_grade_subclass') and \
                get_session_variable('student_grade_first_name') and \
                get_session_variable('student_grade_second_name') and \
                get_session_variable('student_grade_subject') and \
                get_session_variable('student_grade_grade'):
            query = \
                '''
                UPDATE {}
                SET {} = {}
                WHERE class = {}
                AND subclass = "{}"
                AND first_name = "{}"
                AND second_name = "{}"
                AND third_name {}
                '''.format(
                    DBWriter.TABLE_STUDENTS_NAME,
                    get_session_variable('student_grade_subject') + '_grade',
                    get_session_variable('student_grade_grade'),
                    get_session_variable('student_grade_class'),
                    get_session_variable('student_grade_subclass'),
                    get_session_variable('student_grade_first_name'),
                    get_session_variable('student_grade_second_name'),
                    'IS NULL' \
                            if get_session_variable('student_grade_third_name') == '(нет)' \
                            else '= "{}"'.format(get_session_variable('student_grade_third_name'))
                )

            DBWriter.send_query(query)
            result = DBWriter.save_changes()

    return result

import db_manipulate.db_connector as db_connector

def get_inquire(values_dict: dict, session, DBReader) -> bool:
    result = False

    if type(values_dict) is not dict or \
            type(DBReader) is not db_connector.DBFetcher:
        return result

    get_session_variable = lambda session_variable: \
                         session[session_variable] if session_variable in session.keys() else None
    
    if 'students_class' in values_dict.keys():
        students_class = values_dict['students_class']

        try:
            students_class = int(students_class)

            if students_class >= 1 and students_class <= 11:
                if get_session_variable('students_class') != students_class:
                    session['students_class'] = students_class
                    session['students_subclasses'] = []
                    session['students_subclass'] = ''
                    session['students_n'] = 0

                    query = \
                            '''
                            SELECT DISTINCT subclass FROM {}
                            WHERE class = {}
                            '''.format(
                                DBReader.TABLE_STUDENTS_NAME,
                                get_session_variable('students_class')
                            )

                    students_subclasses = DBReader.send_query(query)
                    
                    if students_subclasses:
                        students_subclasses = [subcl[0] for subcl in students_subclasses]
                        session['students_subclasses'] = students_subclasses

        except (ValueError, TypeError):
            pass

    if 'students_subclass' in values_dict.keys():
        students_subclass = values_dict['students_subclass']

        if students_subclass and students_subclass in get_session_variable('students_subclasses') and \
                get_session_variable('students_class'):
            session['students_subclass'] = students_subclass

            query = \
                    '''
                    SELECT COUNT(first_name) AS FirstName FROM {}
                    WHERE class = {}
                    '''.format(
                        DBReader.TABLE_STUDENTS_NAME,
                        get_session_variable('students_class')
                    )

            students_amount = DBReader.send_query(query)
            
            if students_amount:
                students_amount = students_amount[0][0]
                session['students_amount'] = students_amount

    if 'teachers_subject_amount' in values_dict.keys():
        teachers_subject = values_dict['teachers_subject_amount']

        if teachers_subject != get_session_variable('teachers_subject'):
            session['teachers_subject'] = teachers_subject

            if get_session_variable('teachers_subject'):
                query = \
                        '''
                        SELECT DISTINCT first_name,second_name,third_name FROM {}
                        WHERE subject = "{}"
                        '''.format(
                            DBReader.TABLE_TEACHERS_NAME,
                            get_session_variable('teachers_subject')
                        )

                teachers = DBReader.send_query(query)

                if teachers:
                    session['teachers_amount'] = len(teachers)

    if 'cabinets_amount_get' in values_dict.keys():
        if values_dict['cabinets_amount_get']:
            query = \
                    '''
                    SELECT DISTINCT classroom FROM {}
                    WHERE classroom IS NOT NULL
                    '''.format(
                        DBReader.TABLE_TEACHERS_NAME
                    )

            classrooms = DBReader.send_query(query)
            
            if classrooms:
                session['cabinets_amount'] = len(classrooms)

    return result

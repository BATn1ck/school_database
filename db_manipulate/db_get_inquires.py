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

    if 'students_classes_amount_get' in values_dict.keys():
        amount = []

        if values_dict['students_classes_amount_get']:
            for cl in range(1, 12):
                query = \
                        '''
                        SELECT DISTINCT * FROM {}
                        WHERE class = {}
                        '''.format(
                            DBReader.TABLE_STUDENTS_NAME,
                            cl
                        )

                amount_students = DBReader.send_query(query)

                if amount_students:
                    amount_students = len(amount_students)
                else:
                    amount_students = 0

                amount.append(amount_students)
        
        session['students_classes_amount'] = amount

    if 'students_progress_class' in values_dict.keys():
        stud_class = values_dict['students_progress_class']

        try:
            stud_class = int(stud_class)

            if get_session_variable('students_progress_class') != stud_class and \
                    stud_class >= 1 and stud_class <= 11:
                session['students_progress_class'] = stud_class
                session['students_progress_subclasses'] = []
                session['students_progress_subclass'] = ''
                session['students_progress_losers_amount'] = 0
                session['students_progress_good_amount'] = 0
                session['students_progress_excellent_amount'] = 0

                query = \
                        '''
                        SELECT DISTINCT subclass FROM {}
                        WHERE class = {}
                        '''.format(
                            DBReader.TABLE_STUDENTS_NAME,
                            get_session_variable('students_progress_class')
                        )

                stud_subclasses = DBReader.send_query(query)

                if stud_subclasses:
                    stud_subclasses = [subcl[0] for subcl in stud_subclasses]
                    session['students_progress_subclasses'] = stud_subclasses

        except (ValueError, TypeError):
            pass

    if 'students_progress_subclass' in values_dict.keys():
        stud_subclass = values_dict['students_progress_subclass']

        if get_session_variable('students_progress_subclass') != stud_subclass and \
                type(stud_subclass) is str and \
                len(stud_subclass) == 1:
            session['students_progress_subclass'] = stud_subclass
            session['students_progress_losers_amount'] = 0
            session['students_progress_good_amount'] = 0
            session['students_progress_excellent_amount'] = 0

            query = \
                    '''
                    SELECT * FROM {}
                    WHERE class = {}
                    AND subclass = "{}"
                    '''.format(
                        DBReader.TABLE_STUDENTS_NAME,
                        get_session_variable('students_progress_class'),
                        get_session_variable('students_progress_subclass')
                    )

            grades = DBReader.send_query(query)
            amount_losers = 0
            amount_good = 0
            amount_excellent = 0

            if grades:
                for stud_grades in grades:
                    n_grades = 0
                    average = 0

                    for gr in stud_grades[5:]:
                        if gr:
                            average += gr
                            n_grades += 1

                    average /= n_grades

                    if average < 3:
                        amount_losers += 1
                    elif average >= 4 and average < 5:
                        amount_good += 1
                    elif average == 5:
                        amount_excellent += 1

            session['students_progress_losers_amount'] = amount_losers
            session['students_progress_good_amount'] = amount_good
            session['students_progress_excellent_amount'] = amount_excellent

    return result

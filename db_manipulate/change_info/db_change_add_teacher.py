import db_manipulate.db_connector as db_connector
from school_web_forms import *

def add_teacher(form_teacher: TeacherForm, DBWriter) -> str:
    result = ''

    if not form_teacher or \
            type(form_teacher) is not TeacherForm or \
            not form_teacher.validate_on_submit():
        return result

    first_name = form_teacher.first_name.data
    second_name = form_teacher.second_name.data
    third_name = form_teacher.third_name.data
    lesson = form_teacher.lesson.data
    cabinet_num = form_teacher.cabinet_num.data
    class_num = form_teacher.class_num.data
    subclass = form_teacher.subclass.data

    query = \
            '''
            INSERT INTO {}
            VALUES (
            "{}", "{}", {},
            "{}", {},
            {}, "{}"
            )
            '''.format(
                DBWriter.TABLE_TEACHERS_NAME,
                first_name,
                second_name,
                'NULL' if not third_name else '"{}"'.format(third_name),
                lesson,
                'NULL' if not cabinet_num else cabinet_num,
                class_num,
                subclass
            )

    DBWriter.send_query(query):
    
    if DBWriter.save_changes():
        result = 'Учитель: успешно добавлен'
    else:
        result = 'Ошибка добавления учителя'

    return result

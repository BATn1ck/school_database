import db_manipulate.db_connector as db_connector

def detele_student(values_dict: dict, session, DBWriter: db_connector.DBEditor) -> bool:
    if 'student_delete_class' in values_dict.keys():
        pass

#!/usr/bin/env python
import secrets 

from db_manipulate import db_connector, db_get_subject, db_get_teacher
from flask import Flask, render_template, request, session, redirect
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
bootstrap = Bootstrap(app)

get_session_variable = lambda session_variable: \
        session[session_variable] if session_variable in session.keys() else None

@app.route("/", methods=['GET', 'POST'])
def main():
    taked_subject = '' 
    if request.method == 'POST':
        values_dict = request.values.to_dict()
        #print(values_dict)
        taked_subject = db_get_subject.handle_subject(values_dict, session, DBReader)
        taked_teacher = db_get_teacher.handle_teacher(values_dict, session, DBReader)
        
        if taked_subject:
            session['taked_subject'] = taked_subject

        if taked_teacher:
            session['taked_teacher'] = taked_teacher

        return redirect('/')

    #print(session)
    return render_template('index.html', \
        subject_day_week=get_session_variable("subject_day_week"), \
        subject_lesson_num=get_session_variable("subject_lesson_num"), \
        subject_classes=get_session_variable("subject_classes"), \
        subject_class=get_session_variable("subject_class"), \
        subject_subclasses=get_session_variable("subject_subclasses"), \
        subject_subclass=get_session_variable("subject_subclass"), \
        taked_subject=get_session_variable("taked_subject"), \

        teacher_lessons=teacher_lessons, \
        teacher_lesson=get_session_variable("teacher_lesson"), \
        teacher_class=get_session_variable("teacher_class"), \
        taked_teacher=get_session_variable("taked_teacher"), \

        subclasses=teacher_subclasses
    )

if __name__ == "__main__":
    DBReader = db_connector.DBFetcher(host="localhost", database="school", user="root", password="1234")
    teacher_lessons, teacher_subclasses = db_get_teacher.get_teacher_info(DBReader)
    app.run(debug=True)

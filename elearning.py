from app.models import Teacher, Student, Parent, StudentComment
from app import create_app, db

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Parent': Parent,
        'Student': Student,
        'Teacher': Teacher,
        'StudentComment': StudentComment
    }

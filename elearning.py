from app import app, db
from app.models import Teacher, Student, Parent, StudentComment


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Parent': Parent,
        'Student': Student,
        'Teacher': Teacher,
        'StudentComment': StudentComment
    }

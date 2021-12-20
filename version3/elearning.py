from app import app, db
from app.models import Client, CommunityComment, WebDevChapter1Comment,\
    WebDevChapter1Objectives, WebDevChapter1Quiz, Student, Parent


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        Student=Student,
        Parent=Parent,
        Client=Client,
        CommunityComment=CommunityComment,
        WebDevChapter1Comment=WebDevChapter1Comment,
        WebDevChapter1Objectives=WebDevChapter1Objectives,
        WebDevChapter1Quiz=WebDevChapter1Quiz
        )

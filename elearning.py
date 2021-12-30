from app import create_app, db
from app.models import CommunityComment, WebDevChapter1Comment,\
    WebDevChapter1Objectives, WebDevChapter1Quiz, Student, Parent,\
    Teacher, WebDevChapter1QuizOptions, AnonymousTemplateInheritanceComment,\
    User, Admin, Courses, FlaskStudentStories, WebDevelopmentOverview,\
    TableOfContents, Chapter, ChapterObjectives,ChapterQuiz

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        Student=Student,
        Parent=Parent,
        Teacher=Teacher,
        CommunityComment=CommunityComment,
        WebDevChapter1Comment=WebDevChapter1Comment,
        WebDevChapter1Objectives=WebDevChapter1Objectives,
        WebDevChapter1Quiz=WebDevChapter1Quiz,
        WebDevChapter1QuizOptions=WebDevChapter1QuizOptions,
        AnonymousTemplateInheritanceComment=AnonymousTemplateInheritanceComment,
        User=User,
        Admin=Admin,
        Courses=Courses,
        FlaskStudentStories=FlaskStudentStories,
        WebDevelopmentOverview=WebDevelopmentOverview,
        TableOfContents=TableOfContents,
        Chapter=Chapter,
        ChapterObjectives=ChapterObjectives,
        ChapterQuiz=ChapterQuiz
        )
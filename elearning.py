from app import create_app, db
from app.models import CommunityComment, WebDevChapter1Comment,\
    WebDevChapter1Objectives, WebDevChapter1Quiz, Student, Parent,\
    Teacher, AnonymousTemplateInheritanceComment,\
    User, Admin, Courses, FlaskStudentStories, WebDevelopmentOverview,\
    TableOfContents, Chapter, ChapterQuiz,\
    WebDevChapter1Quiz1Options, WebDevChapter1Quiz2Options,\
    WebDevChapter1Quiz3Options, WebDevChapter1Quiz4Options, BlogArticles,\
    Events, TeacherMessage, TeacherNotifications, StudentMessage,\
    StudentNotification, WebDevChapter2Comment, WebDevChapter2Objectives,\
    WebDevChapter2Quiz, WebDevChapter2Quiz1Options,\
    WebDevChapter2Quiz2Options, WebDevChapter2Quiz3Options,\
    WebDevChapter2Quiz4Options, WebDevChapter1Quiz5Options, \
    WebDevChapter2Quiz5Options

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
        AnonymousTemplateInheritanceComment=AnonymousTemplateInheritanceComment,
        User=User,
        Admin=Admin,
        Courses=Courses,
        FlaskStudentStories=FlaskStudentStories,
        WebDevelopmentOverview=WebDevelopmentOverview,
        TableOfContents=TableOfContents,
        Chapter=Chapter,
        ChapterQuiz=ChapterQuiz,
        BlogArticles=BlogArticles,
        WebDevChapter1Quiz1Options=WebDevChapter1Quiz1Options,
        WebDevChapter1Quiz2Options=WebDevChapter1Quiz2Options,
        WebDevChapter1Quiz3Options=WebDevChapter1Quiz3Options,
        WebDevChapter1Quiz4Options=WebDevChapter1Quiz4Options,
        Events=Events,
        TeacherMessage=TeacherMessage,
        TeacherNotifications=TeacherNotifications,
        StudentMessage=StudentMessage,
        StudentNotification=StudentNotification,
        WebDevChapter2Comment=WebDevChapter2Comment,
        WebDevChapter2Objectives=WebDevChapter2Objectives,
        WebDevChapter2Quiz=WebDevChapter2Quiz,
        WebDevChapter2Quiz1Options=WebDevChapter2Quiz1Options,
        WebDevChapter2Quiz2Options=WebDevChapter2Quiz2Options,
        WebDevChapter2Quiz3Options=WebDevChapter2Quiz3Options,
        WebDevChapter2Quiz4Options=WebDevChapter2Quiz4Options,
        WebDevChapter1Quiz5Options=WebDevChapter1Quiz5Options,
        WebDevChapter2Quiz5Options=WebDevChapter2Quiz5Options
        )

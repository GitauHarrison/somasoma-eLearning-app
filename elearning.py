from app import create_app, db
from app.models import CommunityComment, WebDevChapter1Comment,\
    WebDevChapter1Objectives, WebDevChapter1QuizTotalScore, Student, Parent,\
    Teacher, AnonymousTemplateInheritanceComment,\
    User, Admin, Courses, FlaskStudentStories, WebDevelopmentOverview,\
    TableOfContents, Chapter, ChapterQuiz,\
    WebDevChapter1Quiz1Options, WebDevChapter1Quiz2Options,\
    WebDevChapter1Quiz3Options, WebDevChapter1Quiz4Options, BlogArticles,\
    Events, TeacherMessage, TeacherNotifications, StudentMessage,\
    StudentNotification, WebDevChapter2Comment, WebDevChapter2Objectives,\
    WebDevChapter2Quiz1Options, WebDevChapter2QuizTotalScore,\
    WebDevChapter2Quiz2Options, WebDevChapter2Quiz3Options,\
    WebDevChapter2Quiz4Options, WebDevChapter1Quiz5Options, \
    WebDevChapter2Quiz5Options, WebDevChapter3Comment,\
    WebDevChapter3Objectives, GeneralMultipleChoicesQuiz,\
    GeneralMultipleChoicesAnswer1, GeneralMultipleChoicesAnswer2,\
    GeneralMultipleChoicesAnswer3, GeneralMultipleChoicesAnswer4,\
    GeneralMultipleChoicesAnswer5, GeneralMultipleChoicesAnswer6,\
    GeneralMultipleChoicesAnswer7, GeneralMultipleChoicesAnswer8,\
    GeneralMultipleChoicesAnswer9, GeneralMultipleChoicesAnswer10,\
    WebDevChapter3QuizTotalScore

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
        WebDevChapter2Quiz1Options=WebDevChapter2Quiz1Options,
        WebDevChapter2Quiz2Options=WebDevChapter2Quiz2Options,
        WebDevChapter2Quiz3Options=WebDevChapter2Quiz3Options,
        WebDevChapter2Quiz4Options=WebDevChapter2Quiz4Options,
        WebDevChapter1Quiz5Options=WebDevChapter1Quiz5Options,
        WebDevChapter2Quiz5Options=WebDevChapter2Quiz5Options,
        WebDevChapter3Comment=WebDevChapter3Comment,
        WebDevChapter3Objectives=WebDevChapter3Objectives,
        GeneralMultipleChoicesQuiz=GeneralMultipleChoicesQuiz,
        GeneralMultipleChoicesAnswer1=GeneralMultipleChoicesAnswer1,
        GeneralMultipleChoicesAnswer2=GeneralMultipleChoicesAnswer2,
        GeneralMultipleChoicesAnswer3=GeneralMultipleChoicesAnswer3,
        GeneralMultipleChoicesAnswer4=GeneralMultipleChoicesAnswer4,
        GeneralMultipleChoicesAnswer5=GeneralMultipleChoicesAnswer5,
        GeneralMultipleChoicesAnswer6=GeneralMultipleChoicesAnswer6,
        GeneralMultipleChoicesAnswer7=GeneralMultipleChoicesAnswer7,
        GeneralMultipleChoicesAnswer8=GeneralMultipleChoicesAnswer8,
        GeneralMultipleChoicesAnswer9=GeneralMultipleChoicesAnswer9,
        GeneralMultipleChoicesAnswer10=GeneralMultipleChoicesAnswer10,
        WebDevChapter1QuizTotalScore=WebDevChapter1QuizTotalScore,
        WebDevChapter2QuizTotalScore=WebDevChapter2QuizTotalScore,\
        WebDevChapter3QuizTotalScore=WebDevChapter3QuizTotalScore
        )

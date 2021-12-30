from app import db
from app.admin import bp
from flask import render_template, redirect, url_for, flash, request,\
    current_app
from app.admin.forms import EditProfileForm, CoursesForm, BlogArticlesForm
from app.auth.forms import TeacherRegistrationForm
from app.models import BlogArticles, CommunityComment, Admin, Student,\
    Teacher, Parent, User, Courses, BlogArticles, FlaskStudentStories
from flask_login import current_user, login_required
from datetime import datetime
from app.admin.email import send_registration_details_teacher,\
    send_flask_stories_email
import os
from werkzeug.utils import secure_filename


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.admin_last_seen = datetime.utcnow()
        db.session.commit()


# Dashboard

@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard_admin():
    admin = Admin.query.filter_by(
        admin_full_name=current_user.admin_full_name
        ).first()

    students = Student.query.order_by(Student.student_last_seen.desc()).all()
    teachers = Teacher.query.order_by(Teacher.teacher_last_seen.desc()).all()
    parents = Parent.query.order_by(Parent.parent_last_seen.desc()).all()
    all_students = len(Student.query.all())
    all_teachers = len(Teacher.query.all())
    all_parents = len(Parent.query.all())

    # ---------------------
    # Teacher Registration
    # ---------------------
    teacher_form = TeacherRegistrationForm()
    if teacher_form.validate_on_submit():
        teacher = Teacher(
            teacher_full_name=teacher_form.teacher_full_name.data,
            teacher_email=teacher_form.teacher_email.data,
            teacher_phone=teacher_form.teacher_phone.data,
            teacher_residence=teacher_form.teacher_residence.data,
            teacher_course=teacher_form.teacher_course.data
        )
        teacher.set_password(teacher_form.teacher_password.data)
        db.session.add(teacher)
        db.session.commit()
        send_registration_details_teacher(teacher)
        flash('Teacher successfully registered')
        return redirect(url_for('admin.dashboard_admin'))
    # ---------------------
    # End of teacher registration
    # ---------------------

    # ----------------
    # Course Offering
    # ----------------
    course_form = CoursesForm()
    if course_form.validate_on_submit():
        course = Courses(
            title=course_form.title.data,
            body=course_form.body.data,
            overview=course_form.overview.data,
            next_class_date=course_form.next_class_date.data,
            link=course_form.link.data
            )

        # Handling file upload
        uploaded_file = course_form.course_image.data
        filename = secure_filename(uploaded_file.filename)
        if not os.path.exists(current_app.config['UPLOAD_PATH']):
            os.makedirs(current_app.config['UPLOAD_PATH'])
        course_image_path = os.path.join(
            current_app.config['UPLOAD_PATH'],
            filename
            )
        print('Img path:', course_image_path)
        uploaded_file.save(course_image_path)
        course.course_image = course_image_path
        print('Db path: ', course.course_image)

        course_image_path_list = course.course_image.split('/')[1:]
        print('Img path list: ', course_image_path_list)
        new_course_image_path = '/'.join(course_image_path_list)
        print('New img path: ', new_course_image_path)
        course.course_image = new_course_image_path
        print(course.course_image)

        db.session.add(course)
        db.session.commit()
        flash('Your course has been updated. Take action now!')
        return redirect(url_for('admin.dashboard_admin', _anchor='courses'))

    page = request.args.get('page', 1, type=int)
    courses = Courses.query.order_by(
        Courses.timestamp.desc()
        ).paginate(
            page,
            current_app.config['POSTS_PER_PAGE'],
            False
            )
    next_url = url_for(
        'admin.dashboard_admin',
        page=courses.next_num,
        _anchor="courses") \
        if courses.has_next else None
    prev_url = url_for(
        'admin.dashboard_admin',
        page=courses.prev_num,
        _anchor="courses") \
        if courses.has_prev else None
    all_courses = len(Courses.query.all())

    # ----------------
    # End of Course Offering
    # ----------------

    # ----------------
    # Blogs: anonymous user
    # ----------------

    blog_articles_form = BlogArticlesForm()
    if blog_articles_form.validate_on_submit():
        blog_articles = BlogArticles(
            article_image=blog_articles_form.article_image.data,
            article_name=blog_articles_form.article_name.data,
            body=blog_articles_form.body.data,
            link=blog_articles_form.link.data
        )

        # Handling file upload
        uploaded_file = blog_articles_form.article_image.data
        filename = secure_filename(uploaded_file.filename)
        if not os.path.exists(current_app.config['UPLOAD_PATH']):
            os.makedirs(current_app.config['UPLOAD_PATH'])
        blog_image_path = os.path.join(
            current_app.config['UPLOAD_PATH'],
            filename
            )
        print('Img path:', blog_image_path)
        uploaded_file.save(blog_image_path)
        blog_articles.article_image = blog_image_path
        print('Db path: ', blog_articles.article_image)

        blog_image_path_list = blog_articles.article_image.split('/')[1:]
        print('Img path list: ', blog_image_path_list)
        new_blog_image_path = '/'.join(blog_image_path_list)
        print('New img path: ', new_blog_image_path)
        blog_articles.article_image = new_blog_image_path
        print(blog_articles.article_image)

        db.session.add(blog_articles)
        db.session.commit()
        flash('You have addeded a new blog article')
        return redirect(url_for('admin.dashboard_admin'))
    all_blog_articles = len(BlogArticles.query.all())

    # ----------------
    # End of Blogs: anonymous user
    # ----------------

    return render_template(
        'admin/dashboard_admin.html',
        title='Admin Dashboard',
        admin=admin,

        # All users
        students=students,
        teachers=teachers,
        parents=parents,

        all_students=all_students,
        all_teachers=all_teachers,
        all_parents=all_parents,

        # Forms
        teacher_form=teacher_form,
        course_form=course_form,

        # Courses
        courses=courses.items,
        next_url=next_url,
        prev_url=prev_url,
        all_courses=all_courses,

        # Blog
        blog_articles_form=blog_articles_form,
        all_blog_articles=all_blog_articles
        )


# Profile routes


@bp.route('/profile/<admin_full_name>')
@login_required
def profile_admin(admin_full_name):
    admin = Admin.query.filter_by(
        admin_full_name=admin_full_name
        ).first_or_404()
    page = request.args.get('page', 1, type=int)
    comments = admin.comments.order_by(
        CommunityComment.timestamp.desc()
        ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'admin.dashboard_admin', admin_full_name=admin_full_name,
        page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for(
        'admin.dashboard_admin', admin_full_name=admin_full_name,
        page=comments.prev_num) \
        if comments.has_prev else None
    return render_template(
        'admin/profile_admin.html',
        title='Profile',
        admin=admin,
        comments=comments.items,
        next_url=next_url,
        prev_url=prev_url
    )

# Edit profile routes


@bp.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile_admin():
    admin = Admin.query.filter_by(
        admin_full_name=current_user.admin_full_name
        ).first()
    form = EditProfileForm(current_user.admin_email)
    if form.validate_on_submit():
        current_user.admin_email = form.email.data
        current_user.admin_about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('admin.dashboard_admin'))
    elif request.method == 'GET':
        form.email.data = current_user.admin_email
        form.about_me.data = current_user.admin_about_me
    return render_template(
        'admin/edit_profile_admin.html',
        title='Edit Profile',
        form=form,
        admin=admin
    )

# ==========================================
# DELETE USERS ACCOUNT
# ==========================================


@bp.route('/student/<student_id>/delete-account')
def delete_account_student(student_id):
    student = Student.query.filter_by(
        id=student_id
        ).first()
    db.session.delete(student)
    db.session.commit()
    flash(f'Student {student_id} account has been deleted!')
    return redirect(url_for('admin.dashboard_admin'))


@bp.route('/teacher/<teacher_id>/delete-account')
def delete_account_teacher(teacher_id):
    teacher = Teacher.query.filter_by(
        id=teacher_id
        ).first()
    db.session.delete(teacher)
    db.session.commit()
    flash(f'Teacher {teacher_id} account has been deleted!')
    return redirect(url_for('admin.dashboard_admin'))


@bp.route('/parent/<parent_id>/delete-account')
def delete_account_parent(parent_id):
    parent = Parent.query.filter_by(
        id=parent_id
        ).first()
    db.session.delete(parent)
    db.session.commit()
    flash(f'Parent {parent_id} account has been deleted!')
    return redirect(url_for('admin.dashboard_admin'))

# ==========================================
# END OF DELETE USERS ACCOUNT
# ==========================================

# ==========================================
# MANAGE COURSES
# ==========================================


@bp.route('/admin/courses/<course_id>/delete')
def delete_course(course_id):
    course = Courses.query.filter_by(
        id=course_id
        ).first()
    db.session.delete(course)
    db.session.commit()
    flash(f'Course {course_id} has been deleted!')
    return redirect(url_for('admin.dashboard_admin', _anchor='courses'))


@bp.route('/admin/courses/<course_id>/allow', methods=['GET', 'POST'])
def allow_course(course_id):
    course = Courses.query.filter_by(
        id=course_id
        ).first()
    course.allowed_status = True
    db.session.commit()
    flash(f'Course {course_id} has been authorized!')
    return redirect(url_for('admin.dashboard_admin', _anchor="courses"))


# ==========================================
# END OF MANAGE COURSES
# ==========================================

# ==========================================
# MANAGE BLOG POSTS
# ==========================================

@bp.route('/blog/articles/review')
@login_required
def review_blog_articles():
    admin = Admin.query.filter_by(
        admin_full_name=current_user.admin_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    blogs = BlogArticles.query.order_by(
        BlogArticles.timestamp.desc()
        ).paginate(
            page,
            current_app.config['POSTS_PER_PAGE'],
            False
            )
    next_url = url_for(
        'admin.review_blog_articles',
        page=blogs.next_num,
        _anchor="blog") \
        if blogs.has_next else None
    prev_url = url_for(
        'admin.review_blog_articles',
        page=blogs.prev_num,
        _anchor="blog") \
        if blogs.has_prev else None
    all_blogs = len(BlogArticles.query.all())
    return render_template(
        'admin/review_blog_article.html',
        title='Review Blog Article',
        blogs=blogs.items,
        next_url=next_url,
        prev_url=prev_url,
        all_blogs=all_blogs,
        admin=admin
    )


@bp.route('blog/articles/<blog_article_id>/delete')
def delete_blog_article(blog_article_id):
    blog_article = BlogArticles.query.filter_by(
        id=blog_article_id
    ).first()
    db.session.delete(blog_article)
    db.session.commit()
    flash(f'Blog article {blog_article_id} has been deleted')
    return redirect(url_for('admin.dashboard_admin'))


@bp.route('/blog/articles/<blog_article_id>/allow')
def allow_blog_article(blog_article_id):
    blog_article = BlogArticles.query.filter_by(
        id=blog_article_id
    ).first()
    blog_article.allowed_status = True
    db.session.commit()
    flash(f'Blog article {blog_article_id} has been authorized')
    return redirect(url_for('admin.dashboard_admin'))

# ==========================================
# END OF MANAGE BLOG POSTS
# ==========================================

# ==========================================
# MANAGE STUDENT STORIES
# ==========================================


# Flask


@bp.route('/student-stories/flask/review')
@login_required
def review_flask_stories():
    admin = Admin.query.filter_by(
        admin_full_name=current_user.admin_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    flask_students = FlaskStudentStories.query.order_by(
        FlaskStudentStories.timestamp.desc()
        ).paginate(
            page,
            current_app.config['POSTS_PER_PAGE'],
            False
            )
    next_url = url_for(
        'admin.review_flask_stories',
        page=flask_students.next_num,
        _anchor="student-stories") \
        if flask_students.has_next else None
    prev_url = url_for(
        'admin.review_flask_stories',
        page=flask_students.prev_num,
        _anchor="student-stories") \
        if flask_students.has_prev else None
    all_flask_students = len(FlaskStudentStories.query.all())
    return render_template(
        'admin/stories/flask.html',
        title='Review Flask Stories',
        flask_students=flask_students.items,
        next_url=next_url,
        prev_url=prev_url,
        all_flask_students=all_flask_students,
        admin=admin
        )


@bp.route('/student-stories/flask/<int:id>/delete')
def delete_flask_stories(id):
    student = FlaskStudentStories.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash(f'Flask story {id} has been deleted.')
    return redirect(url_for(
        'admin.review_flask_stories',
        _anchor="student-stories"
        )
    )


@bp.route('/student-stories/flask/<int:id>/allow')
def allow_flask_stories(id):
    student = FlaskStudentStories.query.get_or_404(id)
    student.allowed_status = True
    db.session.add(student)
    db.session.commit()
    send_flask_stories_email(student)
    flash(f'Flask story {id} has been approved.')
    return redirect(url_for(
        'admin.review_flask_stories',
        _anchor="student-stories"
        )
    )
# ==========================================
# MANAGE STUDENT STORIES
# ==========================================
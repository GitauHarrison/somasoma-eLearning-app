from flask import flash, url_for, redirect, current_app, session, jsonify,\
    render_template, request
from app.main import bp
from app import db
from flask_login import login_required, current_user
import stripe
from datetime import datetime
from app.models import Teacher, Student, Parent, ParentComment, TeacherComment,\
    StudentComment
from app.main.forms import EmptyForm, CommentForm, ParentEditProfileForm,\
    StudentEditProfileForm, TeacherEditProfileForm


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


# Anonymous User

@bp.route('/')
@bp.route('/home')
def home():
    return render_template('home.html')


@bp.route('/python')
def python_course():
    return render_template('courses/home_page_courses/python_course.html',
                           title='Python'
                           )


@bp.route('/scratch-jr')
def scratch_jr_course():
    return render_template('courses/home_page_courses/scratch_jr_course.html',
                           title='Scratch Jr'
                           )


@bp.route('/scratch')
def scratch_course():
    return render_template('courses/home_page_courses/scratch_course.html',
                           title='Scratch'
                           )


# --------------------------
# Logged In Student Courses
# --------------------------


@bp.route('/student/<username>/courses')
@login_required
def student_paid_courses(username):
    student = Student.query.filter_by(username=username).first()
    return render_template('courses/signed_up_user_courses/python_course.html',
                           student=student,
                           title='Your Courses'
                           )


@bp.route('/student/<username>/courses/python', methods=['GET', 'POST'])
@login_required
def student_start_python(username):
    student = Student.query.filter_by(username=username).first_or_404()
    all_students = Student.query.all()
    form = CommentForm()
    if form.validate_on_submit():
        comment = StudentComment(body=form.body.data,
                                 author=current_user)
        db.session.add(comment)
        db.session.commit()
        flash('You will receive an email when your comment is live')
        return redirect(url_for('main.student_start_python',
                                username=current_user.username
                                )
                        )
    page = request.args.get('page', 1, type=int)
    comments = StudentComment.query.order_by(
        StudentComment.timestamp.asc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False
        )
    next_url = url_for('main.student_start_python',
                       username=current_user.username,
                       _anchor='comments',
                       page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for('main.student_start_python',
                       username=current_user.username,
                       _anchor='comments',
                       page=comments.prev_num) \
        if comments.has_prev else None
    all_comments = StudentComment.query.all()
    total_comments = len(all_comments)
    return render_template('courses/signed_up_user_courses/python_course_content.html',
                           student=student,
                           form=form,
                           title='Python',
                           total_comments=total_comments,
                           next_url=next_url,
                           prev_url=prev_url,
                           comments=comments.items,
                           all_students=all_students
                           )


# ------------
# User Profile
# ------------

@bp.route('/profile/parent/<username>')
@login_required
def parent_profile(username):
    parent = Parent.query.filter_by(username=username).first_or_404()
    return render_template('parent_profile.html',
                           parent=parent,
                           title='Parent Profile'
                           )


@bp.route('/profile/parent/<username>/edit-profile', methods=['GET', 'POST'])
def edit_parent_profile(username):
    parent = Parent.query.filter_by(username=username).first_or_404()
    form = ParentEditProfileForm(parent.username)
    if form.validate_on_submit():
        parent.username = form.username.data
        parent.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('main.parent_profile',
                                username=parent.username))
    elif request.method == 'GET':
        form.username.data = parent.username
        form.about_me.data = parent.about_me
    return render_template('edit_profile.html',
                           form=form,
                           title='Edit Parent Profile'
                           )


@bp.route('/profile/parent/<username>/comments')
@login_required
def parent_profile_comment(username):
    parent = Parent.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    comments = parent.comments.order_by(
        ParentComment.timestamp.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False
        )
    next_url = url_for('main.parent_profile_comment',
                       username=current_user.username,
                       _anchor='comments',
                       page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for('main.parent_profile_comment',
                       username=current_user.username,
                       _anchor='comments',
                       page=comments.prev_num) \
        if comments.has_prev else None
    return render_template('comments/parent_profile_comment.html',
                           parent=parent,
                           title='Parent Comment',
                           next_url=next_url,
                           prev_url=prev_url,
                           comments=comments.items
                           )


@bp.route('/profile/student/<username>')
@login_required
def student_profile(username):
    student = Student.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    return render_template('student_profile.html',
                           student=student,
                           form=form,
                           title='Student Profile'
                           )


@bp.route('/profile/student/<username>/edit-profile', methods=['GET', 'POST'])
def edit_student_profile(username):
    student = Student.query.filter_by(username=username).first_or_404()
    form = StudentEditProfileForm(student.username)
    if form.validate_on_submit():
        student.username = form.username.data
        student.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('main.student_profile',
                                username=student.username))
    elif request.method == 'GET':
        form.username.data = student.username
        form.about_me.data = student.about_me
    return render_template('edit_profile.html',
                           form=form,
                           title='Edit Student Profile'
                           )


@bp.route('/profile/student/<username>/comments')
def student_profile_comment(username):
    student = Student.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    comments = student.comments.order_by(
        StudentComment.timestamp.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False
        )
    next_url = url_for('main.student_profile_comment',
                       username=current_user.username,
                       _anchor='comments',
                       page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for('main.student_profile_comment',
                       username=current_user.username,
                       _anchor='comments',
                       page=comments.prev_num) \
        if comments.has_prev else None
    return render_template('comments/student_profile_comment.html',
                           student=student,
                           title='Student Comment',
                           next_url=next_url,
                           prev_url=prev_url,
                           comments=comments.items
                           )


@bp.route('/profile/teacher/<username>')
@login_required
def teacher_profile(username):
    teacher = Teacher.query.filter_by(username=username).first_or_404()
    return render_template('teacher_profile.html',
                           teacher=teacher,
                           title='Teacher Profile'
                           )


@bp.route('/profile/teacher/<username>/edit-profile', methods=['GET', 'POST'])
def edit_teacher_profile(username):
    teacher = Teacher.query.filter_by(username=username).first_or_404()
    form = TeacherEditProfileForm(teacher.username)
    if form.validate_on_submit():
        teacher.username = form.username.data
        teacher.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('main.teacher_profile',
                                username=teacher.username))
    elif request.method == 'GET':
        form.username.data = teacher.username
        form.about_me.data = teacher.about_me
    return render_template('edit_profile.html',
                           form=form,
                           title='Edit Teacher Profile'
                           )


@bp.route('/profile/teacher/<username>/comments')
@login_required
def teacher_profile_comment(username):
    teacher = Teacher.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    comments = teacher.comments.order_by(
        TeacherComment.timestamp.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False
        )
    next_url = url_for('main.teacher_profile_comment',
                       username=current_user.username,
                       _anchor='comments',
                       page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for('main.teacher_profile_comment',
                       username=current_user.username,
                       _anchor='comments',
                       page=comments.prev_num) \
        if comments.has_prev else None
    return render_template('comments/teacher_profile_comment.html',
                           teacher=teacher,
                           title='Teacher Comment',
                           next_url=next_url,
                           prev_url=prev_url,
                           comments=comments.items
                           )


@bp.route('/profile/parents/all')
@login_required
def all_parents():
    page = request.args.get('page', 1, type=int)
    comments = ParentComment.query.order_by(
        ParentComment.timestamp.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False
        )
    next_url = url_for('main.all_parents',
                       _anchor='comments',
                       page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for('main.all_parents',
                       _anchor='comments',
                       page=comments.prev_num) \
        if comments.has_prev else None
    return render_template('all_parents.html',
                           title='Parents Comments',
                           next_url=next_url,
                           prev_url=prev_url,
                           comments=comments.items
                           )


@bp.route('/profile/students/all')
@login_required
def all_students():
    page = request.args.get('page', 1, type=int)
    comments = StudentComment.query.order_by(
        StudentComment.timestamp.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False
        )
    next_url = url_for('main.all_students',
                       _anchor='comments',
                       page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for('main.all_students',
                       _anchor='comments',
                       page=comments.prev_num) \
        if comments.has_prev else None
    return render_template('all_students.html',
                           title='Students Comments',
                           next_url=next_url,
                           prev_url=prev_url,
                           comments=comments.items
                           )


@bp.route('/profile/teachers/all')
@login_required
def all_teachers():
    page = request.args.get('page', 1, type=int)
    comments = TeacherComment.query.order_by(
        TeacherComment.timestamp.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False
        )
    next_url = url_for('main.all_teachers',
                       _anchor='comments',
                       page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for('main.all_teachers',
                       _anchor='comments',
                       page=comments.prev_num) \
        if comments.has_prev else None
    return render_template('all_teachers.html',
                           title='Parent Comment',
                           next_url=next_url,
                           prev_url=prev_url,
                           comments=comments.items
                           )


# -------------------
# End of User Profile
# -------------------


# --------------------------
# STRIPE PAYMENT INTEGRATION
# --------------------------

@bp.route('/student/enrollment')
def student_enrollment():
    return render_template('stripe_student_enrollment.html',
                           title='Student Enrollment'
                           )


@bp.route('/config')
def get_publishable_key():
    stripe_config = {'publicKey': current_app.config['STRIPE_PUBLISHABLE_KEY']}
    return jsonify(stripe_config)


@bp.route('/create-checkout-session')
def create_checkout_session():
    domain_url = 'http://localhost:5000/'
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    try:
        checkout_session = stripe.checkout.Session.create(
            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have
            # the session ID set as a query param
            # success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}'
            success_url=domain_url + 'success',
            cancel_url=domain_url + 'cancelled',
            payment_method_types=['card'],
            billing_address_collection='required',
            mode='payment',
            line_items=[
                {
                    'quantity': 1,
                    'price': 'price_1InHEyFjP6O4anVpZ3hFE4Oi',
                },
                {
                    'quantity': 1,
                    'price': 'price_1InHGrFjP6O4anVpUxhXJJUz',
                },
                {
                    'quantity': 1,
                    'price': 'price_1InHJ0FjP6O4anVpgFRikVVv',
                }
            ]
        )
        return jsonify({'sessionId': checkout_session['id']})
    except Exception as e:
        return jsonify(error=str(e)), 403


@bp.route('/success')
def success():
    return render_template('stripe_success.html', title='Success')


@bp.route('/cancelled')
def cancel():
    return render_template('stripe_cancel.html', title='Cancel')


@bp.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, current_app.config["STRIPE_ENDPOINT_SECRET"]
        )

    except ValueError as e:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return "Invalid signature", 400

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        print("Payment was successful.")
        # TODO: you can run some custom code here

    return "Success", 200

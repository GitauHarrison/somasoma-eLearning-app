from app import db, products
from app.main import bp
from flask import render_template, redirect, url_for, flash, request,\
    current_app, abort
from app.main.forms import CommentForm, EditProfileForm,\
    Chapter1WebDevelopmentForm, QuizForm, Chapter1QuizOptionsForm,\
    EmptyForm, AnonymousCommentForm
from app.models import WebDevChapter1Comment, CommunityComment,\
    WebDevChapter1Objectives, WebDevChapter1Quiz, WebDevChapter1QuizOptions,\
    Parent, Student, Teacher, User, AnonymousTemplateInheritanceComment
from flask_login import current_user, login_required
from datetime import datetime
import stripe


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.student_last_seen = datetime.utcnow()
        db.session.commit()


# ===========================================================
# PAYMENT
# ===========================================================


@bp.route('/checkout')
def checkout():
    return render_template(
        'payment/orders.html',
        title='Orders',
        products=products
    )


@bp.route('/order/<product_id>', methods=['POST'])
def order(product_id):
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    if product_id not in products:
        abort(404)
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                'price_data': {
                    'product_data': {
                        'name': products[product_id]['name'],
                    },
                    'unit_amount': products[product_id]['price'],
                    'currency': 'usd',
                },
                'quantity': 1,
                'adjustable_quantity': products[product_id].get(
                    'adjustable_quantity',
                    {'enabled': False}
                ),
            },
        ],
        payment_method_types=['card'],
        mode='payment',
        success_url=request.host_url + 'order/success',
        cancel_url=request.host_url + 'order/cancel',
    )
    return redirect(checkout_session.url)


@bp.route('/order/success')
def success():
    flash(
        'Thank you for your order! Check your email for further instructions'
        )
    return render_template(
        'payment/success.html',
        title='Order Successful'
        )


@bp.route('/order/cancel')
def cancel():
    flash('Your order has been cancelled')
    return render_template(
        'payment/cancel.html',
        title='Order Cancelled'
        )


@bp.route('/event', methods=['POST'])
def new_event():
    event = None
    payload = request.data
    signature = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, signature, current_app.config['STRIPE_WEBHOOK_SECRET'])
    except Exception as e:
        # the payload could not be verified
        abort(400)

    if event['type'] == 'checkout.session.completed':
        session = stripe.checkout.Session.retrieve(
            event['data']['object'].id, expand=['line_items'])
        print(f'Sale to {session.customer_details.email}:')
        for item in session.line_items.data:
            print(f'  - {item.quantity} {item.description} '
                  f'${item.amount_total/100:.02f} {item.currency.upper()}')

    return {'success': True}


# ===========================================================
# PAYMENT
# ===========================================================


@bp.route('/')
@bp.route('/home')
def home():
    return render_template(
        'main/anonymous-content/home.html',
        title='Home'
        )


@bp.route('/flask-web-deveopment-course')
def flask_web_deveopment_course():
    return render_template(
        'main/anonymous-content/courses_flask_web_development.html',
        title='Flask Web Development Course'
        )


@bp.route('/events')
def events():
    return render_template(
        'main/anonymous-content/events.html',
        title='Events'
        )


@bp.route('/blog')
def blog():
    return render_template(
        'main/anonymous-content/blog.html',
        title='Blog'
        )


@bp.route('/blog/template-inheritance', methods=['GET', 'POST'])
def blog_template_inheritance():
    form = AnonymousCommentForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        comment = AnonymousTemplateInheritanceComment(
            body=form.comment.data,
            author=user
            )
        db.session.add(comment)
        db.session.add(user)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for(
            'main.blog_template_inheritance',
            _anchor='comments'))
    page = request.args.get('page', 1, type=int)
    comments = AnonymousTemplateInheritanceComment.query.order_by(
        AnonymousTemplateInheritanceComment.timestamp.desc()
        ).paginate(
        page,
        current_app.config['POSTS_PER_PAGE'],
        False
        )
    next_url = url_for(
        'main.blog_template_inheritance',
        page=comments.next_num,
        _anchor="comments") \
        if comments.has_next else None
    prev_url = url_for(
        'main.blog_template_inheritance',
        page=comments.prev_num,
        _anchor="comments") \
        if comments.has_prev else None
    all_comments = len(AnonymousTemplateInheritanceComment.query.all())
    return render_template(
        'main/anonymous-content/blog_template_inheritance.html',
        title='Template Inheritance',
        form=form,
        comments=comments.items,
        next_url=next_url,
        prev_url=prev_url,
        all_comments=all_comments
        )

# Dashboard routes


@bp.route('/student/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard_student():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    comments = CommunityComment.query.order_by(
        CommunityComment.timestamp.desc()
        ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    my_comments = current_user.followed_comments().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
                    'main.dashboard_student',
                    page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for(
        'main.dashboard_student',
        page=comments.prev_num) \
        if comments.has_prev else None
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = CommunityComment(
            body=comment_form.comment.data,
            author=current_user
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
        return redirect(url_for('main.dashboard_student'))

    # Calculate the number of objectives achieved
    all_objectives = student.webdev_chapter1_objectives.order_by(
        WebDevChapter1Objectives.timestamp.desc()).all()
    objectives_list = []
    num_of_true_status = 0
    for objective in all_objectives:
        objectives_list.append(objective.objective_1)
        objectives_list.append(objective.objective_2)
        objectives_list.append(objective.objective_3)
        objectives_list.append(objective.objective_4)
        objectives_list.append(objective.objective_5)
        objectives_list.append(objective.objective_6)
        objectives_list.append(objective.objective_7)
    num_of_true_status = objectives_list.count(True)
    try:
        percentage_achieved = round(
            (num_of_true_status / len(objectives_list)) * 100, 2
        )
    except ZeroDivisionError:
        percentage_achieved = 0
    return render_template(
                           'main/dashboard_student.html',
                           title='Student Dashboard',
                           comment_form=comment_form,
                           comments=comments.items,
                           my_comments=my_comments.items,
                           next_url=next_url,
                           prev_url=prev_url,
                           all_objectives=all_objectives,
                           percentage_achieved=percentage_achieved,
                           student=student
                           )


@bp.route('/parent/dashboard')
@login_required
def dashboard_parent():
    parent = Parent.query.filter_by(
        parent_full_name=current_user.parent_full_name
        ).first()
    return render_template(
        'main/dashboard_parent.html',
        title='Parent Dashboard',
        parent=parent
        )


@bp.route('/teacher/dashboard')
@login_required
def dashboard_teacher():
    teacher = Teacher.query.filter_by(
        teacher_full_name=current_user.teacher_full_name
        ).first()
    return render_template(
        'main/dashboard_teacher.html',
        teacher=teacher
        )

# End of dashboard routes

# Profile routes


@bp.route('/student/<student_full_name>/profile')
@login_required
def profile_student(student_full_name):
    student = Student.query.filter_by(
        student_full_name=student_full_name
        ).first_or_404()
    page = request.args.get('page', 1, type=int)
    comments = student.comments.order_by(
        CommunityComment.timestamp.desc()
        ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'main.dashboard_student', student_full_name=student_full_name,
        page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for(
        'main.dashboard_student', student_full_name=student_full_name,
        page=comments.prev_num) \
        if comments.has_prev else None
    form = EmptyForm()
    return render_template(
        'main/profile_student.html',
        title='Profile',
        student=student,
        comments=comments.items,
        next_url=next_url,
        prev_url=prev_url,
        form=form
    )


@bp.route('/student/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile_student():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first()
    form = EditProfileForm(current_user.student_email)
    if form.validate_on_submit():
        current_user.student_email = form.email.data
        current_user.student_about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.dashboard_student'))
    elif request.method == 'GET':
        form.email.data = current_user.student_email
        form.about_me.data = current_user.student_about_me
    return render_template(
        'main/edit_profile_student.html',
        title='Edit Profile',
        form=form,
        student=student
    )

# End of profile routes

# Followership routes


@bp.route('/follow/<student_full_name>', methods=['POST'])
@login_required
def follow_student(student_full_name):
    student = Student.query.filter_by(
        student_full_name=student_full_name
        ).first()
    form = EmptyForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(
            student_full_name=student_full_name
            ).first()
        if student is None:
            flash(f'User {student_full_name} not found')
            return redirect(url_for('main.dashboard_student'))
        if student == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for(
                'main.profile_student',
                student_full_name=student_full_name
                )
            )
        current_user.follow(student)
        db.session.commit()
        flash(f'You are following {student.student_full_name}!')
        return redirect(url_for(
            'main.profile_student',
            student_full_name=student_full_name
            )
        )
    else:
        return redirect(url_for('main.dashboard_student'))


@bp.route('/unfollow/<student_full_name>', methods=['POST'])
@login_required
def unfollow_student(student_full_name):
    student = Student.query.filter_by(
        student_full_name=student_full_name
        ).first()
    form = EmptyForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(
            student_full_name=student_full_name
            ).first()
        if student is None:
            flash(f'User {student_full_name} not found')
            return redirect(url_for('main.dashboard_student'))
        if student == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for(
                'main.profile_student',
                student_full_name=student_full_name
                )
            )
        current_user.unfollow(student)
        db.session.commit()
        flash(f'You are not following {student.student_full_name}!')
        return redirect(url_for(
            'main.profile_student',
            student_full_name=student_full_name
            )
        )
    else:
        return redirect(url_for('main.dashboard_student'))

# End of followership routes

# ========================================
# WEB DEVELOPMENT COURSE ROUTES
# ========================================

# Overview


@bp.route('/student/web-development-overview')
@login_required
def web_development_overview():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first()
    return render_template(
        'main/web-development-course/web_development_overview.html',
        title='Web Development',
        student=student
        )

# Chapters


@bp.route('/student/web-development/chapter-1', methods=['GET', 'POST'])
@login_required
def web_development_chapter_1():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    comments = WebDevChapter1Comment.query.order_by(
        WebDevChapter1Comment.timestamp.desc()
        ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'main.web_development_chapter_1',
        _anchor="comments",
        page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for(
        'main.web_development_chapter_1',
        _anchor='comments',
        page=comments.prev_num) \
        if comments.has_prev else None
    form = CommentForm()
    if form.validate_on_submit():
        comment = WebDevChapter1Comment(
            body=form.comment.data,
            author=current_user
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
        return redirect(url_for(
            'main.web_development_chapter_1',
            _anchor='comments',
            student=student
            )
        )
    all_comments = len(WebDevChapter1Comment.query.all())

    # Objectives form
    objectives_form = Chapter1WebDevelopmentForm()
    if objectives_form.validate_on_submit():
        objectives = WebDevChapter1Objectives(
            objective_1=objectives_form.objective_1.data,
            objective_2=objectives_form.objective_2.data,
            objective_3=objectives_form.objective_3.data,
            objective_4=objectives_form.objective_4.data,
            objective_5=objectives_form.objective_5.data,
            objective_6=objectives_form.objective_6.data,
            objective_7=objectives_form.objective_7.data,
            author=current_user
        )
        db.session.add(objectives)
        db.session.commit()
        flash('Your response has been saved')
        return redirect(url_for(
            'main.web_development_chapter_1',
            _anchor='objectives'
        ))
    return render_template(
        'main/web-development-course/web_development_chapter_1.html',
        title='Chapter 1: Introduction to Web Development',
        form=form,
        objectives_form=objectives_form,
        comments=comments.items,
        next_url=next_url,
        prev_url=prev_url,
        all_comments=all_comments,
        student=student
        )


@bp.route('/student/web-development/chapter-2', methods=['GET', 'POST'])
@login_required
def web_development_chapter_2():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first()
    form = CommentForm()
    return render_template(
        'main/web-development-course/web_development_chapter_2.html',
        title='Chapter 2: What is HTML?',
        form=form,
        student=student
        )

# Objectives


@bp.route('/student/web-development/chapter-1/objectives-status')
@login_required
def web_development_chapter_1_objectives_status():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    objectives = WebDevChapter1Objectives.query.order_by(
        WebDevChapter1Objectives.timestamp.desc()
        ).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for(
        'main.web_development_chapter_1_objectives_status',
        _anchor="objectives",
        page=objectives.next_num) \
        if objectives.has_next else None
    prev_url = url_for(
        'main.web_development_chapter_1_objectives_status',
        _anchor='objectives',
        page=objectives.prev_num) \
        if objectives.has_prev else None
    return render_template(
        'main/web-development-course/chapter_1_objectives_status.html',
        title='Chapter 1: Achievement Status',
        objectives=objectives.items,
        next_url=next_url,
        prev_url=prev_url,
        student=student
        )


# Quizzes


@bp.route('/student/web-development/chapter-1/quizzes/form', methods=['GET', 'POST'])
@login_required
def web_development_chapter_1_quizzes_form():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first()
    form = QuizForm()
    if form.validate_on_submit():
        quiz = WebDevChapter1Quiz(
            title=form.title.data,
            body=form.body.data
        )
        db.session.add(quiz)
        db.session.commit()
        flash('Your quiz has been added!', 'success')
        return redirect(url_for(
            'main.web_development_chapter_1_quizzes_form',
            student_full_name=student.student_full_name
        ))
    return render_template(
        'main/quizzes-forms/quiz_type_1.html',
        title='Quiz Type 1',
        student=student,
        form=form
        )


@bp.route('/student/web-development/chapter-1/quizzes', methods=['GET', 'POST'])
@login_required
def web_development_chapter_1_quiz():
    student = Student.query.filter_by(
        student_full_name=current_user.student_full_name
        ).first()
    page = request.args.get('page', 1, type=int)
    options = WebDevChapter1QuizOptions.query.order_by(
        WebDevChapter1QuizOptions.timestamp.asc()
        ).paginate(
        page, current_app.config['POSTS_PER_QUIZ_PAGE'], False)
    quizzes = WebDevChapter1Quiz.query.order_by(
        WebDevChapter1Quiz.timestamp.asc()
        ).paginate(
        page, current_app.config['POSTS_PER_QUIZ_PAGE'], False)
    next_url = url_for(
        'main.web_development_chapter_1_quiz',
        student_full_name=student.student_full_name,
        _anchor="quizzes",
        page=quizzes.next_num) \
        if quizzes.has_next else None
    prev_url = url_for(
        'main.web_development_chapter_1_quiz',
        student_full_name=student.student_full_name,
        _anchor='quizzes',
        page=quizzes.prev_num) \
        if quizzes.has_prev else None
    form = Chapter1QuizOptionsForm()
    return render_template(
        'main/web-development-course/chapter_1_quizzes.html',
        title='Chapter 1: Quizzes',
        student=student,
        quizzes=quizzes.items,
        options=options.items,
        form=form,
        next_url=next_url,
        prev_url=prev_url
        )

# ========================================
# END OF WEB DEVELOPMENT COURSE ROUTES
# ========================================

from app import db, products
from app.main import bp
from flask import render_template, redirect, url_for, flash, request,\
    current_app, abort
from app.main.forms import AnonymousCommentForm, StudentStoriesForm
from app.models import BlogArticles, Parent, User, Admin,\
    AnonymousTemplateInheritanceComment, Courses, FlaskStudentStories,\
    Events
from app.main.email import send_flask_stories_email
from flask_login import current_user, login_required
from datetime import datetime
import stripe
import os
from werkzeug.utils import secure_filename


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
# END OF PAYMENT
# ===========================================================


@bp.route('/')
@bp.route('/home')
def home():
    return render_template(
        'main/anonymous-content/home.html',
        title='Home'
        )


@bp.route('/courses')
def courses():
    page = request.args.get('page', 1, type=int)
    allowed_courses = Courses.query.filter_by(
        allowed_status=True).order_by(Courses.timestamp.desc()).paginate(
        page,
        current_app.config['POSTS_PER_PAGE'],
        False
        )
    next_url = url_for(
        'main.courses',
        _anchor='courses-offerings',
        page=allowed_courses.next_num) \
        if allowed_courses.has_next else None
    prev_url = url_for(
        'main.courses',
        _anchor='courses-offerings',
        page=allowed_courses.prev_num) \
        if allowed_courses.has_prev else None
    return render_template(
        'main/anonymous-content/courses.html',
        title='Courses',
        allowed_courses=allowed_courses.items,
        next_url=next_url,
        prev_url=prev_url
        )


@bp.route('/flask-web-deveopment-course')
def flask_web_deveopment_course():
    page = request.args.get('page', 1, type=int)
    allowed_students = FlaskStudentStories.query.filter_by(
        allowed_status=True).order_by(
        FlaskStudentStories.timestamp.desc()).paginate(
        page,
        current_app.config['POSTS_PER_PAGE'],
        False
        )
    next_url = url_for(
        'main.flask_web_deveopment_course',
        _anchor='student-stories',
        page=allowed_students.next_num) \
        if allowed_students.has_next else None
    prev_url = url_for(
        'main.flask_web_deveopment_course',
        _anchor='student-stories',
        page=allowed_students.prev_num) \
        if allowed_students.has_prev else None
    return render_template(
        'main/anonymous-content/courses_flask_web_development.html',
        title='Flask Web Development Course',
        allowed_students=allowed_students.items,
        next_url=next_url,
        prev_url=prev_url
        )


@bp.route('/events')
def events():
    page = request.args.get('page', 1, type=int)
    events = Events.query.filter_by(
        allowed_status=True).order_by(
        Events.timestamp.desc()).paginate(
        page,
        current_app.config['POSTS_PER_PAGE'],
        False
        )
    next_url = url_for(
        'main.events',
        _anchor='events',
        page=events.next_num) \
        if events.has_next else None
    prev_url = url_for(
        'main.events',
        _anchor='events',
        page=events.prev_num) \
        if events.has_prev else None
    return render_template(
        'main/anonymous-content/events.html',
        title='Events',
        events=events.items,
        next_url=next_url,
        prev_url=prev_url
        )

# =============================
# BLOG
# =============================


@bp.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    allowed_blogs = BlogArticles.query.filter_by(
        allowed_status=True).order_by(
        BlogArticles.timestamp.desc()).paginate(
        page,
        current_app.config['POSTS_PER_PAGE'],
        False
        )
    next_url = url_for(
        'main.blog',
        _anchor="blogs",
        page=allowed_blogs.next_num) \
        if allowed_blogs.has_next else None
    prev_url = url_for(
        'main.blog',
        _anchor="blogs",
        page=allowed_blogs.prev_num) \
        if allowed_blogs.has_prev else None
    return render_template(
        'main/anonymous-content/blog.html',
        title='Blog',
        allowed_blogs=allowed_blogs.items,
        next_url=next_url,
        prev_url=prev_url
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

# =============================
# END OF BLOG
# =============================

# =============================
# STUDENT STORIES
# =============================


@bp.route('/flask/student-stories/form', methods=['GET', 'POST'])
def flask_student_stories_form():
    form = StudentStoriesForm()
    if form.validate_on_submit():
        student = FlaskStudentStories(
            username=form.username.data,
            email=form.email.data,
            body=form.body.data
            )

        # Handling file upload
        uploaded_file = form.student_image.data
        filename = secure_filename(uploaded_file.filename)
        if not os.path.exists(current_app.config['UPLOAD_PATH']):
            os.makedirs(current_app.config['UPLOAD_PATH'])
        student_image_path = os.path.join(
            current_app.config['UPLOAD_PATH'],
            filename
            )
        print('Img path:', student_image_path)
        uploaded_file.save(student_image_path)
        student.student_image = student_image_path
        print('Db path: ', student.student_image)

        student_image_path_list = student.student_image.split('/')[1:]
        print('Img path list: ', student_image_path_list)
        new_student_image_path = '/'.join(student_image_path_list)
        print('New img path: ', new_student_image_path)
        student.student_image = new_student_image_path
        print(student.student_image)

        db.session.add(student)
        db.session.commit()
        admins = Admin.query.all()
        for admin in admins:
            send_flask_stories_email(admin)
        flash(
            'Your student story has been saved. '
            'You wil receive an email when it is published')
        return redirect(url_for('main.flask_student_stories_form'))
    return render_template(
        'main/anonymous-content/blog_flask_stories_form.html',
        title='Flask Stories',
        form=form
        )

# =============================
# END OF STUDENT STORIES
# =============================


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

# End of dashboard routes

# =============================
# ANONYMOUS CONTENT
# =============================


@bp.route('/unknown-user')
def anonymous_user():
    return render_template(
        'main/anonymous-content/unknown_user.html',
        title='Who Are You?')

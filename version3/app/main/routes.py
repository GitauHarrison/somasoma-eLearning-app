from app import db, products
from app.main import bp
from flask import render_template, redirect, url_for, flash, request,\
    current_app, abort
from app.main.forms import CommentForm, EditProfileForm,\
    Chapter1WebDevelopmentForm, QuizForm, Chapter1QuizOptionsForm,\
    EmptyForm, AnonymousCommentForm
from app.models import WebDevChapter1Comment, CommunityComment,\
    WebDevChapter1Objectives, WebDevChapter1Quiz, WebDevChapter1QuizOptions,\
    Parent, Student, Teacher, User, AnonymousTemplateInheritanceComment, Admin
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
        'Thank you for your order! It will be reviewed and the admin will '
        'contact you shortly via email.',
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
# END OF PAYMENT
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
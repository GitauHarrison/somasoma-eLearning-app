from flask import flash, url_for, redirect, current_app, session, jsonify,\
    render_template, request
from app.main import bp
from app import db
from flask_login import login_required, current_user
import stripe
from datetime import datetime
from app.models import Client, ClientComment
from app.main.forms import EmptyForm, CommentForm, ClientEditProfileForm


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


@bp.route('/client/<username>/courses')
@login_required
def client_paid_courses(username):
    client = Client.query.filter_by(student_username=username).first()
    return render_template('courses/signed_up_user_courses/python_course.html',
                           client=client,
                           title='Your Courses'
                           )


@bp.route('/client/<username>/courses/python', methods=['GET', 'POST'])
@login_required
def client_start_python(username):
    client = Client.query.filter_by(student_username=username).first_or_404()
    clients = Client.query.all()
    form = CommentForm()
    if form.validate_on_submit():
        comment = ClientComment(body=form.body.data,
                                author=current_user)
        db.session.add(comment)
        db.session.commit()
        flash('You will receive an email when your comment is live')
        return redirect(url_for('main.client_start_python',
                                username=current_user.student_username
                                )
                        )
    page = request.args.get('page', 1, type=int)
    comments = ClientComment.query.order_by(
        ClientComment.timestamp.asc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False
        )
    next_url = url_for('main.client_start_python',
                       username=current_user.student_username,
                       _anchor='comments',
                       page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for('main.client_start_python',
                       username=current_user.student_username,
                       _anchor='comments',
                       page=comments.prev_num) \
        if comments.has_prev else None
    all_comments = ClientComment.query.all()
    total_comments = len(all_comments)
    return render_template('courses/signed_up_user_courses/python_course_content.html',
                           client=client,
                           clients=clients,
                           form=form,
                           title='Python',
                           total_comments=total_comments,
                           next_url=next_url,
                           prev_url=prev_url,
                           comments=comments.items,
                           )


# ------------
# User Profile
# ------------

@bp.route('/profile/client/<username>')
@login_required
def client_profile(username):
    client = Client.query.filter_by(student_username=username).first_or_404()
    return render_template('client_profile.html',
                           client=client,
                           title='Client Profile'
                           )


@bp.route('/profile/client/<username>/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_client_profile(username):
    client = Client.query.filter_by(student_username=username).first_or_404()
    form = ClientEditProfileForm(client.student_username)
    if form.validate_on_submit():
        client.student_username = form.username.data
        client.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('main.client_profile',
                                username=client.student_username))
    elif request.method == 'GET':
        form.username.data = client.student_username
        form.about_me.data = client.about_me
    return render_template('edit_profile.html',
                           form=form,
                           title='Edit Client Profile'
                           )


@bp.route('/profile/client/<username>/comments')
@login_required
def client_profile_comment(username):
    client = Client.query.filter_by(student_username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    comments = client.posts.order_by(
        ClientComment.timestamp.asc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False
        )
    next_url = url_for('main.client_profile_comment',
                       username=current_user.student_username,
                       _anchor='comments',
                       page=comments.next_num) \
        if comments.has_next else None
    prev_url = url_for('main.client_profile_comment',
                       username=current_user.student_username,
                       _anchor='comments',
                       page=comments.prev_num) \
        if comments.has_prev else None
    return render_template('comments/client_profile_comment.html',
                           client=client,
                           title='Client Comment',
                           next_url=next_url,
                           prev_url=prev_url,
                           comments=comments.items,
                           )


@bp.route('/profile/clients/all')
@login_required
def all_clients():
    return render_template('all_clients.html',
                           title='Clients Comments'
                           )


# -------------------
# End of User Profile
# -------------------


# --------------------------
# STRIPE PAYMENT INTEGRATION
# --------------------------

@bp.route('/client/enrollment')
def client_enrollment():
    return render_template('stripe_client_enrollment.html',
                           title='Client Enrollment'
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

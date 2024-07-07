from flask import Blueprint, request
from controllers.userController import get_users, add_user, login_user, verify_otp, guest_login, add_google_user

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/', methods=['GET'])
def get_users_route():
    return get_users()

@user_bp.route('/add', methods=['POST'])
def add_user_route():
    return add_user(request)

@user_bp.route('/login', methods=['POST'])
def login_user_route():
    return login_user(request)

@user_bp.route('/verify-otp', methods=['POST'])
def verify_otp_route():
    return verify_otp()

@user_bp.route('/guest-login', methods=['POST'])
def guest_login_route():
    return guest_login(request)

@user_bp.route('/addGoogleUser', methods=['POST'])
def add_google_user_route():
    return add_google_user()

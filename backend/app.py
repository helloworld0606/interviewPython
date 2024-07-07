from flask import Flask, request
from flask_cors import CORS
from routes.userRoutes import user_bp
from routes.otpRoutes import otp_bp
from utils.fileUtils import init_data_file, read_data, write_data, read_guest_data, write_guest_data
from controllers.userController import login_user, add_google_user, verify_otp

app = Flask(__name__)
CORS(app)

app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(otp_bp, url_prefix='/2fa')

@app.route('/login', methods=['POST'])
def login():
    return login_user(request)

@app.route('/addGoogleUser', methods=['POST'])
def add_google_user_route():
    return add_google_user(request)

@app.route('/verify-otp', methods=['POST'])
def verify_otp_route():
    return verify_otp(request)

if __name__ == '__main__':
    init_data_file()
    app.run(port=3000)

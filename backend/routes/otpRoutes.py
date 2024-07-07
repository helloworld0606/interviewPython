from flask import Blueprint, jsonify, request
import pyotp
import qrcode
from io import BytesIO
from base64 import b64encode
from utils.fileUtils import read_data, write_data, read_guest_data

otp_bp = Blueprint('otp_bp', __name__)

@otp_bp.route('/generate', methods=['GET'])
def generate_otp():
    secret = pyotp.random_base32()
    otp_auth_url = pyotp.totp.TOTP(secret).provisioning_uri(name="MyApp", issuer_name="MyApp")
    qr = qrcode.make(otp_auth_url)
    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    qr_code_url = b64encode(buffered.getvalue()).decode()

    return jsonify({
        "secret": secret,
        "qrCode": f"data:image/png;base64,{qr_code_url}"
    }), 200

@otp_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    user_id = data.get('userId')
    otp = data.get('otp')
    print(f"Verifying OTP for user {user_id} with OTP {otp}")  # 调试信息
    users = read_data()
    guest_data = read_guest_data()
    
    # 尝试查找普通用户
    user = next((u for u in users['users'] if u['id'] == user_id), None)
    if user:
        print(f"Found regular user: {user}")
    else:
        # 如果没有找到普通用户，尝试查找guest用户
        guest_user = guest_data.get('guest')
        if guest_user and guest_user.get('id') == user_id:
            user = guest_user
            print(f"Found guest user: {user}")

    if not user:
        print("User not found")  # 调试信息
        return jsonify({"error": "User not found"}), 404

    print(f"Using secret: {user['twoFactorSecret']}")  # 调试信息
    verified = pyotp.TOTP(user['twoFactorSecret']).verify(otp)
    if verified:
        print("OTP verification successful")  # 调试信息
        return jsonify({"message": "OTP verification successful"}), 200
    else:
        print("Invalid OTP")  # 调试信息
        return jsonify({"error": "Invalid OTP"}), 400

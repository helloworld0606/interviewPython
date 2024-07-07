import bcrypt
import pyotp
import qrcode
from io import BytesIO
from base64 import b64encode
from flask import jsonify, request
from utils.fileUtils import init_data_file, read_data, write_data, read_guest_data, write_guest_data
from PIL import Image

def get_users():
    data = read_data()
    return jsonify(data['users'])

def add_user():
    data = read_data()
    new_user = request.json

    # 加密密码
    hashed = bcrypt.hashpw(new_user['password'].encode('utf-8'), bcrypt.gensalt())
    new_user['password'] = hashed.decode('utf-8')

    data['users'].append(new_user)
    write_data(data)
    return jsonify(new_user), 201

def login_user(request):
    data = read_data()
    account = request.json.get('account')
    password = request.json.get('password')
    
    user = next((u for u in data['users'] if u['account'] == account), None)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        secret = pyotp.random_base32()
        user['twoFactorSecret'] = secret
        write_data(data)

        print(f"Generated secret for user {user['id']}: {secret}")  # 调试信息

        
        otp_auth_url = pyotp.totp.TOTP(secret).provisioning_uri(name="MyApp", issuer_name="MyApp")
        qr = qrcode.make(otp_auth_url)
        qr.show() 
        buffered = BytesIO()
        qr.save(buffered, format="PNG")
        img = Image.open(buffered)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        qr_code_url = b64encode(buffered.getvalue()).decode()
        
        return jsonify({
            "message": "2FA required",
            "userId": user['id'],
            "qrCodeUrl": f"data:image/png;base64,{qr_code_url}"
        }), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 400

def verify_otp():
    data = read_data()
    guest_data = read_guest_data()  # 读取guest数据
    user_id = request.json.get('userId')
    otp = request.json.get('otp')

    print(f"Verifying OTP for user ID: {user_id} with OTP: {otp}")

    # 尝试查找普通用户
    user = next((u for u in data.get('users', []) if u.get('id') == user_id), None)
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


def guest_login():
    data = read_guest_data()
    guest_user = data.get('guest')
    
    if not guest_user:
        return jsonify({"error": "No guest user available"}), 400
    
    totp = pyotp.TOTP(guest_user['twoFactorSecret'])
    otp = totp.now()
    return jsonify({"otp": otp}), 200

def add_google_user():
    guest_data = read_guest_data()
    account = request.json.get('account')
    uid = request.json.get('uid')

    secret = pyotp.random_base32()
    guest_user = {
        "id": uid,
        "account": account,
        "password": "",
        "isGuest": True,
        "twoFactorSecret": secret
    }
    guest_data['guest'] = guest_user
    write_guest_data(guest_data)

    otp_auth_url = pyotp.totp.TOTP(secret).provisioning_uri(name="MyApp", issuer_name="MyApp")
    qr = qrcode.make(otp_auth_url)
    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    img = Image.open(buffered)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    qr_code_url = b64encode(buffered.getvalue()).decode()

    return jsonify({
        "message": "Google guest added successfully",
        "userId": uid,
        "qrCodeUrl": f"data:image/png;base64,{qr_code_url}"
    }), 201

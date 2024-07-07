import pyotp

def generate_test_otp(secret):
    totp = pyotp.TOTP(secret)
    return totp.now()

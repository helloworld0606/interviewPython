# Login Page

## Environment Requirements
### General
- Windows 10

### Backend
- Python 3.12.4

### Frontend
- Node.js v20.11.1
- npm v10.5.0

## Installation Instructions

1. **Clone the repository**
    ```bash
    git clone https://github.com/helloworld0606/interviewPython.git
    ```

2. **Set up the backend server** (cmd)
    ```bash
    cd C:\interviewPython\backend
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    ```

    **Install Rust** (if not already installed) Rust is needed to compile `bcrypt`
    ```bash
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    ```

   **Run the backend server**
    ```bash
    python app.py
    ```

4. **Run the frontend server** (terminal)
   ```bash
    cd C:\interviewPython\frontend
    npm install
    npm audit  # find security vulnerabilities
    npm audit fix  # fix any security vulnerabilities
    npm run serve
    ```

5. **The app will run at [http://localhost:8080/](http://localhost:8080/)**



## Account info in db.json
"make sure backend is running"

Get account
```bash
curl -X GET http://localhost:3000/users
```
Add account
```
curl -X POST "http://localhost:3000/users" -H "Content-Type: application/json" -d "{\"id\": 2, \"name\": \"James\", \"account\": \"james123@gmail.com\", \"password\": \"DEF789\"}"
```
Login account
```
curl -X POST "http://localhost:3000/users/login" -H "Content-Type: application/json" -d "{\"account\":\"alice123@gmail.com\",\"password\":\"ABC123456\"}"
```
Two Factor Auth
1. When login is successful, a QR code window will pop up.
2. Scan the QR code using the Authenticator app on your iPhone.
3. Replace XXXXXX (6 digits) with the one-time code from MyApp.

```
curl -X POST "http://localhost:3000/2fa/verify-otp" -H "Content-Type: application/json" -d "{\"userId\":1,\"otp\”:\”XXXXXX\”}”
```

## Test account:
```
Account: alice123@gmail.com
Password: ABC123456
```

- The login info will be saved in session storage
- To try a new login, open the inspect window —> go to Application —> SessionStorage —> clear all login records —> refresh the website

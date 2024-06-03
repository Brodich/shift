from flask import Flask, request, jsonify
from auth import login, verify_token
from models import employees

app = Flask(__name__)
app.config.from_object('config.Config')

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/example')
def example():
    data = {
        'name': 'John',
        'age': 30,
        'city': 'New York'
    }
    return jsonify(data)
    
@app.route('/login', methods=['POST'])
def login_route():
    print("Login endpoint reached")
    response = login()
    print("Login response:", response.get_json())
    return response

@app.route('/salary', methods=['GET'])
def get_salary():
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        username = verify_token(token)
        if username:
            employee = employees.get(username)
            return jsonify({
                "salary": employee["salary"],
                "next_raise_date": employee["next_raise_date"]
            })
        else:
            return jsonify({"message": "Invalid or expired token"}), 401
    else:
        return jsonify({"message": "Token required"}), 403

if __name__ == '__main__':
    app.run(debug=True)

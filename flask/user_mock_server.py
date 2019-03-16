from flask import Flask, jsonify, g

app = Flask(__name__)

@app.before_request
def set_up_data():
    g.data = [
        {"id":1, "first name":"Tom", "last name":"sir", "address":"shenzhen",
        "company":"fubei", "job":"Tester", "favorate_color":"red", "credit_card_number":"123456"},
        {"id":2, "first name":"Andy", "last name":"lady", "address":"beijing",
        "company":"baidu", "job":"developer", "favorate_color":"blue", "credit_card_number":"654321"}
    ]

    g.user_does_no_exist = {"message":"User does not exist"}

@app.route('/api/users')
def get_all_user():
    return jsonify(g.data)


if __name__ == '__main__':
    app.run()
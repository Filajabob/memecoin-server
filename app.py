from flask import Flask, request
import objs

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello from Flask!'


@app.route('/user/new-user', methods=["GET"])
def new_user():
    firstname = request.args.get("firstname")
    lastname = request.args.get("lastname")
    password = request.args.get("password")

    if None in (firstname, lastname, password):
        return {
            "status": "failure",
            "message": "No value was recieved for firstname, lastname, or password"
               }, 400

    user = objs.User.new(firstname, lastname, password)

    return {
        "status": "success",
        "message": f"User {user.id} was created.",
        "user_id": user.id
           }, 200


# Run the Flask app if not on PythonAnywhere
if __name__ == '__main__':
    app.run(debug=True)

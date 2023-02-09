from flask import Flask, request
import objs
from objs.errors import *
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello from Flask!'


@app.route('/user/new-user', methods=["POST"])
def new_user():
    firstname = request.args.get("firstname")
    lastname = request.args.get("lastname")
    alias = request.args.get("alias")
    email = request.args.get("email")
    password = request.args.get("password")

    if None in (firstname, lastname, alias, email, password):
        return {
            "status": "failure",
            "message": "No value was received for firstname, lastname, alias, email, or password"
               }, 400

    try:
        user = objs.User.new(firstname, lastname, alias, email, password)
    except DuplicateAlias:
        return {
            "status": "failure",
            "message": "Alias is not unique."
        }, 409

    return {
        "status": "success",
        "message": f"U{user.id} was created.",
        "user_id": user.id
           }, 200


@app.route('/user/run/transaction/<user_attr_type>', methods=["POST"])
def transaction(user_attr_type):
    if request.args.get("amount") is None:
        return {
                   "status": "failure",
                   "message": "Argument 'amount' was not provided.",
               }, 400
    try:
        if user_attr_type == "id":
            transaction_obj = objs.Transaction(objs.User.load_from_id(request.args.get("sender")),
                                               objs.User.load_from_id(request.args.get("recipient")),
                                               int(request.args.get("amount")))

        elif user_attr_type == "username":
            transaction_obj = objs.Transaction(objs.User.load_from_alias(request.args.get("sender")),
                                               objs.User.load_from_alias(request.args.get("recipient")),
                                               int(request.args.get("amount")))

        else:
            return {
                "status": "failure",
                "message": f"Invalid user_attr_type \"{user_attr_type}\""
            }, 400

    except UserNotFound:
        return {
            "status": "failure",
            "message": "User does not exist."
        }, 404

    # Authenticate
    if request.args.get("password") != transaction_obj.sender.password:
        return {
            "status": "failure",
            "message": "Incorrect password."
        }, 403

    try:
        transaction_obj.execute()

        return {
            "status": "success",
            "message": f"{transaction_obj.amount} MemeCoins were sent from U{transaction_obj.sender.id} to "
                       f"U{transaction_obj.recipient.id}."
        }, 200
    except InsufficientFunds:
        return {
            "status": "failure",
            "message": "Insufficient funds."
        }, 409


# Run the Flask app if not on PythonAnywhere
if __name__ == '__main__':
    app.run(debug=True)

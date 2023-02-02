from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello from Flask!'

# Run the Flask app if not on PythonAnywhere
if __name__ == '__main__':
    app.run()

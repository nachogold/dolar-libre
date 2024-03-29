from flask import Flask
from views import views

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True #allow flask to reload templates upon changes

app.register_blueprint(views, url_prefix="/")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5000"),debug=False)

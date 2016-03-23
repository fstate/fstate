from flask import *
#from flask.ext.login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "KeepThisS3cr3t"
#login_manager = LoginManager()
#login_manager.init_app(app)
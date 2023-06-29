from flask import Flask

def create_app():
    app = Flask(__name__,template_folder='../templates')
    app.jinja_env.globals.update(zip=zip) #defines jinja zip function to be same as py zip for HTML use
    app.config.update(SECRET_KEY="MyTotallSecreyKey")
    app.static_folder = '../static'

    from mysite.routes import routeBP
    app.register_blueprint(routeBP)

    return app
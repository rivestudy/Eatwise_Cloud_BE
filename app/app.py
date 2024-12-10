from flask import Flask
from app.routes.articles import articles_bp
#from app.routes.predictions import predictions_bp
#from app.routes.histories import histories_bp
from app.routes.users import users_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(articles_bp)
    #app.register_blueprint(predictions_bp)
    #app.register_blueprint(histories_bp)
    app.register_blueprint(users_bp)
    
    app.config.from_object('app.utils.config.Config')
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)  # Enable debug mode in development

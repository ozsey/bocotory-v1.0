from flask import render_template
from app import app
from config import DevelopmentConfig, ProductionConfig

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.config.from_object(DevelopmentConfig)
    app.run(port=DevelopmentConfig.PORT)
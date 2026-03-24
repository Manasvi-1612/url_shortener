from app import app
from apig_wsgi import make_lambda_handler
lambda_handler = make_lambda_handler(app)
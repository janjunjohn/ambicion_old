#
# Gunicorn config file
#
wsgi_app = 'main:app'

# Server Mechanics
#========================================

# daemon mode
daemon = False

# enviroment variables
raw_env = [
    'PYTHON_EMAIL=pythontest3699@gmail.com',
    'AMBICION_EMAIL=ambicion.japan@gmail.com',
    'SENDGRID_API_KEY=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',
    'SECRET_KEY=pC40AwFER#M!!'
]

# Server Socket
#========================================
bind = '0.0.0.0:8000'

# Worker Processes
#========================================
workers = 2


from decouple import config

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = config('email')
EMAIL_HOST_PASSWORD = config('email_pass')
EMAIL_PORT = 587
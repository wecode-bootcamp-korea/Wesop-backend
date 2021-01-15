import json
import bcrypt
import jwt
import re

from django.views import View
from django.http  import JsonResponse

from user.models  import User
from my_settings  import SECRET_KEY

class SignView(View):
    def post(self, request):
        data       = json.loads(request.body)
        email      = data.get('email')
        password   = data.get('password')
        last_name  = data.get('last_name')
        first_name = data.get('first_name')

        try:
            email_regex = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

            if not email:
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)
            if not email_regex.match(email):
                return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)
            if User.objects.filter(email=email).exists():
                signin_user = User.objects.get(email=email)
                if bcryt.checkpw(password.encode(), signin_user.password.encode()):
                    token = jwt.endcode({'id':signin_user.id}, SECRET_KEY, algorithm='HS256')
                    return JsonResponse({'message':'SIGN_IN_SUCCESS', 'TOKEN':token}, status = 200)
            else:
                password_regex = re.compile('^(?=.*[A-Z])(?=.*\d){8,}$')
                if not password_regex.match(password):
                    return JsonResponse({'message': 'INVALID_PASSWORD'}, status=400)
                encoded_pw = password.encode('utf-8')
                hashed_pw  = bcrypt.hashpw(encoded_pw, bcrypt.gensalt())
                encrpt_pw  = hashed_pw.decode('utf-8')
                User.objects.create(
                    email  = email,
                    password = encrypt_pw,
                    last_name = last_name,
                    first_name = first_name
                    )
                return JsonResponse({'message': 'SIGN_UP_SUCCESS'}, status=200)
        except:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        
        
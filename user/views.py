import json
import bcrypt
import jwt
import re

from django.views import View
from django.http  import JsonResponse

from user.models  import User
from my_settings  import SECRET_KEY, algorithm

class UserCheckEmailView(View):
    def post(self, request):
        data  = json.loads(request.body)
        email = data.get('email')
        
        email_regex = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

        if not email:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        if not email_regex.match(email):
            return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'message': 'signIn'}, status=200)
        if not User.objects.filter(email=email).exists():
            return JsonResponse({'message': 'signUp'}, status=200)
      
    
class UserSignUpView(View):
    def post(self, request):
        data       = json.loads(request.body)
        email      = data.get('email')
        password   = data.get('password')
        last_name  = data.get('last_name')
        first_name = data.get('first_name')

        password_regex = re.compile(r'^(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,}$')
        if not password_regex.match(password):
            return JsonResponse({'message': 'INVALID_PASSWORD'}, status=400)

        encoded_pw = password.encode('utf-8')
        hashed_pw  = bcrypt.hashpw(encoded_pw, bcrypt.gensalt())
        encrypt_pw  = hashed_pw.decode('utf-8')

        User.objects.get_or_create(
            email      = email,
            password   = encrypt_pw,
            last_name  = last_name,
            first_name = first_name
            )
        return JsonResponse({'message': 'SIGN_UP_SUCCESS'}, status=200)

class UserSignInView(View):
    def post(self, request):
        data     = json.loads(request.body)
        email    = data.get('email')
        password = data.get('password')

        email_regex = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

        if not email:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        if not email_regex.match(email):
            return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)
        if not User.objects.filter(email=email).exists():
            return JsonResponse({'message': 'NOT_EXIST_EMAIL'}, status=400)
                
        signin_user = User.objects.get(email=email)
        if bcrypt.checkpw(password.encode(), signin_user.password.encode()):
            token = jwt.encode({'id':signin_user.id}, SECRET_KEY, algorithm)
            return JsonResponse({'message':'SIGN_IN_SUCCESS', 'TOKEN':token}, status = 200)
        return JsonResponse({'message':'INVALID_PASSWORD'}, status=400)              
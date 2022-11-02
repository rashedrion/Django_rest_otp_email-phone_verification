
from rest_framework.response import Response

from accounts.helpers import send_otp_to_mobile
from .models import *
from .serializers import *
from rest_framework.views import APIView


class RegisterView(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'status': 403, 'errors': serializer.errors})

            serializer.save()
            return Response({'status': 200, 'message': 'an email OTP sent on your number and email'})

        except Exception as e:
            print(e)
            return Response({'status': 404, 'errors': 'Oops! something went wrong'})


class VerifyOtp(APIView):
    def post(self, request):
        try:
            data = request.data
            user_obj = User.objects.get(phone=data.get('phone'))
            otp = data.get('otp')

            if user_obj.otp == otp:
                user_obj.is_phone_verified = True
                user_obj.save()
                return Response({'status': 200, 'message': 'your OTP is now verified'})

            return Response({'status': 403, 'message': 'your OTP is Wrong'})

        except Exception as e:
            print(e)
        return Response({'status': 404, 'message': 'Something went wrong!'})

    def patch(self, request):
        try:
            data = request.data

            if not User.objects.filter(phone=data.get('phone')).exists():
                return Response({'status': 404, 'message': 'User not found'})

            if send_otp_to_mobile(data.get('phone')):
                return Response({'status': 200, 'message': 'New OTP sent to mobile'})

            return Response({'status': 403, 'message': 'try after few seconds...'})

        except Exception as e:
            print(e)

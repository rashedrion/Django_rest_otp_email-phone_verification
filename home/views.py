from django import views
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from functools import partial
from django.forms import SplitHiddenDateTimeWidget
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics


# Generic views rest_framework


class StudentGeneric(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentGeneric1(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'id'

# function base views


@api_view(['GET'])
def get_book(request):
    book_objs = Book.objects.all()
    serializer = BookSerializer(book_objs, many=True)
    return Response({'status': '200', 'payload': serializer.data})

# class base views JWTAuthentication


class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went wrong'})

        serializer.save()

        user = User.objects.get(username=serializer.data['username'])
        refresh = RefreshToken.for_user(user)

        return Response({'status': 200, 'payload': serializer.data, 'refresh': str(refresh),
                         'access': str(refresh.access_token), 'message': 'your data is saved'})


class StudentAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student_objs = Student.objects.all()
        serializer = StudentSerializer(student_objs,  many=True)
        print(request.user)
        return Response({'status': '200', 'payload': serializer.data})

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went wrong'})

        serializer.save()

        return Response({'status': 200, 'payload': serializer.data, 'message': 'your data is saved'})

    def put(self, request):
        try:
            student_objs = Student.objects.get(id=request.data['id'])
            serializer = StudentSerializer(
                student_objs, data=request.data, partial=False)
            if not serializer.is_valid():
                return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went wrong'})

            serializer.save()

            return Response({'status': 200, 'payload': serializer.data, 'message': 'your data is saved'})

        except Exception as e:
            return Response({'status': 403, 'message': 'invalid id '})

    def patch(self, request):
        try:
            student_objs = Student.objects.get(id=request.data['id'])
            serializer = StudentSerializer(
                student_objs, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went wrong'})

            serializer.save()

            return Response({'status': 200, 'payload': serializer.data, 'message': 'your data is saved'})

        except Exception as e:
            return Response({'status': 403, 'message': 'invalid id '})

    def delete(self, request):
        try:

            student_objs = Student.objects.get(id=request.data['id'])
            student_objs.delete()

            return Response({'status': 200,  'message': 'delete done'})

        except Exception as e:
            return Response({'status': 403, 'message': 'invalid id '})

# function base views

# @api_view(['GET'])
# def home(request):
#     student_objs = Student.objects.all()
#     serializer = StudentSerializer(student_objs,  many=True)
#     return Response({'status': '200', 'payload': serializer.data})


# @api_view(['POST'])
# def post_student(request):
#     serializer = StudentSerializer(data=request.data)
#     if not serializer.is_valid():
#         return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went wrong'})

#     serializer.save()

#     return Response({'status': 200, 'payload': serializer.data, 'message': 'your data is saved'})


# @api_view(['PATCH'])
# def update_student(request, id):
#     try:
#         student_objs = Student.objects.get(id=id)
#         serializer = StudentSerializer(
#             student_objs, data=request.data, partial=True)
#         if not serializer.is_valid():
#             return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went wrong'})

#         serializer.save()

#         return Response({'status': 200, 'payload': serializer.data, 'message': 'your data is saved'})

#     except Exception as e:
#         return Response({'status': 403, 'message': 'invalid id '})


# @api_view(['DELETE'])
# def delete_student(request, id):
#     try:
#         student_objs = Student.objects.get(id=id)
#         student_objs.delete()

#         return Response({'status': 200,  'message': 'delete done'})

#     except Exception as e:
#         return Response({'status': 403, 'message': 'invalid id '})

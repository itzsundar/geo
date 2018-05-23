from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from models import *
from django.conf import settings
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from serializers import *
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class GetCountries(APIView):
    def get(self,request):
    	queryset = CountryList.objects.all()
    	serializer = CountryListSerializer(queryset, many=True)
        return Response(serializer.data,status=200)

class GetProfile(APIView):

    def get(self,request,employee_id,user_id):
            profile_info = Profile.objects.get(employee_id=employee_id,user=user_id)
            data = ProfileSerializer(profile_info).data
            journey = EmployeeJourney.objects.all()
            for item in journey:
            	data['from'] = item.user_from
            	data['to'] = item.user_to
            	data['journey_date'] = item.journey_date
            email_id = User.objects.get(id=user_id).email
            data['email']=email_id
            return Response(data,status=200)

class EmployeeView(APIView):
	def get(self, request):
		queryset = Employee.objects.all()
		serializer = EmployeeSerializer(queryset, many=True)
		return Response(serializer.data, status=200)

class UserCreateApiview(APIView):
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        request.POST._mutable = True
        info = request.data
        serializer = UserCreateSerializers(data= request.data)
        if serializer.is_valid():
            user_serializer = serializer.save()
            # save data into employee table
            serializer = EmployeeSerializer(data=request.data)
            if serializer.is_valid():
                employee = serializer.save()
                #save data into profile table - FullName as name in profile page
                info['user_id'] = user_serializer.id
                info['employee_id'] = employee.id
                info['name'] = request.data['fullname']
                serializer = ProfileSignUpSerializer(data=info)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'status': 'Registered successfully.'}, status=200)
        return Response(serializer.errors, status=401)


class UserLoginApiview(APIView):
    serializer_class = UserLoginSerializers

    def post(self, request, *args, **kwargs):
        try:
            if 'email' in request.data and 'password' in request.data:
                email = self.request.data['email']
                password = self.request.data['password']
                user = authenticate(username=email, password=password)
                usr = User.objects.get(email=request.data['email'])
                pwd_valid = check_password(password, usr.password)
                if not usr.is_active:
                    return Response({'status': 'Your account is inactive'}, status=401)
                if pwd_valid:
                    user_profile = Profile.objects.get(user_id=usr.id)
                    return Response({'user_id': usr.id,
                                     'fullname': user_profile.name,
                                     'employee_id': user_profile.employee_id,
                                     'email':email,
                                     'token':'ida0bkbq1ulq8bav9mxd110eep1j0mpt',
                                     },status=200)
                else:
                    return Response({'status': 'Password is incorrect.'},status=401)
        except Exception as p:
            return Response({'status': "Couldn't found your Totient Account."},status=401)
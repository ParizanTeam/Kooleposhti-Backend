from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from accounts.models import Instructor, Student
from accounts.permissions import *
from ..models import *
from ..serializers import *
from rest_framework import status
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
import random
import string
from django.utils import timezone

class DiscountViewSet(ModelViewSet):
	serializer_class = DiscountSerializer
	permission_classes = [IsInstructorOrReadOnly]
	queryset =Discount.objects.all()

	def create(self, request, *args, **kwargs):
		data = request.data.copy()
		auto_gen=False
		if("code" not in data.keys() or data["code"]==""):
			random_code=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
			data["code"]=random_code
			auto_gen=True
		serializer = self.get_serializer(data=data)
		serializer.is_valid(raise_exception=True)
		discount = serializer.save()
		if(auto_gen):
			discount.code+=str(discount.id)
			discount.save()
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, 
				status=status.HTTP_201_CREATED, headers=headers)


	@action(detail=False,url_path="codes/(?P<course>[0-9]+)")
	def get_owner_code(self, request,course=None):
		owner= request.user.instructor
		discounts=Discount.objects.filter(owner=owner,course=course)
		serializer = self.get_serializer(discounts, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@action(detail=False,url_path="validate/(?P<code>[0-9a-zA-Z]+)")
	def validate_code(self, request,code=None):
		discount=Discount.objects.filter(code=code)

		if(not discount.exists()):
			return Response("Not Found", status=status.HTTP_404_NOT_FOUND)

		discount=discount.get()

		if(timezone.now()>discount.expiration_date):
			return Response("Expired", status=status.HTTP_410_GONE)

		serializer = self.get_serializer(discount)
		return Response(serializer.data, status=status.HTTP_200_OK)
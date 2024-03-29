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
		user = request.user
		if(data["title"]==""):
			data["title"]=f"{user.username}'s Discount Code "
		if("code" not in data.keys() or data["code"]==""):
			random_code=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
			data["code"]=random_code
			auto_gen=True
		serializer = self.get_serializer(data=data)
		serializer.is_valid(raise_exception=True)
		discount = serializer.save()

		if not discount.is_course_owner(user.instructor):
			return Response('you are not the course owner.', 
							status=status.HTTP_403_FORBIDDEN)
		if(auto_gen):
			discount.code+=str(discount.id)
			discount.save()
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, 
				status=status.HTTP_201_CREATED, headers=headers)

	def destroy(self, request, *args, **kwargs):
		instructor= request.user.instructor
		discount= self.get_object()
		print(f"discount id: {discount.course.id}")
		if not discount.is_course_owner(instructor):
			return Response('you are not the course owner.', 
							status=status.HTTP_403_FORBIDDEN)
		self.perform_destroy(discount)
		return Response(status=status.HTTP_204_NO_CONTENT)

	@action(detail=False,url_path="codes/(?P<course>[0-9]+)")
	def get_owner_code(self, request,course=None):
		owner= request.user.instructor
		discounts=Discount.objects.filter(owner=owner,course=course)
		serializer = self.get_serializer(discounts, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
	
	@staticmethod
	def validate_code(code,course_id):
		discount=Discount.objects.filter(code=code)

		if(not discount.exists()):
			return Response("Invalid discount code", status=status.HTTP_403_FORBIDDEN)

		discount=discount.get()

		if(discount.course.id!=int(course_id)):
			return Response("Invalid discount code", status=status.HTTP_403_FORBIDDEN)

		if(timezone.now()>discount.expiration_date):
			return Response("The discount code has expired", status=status.HTTP_410_GONE)
		return discount

	# (?P<code>[0-9a-zA-Z]+)?c=(?P<course_id>[0-9]+)
	@action(detail=False,url_path="validate")
	def validate_code_view(self,request):
		code = self.request.GET.get('code')
		course_id = self.request.GET.get('course')
		result=DiscountViewSet.validate_code(code,course_id)
		if type(result) is Response:
			return result
		serializer = self.get_serializer(result)
		return Response(serializer.data, status=status.HTTP_200_OK)

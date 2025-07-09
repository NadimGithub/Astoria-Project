from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LeadSerializer
from .models import Lead
import requests
from datetime import date
from django.contrib import messages


def index(request):
    return render(request, 'index.html')
def submit_lead(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        # 1. Save to your local DB
        Lead.objects.create(name=name, email=email, phone=phone)

        # 2. Push to MDoc CRM API
        mdoc_data = {
            "DataFrom": "T",
            "ApiKey": "a28cc43c-526d-4010-970e-0d0e92c18902",
            "EnquiryDate": date.today().strftime("%Y-%m-%d"),
            "FirstName": name,
            "MobileNo": phone,
            "Email": email,
            "Source": "Digitals",
            "SourceDetail": "Google Ad",
        }

        try:
            response = requests.post(
                "https://nirman.maksoftbox.com/MDocBoxAPI/MdocAddEnquiryORTeleCalling",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data=mdoc_data,
                timeout=5
            )
            print("MDoc Response:", response.text)
        except Exception as e:
            print("MDoc Push Error:", e)

        messages.success(request, 'Lead submitted successfully!')
        return redirect('leads:index')
    return redirect('leads:index')

# def submit_lead(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         Lead.objects.create(name=name, email=email, phone=phone)
#         return redirect('leads:index')
#     return redirect('leads:index')

# class LeadCreateView(APIView):
#     def get(self, request):
#         """Handle GET requests to retrieve all leads"""
#         leads = Lead.objects.all()
#         serializer = LeadSerializer(leads, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         """Handle POST requests to create a new lead"""
#         serializer = LeadSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()

#             # Prepare data for MDoc push
#             mdoc_data = {
#                 "DataFrom": "T",
#                 "ApiKey": "a28cc43c-526d-4010-970e-0d0e92c18902",
#                 "EnquiryDate": date.today().strftime("%Y-%m-%d"),
#                 "FirstName": request.data.get("name"),
#                 "MobileNo": request.data.get("phone"),
#                 "Email": request.data.get("email"),
#                 "Source": "Digitals",
#                 "SourceDetail": "Google Ad",
#             }

#             try:
#                 requests.post(
#                     "https://nirman.maksoftbox.com/MDocBoxAPI/MdocAddEnquiryORTeleCalling",
#                     headers={"Content-Type": "application/x-www-form-urlencoded"},
#                     data=mdoc_data,
#                     timeout=5
#                 )
#             except Exception as e:
#                 print("MDoc API error:", e)

#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

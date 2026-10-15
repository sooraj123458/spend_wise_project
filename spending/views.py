from django.shortcuts import render,get_object_or_404

from rest_framework.views import APIView

from spending.serializer import SignUpSerializer

from django.contrib.auth.models import User

from rest_framework.response import Response

from spending.models import Expense

from spending.serializer import ExpenseSerializer

from rest_framework import authentication,permissions

from spending.permissions import IsOwner

from datetime import datetime

from django.db.models import Sum

# Create your views here.

class SignUpView(APIView):

    def post(self,request):

        form_data=request.data

        serializer_instance=SignUpSerializer(data=form_data)

        if serializer_instance.is_valid():

            cleaned_data=serializer_instance.validated_data

            qs=User.objects.create_user(**cleaned_data)

            serial_instance=SignUpSerializer(qs)

            return Response(data=serial_instance.data)

        else:

            return Response(data=serializer_instance.errors)

class GetMEeView(APIView):

    def get(self,request):

        auth_user=request.user

        qs=User.objects.get(username=auth_user)

        instance=SignUpSerializer(qs)

        return Response(data=instance.data)



    

class EpenseListCreateCreateView(APIView):

    #authentication_classes=[authentication.BasicAuthentication]

    authentication_classes=[authentication.TokenAuthentication]

    #authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        auth_user=request.user

        qs=Expense.objects.filter(owner=auth_user)

        serializer_instance=ExpenseSerializer(qs,many=True)

        return Response(data=serializer_instance.data)

    def post(sef,request):

        form_data=request.data

        serializer_instance=ExpenseSerializer(data=form_data)

        if serializer_instance.is_valid():

            serializer_instance.save(owner=request.user)

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)

        

class ExpenseRetriveUpdateDeleteView(APIView):

    #authentication_classes=[authentication.BasicAuthentication]

    authentication_classes=[authentication.TokenAuthentication]

    #permission_classes=[permissions.IsAuthenticated]

    permission_classes=[IsOwner]

    def get(self,request,pk=None):

        #qs=Expense.objects.get(id=pk)

        instance=get_object_or_404(Expense,id=pk)

        self.check_object_permissions(request,instance)

        serilaizer_instance=ExpenseSerializer(instance)

        return Response(data=serilaizer_instance.data)

    

    def put(self,request,pk=None):  

        instance=get_object_or_404(Expense,id=pk)

        #qs=Expense.objects.filter(id=pk).update(**Cleaned_data)

        self.check_object_permissions(request,instance)

        form_data=request.data

        serializer_instance=ExpenseSerializer(data=form_data,instance=instance)   

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)


        

    def delete(self,request,pk=None):

        #qs=Expense.objects.get(id=pk).delete()

        instance=get_object_or_404(Expense,id=pk).delete()

        self.check_object_permissions(request,instance)  

        response_data={"message":"deleted.."}

        return Response(data=response_data)


class ExpenseSummaryView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        response_data={
            "today_total":0
        }  

        curr_date=datetime.now().date()

        curr_month=datetime.now().month

        curr_year=datetime.now().year

        #monthly summary

        monthly_transactions=Expense.objects.filter(owner=request.user,created_at__month=curr_month,created_at__year=curr_year)

        if monthly_transactions:

            month_summary=monthly_transactions.values("amount").aggregate(total=Sum("amount")).get("total")

        #today summary

        today_transactions=Expense.objects.filter(owner=request.user,created_at__date=curr_date)

        if today_transactions:

            total_value=today_transactions.values("amount").aggregate(total=Sum("amount")).get("total")  #{total:677787}

            #today summary total

            category_summary=today_transactions.values("category").annotate(total=Sum("amount")) 

            response_data={
                "monthly_total":month_summary,

                "today_total":total_value,

                "category_summary":category_summary
                }

        return Response(data=response_data)   

from spending.ai_service import get_budget_paln     

class BudgetPlanView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):

        response_data={
            " monthly_total_expense":0
        }

        curr_month=datetime.now().month

        curr_year=datetime.now().year

        #monthly trasactions
        monthly_transactions=Expense.objects.filter(owner=request.user,created_at__month=curr_month,created_at__year=curr_year)

        if monthly_transactions:

            monthly_transactionss=monthly_transactions.values("amount").aggregate(total=Sum("amount")).get("total")

            monthly_category_summary=monthly_transactions.values("category").annotate(total=Sum("amount"))

            response_data={

                "monthly_total":monthly_transactionss,
                "category_summary":monthly_category_summary
                
                }

        

            budget_plan=get_budget_paln(response_data)

            response_data["plan"]=budget_plan

        return Response(response_data)   















            

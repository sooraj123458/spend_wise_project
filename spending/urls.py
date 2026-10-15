from django.urls import path

from spending.views import SignUpView,GetMEeView

from spending.views import EpenseListCreateCreateView,ExpenseRetriveUpdateDeleteView,ExpenseSummaryView,BudgetPlanView

from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
path("register/",SignUpView.as_view()),
path('getme/',GetMEeView.as_view()),
path('expenses/',EpenseListCreateCreateView.as_view()),
path('expenses/<int:pk>/',ExpenseRetriveUpdateDeleteView.as_view()),


#token
path('token/',ObtainAuthToken.as_view()),
path('expenses/summary/',ExpenseSummaryView.as_view()),
path('budget/plan/',BudgetPlanView.as_view()),

]

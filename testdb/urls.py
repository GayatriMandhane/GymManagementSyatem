from django.urls import include, path,re_path
from testdb import views_expense, views_search, views_subscriptions, views_dashboard
from testdb import views_member
from testdb import views, views_attendence, views_member, views_enquiry,views_notification
from .views import LoginAPI, RegisterAPI
from knox import views as knox_views
from .views import connectAPI


urlpatterns = [
   #  path('', include(router.urls)),
   path('api/register/', RegisterAPI.as_view(), name='register'),
   path('api/login/', LoginAPI.as_view(), name='login'),
   path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
   path('',connectAPI.as_view()),
   re_path(r'^Enquiry$',views_enquiry.enquiryApi),
   re_path(r'^Enquiry/([0-9]+$)',views_enquiry.enquiryApi),
   re_path(r'^members$',views_member.membersApi),
   re_path(r'^members/([0-9]+$)',views_member.membersApi),
   path('memberfind/',views_search.MemberSearch.as_view()),
   path('attendencefind/',views_search.AttendanceSearch.as_view()),
   path('subscriptionfind/',views_search.BillSearch.as_view()),
   re_path(r'^attendence$',views_attendence.attendenceApi),
   re_path(r'^attendence/([0-9]+$)',views_attendence.attendenceApi),
   re_path(r'^dashboard$',views_dashboard.dashboardApi),
   re_path(r'^dashboard/([0-9]+$)',views_dashboard.dashboardApi),
   re_path(r'^subscription$',views_subscriptions.subscriptionApi),
   re_path(r'^subscription/([0-9]+$)',views_subscriptions.subscriptionApi),
   re_path(r'^notification$',views_notification.notification),
   re_path(r'^notification/([0-9]+$)',views_notification.notification),
   re_path(r'^expense$',views_expense.expenseApi),
   re_path(r'^expense/([0-9]+$)',views_expense.expenseApi)




   

]
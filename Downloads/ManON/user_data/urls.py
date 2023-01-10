from django.urls import path
from . import views


urlpatterns = [
    path('get/', views.GetAPI.as_view()),
    path('register/', views.RegisterAPI.as_view(), name="register"),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('SentMailView/', views.SentMailView.as_view(), name="sentmail"),
    path('ResetPasswordview/', views.ResetPasswordview.as_view()),
    path('update/', views.ProfileUpdate.as_view()),
    # path('update1/', views.Update.as_view()),
    path('otp/', views.OtpVerification.as_view()),
    path('celery_test/', views.my_test),

]

from django.urls import path
from .views import UserRegistrationForm, UserLoginForm, UserLogout, DepositMoney, UserProfile, ReturnBorrowedBook, UpdateUserInfo, ChangePassword

urlpatterns = [
    path('registration/', UserRegistrationForm.as_view(), name="registration"),
    path('login/', UserLoginForm.as_view(), name="login"),
    path('logout/', UserLogout.as_view(), name="logout"),
    path('deposit/', DepositMoney.as_view(), name="deposit"),
    path('profile/', UserProfile.as_view(), name="profile"),
    path('update/', UpdateUserInfo.as_view(), name="update_info"),
    path('update/password', ChangePassword.as_view(), name="update_password"),
    path('book/return/<slug:slug>/',
         ReturnBorrowedBook.as_view(), name="return_book"),
]
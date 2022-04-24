from django.urls import path
from . import views
urlpatterns = [
    path('', views.MainView.as_view()),
    path("logout", views.Logout.as_view()),
    path("login", views.LoginView.as_view()),
    path('add_news', views.AddNewsView.as_view()),
    path('edit_news/<int:pk>', views.EditNewsView.as_view())
]
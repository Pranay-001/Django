from django.contrib import admin
from django.urls import path,include
from myDictionary import views
admin.site.site_header = "WordWorld"
admin.site.site_title = "WordWorld Portal"
admin.site.index_title = "Welcome to WordWorld Portal"
urlpatterns = [
    path('', views.loginUser,name="loginUser"),
    path('loginUser', views.loginUser,name="loginUser"),
    path('home', views.home,name="home"),
    path('history',views.history,name="history"),
    path('logout', views.logoutUser,name="logoutUser"),
    path('validate',views.validate,name="validate"),
    path('search/', views.search, name="search"),
    path('search/home', views.searchHome, name="searchHome"),
    path('search/logout', views.searchLogout, name="searchLogout"),
    path('search/history', views.searchHistory, name="searchHistory"),
    path('userverification',views.userverification,name="userverification"),
    path('historySrc/',views.historySrc,name="historySrc")
]

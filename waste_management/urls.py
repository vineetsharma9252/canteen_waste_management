"""
URL configuration for waste_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin 
from django.conf import settings
from django.urls import path , include
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('classify/', views.waste_classification_view, name='waste_classification_view'),
    path('admin/', admin.site.urls),
    # path('',views.customer_registration,name = 'Login_page'),cls
    path('customers', include('customers.urls')), 
    # path('',views.custom_login_view , name='login_page') , 
    path('', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('prebooking/', views.prebooking, name='prebooking'),
    path('homepage/',views.homepage,name= "home"),
    path('report_page/',views.sanitation_report,name="Report_Page"),
    path('fact/',views.facts , name="Facts"),
    path('Recycle_guide/',views.Recycling_guide,name="Recycle_Guide"),
    path('DashBoard/',views.waste_dashBoard,name="Analysis_DashBoard"),
    path('login/mess_login/schedule/',views.Waste_Schedule,name="Waste_Schedule_page"),
    path('Waste_FAQ/',views.Waste_FAQ,name="Waste_FAQ_Page"),
    path('Waste_Quiz/',views.Waste_Quiz,name="Waste_Quiz"),
    # path('user_list/',views.user_list,name='user_list'),
    path('chat/',views.chat_view , name='chat_view'),
    path("logout/",views.custom_logout_view , name="logout"),
    path('generater_page/',views.generater_page , name='generater_page'),
    path('community/',views.community,name="community"),
    path("prebooking/default_diet/" , views.default_diet , name="default_diet"),
    # path("prebooking",views.prebooking , name="prebooking"),
    path("prebooking/update_default_diet/" , views.update_default_diet , name="update_default_diet"),
    path("login/mess_login/", views.mess_login , name="mess_login"),
    path("login/mess_login/mess_interface",views.mess_interface,name="mess_interface"),
    path("login/mess_login/mess_complaint_interface",views.mess_complaint_interface,name="mess_complaint_interface")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


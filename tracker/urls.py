from django.conf.urls import url
from tracker import views

urlpatterns = [
    url(r'^register/?$', views.UserCreateApiview.as_view(), name='register'),
    url(r'^login/?$', views.UserLoginApiview.as_view(), name='login'),
    url(r'^get_profile/(?P<employee_id>[0-9]+)/(?P<user_id>[0-9]+)/?$', views.GetProfile.as_view(), name='get_profile'),
    url(r'^employee_details/?$', views.EmployeeView.as_view(), name='employee_details'),
    url(r'^countries/?$', views.GetCountries.as_view(), name='countries'),
]

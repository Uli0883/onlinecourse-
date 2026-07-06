from django.urls import path
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    # Rutas que ya tienes (y que se ven en tu error):
    # path('admin/', admin.site.urls),
    # path('', views.CourseListView.as_view(), name='course_list'),
    path('course/<int:course_id>/', views.CourseDetailView.as_view(), name='course_details'),
    path('course/<int:course_id>/exam/', views.exam_view, name='exam'),
    path('course/<int:course_id>/submit/', views.submit_view, name='submit'),
    path('course/<int:course_id>/result/<int:submission_id>/', views.show_exam_result, name='show_exam_result'),
    
    # 👉 RUTAS QUE TE FALTAN:
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('registration/', views.registration_request, name='registration'),
]
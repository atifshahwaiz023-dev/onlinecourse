from django.urls import path
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    # path for course list
    path('', views.CourseListView.as_view(), name='index'),
    # path for course details
    path('<int:course_id>/', views.CourseDetailView.as_view(), name='course_details'),
    # path for enroll
    path('<int:course_id>/enroll/', views.enroll, name='enroll'),
    # path for submit
    path('<int:course_id>/submit/', views.submit, name='submit'),
    # path for show exam result
    path('course/<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
]

from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('analyze_csv/', views.analyze_csv, name='analyze_csv'),

]
 
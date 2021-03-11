from phase1 import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'phase1'
urlpatterns = [
    path('', views.YourViewName.as_view(), name='phase1'),
    path('<int:pk>/', views.delete, name='phase1Delete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

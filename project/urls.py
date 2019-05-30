from django.contrib import admin
from django.urls import path
from django.urls import include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from django.conf import settings
from posts.views import UserViewSet
from posts.views import PostViewSet
from posts.views import Profile, PostPost, Search, Login, Registr, get_data, ChartData,\
    Ind, Table, RezultCharts, ChartRez, Analitic, ChartRezAll, DeletePerson, EditPerson, LogOut, PdfView

admin.site.site_header = settings.ADMIN_SITE_HEADER

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view()),
    path('user/<username>/addUser/', Profile.as_view()),
    path('user/<username>/addUser/post/', PostPost.as_view()),
    path('user/<username>/', Table.as_view()),
    path('user/<username>/result/pdf/', PdfView.pdf_generation),
    path('logout/', LogOut.as_view()),
    path('search/', Search.as_view()),
    path('login/', Login.as_view()),
    path('schema/', get_swagger_view(title='Pastebin API')),
    path('registration/', Registr.as_view()),
    path('api/data/', get_data, name='api-data'),
    path('user/<username>/charts/', ChartData.as_view()),
    path('user/<username>/chart/', Ind.as_view()),
    path('user/<username>/result/', RezultCharts.as_view()),
    path('user/<username>/chartResult/', ChartRez.as_view()),
    path('user/<username>/resultAll/', Analitic.as_view()),
    path('user/<username>/resultAllL/', ChartRezAll.as_view()),
    path('user/<username>/delete/<int:id>/', DeletePerson.delete),
    path('user/<username>/edit/<int:id>/', EditPerson.edit),
    path('', include(router.urls)),
]

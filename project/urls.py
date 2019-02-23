from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from posts.views import Profile, PostPost, Search, SearchTags, TagJson, Login, Registr, get_data, ChartData,\
    Ind, Table, RezultCharts, ChartRez, Analitic, ChartRezAll, DeletePerson, EditPerson, LogOut, PdfView

admin.site.site_header = settings.ADMIN_SITE_HEADER


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view()),
    path('user/<username>/addUser/', Profile.as_view()),
    path('user/<username>/addUser/post/', PostPost.as_view()),
    path('user/<username>/', Table.as_view()),
    path('user/<username>/result/pdf/', PdfView.pdf_generation),
    path('logout/', LogOut.as_view()),
    path('search/', Search.as_view()),
    path('search/hashtag/', SearchTags.as_view()),
    path('login/', Login.as_view()),
    path('logouttt/', auth_views.LogoutView),
    path('registration/', Registr.as_view()),
    path('hashtag.json/', TagJson.as_view),
    path('api/data/', get_data, name='api-data'),
    path('user/<username>/charts/', ChartData.as_view()),
    path('user/<username>/chart/', Ind.as_view()),
    path('user/<username>/result/', RezultCharts.as_view()),
    path('user/<username>/chartResult/', ChartRez.as_view()),
    path('user/<username>/resultAll/', Analitic.as_view()),
    path('user/<username>/resultAllL/', ChartRezAll.as_view()),
    path('user/<username>/delete/<int:id>/', DeletePerson.delete),
    path('user/<username>/edit/<int:id>/', EditPerson.edit),
]

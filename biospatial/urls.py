
from django.conf.urls import include, url
from django.contrib import admin
from gbif import views
from drivers import views as driver_views
from django.conf.urls.static import static
from biospatial import settings




urlpatterns = [
    # Examples:
    # url(r'^$', 'biospatial.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/',views.HelloWorld,name='HelloWorld'),
    url(r'^getTree/',views.showTreeInGrid,name='showTreeInGrid'),
    url(r'^getAllTrees',views.showAllLevelsInTreeInGrid,name='showAllLevelsInTreeInGrid'),
    url(r'^extractDataOf',driver_views.ExtractDataFromCSVFile,name='ExtractDataFromCSVFile'),
] 

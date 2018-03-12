
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^register$', views.RegisterView.as_view(), name='register'),
    url(r'^addprod$', views.AddProdView.as_view(), name='addprod'),
    url(r'^allowaccess$', views.AllowAccessView.as_view(), name='allowaccess'),
    url(r'^seltestlab$', views.SelTestLabView.as_view(), name='seltestlab'),
    url(r'^addsamples$', views.AddSamplesView.as_view(), name='addsamples'),
    url(r'^addtbresults$', views.AddTBresultsView.as_view(), name='addtbresults'),
    url(r'^addtresults$', views.AddTresultsView.as_view(), name='addtresults'),
    url(r'^viewprods$', views.viewprods, name='viewprods'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^viewtresults$', views.ViewTresultsView.as_view(), name='viewtresults'),
    url(r'viewdetcert$', views.viewdetcert.as_view(), name='viewdetcert'),
    url(r'viewtcerti$', views.viewTcert.as_view(), name='viewtcerti'),
    url(r'^failanalys$', views.failanalysis, name='failanalys'),
    url(r'^viewprojs$', views.viewprojs, name='viewprojs'),

]
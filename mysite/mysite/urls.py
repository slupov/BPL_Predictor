"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import include, path
from polls.Data.Extraction.raw_data_extraction import seed_db_raw_data
from polls.Data.Extraction.season_tables_extraction import get_season_data
from polls.Data.Extraction.training_model import seed_training_model

urlpatterns = [
    path('', include('polls.urls')),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]

seed_db_raw_data()

# Following test gets the current seasons table as an object
# test = get_season_data('18/19', '2018-08-19')
# test = test['Man United']
#
# print(test)

seed_training_model()

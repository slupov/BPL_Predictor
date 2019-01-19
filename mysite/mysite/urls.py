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
from polls.Data.Extraction.concentration_extraction import extract_concentration
import time

urlpatterns = [
    path('', include('polls.urls')),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]

start_time = time.time()
seed_db_raw_data()
print("Raw data seed took %s seconds to finish." % (time.time() - start_time))

start_time = time.time()
seed_training_model()
print("Training model data seed took %s seconds to finish." % (time.time() - start_time))


# Following test gets the current seasons table as an object
# season_data = get_season_data('17/18', '2018-05-13')['Man City']
# print(season_data)

# print(extract_concentration('Man United', 'Man City', '2017-12-10', '17/18'))
#
# print('DEBUG')
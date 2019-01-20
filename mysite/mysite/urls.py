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

from polls.Data.Extraction.raw_match_data_seed import seed_raw_match_data
from polls.Data.Extraction.raw_season_tables_seed import seed_raw_season_tables

from polls.Data.Extraction.training_model import seed_training_model
from polls.Data.Extraction.Web.scrape_league_standings import scrape_league_standings


import time

urlpatterns = [
    path('', include('polls.urls')),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]

start_time = time.time()
scrape_league_standings()
print("Team standings scraping took %s seconds to finish.\n" % (time.time() - start_time))

start_time = time.time()
seed_raw_match_data()
print("Raw match data seed took %s seconds to finish.\n" % (time.time() - start_time))

start_time = time.time()
seed_raw_season_tables()
print("Raw season tables seed took %s seconds to finish.\n" % (time.time() - start_time))

start_time = time.time()
seed_training_model()
print("Training model data seed took %s seconds to finish." % (time.time() - start_time))

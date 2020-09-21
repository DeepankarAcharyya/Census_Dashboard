import os
import sys
import site
from django.core.wsgi import get_wsgi_application

# Add the app's directory to the PYTHONPATH
sys.path.append('C:/Users/BijitAcharyya/Desktop/charts_django/rsac_dashboard/Census_Dashboard/dashboard')
sys.path.append('C:/Users/BijitAcharyya/Desktop/charts_django/rsac_dashboard/Census_Dashboard/dashboard/board')

os.environ['DJANGO_SETTINGS_MODULE'] = 'dashboard.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

application = get_wsgi_application()

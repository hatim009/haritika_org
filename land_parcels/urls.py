from rest_framework import routers
from .views import LandParcelViewSet

router = routers.SimpleRouter()
router.register(r'land_parcels', LandParcelViewSet)

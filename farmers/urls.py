from rest_framework import routers
from .views import FarmerViewSet


router = routers.SimpleRouter()
router.register(r'farmers', FarmerViewSet)

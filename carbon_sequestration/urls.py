from rest_framework import routers
from .views import CarbonSequestrationViewSet

router = routers.SimpleRouter()
router.register(r'projects/1', CarbonSequestrationViewSet)

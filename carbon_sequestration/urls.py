from rest_framework import routers
from .views import CarbonSequestrationViewSet

router = routers.SimpleRouter()
router.register(r'carbon-sequestration', CarbonSequestrationViewSet)

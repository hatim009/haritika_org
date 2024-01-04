from rest_framework import routers
from .views import BeneficiaryViewset


router = routers.SimpleRouter()
router.register(r'beneficiaries', BeneficiaryViewset)

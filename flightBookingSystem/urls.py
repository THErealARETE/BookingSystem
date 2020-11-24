from django.urls import path, include

from .views import FlightViewSet , TicketViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('flight', FlightViewSet)
router.register('ticket', TicketViewSet)

urlpatterns = router.urls
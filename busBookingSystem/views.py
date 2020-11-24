from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404

from rest_framework.response import Response

from rest_framework import viewsets,exceptions

from rest_framework.views import status

from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import action

from .serializers import BusSerializer , StateBus

from .helper import (validate_request_data, convert_date)

from .models import StateBus , DestinationState

from .permissions import IsAdminUser, IsOwner 



class BusViewSet(viewsets.ModelViewSet):
    """
    POST bus/
    GET bus/
    GET bus/:pk/
    PUT bus/:pk/
    DELETE bus/:pk/
    """
    serializer_class = StateBus
    queryset = StateBus.objects.all()

    def get_permissions(self):
        permission_classes = [IsAuthenticated, ]
        if self.action in ('create', 'destroy', 'update'):
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, pk=None):
        data = request.data
        if data['depart_date'] > data['arrive_date']:
            return Response(
                data={
                    "message": "Departure date cannot be greater than Arrival date"
                }, status=status.HTTP_400_BAD_REQUEST
            )
        new_bus_state = dict(
            state_number=data['state_number'],
            state_name = data['state_name'],
            state_camp_name = data['state_camp_name'],
            amount=data['amount'],
            payment_link=data['payment_link'],
            pickup_location = data['pickup_location']
            # depart_date=data['depart_date'],
            # arrive_date=data['arrive_date'],
            # departure=data['departure_location'],
           
        )
        serializer = BusSerializer(data=new_bus_state)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, version, pk=None):
        queryset = Bus.objects.all()
        data = request.data
        if data['depart_date'] > data['arrive_date']:
            return Response(
                data={
                    "message": "Departure date cannot be greater than Arrival date"
                }, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            bus = get_object_or_404(queryset, pk=pk)
            serializer = BusSerializer()
            updated_bus = serializer.update(bus, data)
            return Response(BusSerializer(updated_bus).data,
                            status=status.HTTP_200_OK)
        except Bus.DoesNotExist:
            return Response(
                data={
                    "message": "Bus state with id: {} does not exist".format(pk)
                },
                status=status.HTTP_404_NOT_FOUND)

    @action(detail=True,
            methods=['GET'],
            url_path='reserved_bus/(?P<date>[0-9_-]+)')
    def get_reserved_fight_status(self, request, version, pk=None, date=None):
        search_date = convert_date(date)
        bus = Bus.objects.filter(date_reserved__gte=search_date,
                                        date_reserved__lte=search_date+timedelta(hours=24))
        users = [
            user for user in bus
        ]
        serializer = BusSerializer(users, many=True)
        return Response(
            data={
                "reserved_flight": serializer.data,
                "reserved_flight_count": bus.count()
            },
            status=status.HTTP_200_OK)

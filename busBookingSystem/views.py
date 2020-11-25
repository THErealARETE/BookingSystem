from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404

from rest_framework.response import Response

from rest_framework import viewsets,exceptions

from rest_framework.views import status

from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import action

from .serializers import BusSerializer , StateBus

from .helper import validate_request_data, convert_date

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
            pickup_location = data['pickup_location'],
            depart_date=data['depart_date'],
            arrive_date=data['arrive_date'],
            # departure=data['departure_location'],
           
        )
        serializer = BusSerializer(data=new_bus_state)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        queryset = StateBus.objects.all()
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




# class TicketViewSet(viewsets.ModelViewSet):
#     """
#     POST ticket/
#     GET  ticket/
#     GET  ticket/:pk/
#     PUT  ticket/:pk/
#     DELETE ticket/:pk/
#     """
#     serializer_class  = 
#     queryset = Ticket.objects.all()

#     def get_permissions(self):
#         permission_classes = [IsAuthenticated, ]
#         if self.action in ('destroy', 'update'):
#             permission_classes = [IsOwner]
#         return [permission() for permission in permission_classes]

#     def create(self,request,pk=None):
#         user = request.user
#         data = request.data
#         queryset = Flight.objects.all()
#         flight = get_object_or_404(queryset, pk=data['flight'])
#         ticket = Ticket.objects.filter(user=user, flight=flight)
#         if ticket.exists():
#             return Response(data={"message":"A ticket already exists"},
#                             status=status.HTTP_409_CONFLICT)
#         if flight:
#             new_ticket = dict(
#                 user=user.id,
#                 flight=flight.pk,
#                 date_of_birth=data['date_of_birth'],
#                 phone_number=data['phone_number'],
#                 passport_number=data['passport_number'],
#                 contact_address=data['contact_address'],
#                 depart_date=flight.depart_date,
#                 arrive_date=flight.arrive_date,
#                 departure=flight.departure,
#                 destination=flight.destination,
#                 status=Ticket.BOOKED
#             )
#             serializer = TicketSerializer(data=new_ticket)
#             if serializer.is_valid():
#                 serializer.save()
#                 ticket_pk = serializer.data
#                 # ticket_notification.delay(ticket_pk['id'])
#                 return Response(serializer.data,
#                                 status=status.HTTP_201_CREATED)
#             return Response(serializer.errors,
#                             status=status.HTTP_400_BAD_REQUEST)

#     @validate_request_data
#     def update(self,request,pk=None):
#         user = request.user
#         data = request.data
#         queryset = Ticket.objects.all()
#         ticket = get_object_or_404(queryset, pk=pk, user=user)

#         if data['confirm_payment'] not in (Ticket.YES, Ticket.NO):
#             msg = "Confirm payment can either be a Yes or No"
#             raise exceptions.ValidationError(msg)
    
#         if data['confirm_payment'] == Ticket.YES:
#             if user != ticket.user:
#                 return Response(data={"message":"User is not authorized to perform this operation"},
#                                 status=status.HTTP_401_UNAUTHORIZED)

#             if ticket.status == ticket.RESERVED:
#                 return Response(data={"message":"This flight has been reserved"},
#                                 status=status.HTTP_409_CONFLICT)
#             try:
#                 flight_number = ticket.flight.flight_number
#                 flight = Flight.objects.get(flight_number=flight_number)
#                 new_data = dict(
#                     amount=flight.amount,
#                     date_reserved=datetime.now(),
#                     status=Ticket.RESERVED
#                 )
#                 serializer = TicketSerializer()
#                 updated_ticket = serializer.update(ticket,new_data)
#                 flight.customers = user
#                 flight.date_reserved = ticket.date_reserved
#                 flight.save()
#                 flight_reservation.delay(pk)
#                 return Response(TicketSerializer(updated_ticket).data,
#                             status=status.HTTP_200_OK)
#             except Flight.DoesNotExist:
#                 return Response(
#                     data={"message":"Flight object not found"},
#                     status=status.HTTP_404_NOT_FOUND)
#         else:
#             flight_decline.delay(pk)
#             return Response(data={
#                 "message": "Confirmation declined"
#             },status=status.HTTP_200_OK)


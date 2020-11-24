from django.db import models

# Create your models here.

import uuid

from django.utils.translation import ugettext_lazy as _

from djmoney.models.fields import MoneyField

from django.conf import settings




class DestinationState(models.Model):

    """ Model defines a destination state """

    STATE_CHOICES = (
        ('first', 'Pick an available state'),
        ('AB', 'Abia'),
        ('AD', 'Adamawa'),
        ('AK', 'Akwa Ibom'),
        ('AN', 'Anambra'),
        ('BA', 'Bauchi'),
        ('BY', 'Bayelsa'),
        ('BN', 'Benue'),
        ('BO', 'Borno'),
        ('CR', 'Cross River'),
        ('DT', 'Delta'),
        ('EB', 'Ebonyi'),
        ('ED', 'Edo'),
        ('EK', 'Ekiti'),
        ('EN', 'Enugu'),
        ('FCT', 'Abuja'),
        ('GM', 'Gombe'),
        ('IM', 'Imo'),
        ('JG', 'Jigawa'),
        ('KD', 'Kaduna'),
        ('KN', 'Kano'),
        ('KT', 'Kastina'),
        ('KB', 'Kebbi'),
        ('KG', 'Kogi'),
        ('KW', 'Kwara'),
        ('LA', 'Lagos'),
        ('NS', 'Nassarawa'),
        ('NG', 'Niger'),
        ('OG', 'Ogun'),
        ('OD', 'Ondo'),
        ('OS', 'Osun'),
        ('OY', 'Oyo'),
        ('PL', 'Plateau'),
        ('RV', 'Rivers'),
        ('SO', 'Sokoto'),
        ('TR', 'Taraba'),
        ('YB', 'Yobe'),
        ('ZM', 'Zamfara')
    )
    State_name = models.CharField(max_length=500, choices=STATE_CHOICES , default='first')
    state_number = models.AutoField(primary_key=True , unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ticket_id = models.CharField(max_length=50, blank=True)

    
    def save(self, *args, **kwargs):
        if len(self.ticket_id.strip(" "))==0:
            self.ticket_id = generate_ticket_id()
        super(Ticket, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.ticket_id)


def generate_ticket_id():
    return str(uuid.uuid4()).split("-")[-1]



class StateBus(models.Model):
    """
    This model defines a bus state object
    """

    state_number = models.IntegerField( blank=False, unique=True)
    state_name = models.CharField(max_length=50 , blank=False , unique=True , null=True )
    state_camp_name = models.CharField(max_length=200 , blank=True , null=True)
    depart_date = models.DateField(_(u"Depart Date"), blank=True, null=True)
    arrive_date = models.DateField(_(u"Arrive Date"), blank=True, null=True)
    payment_link = models.CharField(blank=True ,  null=True , max_length= 200)
    departure_location = models.CharField(max_length=50, blank=True)
    customers = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    # date_reserved = models.DateTimeField(blank=True, null=True)
    amount = MoneyField(max_digits=14, decimal_places=2,
                        default_currency="USD", null=True, blank=True)
    pickup_location = models.CharField(max_length=50, blank=True)                    
    destination = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.state_name)

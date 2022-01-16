from django.db import models

sections = [
    (1, 'main hall'),
    (2, '1st balcony'),
    (3, '2nd balcony')
]

ranks = [
    (1, '1st rank'),
    (2, '2nd rank'),
    (3, '3th rank')
]

seat_properties = [
    (1, 'aisle seat'),
    (2, 'front row seat'),
    (3, 'high seat')
]


class Seat(models.Model):
    section = models.CharField(choices=sections, default=None, blank=False, max_length=11)
    rank = models.CharField(choices=ranks, default=None, blank=False, max_length=8)
    seat_number = models.IntegerField(blank=False, null=False)
    is_sold = models.BooleanField(default=False)
    properties = models.CharField(choices=seat_properties, blank=True, default=None, max_length=50)
    row = models.CharField(blank=False, max_length=2)

    class Meta:
        unique_together = ('section', 'rank', 'seat_number', 'row')

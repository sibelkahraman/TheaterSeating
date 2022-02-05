from seat.models import Seat
from rest_framework.response import Response

"""
    3 sections => main hall, 1st balcony, 2nd balcony
    ranks => 1st rank, 2nd rank, 3th rank
    1st only for main hall and 1st balcony
    3th only for 1st and 2nd balcony

    One row has 20 seats

    Theater Visualization

    Main Hall
        A       1st rank
        B       1st rank
        C       2nd rank
        .
        .
        .
        H       2nd rank
    1st Balcony
        A       1st rank
        B       2nd rank
        C       2nd rank
        D       3th rank
        .
        .
        .
        H       3th rank
    2nd Balcony
        A       2nd rank
        B       2nd rank
        C       2nd rank
        D       3th rank
        .
        .
        .
        H       3th rank
"""


class CreateSeat:
    def seat(self):
        if not Seat.objects.first():
            rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            for row in rows:
                section = 1
                self.create_seats(section, row)
            for row in rows:
                section = 2
                self.create_seats(section, row)
            for row in rows:
                section = 3
                self.create_seats(section, row)

            return Response(data='Database is created', status=201)
        return Response(data='Database is already created', status=200)

    @staticmethod
    def create_seats(section, row, rank=2):
        for seat in range(1, 21):
            property = []
            if seat in [1, 20]:
                # aisle seat
                property.append(1)
            if row == 'A' and section == 1:
                # front row seat
                property.append(2)
            if row in ['H', 'G'] and section == 3:
                # high seat
                property.append(3)

            if row < 'C' and section == 1:
                rank = 1
            if row == 'A' and section == 2:
                rank = 1

            if row > 'C' and section == 2:
                rank = 3
            if row > 'C' and section == 3:
                rank = 3

            s = Seat(rank=rank, section=section, row=row, seat_number=seat, properties=property)
            s.save()

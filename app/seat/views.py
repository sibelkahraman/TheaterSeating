from seat.create_seat import CreateSeat
from seat.reserve import Reserve

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

import json


class SeatView(ModelViewSet):

    def create(self, request, *args, **kwargs):
        seat = CreateSeat()
        return seat.seat()

    def reserve(self, request, *args, **kwargs):
        data = request.data
        group = data['group']
        section = data['section']
        reserve = Reserve()
        sold_seats = reserve.arrange_seat(group, section, sold_seats={})
        # for group in group_list:
        #     pass
        return Response(data=json.dumps(sold_seats), status=200)





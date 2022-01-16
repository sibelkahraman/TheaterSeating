from seat.models import Seat

from rest_framework.response import Response
from django.db.models import Count

from itertools import combinations
import json


class Reserve:
    def arrange_seat(self, groups, section, sold_seats={}):
        min_group_number = min(groups)
        # gets first row that has total empty seat that at least equal to smallest group in groups

        row = Seat.objects.filter(is_sold=False, section=1).values('row').\
            annotate(sold=Count('is_sold')).\
            filter(sold__gte=min_group_number).\
            order_by('row')[0]['row']
        first_empty_seat = Seat.objects.filter(is_sold=False, section=section, row=row).first()
        last_empty_seat = Seat.objects.filter(is_sold=False, section=section, row=row).last()
        total_empty_seat = last_empty_seat.seat_number - first_empty_seat.seat_number + 1
        print(total_empty_seat)
        first_empty_seat_number = first_empty_seat.seat_number
        # row = first_empty_seat.row

        if total_empty_seat >= sum(groups):
            print('true')
            sold_seats = self.standard_seating(groups, first_empty_seat, section, row, sold_seats)
        # advance seating for keeps group together
        else:
            sub_group = self.find_sub_group_for_empty_seat(groups, total_empty_seat)

            seated_group = self.find_a_group_fits_empty_seat(sub_group, total_empty_seat)
            if not seated_group:
                max_number_of_group = max(sub_group)
                seats = list(range(first_empty_seat_number, first_empty_seat_number + max_number_of_group))
                seat_ids = list(Seat.objects.filter(is_sold=False, section=section, seat_number__in=seats, row=row).\
                                values_list('id', flat=True))

                Seat.objects.filter(is_sold=False, section=section, id__in=seat_ids, row=row).\
                    update(is_sold=True)
                sold_seats[str((section, row, max_number_of_group))] = seats
                groups.remove(max_number_of_group)
                if groups:
                    self.arrange_seat(groups, section, sold_seats=sold_seats)
            else:
                sold_seats = self.standard_seating(seated_group, first_empty_seat, section, row, sold_seats)
                [groups.remove(x) for x in seated_group]
                if groups:
                    self.arrange_seat(groups, section, sold_seats=sold_seats)
        return sold_seats

    @staticmethod
    def find_sub_group_for_empty_seat(groups, total_empty_seat):
        sub_group = []
        for i in groups:
            if i <= total_empty_seat:
                sub_group.append(i)
        return sub_group

    def list(self, request, *args, **kwargs):
        print('11111')
        section = 1
        group_list = [1, 8, 2, 7]
        # min_group_number = min(group_list)
        # # gets first row that has total empty seat that at least equal to smallest group in groups
        # # Seat.objects.filter(is_sold=False, section=1).values('row').annotate(sold=Count('is_sold')).filter(sold__gte=4).order_by('row')[0]['row']
        # first_empty_seat = Seat.objects.filter(is_sold=False, section=section).first()
        # last_empty_seat = Seat.objects.filter(is_sold=False, section=section).last()
        # total_empty_seat = last_empty_seat.seat_number - first_empty_seat.seat_number + 1
        # print(total_empty_seat)
        # sold_seats = {}
        # first_empty_seat_number = first_empty_seat.seat_number
        # row = first_empty_seat.row
        # if total_empty_seat >= sum(group_list):
        #     self.standard_seating(group_list, first_empty_seat, section, row)
        # else:
        #     # firstly find set of groups that are smaller than
        #
        #     sub_group = []
        #     for i in group_list:
        #         if i <= total_empty_seat:
        #             sub_group.append(i)
        #     seated = self.seat_a_group(sub_group, total_empty_seat)
        #     # if there no group that fit the empty seats
        #     if not seated:
        #         max_number_of_group = max(sub_group)
        #         seats = list(range(first_empty_seat_number, first_empty_seat_number + max_number_of_group))
        #         seat_ids = list(Seat.objects.filter(is_sold=False, section=section, seat_number__in=seats, row=row).\
        #                         values_list('id', flat=True))
        #
        #         Seat.objects.filter(is_sold=False, section=section, seat_number__in=seat_ids, row=row).\
        #             update(is_sold=True)
        #         sold_seats[max_number_of_group] = seat_ids
        #         group_list.remove(max_number_of_group)
        #     else:
        #         self.standard_seating(seated, first_empty_seat, section, row)
        #         [group_list.remove(x) for x in seated]
        #         if group_list:
        sold_seats = self.arrange_seat(group_list, section, sold_seats={})
        # for group in group_list:
        #     pass
        return Response(data=json.dumps(sold_seats), status=200)

    def find_a_group_fits_empty_seat(self, groups, number_of_empty_seat):
        if number_of_empty_seat in groups:
            return [number_of_empty_seat]
        else:
            # find possible sub group of given groups
            sub_groups = []
            for i in range(2, len(groups)-2):
                sub_group = combinations(groups, i)
                sub_groups.append(sub_group)

        for group in sub_groups:
            if number_of_empty_seat == sum(group):
                return group

        return []

    def standard_seating(self, group_list, first_empty_seat, section, row, sold_seats={}):
        # standard seating
        import ipdb
        # ipdb.set_trace()


        last_sold_seat_number = first_empty_seat.seat_number
        for group in group_list:
            seats = list(range(last_sold_seat_number, last_sold_seat_number + group))
            seat_ids = list(Seat.objects.filter(is_sold=False, section=section, seat_number__in=seats, row=row). \
                            values_list('id', flat=True))
            Seat.objects.filter(is_sold=False, section=section, seat_number__in=seats, row=row).update(is_sold=True)
            sold_seats[str((section, row, group))] = seats
            last_sold_seat_number = last_sold_seat_number + group
        return sold_seats
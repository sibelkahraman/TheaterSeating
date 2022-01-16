# from seat.models import Seat
#
# """
#     3 sections => main hall, 1st balcony, 2nd balcony
#     ranks => 1st rank, 2nd rank, 3th rank
#     1st only for main hall and 1st balcony
#     3th only for 1st and 2nd balcony
#
#     One row has 20 seats
#
#     Theater Visualization
#
#     Main Hall
#         A       1st rank
#         B       1st rank
#         C       2nd rank
#         .
#         .
#         .
#         H       2nd rank
#     1st Balcony
#         A       1st rank
#         B       2nd rank
#         C       2nd rank
#         D       2nd rank
#         E       3th rank
#         .
#         .
#         H       3th rank
#     2nd Balcony
#         A       2nd rank
#         B       2nd rank
#         C       2nd rank
#         D       3th rank
#         .
#         .
#         .
#         H       3th rank
# """
#
# rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
#
# for row in rows:
#     property = []
#     rank = 2
#     section = 'main hall'
#     if row == 'A':
#         property.append('front row seat')
#     if row < 'C':
#         rank = 1
#     for seat in range(1, 21):
#         if seat in [1, 20]:
#             property.append('aisle seat')
#
#         s = Seat(rank=rank, section=section, row=row, seat_number=seat, properties=property)
#         s.save()
#         import ipdb
#         ipdb.set_trace()
#         print(s)

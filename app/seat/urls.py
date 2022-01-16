from django.conf.urls import url

from seat.views import SeatView


urlpatterns = [
    url(r'create', SeatView.as_view({'get': 'create'}), name='create theater seats'),
    url(r'reserve', SeatView.as_view({'post': 'reserve'}), name='reserve theater seats')
]

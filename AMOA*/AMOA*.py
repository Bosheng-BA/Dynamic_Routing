import gaptraffic
import Sour_and_Des


def route(flight):

    return 1, holding


def find_start_time(flight):
    if flight.departure == 'ZBTJ':
        startt = flight.ttot - 600
    else:
        startt = flight.aldt
    flight_start_time = startt

    return flight_start_time


for flight in Sour_and_Des.flights:
    route, holding = route(flight)
    if route is False and holding is False:
        ti = find_start_time(flight)
        ti += 60
        route, holding = route(flight)

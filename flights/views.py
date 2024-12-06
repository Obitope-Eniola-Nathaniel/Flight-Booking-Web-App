from django import forms
from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from .models import Flight, Passenger, Airport

# Create your views here.
def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })


def flight(request, flight_id):
    try:
        flight = Flight.objects.get(id=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight not found.")
    
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    })

def book(request, flight_id):
    # For a post request add a new flight
    if request.method == "POST":
        try:
           # Finding the passenger based on the id submitted from form
            passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
            # Accessing the flight
            flight = Flight.objects.get(pk=flight_id)
        except KeyError:
            return HttpResponseBadRequest("Bad Request: no flight chosen")
        except Flight.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: flight does not exist")
        except Passenger.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: passenger does not exist")
        # Add the passanger to flight
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse("flights:flight", args=(flight_id,)))


















# Create City and display City
def createCity(request):
    airport = Airport.objects.all()
    if request.method == "POST":
        city = request.POST["city"]
        code = request.POST["code"]

        airport = Airport(city=city, code=code)
        airport.save()

        return HttpResponseRedirect(reverse("flights:create_city"))

    return render(request, "flights/create_city.html", {
       "airport": airport
    })

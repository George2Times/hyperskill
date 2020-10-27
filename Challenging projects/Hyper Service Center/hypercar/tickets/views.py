from django.views import View
from django.shortcuts import render, redirect
from collections import deque

menu_choices = {
    "change_oil": "Change oil",
    "inflate_tires": "Inflate tires",
    "diagnostic": "Get diagnostic",
}
change_oil_queue = deque()
inflate_tires_queue = deque()
diagnostics_queue = deque()
next_client = None
line_of_cars = {
    "change_oil": change_oil_queue,
    "inflate_tires": inflate_tires_queue,
    "diagnostic": diagnostics_queue
}
waiting_time = {
    "change_oil": 2,
    "inflate_tires": 5,
    "diagnostic": 30
}


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'welcome.html')


class MenuView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'menu.html', context={'menu_choices': menu_choices})


class TicketView(View):

    def get(self, request, service, *args, **kwargs):
        global line_of_cars

        user_id = len(change_oil_queue) + len(inflate_tires_queue) + len(diagnostics_queue) + 1
        time = 0
        for key in line_of_cars.keys():
            time += len(line_of_cars[key]) * waiting_time[key]
            if service == key:
                line_of_cars[key].append(user_id)
                break
        context = {"title": service,
                   "ticket_number": user_id,
                   "estimated_time": time}
        return render(request, 'get_ticket.html', context=context)


class ProcessingView(View):
    def get(self, request, *args, **kwargs):
        context = {
            "queues": {description: len(line_of_cars.get(key, []))
                       for key, description in menu_choices.items()},
        }
        return render(request, 'processing.html', context=context)

    def post(self, request, *args, **kwargs):
        global line_of_cars, next_client
        request.POST.get('submit')

        if len(line_of_cars['change_oil']):
            next_client = line_of_cars['change_oil'].popleft()
        elif len(line_of_cars['inflate_tires']):
            next_client = line_of_cars['inflate_tires'].popleft()
        elif len(line_of_cars['diagnostic']):
            next_client = line_of_cars['diagnostic'].popleft()
        else:
            next_client = None
        return redirect('http://127.0.0.1:8000/next/')


class NextClientView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'next.html', context={"next_client": next_client})

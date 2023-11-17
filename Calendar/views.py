from django.shortcuts import render
import calendar
from calendar import HTMLCalendar

def Calendar(request, year, month):
    # name = "John"
    # month = month.capitalize()
    # convert month name to number
    # month_number = list(calendar.month_name).index(month)
    # month_number = int(month_number)

    # cal = HTMLCalendar().formatmonth(year, month)

    return render(request, 'Calendar/calendar.html', {
        # "name": name,
        "year": year,
        "month": month,
        # "month_number": month_number,
        # "cal": cal,
    })

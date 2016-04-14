from django.apps import AppConfig
from base.models import athlete
from base.models import activity
from stravalib.client import Client
from datetime import datetime
from datetime import timedelta
import chartit
from django.db.models import Sum

class BaseConfig(AppConfig):
    name = 'base'

class stravalib_app(AppConfig):
    name = 'stravalib'

class chartit_app(AppConfig):
    name = 'chartit'

def data_scraper(date_start, date_end):
    meters_to_miles = 0.000621371
    meters_to_feet = 3.28084
    km_to_miles = 0.621371
    athlete_list = athlete.objects.all() # get list of all athletes
    for each_athlete in athlete_list: # for each athlete
        print(each_athlete)
        client = Client(access_token=each_athlete.access_token)
        this_athlete_activities = client.get_activities(date_end, date_start)  # get list of activities for this month
        for each_activity in this_athlete_activities:  # for each activity
            if not activity.objects.filter(pk=each_activity.id):# check if its already in the database
                print(each_activity)
                new_activity = activity(
                    id=each_activity.id,
                    athlete_id=athlete.objects.filter(pk=each_activity.athlete.id)[0],
                    name=each_activity.name,
                    distance=meters_to_miles*each_activity.distance,
                    moving_time=each_activity.moving_time,
                    elapsed_time=each_activity.elapsed_time,
                    total_elevation_gain=meters_to_feet*each_activity.total_elevation_gain,
                    type=each_activity.type,
                    start_date_local=each_activity.start_date_local,
                    average_speed=km_to_miles*each_activity.average_speed,
                    calories=each_activity.calories,
                    photos=each_activity.photos,
                    day=each_activity.start_date_local.day)# if its not in the database, add it
                new_activity.save()

def get_athlete_daily_activities(athlete, date_start, date_end):
    daily_dictionary = {}
    relevant_activities = activity.objects.filter(athlete_id=athlete).filter(start_date_local__lte=date_end).filter(start_date_local__gte=date_start)
    for day in range((date_end-date_start).days):
        this_day_activities = activity.objects.filter(id__in=relevant_activities).filter(start_date_local__gte=date_start+timedelta(day)).filter(start_date_local__lte=date_start+timedelta(day)+timedelta(days=1)).annotate()
        # this_day_activities = activity.objects.filter(id__in=relevant_activities).filter(start_date_local=date_start+timedelta(day)).annotate()
        # print(this_day_activities)
        # this_day_activities = relevant_activities.objects.filter(start_date_local=date_start+datetime.timedelta(day))
        daily_dictionary[day] = this_day_activities
    return daily_dictionary

def get_cumulative_queryset(athlete, date_start, date_end):
    before = date_end
    after = date_start
    running_sum = activity.objects.filter(athlete_id=athlete).filter(start_date_local__lte=before).filter(start_date_local__gte=after).order_by('start_date_local')
    cumulative = 0
    for item in running_sum:
        cumulative += item.total_elevation_gain
        item.cumulative_elevation = cumulative
        item.save()
    return running_sum

def get_elevation_sum(daily_dictionary):
    daily_elevation_list = {}
    daily_elevation_sum = {}
    total_elevation = 0
    for day in daily_dictionary:
        daily_elevation = 0
        for each_activity in daily_dictionary[day]:
            daily_elevation += each_activity.total_elevation_gain
            total_elevation += each_activity.total_elevation_gain
        daily_elevation_list[day+1] = daily_elevation
        daily_elevation_sum[day+1] = total_elevation
    return daily_elevation_list, daily_elevation_sum

def get_leaderboard():
    # return a queryset of athletes in order of elevation total
    return athlete.objects.annotate(elevation=Sum('activity__total_elevation_gain')).order_by('-elevation')

def elev_per_day(activity_set, before, after):
    date_start = after
    date_end = before
    daily_dictionary = {}
    cumulative = 0
    for day in range((date_end-date_start).days):
        this_day_activities = activity.objects.filter(id__in=activity_set).filter(start_date_local__gte=date_start+timedelta(day)).filter(start_date_local__lte=date_start+timedelta(day)+timedelta(days=1)).aggregate(Sum('total_elevation_gain'))
        if this_day_activities['total_elevation_gain__sum']:
            cumulative += this_day_activities['total_elevation_gain__sum']
        daily_dictionary[day+1] = cumulative
    return daily_dictionary

def elevation_chart(before, after):
    # make a list of options/terms for each athlete
    this_series = []
    position = 1
    for each_athlete in get_leaderboard():
        cumulative_set = get_cumulative_queryset(each_athlete, after, before))
        this_series.append({'options':{'source': cumulative_set},
                       'terms':[{str(each_athlete)+'_date':'day'}, {str(each_athlete): 'cumulative_elevation'}]})
        position += 1
    ds = chartit.DataPool(this_series)

    athlete_list_date = [str(x)+'_date' for x in get_leaderboard()]
    athlete_list_elevation = [str(x) for x in get_leaderboard()]
    term_dict = {}
    for key, value in enumerate(athlete_list_date):
        term_dict[value] = [athlete_list_elevation[key],]
    chart_series = [{'options':{'type': 'line', 'stacking': False}, 'terms':term_dict}]

    cht = chartit.Chart(
        datasource=ds,
        series_options=chart_series,
        chart_options={'title': {'text': 'Elevation Summary'},
                       'xAxis': {'title': {'text': 'Day'}},
                       'yAxis': {'title': {'text': 'Elevation (feet)'}},
                       'legend': {'layout': 'vertical',
                                 'align': 'left',
                                 'verticalAlign': 'top',
                                 'reversed': 'true',
                                 'maxHeight':500}
        }
    )
    return cht

def athlete_chart(this_person):

    ds = chartit.DataPool(
       series=
        [{'options': {'source': activity.objects.filter(athlete_id = this_person)},
          'terms': [{'day':'start_date_local'}, 'total_elevation_gain', 'cumulative_elevation']}]
    )

    cht = chartit.Chart(
        datasource=ds,
        series_options=[{'options':{'type': 'column', 'stacking': False, 'xAxis':0, 'yAxis':0},
                         'terms':{'day': ['total_elevation_gain']}},
                        {'options':{'type': 'line', 'stacking': False, 'xAxis':0, 'yAxis':1},
                         'terms':{'day': ['cumulative_elevation']},
                        }],
        chart_options={'title': {'text': 'Activity Stats'},
                       'xAxis': {'tickInterval':1, 'labels': {'rotation': -45}, 'title': {'text': 'date'}}}
    )

    return cht


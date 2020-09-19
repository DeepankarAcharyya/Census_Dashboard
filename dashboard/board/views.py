from django.http import JsonResponse
from django.shortcuts import render
from board.models import census_data
from django.core import serializers
from django.db import connection

def select_page(request):
    if request.method == 'GET':
        print(request.GET)
        value = request.GET['value']
        if value=="overview":
            return get_homebase_data(request,1)
        else:
            return statebase_page(request)


def get_homebase_data(request,id=0):
    population=0
    literates=0
    with connection.cursor() as cursor:
        cursor.execute('select state, sum(lit_total) from board_census_data group by state')
        queryset = cursor.fetchall()

        cursor.execute('select state, sum(pop_males), sum(pop_females) from board_census_data group by state')
        state_set=cursor.fetchall()
        
        cursor.execute('select sum(pop_total) from board_census_data')
        population=cursor.fetchall()

        cursor.execute('select sum(lit_total) from board_census_data')
        literates=cursor.fetchall()

        cursor.execute('select state, (cast(total_literates_male as float)/cast(total_population_male as float) * 100) as male_lr,\
                       (cast(total_literates_female as float)/cast(total_population_female as float) * 100) as female_lr\
                       from(select state, sum(lit_males) as total_literates_male, sum(lit_females) as total_literates_female,\
                            sum(pop_males) as total_population_male, sum(pop_females) as total_population_female\
                            from board_census_data group by state) as foo')
        literacy_rate_fetch=cursor.fetchall()

    literacy_rate=round((literates[0][0]/population[0][0])*100,2)
    literacy_rate_set=[]
    for state in literacy_rate_fetch:
        literacy_rate_set.append({'state':state[0],'male':round(state[1],2),'female':round(state[2],2)})

    states=[]
    state_set_data=[]
    for state in state_set:
        state_set_data.append({"location":state[0],"population_male":state[1],"population_female":state[2]})
        states.append(state[0])

    #print(states)
    literate_total_data = []

    for row in queryset:
        literate_total_data.append({"location":row[0],"population":row[1]})

    if id==0:
        return render(request, 'dashboard_census.html',{ 'literate_total_data': literate_total_data,'no_of_states':len(states), 'state_data':state_set_data, 'states':states, 'population':population[0][0], 'literates':literates[0][0], 'literacy_rate':literacy_rate, 'state_lr':literacy_rate_set})
    else:
        return JsonResponse({'literate_total_data': literate_total_data, 'no_of_states': len(states), 'state_data': state_set_data, 'states': states, 'population': population[0][0], 'literates': literates[0][0], 'literacy_rate': literacy_rate, 'state_lr': literacy_rate_set})

def statebase_page(request):
    population = 0
    literates = 0

    location=request.GET['value']

    with connection.cursor() as cursor:
        query = "select location, lit_total from board_census_data where state='" +location+"';"
        cursor.execute(query)
        queryset = cursor.fetchall()

        query = "select location, pop_males, pop_females from board_census_data where state='" +location+"';"
        cursor.execute(query)
        state_set = cursor.fetchall()

        cursor.execute("select sum(pop_total) from board_census_data where state='"+location+"' group by state;")
        population = cursor.fetchall()

        cursor.execute("select sum(lit_total) from board_census_data where state='"+location+"' group by state;")
        literates = cursor.fetchall()

        cursor.execute("select location, (cast(total_literates_male as float)/cast(total_population_male as float) * 100) as male_lr,\
                       (cast(total_literates_female as float)/cast(total_population_female as float) * 100) as female_lr\
                       from(select location, lit_males as total_literates_male, lit_females as total_literates_female,\
                            pop_males as total_population_male, pop_females as total_population_female\
                            from board_census_data where state='"+location+"') as foo")
        literacy_rate_fetch = cursor.fetchall()

    literacy_rate = round((literates[0][0]/population[0][0])*100, 2)
    literacy_rate_set = []
    for state in literacy_rate_fetch:
        literacy_rate_set.append({'state': state[0], 'male': round(
            state[1], 2), 'female': round(state[2], 2)})

    states = []
    state_set_data = []
    for state in state_set:
        state_set_data.append(
            {"location": state[0], "population_male": state[1], "population_female": state[2]})
        states.append(state[0])

    literate_total_data = []

    for row in queryset:
        literate_total_data.append({"location": row[0], "population": row[1]})

    return JsonResponse({'literate_total_data': literate_total_data, 'no_of_states': len(states), 'state_data': state_set_data, 'states': states, 'population': population[0][0], 'literates': literates[0][0], 'literacy_rate': literacy_rate, 'state_lr': literacy_rate_set})

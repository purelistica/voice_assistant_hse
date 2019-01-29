from behave import *
from modules import maps_functions, record_audio, ya_speech
from modules import locations, directions

route_modes = ['walking', 'driving', 'transit']


@given('locations Пашин дом and Библиотека are saved')
def step_impl(context):
    d = {'пашин дом': {'lat': 59.93852459999999, 'lng': 30.2266464},
         'библиотека': {'lat': 59.94315899999999, 'lng': 30.2350171}}
    locations.update_locations(d)


@when('user says Set up route from {origin} to {destination}')
def step_impl(context, origin, destination):
    context.command = 'route'
    context.route_from = origin
    context.route_to = destination


@when('user says Set up route to {destination}')
def step_impl(context, destination):
    context.command = 'route'
    context.route_from = 'current'
    context.route_to = destination


@when(u'User says go by {mode}')
def step_impl(context, mode):
    if mode == 'foot':
        context.route_mode = 'walking'
    elif mode == 'car':
        context.route_mode = 'driving'
    elif mode == 'transport':
        context.route_mode = 'transit'
    else:
        context.route_mode = None


@when(u'user says choose the fastest mode')
def step_impl(context):
    context.route_mode = 'fastest'


@then(u'VA validates locations')
def step_impl(context):
    if context.route_from == 'current':
        context.route_from = maps_functions.get_current_geo()
    else:
        context.route_from = locations.get_by_name(context.route_from)
    context.route_to = locations.get_by_name(context.route_to)


@when(u'VA asks "Which way?"')
def step_impl(context):
    assert context.route_from != 'not found' and context.route_to != 'not found'
    assert context.route_from is not None and context.route_to is not None


@then(u'VA names the travel mode')
def step_impl(context):
    assert context.route_mode == 'fastest'
    dur_mode = {}
    for mode in route_modes:
        route = directions.get_directions(context.route_from,
                                          context.route_from,
                                          mode)
        dur = directions.route_duration(route)
        dur_mode[mode] = dur
    context.route_mode = min(dur_mode, key=dur_mode.get)
    # context.route_dur = dur_mode[context.route_mode]


@then(u'VA says time')
def step_impl(context):
    assert context.route_mode in route_modes
    route = directions.get_directions(context.route_from,
                                      context.route_from,
                                      context.route_mode)
    assert route is not None
    context.route = route
    context.route_dur = directions.route_duration(route)
    ya_speech.synthesize('Маршрут займет ' + str(context.route_dur) + ' минут', context.va)


@then(u'VA says "Invalid location(s)"')
def step_impl(context):
    assert context.route_from == 'not found' or context.route_to == 'not found'


@when(u'user gives command to start the route')
def step_impl(context):
    ya_speech.synthesize('Начать маршрут', context.va)


@then(u'VA follows the route')
def step_impl(context):
    # mock
    pass

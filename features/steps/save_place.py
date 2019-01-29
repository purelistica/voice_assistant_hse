from behave import *
from modules import maps_functions, record_audio, ya_speech
from modules import locations


@when('user says "Save my location"')
def get_location(context):
    context.user_last_command = ya_speech.recognize("audio_files/save_location.wav")
    assert context.user_last_command == "сохранить текущее местоположение"
    if context.va_task is None:
        context.va_task = 'save'
        context.task_status = 'set'
        context.location = maps_functions.get_current_geo()


@when('user says "Save location"')
def get_location(context):
    context.user_last_command = ya_speech.recognize("audio_files/save.wav")
    assert context.user_last_command == "сохрани место"
    if context.va_task is None:
        context.va_task = 'save'
        context.task_status = 'added'
        context.location = None


@then('VA asks "What is the address?"')
def step_impl(context):
    assert context.va_task == 'save' and context.task_status == 'added' and context.location is None
    ya_speech.synthesize('Задай адрес', context.va)


@when('user says address {address}')
def step_impl(context, address):
    assert context.va_task == 'save'
    if address != '' and address is not None:
        loc = maps_functions.get_geo(address)
        if loc is not None:
            context.location = loc
            context.task_status = 'set'
        else:
            context.task_status = 'rejected'
    else:
        context.task_status = 'rejected'


@then(u'VA names location')
def approve_location(context):
    if context.va_task == 'save':
        if context.location is not None:
            address = maps_functions.get_address(context.location)
            if address is not None:
                ya_speech.synthesize(address, context.va)
            else:
                ya_speech.synthesize('Не могу определить адрес точки', context.va)
            if context.task_status == 'set':
                context.task_status = 'waits_approve'


@then("VA says 'Can't determine location'")
def get_location_fail(context):
    if context.user_last_command == "сохранить текущее местоположение":
        if context.location is None:
            ya_speech.synthesize('Не могу определить местоположение', context.va)


@then('VA asks to set a name')
def location_name(context):
    if context.va_task == 'save' and context.task_status == 'approved':
        ya_speech.synthesize('Задай имя', context.va)


@when('User says {name}')
def location_name(context, name):
    context.name_active = name
    # context.name_active = ya_speech.recognize(context.user)


@then('VA saves location')
def step_impl(context):
    assert context.name_active is not None
    assert context.va_task == 'save'
    assert context.task_status == 'approved'
    res = locations.add_location(context.name_active, context.location)
    if res == 'ok':
        context.task_status = 'done'


@then('VA says "Location already exists"')
def step_impl(context):
    assert context.name_active is not None
    assert context.va_task == 'save'
    assert context.task_status == 'approved'
    res = locations.add_location(context.name_active, context.location)
    if res != 'ok':
        context.task_status = 'rejected'
        ya_speech.synthesize('Место ' + context.name_active + ' уже существует!', context.va)

from behave import *
from modules import maps_functions, ya_speech
from modules import locations


edit_properties = ['name', 'address']


@when('User says delete {name}')
def delete_location_name(context, name):
    if context.va_task is None:
        context.va_task = 'delete'
        context.task_status = 'set'
        context.name_active = name.lower()


@then('VA says "The place is not found"')
def step_impl(context):
    assert context.name_active_loc == 'not found'
    assert context.task_status == 'rejected'
    ya_speech.synthesize('Место ' + context.name_active + ' не найдено', context.va)


@then('VA deletes place')
def delete_location(context):
    assert context.va_task == 'delete'
    assert context.task_status == 'approved'
    res = locations.remove_location(context.name_active)
    if res == "ok" and locations.get_by_name(context.name_active) == 'not found':
        context.task_status = 'done'
    else:
        context.task_status = 'rejected'


# ----------


@when('User says edit {name}')
def step_impl(context, name):
    # context.user_last_command = ya_speech.recognize(context.user)
    # assert context.user_last_command == "редактировать " + name
    if context.va_task is None:
        context.va_task = 'edit'
        context.task_status = 'added'
        context.name_active = name.lower()


@then(u'VA validates input')
def step_impl(context):
    if context.va_task == 'edit' and context.task_status == 'added':
        if context.name_active != '' and context.name_active is not None:
            context.name_active_loc = locations.get_by_name(context.name_active)
            if context.name_active_loc != 'not found' and context.name_active_loc is not None:
                context.task_status = 'set'
            else:
                context.task_status = 'rejected'  # -> VA says "The place is not found"
        else:
            context.task_status = 'rejected'  # не распознали
    elif context.va_task == 'edit' and context.task_status == 'set':
        if context.change_property_val != '' and context.change_property_val is not None:
            if context.change_property == 'name':
                context.task_status = 'waits_approve'
            if context.change_property == 'address':
                loc = maps_functions.get_geo(context.change_property_val)
                if loc is not None:
                    context.task_status = 'waits_approve'
                    context.change_property_location = loc
                else:
                    context.task_status = 'rejected'  # нет такого
        else:
            context.task_status = 'rejected'  # не распознали
    elif context.va_task == 'delete' and context.task_status == 'set':
        if context.name_active != '' and context.name_active is not None:
            context.name_active_loc = locations.get_by_name(context.name_active)
            if context.name_active_loc != 'not found' and context.name_active_loc is not None:
                context.task_status = 'waits_approve'
            else:
                context.task_status = 'rejected'
        else:
            context.task_status = 'rejected'  # ошибка распознавания


@then(u'VA asks "What would you like to change, name or address?"')
def step_impl(context):
    assert context.va_task == 'edit' and context.task_status == 'set'
    ya_speech.synthesize('Вы хотите изменить имя или адрес?', context.va)


@when('user says change {prop}')
def step_impl(context, prop):
    if prop in edit_properties:
        context.change_property = prop
    else:
        context.task_status = 'rejected'  # repeat


@then(u'VA asks "What is the new {prop}?"')
def step_impl(context, prop):
    assert context.task_status == 'set'
    assert context.change_property is not None
    prop_rus = 'имя' if prop == 'name' else 'адрес'
    ya_speech.synthesize('Задайте ' + prop_rus, context.va)


@when('User says new {prop} is {value}')
def location_name_new(context, prop, value):
    assert context.change_property == prop
    context.change_property_val = value


@when(u'VA names updated location')
def step_impl(context):
    if context.change_property == 'name':
        place = context.change_property_val
        address = maps_functions.get_address(context.name_active_loc)
    else:
        place = context.name_active
        address = context.change_property_val
    ya_speech.synthesize(place + ', ' + address, context.va)


@then('VA updates location')
def step_impl(context):
    assert context.va_task == 'edit'
    assert context.task_status == 'approved'
    if context.change_property == 'name':
        name_new = context.change_property_val
        loc_new = context.name_active_loc
    else:
        name_new = context.name_active
        loc_new = maps_functions.get_geo(context.change_property_val)
    res1 = locations.remove_location(context.name_active)
    res2 = locations.add_location(name_new, loc_new)
    if res1 == 'ok' and res2 == 'ok':
        context.task_status = 'done'
    else:
        context.task_status = 'rejected'

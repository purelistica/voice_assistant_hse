from behave import *
from modules import maps_functions, record_audio, ya_speech
from modules import additional_funcs, locations


commands = ['save', 'edit', 'delete', 'route']


@given('service is working')
def listener(context):
    context.user = "audio_files/behave_user.wav"
    context.va = "audio_files/behave_va.wav"
    # instead of prepared files we can work with mic
    # record_audio.listen(context.user)
    context.user_last_command = None
    context.va_task = None
    context.task_status = None  # can be in ['set', 'waits_approve', 'approved', 'rejected', 'done']
    context.name_active = None


@given('location list is empty')
def step_impl(context):
    d = {}
    locations.update_locations(d)


@given('location {name} exists in saved list')
def step_impl(context, name):
    name = name.lower()
    assert locations.get_by_name(name) != 'not found'


@when('user says "Hello, Borya"')
def hello_boris(context):
    # recognize command from mic
    # hello = ya_speech.recognize(context.user)
    context.user_last_command = ya_speech.recognize("audio_files/hello_boris.pcm")
    assert context.user_last_command == 'привет борис'


@then('VA says "Hello"')
def hello_user(context):
    if context.user_last_command == "привет борис":
        ya_speech.synthesize('Привет!', context.va)


@when('user says nothing')
def hello_boris(context):
    context.user_last_command = ya_speech.recognize('audio_files/empty_file.wav')
    assert context.user_last_command is None


@then(u'VA says \'Can\'t recognize name\'')
def hello_user(context):
    if context.user_last_command is None:
        ya_speech.synthesize('Ошибка распознавания', context.va)


@when('User confirms')
def step_impl(context):
    assert ya_speech.recognize("audio_files/da.wav") == 'да'
    if context.va_task is not None and context.task_status == 'waits_approve':
        context.task_status = 'approved'


@when('User does not confirm')
def step_impl(context):
    assert ya_speech.recognize("audio_files/net.wav") == 'нет'
    if context.va_task is not None and context.task_status == 'waits_approve':
        context.task_status = 'rejected'


@then('VA says "Done"')
def step_impl(context):
    assert context.task_status == "done"
    ya_speech.synthesize('Готово!', context.va)


@then('VA says "Cancelled"')
def save_confirm(context):
    assert context.task_status == "rejected"
    ya_speech.synthesize('Задача отменена', context.va)

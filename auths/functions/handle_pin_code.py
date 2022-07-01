import datetime
from random import randint

from django.utils import timezone


def rand_code(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def create_user_pin(user, type):
    from auths.models.user_pin import UserPin
    obj, created = UserPin.objects.get_or_create(user=user, type=type)
    obj.pin = rand_code(6)
    # ic(obj.pin)
    generated_number = int(obj.generated_number)
    delta_time = timezone.now() - obj.last_modified_at
    minutes_5 = datetime.timedelta(minutes=5)

    if generated_number < 3:
        generated_number += 1
        obj.generated_number = generated_number
        obj.save()

    else:
        if delta_time < minutes_5:
            return f"You reached maximum code generating requests please wait for {minutes_5 - delta_time} and request new {type} code again. "
        else:
            obj.generated_number = 0
            obj.pin = rand_code(6)
            obj.save()
    return True


def check_user_pin(user, type, pin):
    from auths.models.user_pin import UserPin
    try:
        obj = UserPin.objects.get(user=user, type=type)
    except:
        return f'The user {user.username} has no {type} pin code.'
    if obj.trials_number < 3:
        if int(obj.pin) == int(pin):
            obj.delete()
            return True
        else:
            obj.trials_number += 1
            obj.save()
            return 'Invalid code.'

    else:
        minutes_5 = datetime.timedelta(minutes=5)
        delta_time = timezone.now() - obj.last_modified_at
        if delta_time < minutes_5:
            return f"You reached maximum number of failed trials please try again after {minutes_5 - delta_time}."
        else:
            obj.trials_number = 0
            obj.pin = rand_code(6)
            obj.save()
            return f"A new pin code has been sent to your email."

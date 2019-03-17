import dateutil.parser
import datetime
import math

# validation of foodtype, location, date, time, amount of people

def parse_int(n):
    try:
        return int(n)
    except ValueError:
        return float('nan')

def foodtype_validation(foodtype):
    if foodtype is not None and foodtype.lower() not in ['chinese', 'japanese', 'indian']:
        return False
    else:
        return True


def location_validation(location):
    # if location is not None and location not in ['new york', 'boston']:
    #     return False
    # else:
    return True


def date_validation(date):
    if datetime.datetime.strptime(date, '%Y-%m-%d').date() < datetime.date.today():
        return False
    try:
        dateutil.parser.parse(date)
        return True
    except ValueError:
        return False


def time_validation(time):
    if time is not None and len(time) != 5:
        return False
    else:
        hour, minute = time.split(':')
        hour = parse_int(hour)
        minute = parse_int(minute)
        if math.isnan(hour) or math.isnan(minute):
            return False
        return True


def amount_validation(amount):
    if amount is not None and int(amount)<=0:
        return False
    else:
        return True


def order_validation(event, foodtype, location, date, time, amount):
    session_attributes = event['sessionAttributes']
    intent_name = event['currentIntent']['name']
    if foodtype is not None and not foodtype_validation(foodtype):
        # when food type is not supported
        slot_to_elicit = 'FoodType'
        message = 'We do not support {} cuisine yet, our most popular cuisine is indian cuisine'.format(foodtype)
        # return build_response(session_attributes, intent_name, slots, slot_to_elicit, message)
        return build_validation_result(False, slot_to_elicit, message)

    if location is not None and not location_validation(location):
        # when location is not supported
        slot_to_elicit = 'Location'
        message = 'We do not support {} area yet, sorry!'.format(location)
        return build_validation_result(False, slot_to_elicit, message)

    if date is not None and not date_validation(date):
        # when date format is not supported
        slot_to_elicit = 'Date'
        message = 'The date format is invalid and you can consult from today onward, sorry!'
        return build_validation_result(False, slot_to_elicit, message)

    if time is not None and not time_validation(time):
        # when time format is not supported
        slot_to_elicit = 'Time'
        message = 'The time format is invalid, sorry!'
        return build_validation_result(False, slot_to_elicit, message)

    if amount is not None and not amount_validation(amount):
        # when amount format is not supported
        slot_to_elicit = 'Amount'
        message = 'The amount format is invalid,it should be number, sorry!'
        return build_validation_result(False, slot_to_elicit, message)
    # the validation of time, amount still under development
    return build_validation_result(True, None, None)


def build_validation_result(is_valid, violated_slot, message_content):
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot,
        }

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }

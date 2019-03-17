import YelpFusion
import intent_validation as vali


def order_food(intent_request):
    foodtype = get_slots(intent_request)["FoodType"]
    location = get_slots(intent_request)["Location"]
    date = get_slots(intent_request)["Date"]
    time = get_slots(intent_request)["Time"]
    amount = get_slots(intent_request)["Amount"]
    source = intent_request['invocationSource']
    if source == 'DialogCodeHook':
        slots = get_slots(intent_request)
        validation_result = vali.order_validation(intent_request, foodtype, location, date, time, amount)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])
        else:
            output_session_attributes = intent_request['sessionAttributes'] if intent_request[
                                                                                   'sessionAttributes'] is not None else {}
            return delegate(output_session_attributes, intent_request["currentIntent"]["slots"])
    response = None
    suggestions = searching(foodtype, location, date, time, amount)
    response = {
        "dialogAction":
            {
                "fulfillmentState": "Fulfilled",
                "type": "Close", "message":
                {
                    "contentType": "PlainText",
                    "content": "Here are our suggestions for " + amount + " people:" + suggestions
                }
            }
    }
    return response


def lambda_handler(event, context):
    return order_food(event)


# search the result by the paramter and return the result in list form
def searching(foodtype, location, date, time, amount):
    result = YelpFusion.findfood(foodtype, location, date, time, amount)
    return result


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


def get_slots(intent_request):
    return intent_request['currentIntent']['slots']

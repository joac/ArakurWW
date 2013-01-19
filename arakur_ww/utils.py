import json

def remote_plc_command(function_name, *args, **kwargs):
    print function_name
    print args
    print kwargs
    data = {'name': function_name,
            'args': args,
            'kwargs' : kwargs,
            }
    return json.dumps(data)

def execute_command(instance, message):
    c = json.loads(message)
    return getattr(instance, c['name'])(*c['args'], **c['kwargs'])

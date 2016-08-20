import hug
import os

print(os.getenv('FOO', 'bar'))

def cors_support(response=None, *args, **kwrgs):
    """add support for cors. in this case, allow all origins"""
    response and response.set_header('Access-Control-Allow-Origin', '*')


@hug.get('/{name}', requires=cors_support)
def say_hi(name: hug.types.text='', hug_timer=3):
    print('Got: ' + name)
    return {"message": "hello " + name, "took": float(hug_timer)}

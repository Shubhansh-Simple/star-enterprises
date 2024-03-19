# utils/custom_messages.py

'''
Write custom messages generator method for application
'''

def generate_msg(quantity, item_name, msg):
    '''Generate the text messages for form submission'''

    return f'{quantity} {item_name}, {msg} successfully!'

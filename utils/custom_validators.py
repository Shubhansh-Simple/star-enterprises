# utils/custom_validators.py

'''
Write custom validation method for application
'''

# python
from datetime import datetime


def validate_entry_date(entry_date):
    '''Validate the provided entry_date using url'''

    expected_date_format = '%Y-%m-%d'
    today_date           = datetime.today().date()

    try:
        entry_date = datetime.strptime(entry_date, expected_date_format).date()

    # Invalid entry_date provided
    except ValueError:
        entry_date = None

    # Future entry_date not supported
    else:
        if entry_date > today_date: entry_date = None

    finally:
        return entry_date



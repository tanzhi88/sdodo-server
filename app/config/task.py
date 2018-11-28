def test_data():
    print('a')

JOBS = [
    {
        'id': 'job1',
        'func': 'test_data',
        'args': '',
        'trigger': {
            'type': 'cron',
            'day_of_week': "mon-fri",
            'hour': '0-23',
            'minute': '0-11',
            'second': '*/5'
        }

    }
]

SCHEDULER_API_ENABLED = True
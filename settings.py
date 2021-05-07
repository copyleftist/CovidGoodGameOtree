from os import environ

DEBUG = 0
SESSION_CONFIGS = [
    dict(
        name='theresa_fernanda_base',
        display_name="Public Covid",
        num_demo_participants=2,
        single_player=False,
        use_browser_bots=False,
        app_sequence=['step1'],
    ),

    dict(
        name='survey',
        display_name='survey',
        num_demo_participants=1,
        app_sequence=['survey', 'payment_info'],
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(
        name='prolific',
        display_name='Prolific experiment',
        #participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '7f%n61qy537uzmsb3$zsxjxlpeqzb=442lk_&t&)(!-xj%fn^h'

INSTALLED_APPS = ['otree']

PARTICIPANT_FIELDS = ['opp_id', 'multiplier', 'disclose', 'contribution',
                      'prolific_id', 'idx', 'is_dropout', 'time_at_last_response']

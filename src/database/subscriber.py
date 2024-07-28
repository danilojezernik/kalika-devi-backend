import datetime

from src import env
from src.domain.subscriber import Subscriber

subscriber = [
    Subscriber(
        name='Danilo',
        surname='Jezernik',
        email=env.EMAIL_1,
        confirmed=False,
        datum_vnosa=datetime.datetime.now()
    ).dict(by_alias=True),
    Subscriber(
        name='Dani',
        surname='Jez',
        email=env.EMAIL_2,
        confirmed=False,
        datum_vnosa=datetime.datetime.now()
    ).dict(by_alias=True)
]

import datetime

from src.domain.links import Links

links = [
    Links(
        title='CSS w3school',
        link='https://www.w3schools.com/css/',
        datum_vnosa=datetime.datetime.now()
    ).dict(by_alias=True)
]
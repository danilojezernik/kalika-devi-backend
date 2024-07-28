import datetime

from src.domain.blog import Blog

blog = [
    Blog(
        title='Test Naslov 1',
        kategorija='angular',
        podnaslov='Test Podnaslov 1',
        datum_vnosa=datetime.datetime.now(),
        vsebina='Test Vsebina 1',
        image='test1.jpg'
    ).dict(by_alias=True),
    Blog(
        title='Test Naslov 2',
        kategorija='angular',
        podnaslov='Test Podnaslov 2',
        datum_vnosa=datetime.datetime.now(),
        vsebina='Test Vsebina 2',
        image='test2.jpg'
    ).dict(by_alias=True),
    Blog(
        title='Test Naslov 3',
        kategorija='angular',
        podnaslov='Test Podnaslov 3',
        datum_vnosa=datetime.datetime.now(),
        vsebina='Test Vsebina 3',
        image='test3.jpg'
    ).dict(by_alias=True),
]

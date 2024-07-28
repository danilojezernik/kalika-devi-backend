import datetime

from src.domain.technology import Technology

technology = [
    Technology(
        technology='Angular',
        title='Angular interview questions',
        subtitle='Angular je framework, ki ga dela Google in je zelo priljubljen. V tem članku bomo pregledali nekaj '
                 'vprašanj, ki se pogosto pojavljajo na tehničnih razgovorih.',
        vsebina='Angular je odprtokodni JavaScriptov ogrodje, ki ga uporabljajo za razvoj enostranskih aplikacij. ',
        image='angular1.jpg',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Technology(
        technology='Vue',
        title='Vue interview questions',
        subtitle='Vue je framework, ki ga dela Google in je zelo priljubljen. V tem članku bomo pregledali nekaj '
                 'vprašanj, ki se pogosto pojavljajo na tehničnih razgovorih.',
        vsebina='Vue je odprtokodni JavaScriptov ogrodje, ki ga uporabljajo za razvoj enostranskih aplikacij. ',
        image='vue2.jpg',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Technology(
        technology='Typescript',
        title='Typescript interview questions',
        subtitle='Typescript je framework, ki ga dela Google in je zelo priljubljen. V tem članku bomo pregledali nekaj'
                 'vprašanj, ki se pogosto pojavljajo na tehničnih razgovorih.',
        vsebina='Typescript je odprtokodni JavaScriptov ogrodje, ki ga uporabljajo za razvoj enostranskih aplikacij. ',
        image='typescript2.jpg',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
]

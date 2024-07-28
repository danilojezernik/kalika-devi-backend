import datetime

from src.domain.projects import Projects

projects = [
    Projects(
        title='Kalkulator',
        subtitle='Kalkulator z javascript',
        category='beginner',
        content='Kalkuliranje preprostih izračunov za izračun stopinj',
        github='',
        website='',
        datum_vnosa=datetime.datetime.now()
    ).dict(by_alias=True)
]

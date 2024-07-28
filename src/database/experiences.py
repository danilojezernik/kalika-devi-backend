import datetime

from src.domain.experiences import Experiences

experiences = [
    Experiences(
        title='Frontend developer za aplikacijo sledenja',
        stack='Frontend developer',
        framework='Angular',
        programming_language='TypeScript',
        company='USCOM d.o.o.',
        employee=True,
        tasks='Delal sem kot frontend razvijalec za aplikacijo sledenja Sledat',
        company_start='3. Nov 2023',
        company_end='',
        datum_vnosa=datetime.datetime.now()
    ).dict(by_alias=True)
]
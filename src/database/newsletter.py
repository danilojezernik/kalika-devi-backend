import datetime

from src.domain.newsletter import Newsletter

newsletter = [
    Newsletter(
        title='Newsletter 1',
        content='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ut convallis magna. Donec felis massa, egestas a auctor in, '
                'mollis at neque. Aliquam et massa efficitur magna porta ultricies. Curabitur ac massa nec ligula tempor dapibus quis a ex. '
                'Maecenas lobortis id erat eu feugiat. Etiam tempor tellus ornare tristique imperdiet. Aliquam erat volutpat. Sed mollis molestie '
                'ligula, sed fermentum metus fermentum non. In sed venenatis nulla, et facilisis est. Maecenas ultrices, eros sit amet posuere '
                'semper, quam nulla dictum velit, bibendum consectetur nisl urna vel lectus. Maecenas porta accumsan sollicitudin. Lorem ipsum '
                'dolor sit amet, consectetur adipiscing elit. Vestibulum diam felis, vulputate id gravida et, sagittis ut elit. Phasellus non nibh '
                'molestie, hendrerit tortor at, dictum ipsum. Phasellus dui sapien, placerat vitae congue vel, feugiat ut purus. Maecenas tincidunt '
                'lorem sit amet molestie auctor.',
        datum_vnosa=datetime.datetime.now()
    ).dict(by_alias=True),
    Newsletter(
        title='Newsletter 1',
        content='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ut convallis magna. Donec felis massa, egestas a auctor in, '
                'mollis at neque. Aliquam et massa efficitur magna porta ultricies. Curabitur ac massa nec ligula tempor dapibus quis a ex. '
                'Maecenas lobortis id erat eu feugiat. Etiam tempor tellus ornare tristique imperdiet. Aliquam erat volutpat. Sed mollis molestie '
                'ligula, sed fermentum metus fermentum non. In sed venenatis nulla, et facilisis est. Maecenas ultrices, eros sit amet posuere '
                'semper, quam nulla dictum velit, bibendum consectetur nisl urna vel lectus. Maecenas porta accumsan sollicitudin. Lorem ipsum '
                'dolor sit amet, consectetur adipiscing elit. Vestibulum diam felis, vulputate id gravida et, sagittis ut elit. Phasellus non nibh '
                'molestie, hendrerit tortor at, dictum ipsum. Phasellus dui sapien, placerat vitae congue vel, feugiat ut purus. Maecenas tincidunt '
                'lorem sit amet molestie auctor.',
        datum_vnosa=datetime.datetime.now()
    ).dict(by_alias=True)
]

import time

from django.utils.lorem_ipsum import COMMON_P

from open.core.writeup.serializers import TextAlgorithmPromptSerializer

"""
dpy runscript writeup_time_serializers

ended up taking 2.59 milliseconds, so not worth the refactoring
"""


def run():
    data = {
        "text": "Today I Saw A Village, what if i had a lot of text" + COMMON_P,
        "temperature": 1,
        "top_k": 20,
    }

    start = time.time()
    serializer = TextAlgorithmPromptSerializer(data=data)
    serializer.is_valid()
    end = time.time()

    difference = end - start

    print(difference)

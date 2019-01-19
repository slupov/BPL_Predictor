from ...models import MatchRawData
from .form_extraction import extract_forms


def seed_training_model():
    # just a test
    test = extract_forms('Man United', 'Man City', '2017-12-10')

    print(test[0], "   ", test[1])

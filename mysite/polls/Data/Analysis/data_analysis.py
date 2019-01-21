import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from ...models import ExtractedFixtures


def analyze_data():
    train_table = ExtractedFixtures.objects.all().order_by('season', 'home_team')

    # for x in train_table:
        # print(x)


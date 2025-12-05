import os
from django.conf import settings
import matplotlib.pyplot as plt


def save_plot(image_path):
    folder = os.path.dirname(image_path)

    # Create directory if it doesn't exist
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    plt.savefig(image_path)
    plt.close()
    return image_path
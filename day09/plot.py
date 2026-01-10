import matplotlib.pyplot as plt
from collections import Counter

def plot_delay_buckets(delays):
    buckets = Counter(d["bucket"] for d in delays)
    plt.bar(buckets.keys(), buckets.values())
    plt.title("Submission Timing Distribution")
    plt.ylabel("Count")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()
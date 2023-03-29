import matplotlib.pyplot as plt


def plot(x, y_empirical, y_theoretical):
  plt.plot(x, y_theoretical, label='theoretical')
  plt.plot(x, y_empirical, label='empirical')
  plt.xlabel("number of cores")
  plt.ylabel("Speedup")
  plt.legend()
  plt.savefig("plot_speedup")
  #plt.show()


if __name__ == "__main__":
    plot([1, 2, 4, 8, 16, 32], 
        [1.0, 1.914575430485374, 2.6049958563761964, 4.165654316229251, 4.630293125152063, 5.1079493074113405],
        [1.0, 1.8797281683795652, 2.52291706145292, 3.9144710753751673, 4.312922021858152, 4.715313644666142])
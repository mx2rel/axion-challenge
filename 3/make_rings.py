import numpy as np


def make_rings(n_samples=70, noise=0.03):
  np.random.seed(42)
  X = np.random.uniform(-1.0, 1.0, size=(n_samples, 2))
  r = np.sqrt(X[:, 0] ** 2 + X[:, 1] ** 2)
  y = np.where((r >= 0.35) & (r <= 0.70), 1.0, -1.0)
  X += np.random.normal(0, noise, size=X.shape)
  # Skalowanie współrzędnych z [-1, 1] do kątów [0, pi] na potrzeby bramki Ry
  X_angles = (X + 1.0) * (np.pi / 2.0)
  return X, X_angles, y
import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp

from make_rings import make_rings
from reuploading_circuit import build_reuploading_circuit
from standard_circuit import build_standard_circuit

np.random.seed(42)

estimator = StatevectorEstimator()
Z0 = SparsePauliOp.from_sparse_list([("Z", [0], 1.0)], num_qubits=2)


def evaluate(circuit_builder, x, th):
  qc = circuit_builder(x, th)
  job = estimator.run([(qc, Z0)])
  return float(job.result()[0].data.evs)


def compute_gradient(circuit_builder, x, th):
  grad = np.zeros_like(th)
  for j in range(len(th)):
    th_plus = th.copy()
    th_minus = th.copy()
    th_plus[j] += np.pi / 2.0
    th_minus[j] -= np.pi / 2.0
    f_plus = evaluate(circuit_builder, x, th_plus)
    f_minus = evaluate(circuit_builder, x, th_minus)
    grad[j] = (f_plus - f_minus) / 2.0
  return grad


def train_model(
    circuit_builder, num_params=6, X=None, y=None, epochs=35, lr=0.15
):
  th = np.random.uniform(-0.1, 0.1, num_params)
  loss_history = []
  acc_history = []
  M = len(X)

  for epoch in range(1, epochs + 1):
    grad_L = np.zeros_like(th)
    total_loss = 0.0
    correct = 0

    for x_i, y_i in zip(X, y):
      f_i = evaluate(circuit_builder, x_i, th)
      total_loss += (f_i - y_i) ** 2

      if np.sign(f_i) == y_i:
        correct += 1

      df_dth = compute_gradient(circuit_builder, x_i, th)
      grad_L += 2.0 * (f_i - y_i) * df_dth

    th -= lr * (grad_L / M)

    epoch_loss = total_loss / M
    epoch_acc = (correct / M) * 100.0
    loss_history.append(epoch_loss)
    acc_history.append(epoch_acc)

    if epoch % 5 == 0 or epoch == epochs:
      print(
          f"  Epoka {epoch:2d}/{epochs:2d} | Loss: {epoch_loss:.4f} | Acc:"
          f" {epoch_acc:5.1f}%"
      )

  return th, loss_history, acc_history


if __name__ == "__main__":
  print("Generowanie zbioru 3 koncentrycznych stref...")
  X_raw, X_train, y_train = make_rings(n_samples=70, noise=0.03)

  print("\n=== Trening: Model Standardowy (1x Encoding, 6 wag) ===")
  th_std, loss_std, acc_std = train_model(
      build_standard_circuit,
      num_params=6,
      X=X_train,
      y=y_train,
      epochs=35,
      lr=0.15,
  )

  print("\n=== Trening: Data Re-uploading (2x Encoding, 6 wag) ===")
  th_reup, loss_reup, acc_reup = train_model(
      build_reuploading_circuit,
      num_params=6,
      X=X_train,
      y=y_train,
      epochs=35,
      lr=0.15,
  )

  print("\nObliczanie map granic decyzyjnych...")
  grid_res = 24
  gx = np.linspace(-1.0, 1.0, grid_res)
  gy = np.linspace(-1.0, 1.0, grid_res)
  GX, GY = np.meshgrid(gx, gy)

  preds_std = np.zeros((grid_res, grid_res))
  preds_reup = np.zeros((grid_res, grid_res))

  for i in range(grid_res):
    for j in range(grid_res):
      raw_pt = np.array([GX[i, j], GY[i, j]])
      angle_pt = (raw_pt + 1.0) * (np.pi / 2.0)
      preds_std[i, j] = evaluate(build_standard_circuit, angle_pt, th_std)
      preds_reup[i, j] = evaluate(build_reuploading_circuit, angle_pt, th_reup)

  fig, axs = plt.subplots(2, 2, figsize=(10, 9))

  axs[0, 0].plot(
      loss_std, label="Standardowy (1x)", color="gray", linestyle="--"
  )
  axs[0, 0].plot(
      loss_reup, label="Data Re-uploading (2x)", color="#1f77b4", lw=2
  )
  axs[0, 0].set_title("Funkcja kosztu (MSE Loss)")
  axs[0, 0].set_xlabel("Epoka")
  axs[0, 0].set_ylabel("Loss")
  axs[0, 0].legend()
  axs[0, 0].grid(True, alpha=0.3)

  axs[0, 1].plot(
      acc_std, label="Standardowy (1x)", color="gray", linestyle="--"
  )
  axs[0, 1].plot(
      acc_reup, label="Data Re-uploading (2x)", color="#2ca02c", lw=2
  )
  axs[0, 1].set_title("Dokładność (Accuracy %)")
  axs[0, 1].set_xlabel("Epoka")
  axs[0, 1].set_ylabel("Dokładność (%)")
  axs[0, 1].legend()
  axs[0, 1].grid(True, alpha=0.3)

  axs[1, 0].contourf(
      GX, GY, preds_std, levels=[-10.0, 0.0, 10.0], alpha=0.3, colors=["blue", "red"]
  )
  axs[1, 0].scatter(
      X_raw[y_train == -1, 0],
      X_raw[y_train == -1, 1],
      c="blue",
      edgecolors="k",
      s=30,
      label="Klasa -1",
  )
  axs[1, 0].scatter(
      X_raw[y_train == 1, 0],
      X_raw[y_train == 1, 1],
      c="red",
      edgecolors="k",
      s=30,
      label="Klasa +1",
  )
  axs[1, 0].set_title(f"Model Standardowy (Max Acc: {max(acc_std):.1f}%)")
  axs[1, 0].set_xlim(-1.0, 1.0)
  axs[1, 0].set_ylim(-1.0, 1.0)
  axs[1, 0].legend(loc="upper right", fontsize=8)

  axs[1, 1].contourf(
      GX,
      GY,
      preds_reup,
      levels=[-10.0, 0.0, 10.0],
      alpha=0.3,
      colors=["blue", "red"],
  )
  axs[1, 1].scatter(
      X_raw[y_train == -1, 0],
      X_raw[y_train == -1, 1],
      c="blue",
      edgecolors="k",
      s=30,
      label="Klasa -1",
  )
  axs[1, 1].scatter(
      X_raw[y_train == 1, 0],
      X_raw[y_train == 1, 1],
      c="red",
      edgecolors="k",
      s=30,
      label="Klasa +1",
  )
  axs[1, 1].set_title(f"Data Re-uploading (Max Acc: {max(acc_reup):.1f}%)")
  axs[1, 1].set_xlim(-1.0, 1.0)
  axs[1, 1].set_ylim(-1.0, 1.0)
  axs[1, 1].legend(loc="upper right", fontsize=8)

  plt.tight_layout()
  plt.savefig("wyniki.png", dpi=150)
  plt.show()
import pandas as pd
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class ModelRandkowy(nn.Module):
    def __init__(self, liczba_cech):
        super().__init__()
        self.siec = nn.Sequential(
            nn.Linear(liczba_cech, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )

    def forward(self, x):
        return self.siec(x)


def test(dane, cechy, name, liczba_prob=13):
    X = dane[cechy].values
    y = dane['dec'].values

    # Podział na train i test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Skalowanie bez wycieku danych
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Tensory PyTorch
    X_train_t = torch.tensor(X_train, dtype=torch.float32)
    y_train_t = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
    X_test_t = torch.tensor(X_test, dtype=torch.float32)
    y_test_t = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1)

    criterion = nn.BCEWithLogitsLoss()
    res = []

    for trial in range(liczba_prob):
        # KLUCZOWA POPRAWKA: Za każdym razem tworzymy NOWY model z innym seedem!
        torch.manual_seed(trial + 1)
        model = ModelRandkowy(liczba_cech=X_train_t.shape[1])
        optimizer = torch.optim.Adam(model.parameters(), lr=0.005)

        # Trening (dokładnie 150 epok na próbę)
        model.train()
        for epoch in range(150):
            outputs = model(X_train_t)
            loss = criterion(outputs, y_train_t)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        # Ewaluacja
        model.eval()
        with torch.no_grad():
            prawdopodobienstwo = torch.sigmoid(model(X_test_t))
            predykcje = (prawdopodobienstwo > 0.5).float()

            prawdziwe = (y_test_t == 1)
            wszystkie_pozytywne = prawdziwe.sum().item()

            celnosc = (predykcje == y_test_t).float().mean().item() * 100
            trafione = ((predykcje == 1) & prawdziwe).sum().item()
            alarmy = ((predykcje == 1) & (y_test_t == 0)).sum().item()
            recall = (trafione / wszystkie_pozytywne) * 100

            res.append({'accuracy': celnosc, 'recall': recall, 'false': alarmy})

    avg_results = {
        'avg_accuracy': sum(r['accuracy'] for r in res) / len(res),
        'avg_recall': sum(r['recall'] for r in res) / len(res),
        'avg_false': sum(r['false'] for r in res) / len(res)
    }

    print(
        f"\nŚREDNIE WYNIKI DLA {name} ({liczba_prob} prób):\n"
        f"Accuracy: {avg_results['avg_accuracy']:.2f}% | "
        f"Recall: {avg_results['avg_recall']:.2f}% | "
        f"Fałszywe alarmy: {avg_results['avg_false']:.2f}"
    )

    return avg_results
# Użycie data reuploadingu pozwoli modelowi znacznie lepiej rozrózniać nieliniowe/zawiłe zasady grupowania/przewidywania

## Obszar

Encoding

## Wstęp

Rozważamy problem zgadywania grupy dla pierścienia na przestrzeni 2x2 wyglądającej podobnie do:

```
_OO_
O__O
_OO_
```

_(będzie faktycznie bardziej zaokrąglony)_
gdzie `_` to klasa -1,
a `O` to klasa 1.

## Hipoteza

Zwykły model kwantowy używający tylko bramki Ry do kodowania danych sobie z tym nie poradzi - nie ma wystarczających zasobów matematycznych/sprawczości matematycznej aby wyrazić podzielenie przestrzeni 2D na 3 obszary, bo korzystać może tylko z sin(x) oraz cos(x).
Jeżeli damy modelowi możliwość (w postaci ponownego zakodowania danych, co po przekształceniach matematycznych pozwoli na większą ekspresywność w postaci sin(x), cos(x) ORAZ sin(2x), cos(2x) (itd w przypadku kolejnego zakodowania)), ten z niej skorzysta, bo pozwoli mu to obniżyć funkcję kosztu. Wynika to z potrzeby zmniejszenia okresu sinusoid, więc pomnożenia argumentu funkcji trygonometrycznych.

## Przewidywania

1. Dokładność modelu bez data reuploadingu będzie oscylował w okolicach 65% (m. in. z powodu większej ilości klasy -1) oraz możliwości dokonania tylko jednego podziału
2. Dokładność modelu z parokrotnym data reuploadingiem powinna skoczyć do około 90%, ponieważ rozdzielenie argumentów na 3 strefy jest możliwe ze względu na wyższą ekspresywność modelu. (90% m. in. ze względu na szum na granicach stref)

# Faza względna kubitu i jej znaczenie

Doczytałem o fazie względnej kubitu, interferencji kwantowej i ich znaczeniu w kontekście komputera kwantowego
W ogólnym zapisie na sferze Blocha fazę zapiszemy:
$$\vert{}\psi\rangle = \cos\left(\frac{\theta}{2}\right)\vert{}0\rangle + e^{i\varphi}\sin\left(\frac{\theta}{2}\right)\vert{}1\rangle$$

kąt $\theta$ ustala proporcję prawdopodobieństw, a $\varphi$ odpowiada za fazę względną.

Krótko mówiąc, fazę możemy traktować jako dodatkową informację w kubicie, która mimo tego, że nie wpływa na pomiar prawdopodobieństwa (bo przecież mierzymy amplitudy pionowe, a faza decyduje tylko o obrocie wokół osi pionowej) ma duże znaczenie bo może na niego wpłynąć w przyszłości (tzw. interferencja kwantowa) - informacja ta przechodzi razem z kubitem do następnej bramki.

Dobrym tego przykładem są stany |+> i |->. Licząc prawdopodobieństwa obydwa wykażą 50% szans na 0 i 50% na 1, jednak po zastosowaniu bramki Hadamarda H:

- H|-> zajdzie interferencja destruktywna dla zera (amplitudy znoszą się) oraz konstruktywna dla 1 więc pomiar da 100% pewności na wynik 1
- H|+> zajdzie interferencja konstruktywna dla zera i pomiar tego kubitu da 100% pewności na wynik 0

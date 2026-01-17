from UI.view import View
from model.model import Model
import flet as ft
import datetime

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def set_dates(self):
        first, last = self._model.get_date_range()

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """
        try:

            categoria = int(self._view.dd_category.value)
            first = self._view.dp1.value
            last = self._view.dp2.value
            nodi,archi = self._model.build_graph(categoria,first,last)
            self._view.txt_risultato.controls.append(ft.Text(f'Numero nodi: {nodi}'))
            self._view.txt_risultato.controls.append(ft.Text(f'Numero archi: {archi}'))
            self.populate_dd_prodotti()
        except ValueError:
            self._view.show_alert(f'Inserire categoria prima di proseguire')

        self._view.update()
    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        best_prodotti = self._model.più_venduti()
        self._view.txt_risultato.controls.append(ft.Text(f'I 5 prodotti più venduti:'))
        for prodotto,score in best_prodotti:
            self._view.txt_risultato.controls.append(ft.Text(f'{prodotto.product_name}, score : {score}'))
        self._view.update()


    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        try:
            L = int(self._view.txt_lunghezza_cammino.value)
            iniziale = int(self._view.dd_prodotto_iniziale.value)
            finale = int(self._view.dd_prodotto_finale.value)
            sol,peso=self._model.ricerca_cammino(iniziale,finale,L)
            self._view.txt_risultato.controls.clear()
            self._view.txt_risultato.controls.append(ft.Text(f'Camino migliore:'))
            print(sol)
            for nodo in sol:
                self._view.txt_risultato.controls.append(ft.Text(f'{nodo.product_name}'))

            self._view.txt_risultato.controls.append(ft.Text(f'peso totale {peso}'))
            self._view.update()
        except ValueError:
            self._view.show_alert(f'Inserire prodotto iniziale e finale prima di proseguire')


    def populate_dd_categoria(self):
        categorie = self._model.get_category()
        for categoria in categorie:

            self._view.dd_category.options.append(ft.dropdown.Option(key=categoria[0],text= categoria[1]))
        self._view.update()

    def populate_dd_prodotti(self):
        prodotti = self._model.prodotti
        for id in prodotti:
            prodotto = prodotti[id]
            self._view.dd_prodotto_iniziale.options.append(ft.dropdown.Option(key=prodotto.id, text=prodotto.product_name))
            self._view.dd_prodotto_finale.options.append(
                ft.dropdown.Option(key=prodotto.id, text=prodotto.product_name))
        self._view.update()

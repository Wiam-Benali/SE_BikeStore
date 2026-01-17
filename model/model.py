import copy

import networkx as nx

from database.dao import DAO
from operator import itemgetter


class Model:
    def __init__(self):
        self.prodotti = None
        self.G = nx.DiGraph()

        #ricorsione
        self.sol_ottimale = None
        self.peso_max = 0


    def get_date_range(self):
        return DAO.get_date_range()

    def get_category(self):
        categorie = DAO.read_all_category()
        return categorie

    def build_graph(self,categoria,first,last):
        self.prodotti = DAO.read_product(categoria)
        self.vendite = DAO.read_vendite(self.prodotti,first,last)

        self.G.clear()
        self.G.add_nodes_from(self.prodotti.values())

        for id_nodo,vendite1 in self.vendite:
            nodo = self.prodotti[id_nodo]
            for id_nodo2,vendite2 in self.vendite:
                nodo2= self.prodotti[id_nodo2]
                if nodo != nodo2:
                    peso = vendite1+vendite2
                    if vendite1>vendite2:
                        self.G.add_edge(nodo,nodo2,weight=peso)
                    elif vendite1<vendite2:
                        self.G.add_edge(nodo2,nodo,weight=peso)
                    elif vendite1==vendite2:
                        self.G.add_edge(nodo, nodo2,weight=peso)
                        self.G.add_edge(nodo2, nodo,weight=peso)

        return (len(self.G.nodes()),len(self.G.edges()))

    def più_venduti(self):

        lista_più_venduti = []
        for nodo in self.G.nodes():
            somma_uscenti = 0
            somma_entranti = 0
            entranti =  list(self.G.in_edges(nodo))
            uscenti = list(self.G.out_edges(nodo))

            for u,v in entranti:
                somma_entranti += self.G[u][v]['weight']

            for i,j in uscenti:
                somma_uscenti += self.G[i][j]['weight']

            lista_più_venduti.append((nodo,somma_uscenti-somma_entranti))
        lista_più_venduti = sorted(lista_più_venduti, key=itemgetter(1),reverse=True)

        return lista_più_venduti[:5]


    def ricerca_cammino(self,iniziale,finale,L):
        nodo_iniziale = self.prodotti[iniziale]
        nodo_finale = self.prodotti[finale]
        sol_parziale = [nodo_iniziale]
        peso_attuale = 0
        self.ricorsione(sol_parziale,peso_attuale,nodo_finale,L)
        return self.sol_ottimale,self.peso_max


    def ricorsione(self,sol_parziale,peso_attuale,finale,L):


        if len(sol_parziale)==L :
            if sol_parziale[-1]==finale and  peso_attuale > self.peso_max:
                self.sol_ottimale = copy.deepcopy(sol_parziale)
                self.peso_max = peso_attuale
            return

        ultimo = sol_parziale[-1]
        amissibili = self.trova_amissibili(ultimo, sol_parziale)

        for amissibile in amissibili:
            sol_parziale.append(amissibile)
            peso_attuale += self.G[ultimo][amissibile]['weight']
            self.ricorsione(sol_parziale,peso_attuale,finale,L)
            sol_parziale.pop()
            peso_attuale -= self.G[ultimo][amissibile]['weight']

    def trova_amissibili(self,ultimo,sol_parziale):

        vicini = self.G.successors(ultimo)
        validi= []
        for vicino in vicini:
            if vicino not in sol_parziale:
                validi.append(vicino)

        return validi

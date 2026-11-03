from database.DB_connect import get_connection
from model.strumento import Strumento
from model.prestito import Prestito

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        self._nome = nome
        self._responsabile = responsabile

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, responsabile):
        self._responsabile = responsabile

    def get_strumenti(self) -> list[Strumento] | None:
        """
            Funzione che legge tutti gli strumenti nel database
            :return: una lista con tutti gli strumenti presenti oppure None
        """

        lista_strumenti = []
        cnx = get_connection()
        #se la connessione non è andata a buon fine lancio un'eccezione che sarà gestita
        #nel blocco except delle funzioni che chiameranno qsta funzione
        if cnx is None:
            raise Exception("la connessione al database non è andata a buon fine!!")
        cursore = cnx.cursor(dictionary=True)
        query = """SELECT * FROM strumento"""
        cursore.execute(query)
        for row in cursore:
            strumento = Strumento(row["codice"], row["tipo"], row["marca"],
                                  row["anno_acquisto"], row["valore"], row["disponibile"])
            lista_strumenti.append(strumento)
        cursore.close()
        cnx.close()
        # se nel deposito non era presente nessuno strumento restituisco il valor None
        if lista_strumenti == []:
            return None
        return lista_strumenti



    def cerca_strumenti_per_tipo(self, tipo) -> list[Strumento] | None:
        """
            Funzione che recupera una lista con tutti gli strumenti presenti nel database di un certo tipo
            :param tipo: il tipo dello strumento (es. "Chitarra")
            :return: una lista con tutti gli strumenti del tipo indicato oppure None
        """
        strumenti_del_tipo = []
        cnx = get_connection()
        if cnx is None:
            raise Exception("la connessione al database non è andata a buon fine!!")
        cursore = cnx.cursor(dictionary=True)
        query = """SELECT * FROM strumento
                   WHERE `tipo`=%s """
        cursore.execute(query, (tipo,))
        for row in cursore:
            strumento = Strumento(row["codice"], row["tipo"], row["marca"],
                                  row["anno_acquisto"], row["valore"], row["disponibile"])
            strumenti_del_tipo.append(strumento)
        cursore.close()
        cnx.close()
        # se nessuno strumento di quel tipo è presente nel deposito restituisco il valor None
        if strumenti_del_tipo == []:
            return None
        return strumenti_del_tipo


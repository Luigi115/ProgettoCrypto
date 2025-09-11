from utilityBlocco import listaBlocchi,stampaListaBlocchi, listaBlocchiTotale, ultimoBlocco, stampaBlocco, stampaHeader,listaUltimiNBlocchi
from utilityTransazioni import getTransazioni, stampaTransazioni, dettagliTransazione, getCoinbase, getCoinbaseDaBlocchi
from utility import toBinary



#stampaMessaggiMinerSuFile(estraiMessaggiMiner(listaUltimiNBlocchi(500)))

stampaListaBlocchi(listaBlocchi(5))
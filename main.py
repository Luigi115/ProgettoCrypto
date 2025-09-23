from utilityBlocco import stampaListaBlocchi, listaBlocchiTotale, ultimoBlocco, stampaBlocco, stampaHeader, listaUltimiNBlocchi
from utilityTransazioni import getTransazioni, stampaTransazioni, getCoinbase, getCoinbaseDaBlocchi
from utility import toBinary
from utilityMinerMessage import estraiOpReturn, estraiOpReturnDaTransazioni,filtraOpReturnPerBlocco,stampaOpReturnPerBlocco, print_op_return_messages,collect_op_return_messages,categorize_messages,print_categorized_messages
from tqdm import tqdm

#print(filtraOpReturnPerBlocco(estraiOpReturnDaTransazioni(getCoinbaseDaBlocchi(listaUltimiNBlocchi(1)))))
#print("---------------------------------------------")
#print_op_return_messages(collect_op_return_messages(filtraOpReturnPerBlocco(estraiOpReturnDaTransazioni(getCoinbaseDaBlocchi(listaUltimiNBlocchi(10))))))
print_categorized_messages(categorize_messages(collect_op_return_messages(filtraOpReturnPerBlocco(estraiOpReturnDaTransazioni(getCoinbaseDaBlocchi(listaUltimiNBlocchi(5)))))))
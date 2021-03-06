# Download all pdf files from https://www.argentina.gob.ar/coronavirus/informe-diario
# The details are saved in info.log
# Last update time  is save in last_update.txt


from tqdm import tqdm
from bs4 import BeautifulSoup
import requests
from clint.textui import progress
import os, sys, platform, logging, time
import datetime
from shutil import copyfile




path='./informes/covid19-informediario/junio2020/'
log_archive='info.log'


if platform.platform().startswith('Windows'):
    log_file = os.path.join(os.getenv('HOMEDRIVE'), os.getenv("HOMEPATH"), log_archive)
    
else:
    #log_file = os.path.join(os.getenv('HOME'), log_archive')
     log_file = os.path.join(path, log_archive)
    

print('Archivo log en ', log_file + '\r\n')


logging.basicConfig(level=logging.INFO,                                     #log en cadad directorio
                    format='%(asctime)s : %(levelname)s : %(message)s',
                    filename = log_file,
                    filemode = 'a')


##logging.basicConfig(level=logging.INFO,                                     #log en cadad directorio
##                    format='%(asctime)s : %(levelname)s : %(message)s',
##                    filename = './informes/covid19-informediario/info.log', #log gral
##                    filemode = 'a')


#logger2 = logging.getLogger('log.gral')

logger = logging.getLogger(__name__)
fmt = '%(asctime)s : %(levelname)s : %(message)s'
formatter = logging.Formatter(fmt)
logger.setLevel(logging.INFO)

file_hander = logging.FileHandler('./informes/covid19-informediario/'+__name__+'.log', mode="a")
file_hander.setLevel(logging.INFO)
file_hander.setFormatter(formatter)
logger.addHandler(file_hander)


##log.setFormatter(formatter)




#logging.debug('Comienza el programa')
#logging.info('Procesando con normalidad')
#logging.warning('Advertencia')


url = "https://www.argentina.gob.ar/coronavirus/informe-diario/junio2020"
#url = "https://www.argentina.gob.ar/coronavirus/informe-diario/" # Cambiaron el directorio 
response = requests.get(url)
soup = BeautifulSoup(response.content,'html.parser')

boxList = soup.findAll('a',{'class':'btn btn-primary btn-sm'})
links = [box['href'] for box in boxList]



for x in range(0,len(links)):
    
    response = requests.get(links[x], stream=True)
    length = int(response.headers.get('content-length'))
    
    head, tail = os.path.split(links[x])
   
    print('Downloading... ' + head+'/'+tail)

 
    if not os.path.isfile(path+tail) or length != os.path.getsize(path+tail):
       
       logging.info("Archivo descargado: ./" + str(tail))
       logger.info("Archivo descargado: ./" + str(tail))                       

       with open(path+tail, "wb") as handle:       
           for data in tqdm(iterable=response.iter_content(chunk_size=1024), total=length/1024, unit='KB'):
               if data:
                   handle.write(data)
                   handle.flush()
               
    else:

        print('This file '+ tail +' already exists.\r\n')


timestamp = datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
with open(os.path.join(path,'last_update.txt'), 'w') as f:
    f.write('Last update on: {}'.format(timestamp))

copyfile(path + 'last_update.txt','./informes/covid19-informediario/last_update.txt')

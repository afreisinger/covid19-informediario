# Download all pdf files from https://www.argentina.gob.ar/coronavirus/informe-diario
# The details are saved in info.log


from tqdm import tqdm
from bs4 import BeautifulSoup
import requests
from clint.textui import progress
import os, sys, platform, logging, time
import datetime




path='./informes/covid19-informediario/'
log_archive='info.log'


if platform.platform().startswith('Windows'):
    log_file = os.path.join(os.getenv('HOMEDRIVE'), os.getenv("HOMEPATH"), log_archive)
    
else:
    #log_file = os.path.join(os.getenv('HOME'), log_archive')
     log_file = os.path.join(path, log_archive)
    

print('Archivo log en ', log_file + '\r\n')


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s : %(levelname)s : %(message)s',
                    filename = log_file,
                    filemode = 'a')

#logging.debug('Comienza el programa')
#logging.info('Procesando con normalidad')
#logging.warning('Advertencia')


url = "https://www.argentina.gob.ar/coronavirus/informe-diario/mayo2020"
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
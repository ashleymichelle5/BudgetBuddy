#comandos necesarios para contruir la aplicacion 

#!/usr/bin/env bash
set -o errexit #Salir en caso de error 

pip install -r requirements.txt #Instalar las librerias 

python3 manage.py collectstatic --no-input #Recoger archivos 

python3 manage.py migrate #Hacer migraciones 
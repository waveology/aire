
Este directorio contiene scripts Python correspondientes a los notebooks del repositorio.
La idea es que puedan ejecutarse localmente (en el editor Spyder, por ejemplo), en un entorno que contenga las extensiones (librerías) necesarias.
En esta modalidad, los datos estarían presentes localmente en el directorio 'datos'. Por eso, los scripts no tienen las instrucciones para la descarga que sí aparecen en los notebooks Jupyter.

***
Debido a diferencias entre versiones del software, los pasos a seguir pueden diferir ligeramente de los detalladas en este documento.
En caso de duda siempre viene bien contar con el soporte de algún informático
***

Hay varias formas de preparar el entorno Python para ejecutar estos scripts. 
Una posibilidad sencilla de llevar a cabo en Windows se describe a continuación:

1.- Instalamos el repositorio de paquetes miniconda que está disponible en https://docs.conda.io/en/latest/miniconda.html
     
     Podemos elegir entre dos versiones.
     
     La de 64 bits:
     https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
     
     y la de 32 bits:
     https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86.exe
     
     Para la instalación basta con descargar el correspondiente ejecutable, hacer click en el icono, seguir las instrucciones y esperar a que se complete el proceso.

2.- En Windows: 

       a) accedemos al botón de inicio (abajo a la izquierda)
       b) buscamos la aplicación recién instalada, que suele aparecer con el nombre "Anaconda". 
       c) hacemos click en el icono de color negro llamado "Anaconda prompt" o "Anaconda prompt (miniconda)"
       d) Se abrirá una ventana de fondo negro que es la consola de configuración de entornos conda.

3.- En la consola conda recién abierta haremos lo siguiente:

    a) Creamos un entorno conda llamado "aire" o cualquier otro nombre que nos parezca:
    
          conda create --name aire

    b) Activamos el entorno que acabamos de crear:
    
          conda activate aire

    c) Instalamos una tras otra las extensiones Python necesarias teclando "conda install" + nombre_extensión y pulsando return a continuación:
       
       El entorno de desarrollo (donde escribimos y ejecutamos nuestros programas):
       
          conda install spyder
          
       La extensión que permite usar tablas (dataframes) de datos:   
       
          conda install pandas
       
       Una extensión para hacer dibujos genéricos:
       
          conda install matplotlib
          
       Una extensión para operar numéricamente con vectores y matrices:   
       
          conda install numpy
      
      Una extensión para cálculo científico (estadística y más cosas):
      
          conda install scipy
          
      Una extension que permite hacer regresiones y ajustes de los datos (orientada a machine learning):    
      
          conda install scikit-lyearn

      Una vez completado el proceso podemos teclear "exit" para cerrar la consola.

4.- De nuevo en Windows:

      a) Click en el botón de inicio (abajo a la izquerda)
      b) Buscamos nuestra aplicación conda (suele aparecer como "Anaconda")
      c) Debería aparecer un icono del entorno Spyder
      d) Pulsando sobre él debería abrirse abre el entorno de desarrollo.
      e) Abrimos el script Python que nos interese y lo modificamos y ejecutamos a nuestro antojo.


5.- Existe un procedimiento automatizado para recrear el entorno con las extensiones. Desgraciadamente depende críticamente de las versiones del software presente en la computadora. Por esa razón lo hemos eliminado de este documento.



Antigua Guatemala,
Marzo 2023



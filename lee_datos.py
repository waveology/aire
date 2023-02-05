# -*- coding: utf-8 -*-

"""
Ernesto Barrera
v1.0
Enero 2023
"""

import pandas as pd


def ayuntamiento(ifile, codigo_magnitud=8, codigo_estacion=28079001) :

    # Listado de estaciones
    # ----------------------
    estalist = {
    # código       municipio nombre_estación    
    28079001 : ('Pº. Recoletos',                'Baja.- 04/05/2009 (14:00 h.)'),
    28079002 : ('Glta. de Carlos V',            'Baja.- 04/12/2006 (11:00 h.)'),
    28079003 : ('Pza. del Carmen',              ''),              
    28079035 : ('Pza. del Carmen',              'Código desde enero 2011'),
    28079004 : ('Pza. de España',               ''),
    28079005 : ('Barrio del Pilar',             ''), 
    28079039 : ('Barrio del Pilar',             'Código desde enero 2011'),
    28079006 : ('Pza. Dr. Marañón',             'Baja.- 27/11/2009 (08:00 h.)'),
    28079007 : ('Pza. M. de Salamanca',         'Baja.- 30/12/2009 (14:00 h.)'),
    28079008 : ('Escuelas Aguirre',             ''),
    28079009 : ('Pza. Luca de Tena',            'Baja.- 07/12/2009 (08:00 h.)'),
    28079010 : ('Cuatro Caminos',               ''),
    28079038 : ('Cuatro Caminos',               'Código desde enero 2011'),
    28079011 : ('Av. Ramón y Cajal',            ''),
    28079012 : ('Pza. Manuel Becerra',          'Baja.- 30/12/2009 (14:00 h.)'),
    28079013 : ('Vallecas',                     ''), 
    28079040 : ('Vallecas',                     'Código desde enero 2011'),
    28079014 : ('Pza. Fdez. Ladreda',           'Baja.- 02/12/2009 (09:00 h.)'),
    28079015 : ('Pza. Castilla',                'Baja.- 17/10/2008 (11:00 h.)'),
    28079016 : ('Arturo Soria',                 ''),
    28079017 : ('Villaverde Alto',              ''), 
    28079018 : ('C/ Farolillo',                 ''),
    28079019 : ('Huerta Castañeda',             'Baja.- 30/12/2009 (13:00 h.)'),
    28079020 : ('Moratalaz',                    ''),
    28079036 : ('Moratalaz',                    'Código desde enero 2011'),
    28079021 : ('Pza. Cristo Rey',              'Baja.- 04/12/2009 (14:00 h.)'),
    28079022 : ('Pº. Pontones',                 'Baja.- 20/11/2009 (10:00 h.)'),
    28079023 : ('Final C/ Alcalá',              'Baja.- 30/12/2009 (14:00 h.)'),
    28079024 : ('Casa de Campo',                ''),
    28079025 : ('Santa Eugenia',                'Baja.- 16/11/2009 (10:00 h.)'),
    28079026 : ('Urb. Embajada (Barajas)',      'Baja.- 11/01/2010 (09:00 h.)'),
    28079027 : ('Barajas',                      ''),
    28079047 : ('Méndez Álvaro',                'Alta.- 21/12/2009 (00:00 h.)'),
    28079048 : ('Pº. Castellana',               'Alta.- 01/06/2010 (00:00 h.)'),
    28079049 : ('Retiro',                       'Alta.- 01/01/2010 (00:00 h.)'),
    28079050 : ('Pza. Castilla',                'Alta.- 08/02/2010 (00:00 h.)'),
    28079054 : ('Ensanche Vallecas',            'Alta.- 11/12/2009 (00:00 h.)'),
    28079055 : ('Urb. Embajada (Barajas)',      'Alta.- 20/01/2010 (15:00 h.)'),
    28079056 : ('Plaza Elíptica',               'Alta.- 18/01/2010 (12:00 h.)'),
    28079057 : ('Sanchinarro',                  'Alta.- 24/11/2009 (00:00 h.)'),
    28079058 : ('El Pardo',                     'Alta.- 30/11/2009 (13:00 h.)'),
    28079059 : ('Parque Juan Carlos I',         'Alta.- 14/12/2009 (00:00 h.)'),
    28079086 : ('Tres Olivos',                  'Alta.- 14/01/2010 (13:00 h.)'), 
    28079060 : ('Tres Olivos',                  'Código desde enero 2011'),    
    }
    
    # Listado de magnitudes
    # ---------------------
    maglist = {
    # código     magnitud         unidades    
    1 	:  ('Dióxido de azufre', 'μg/m³'),
    6 	:  ('Monóxido de carbono', 'mg/m³'),
    7 	:  ('Monóxido de nitrógeno', 'μg/m³'),
    8 	:  ('Dióxido de nitrógeno', 'μg/m³'),
    9 	:  ('Partículas en suspensión < PM2.5', 'μg/m³'),
    10 	:  ('Partículas en suspensión < PM10',  'μg/m³'),
    12 	:  ('Óxidos de nitrógeno', 'μg/m³'),
    14 	:  ('Ozono', 'μg/m³'),
    20 	:  ('Tolueno', 'μg/m³'),
    30 	:  ('Benceno', 'μg/m³'),    
    35  :  ('Etilbenceno', 'μg/m³'),
    37  :  ('Metaxileno', 'μg/m³'),
    38  :  ('Paraxileno', 'μg/m³'),
    39  :  ('Ortoxileno', 'μg/m³'),
    42 	:  ('Hidrocarburos totales', 'mg/m³'),
    43  :  ('Metano', 'mg/m³'),
    44  :  ('Hidrocarburos no metánicos', 'mg/m³')    
    }
    

    # Lectura de datos
    # -------------------------------------------
    df = pd.read_csv(ifile,sep=';')
    
    # Selección de estación y contaminante
    # --------------------------------------
    df = df[ (df['ESTACION'] == int(str(codigo_estacion)[-3:])) 
           & (df['MAGNITUD'] == codigo_magnitud) ]

    
    # Eliminamos información innecesaria
    # -----------------------------------------
    df = df.drop(columns=['PROVINCIA','MUNICIPIO',
                          'ESTACION','PUNTO_MUESTREO','MAGNITUD'])
    
    # Pasamos los días de columnas a filas con
    # el contaminante como valor
    # -----------------------------------------
    df1 = df.melt(id_vars=['ANO','MES'],
                 value_vars = [ 'D%02d' % i for i in range(1,32)],
                 var_name='DIA',
                 value_name='valor',  
                 )
    
    # Convertimos el día a valor numérico
    # --------------------------------------------------
    df1['DIA'] = df1['DIA'].apply(lambda x : int(x[1:]))
    
    
    # Pasamos los días de columnas a filas con
    # el flag de calidad como valor
    # -----------------------------------------
    df2 = df.melt(id_vars=['ANO','MES'],
                 value_vars = [ 'V%02d' % i for i in range(1,32)],
                 var_name='DIA',
                 value_name='FLAG',  
                 )
    
    # Convertimos el día a valor numérico
    # --------------------------------------------------
    df2['DIA'] = df2['DIA'].apply(lambda x : int(x[1:]))
    
    # Combinamos filas de columnas iguales
    # --------------------------------------------
    df = df1.merge(df2)
    
    # Retenemos solo valores válidos
    # -----------------------------------------------
    df = df[df['FLAG'] == 'V'].drop(columns='FLAG')
    
    # Generamos una fecha a partir de las columnas
    # -----------------------------------------------
    df['fecha'] = pd.to_datetime({'year':df.ANO,'month':df.MES,'day':df.DIA})
    
    # Eliminamos colunas innecesarias
    # -------------------------------------
    df = df.drop(columns=['ANO','MES','DIA'])

    return df, *maglist[codigo_magnitud], estalist[codigo_estacion][1]


def comunidad(ifile, codigo_magnitud=8, codigo_estacion=28067001) :

    # Listado de magnitudes
    # ---------------------
    maglist = {
    # código     magnitud         unidades    
    1 	:  ('Dióxido de azufre', 'μg/m³'),
    6 	:  ('Monóxido de carbono', 'mg/m³'),
    7 	:  ('Monóxido de nitrógeno', 'μg/m³'),
    8 	:  ('Dióxido de nitrógeno', 'μg/m³'),
    9 	:  ('Partículas en suspensión < PM2.5', 'μg/m³'),
    10 	:  ('Partículas en suspensión < PM10',  'μg/m³'),
    12 	:  ('Óxidos de nitrógeno', 'μg/m³'),
    14 	:  ('Ozono', 'μg/m³'),
    20 	:  ('Tolueno', 'μg/m³'),
    22 	:  ('Black Carbon', 'μg/m³'),
    30 	:  ('Benceno', 'μg/m³'),
    42 	:  ('Hidrocarburos totales', 'mg/m³'),
    44 	:  ('Hidrocarburos no metánicos', 'mg/m³'),
    431 :  ('MetaParaXileno', 'μg/m³')
    }
    
    
        
    # Listado de estaciones
    # ----------------------
    estalist = {
    # código       municipio nombre_estación    
    28005002   :    (  5,  'ALCALÁ DE HENARES'), 
    28006004   :    (  6,  'ALCOBENDAS'), 
    28007004   :    (  7,  'ALCORCÓN'), 
    28009001   :	(  9,  'ALGETE'), 
    28013002   :	( 13,  'ARANJUEZ'), 
    28014002   :	( 14,  'ARGANDA DEL REY'),
    28016001   :	( 16,  'EL ATAZAR'),
    28045002   :	( 45,  'COLMENAR VIEJO'), 
    28047002   :	( 47,  'COLLADO VILLALB A'), 
    28049003   :	( 49,  'COSLADA'), 
    28058004   :	( 58,  'FUENLABRADA'), 
    28065014   :	( 65,  'GETAFE'), 
    28067001   :	( 67,  'GUADALIX DE LA SIERRA'), 
    28074007   :	( 74,  'LEGANÉS'), 
    28080003   :	( 80,  'MAJADAHONDA'), 
    28092005   :	( 92,  'MÓSTOLES'), 
    28102001   :	(102,  'ORUSCO DE TAJUÑA'), 
    28120001   : 	(120,  'PUERTO DE COTOS'), 
    28123002   :	(123,  'RIVAS-VACIAMADRID'), 
    28133002   :	(133,  'SAN MARTÍN DE VALDEIGLESIAS'), 
    28148004   :	(148,  'TORREJÓN DE ARDOZ'), 
    28161001   :	(161,  'VALDEMORO'), 
    28171001   :	(171,  'VILLA DEL PRADO'), 
    28180001   :	(180,  'VILLAREJO DE SALVANÉS')
    }

    
    # Lectura de datos
    # -------------------------------------------
    df = pd.read_csv(ifile,sep=';', decimal=',')
    
    # Selección de estación y contaminante
    # --------------------------------------
    df = df[ (df['estacion']  == int(str(codigo_estacion)[-3:])) 
           & (df['magnitud']  == codigo_magnitud) 
           & (df['municipio'] == estalist[codigo_estacion][0])]

    
    # Tamaño de la muestra
    # -------------------------
    print(' -Info: encontrados datos de %d días' % len(df))
    
    # Eliminamos información innecesaria
    # -----------------------------------------
    df = df.drop(columns=['provincia','municipio',
                          'estacion','punto_muestreo','magnitud'])
    
    # Pasamos los días de columnas a filas con
    # el contaminante como valor
    # -----------------------------------------
    df1 = df.melt(id_vars=['ano','mes','dia'],
                 value_vars = [ 'h%02d' % i for i in range(1,25)],
                 var_name='hora',
                 value_name='valor',  
                 )
    
    
    # Convertimos la hora a valor numérico
    # --------------------------------------------------
    df1['hora'] = df1['hora'].apply(lambda x : int(x[1:]))
    
 
    # Pasamos los días de columnas a filas con
    # el flag de calidad como valor
    # -----------------------------------------
    df2 = df.melt(id_vars=['ano','mes','dia'],
                 value_vars = [ 'v%02d' % i for i in range(1,25)],
                 var_name='hora',
                 value_name='flag',  
                 )
    
    # Convertimos el día a valor numérico
    # --------------------------------------------------
    df2['hora'] = df2['hora'].apply(lambda x : int(x[1:]))
    
    # Combinamos filas de columnas iguales
    # --------------------------------------------
    df = df1.merge(df2)
    
    # Retenemos solo valores válidos
    # -----------------------------------------------
    df = df[df['flag'] == 'V'].drop(columns='flag')
    
    # Generamos una fecha a partir de las columnas
    # -----------------------------------------------
    df['fecha'] = pd.to_datetime({'year':df.ano,'month':df.mes,'day':df.dia,'hour':df.hora})
    
    # Eliminamos colunas innecesarias
    # -------------------------------------
    df = df.drop(columns=['ano','mes','dia','hora'])

    return df, *maglist[codigo_magnitud], estalist[codigo_estacion][1]



def meteo(ifile, codigo_magnitud=83, codigo_estacion=28067001) :

    # Listado de estaciones
    # ----------------------
    estalist = {
    # código       municipio nombre_estación    
    28005002   :    (  5,  'ALCALÁ DE HENARES'), 
    28006004   :    (  6,  'ALCOBENDAS'), 
    28007004   :    (  7,  'ALCORCÓN'), 
    28009001   :	(  9,  'ALGETE'), 
    28013002   :	( 13,  'ARANJUEZ'), 
    28014002   :	( 14,  'ARGANDA DEL REY'),
    28016001   :	( 16,  'EL ATAZAR'),
    28045002   :	( 45,  'COLMENAR VIEJO'), 
    28047002   :	( 47,  'COLLADO VILLALB A'), 
    28049003   :	( 49,  'COSLADA'), 
    28058004   :	( 58,  'FUENLABRADA'), 
    28065014   :	( 65,  'GETAFE'), 
    28067001   :	( 67,  'GUADALIX DE LA SIERRA'), 
    28074007   :	( 74,  'LEGANÉS'), 
    28080003   :	( 80,  'MAJADAHONDA'), 
    28092005   :	( 92,  'MÓSTOLES'), 
    28102001   :	(102,  'ORUSCO DE TAJUÑA'), 
    28120001   : 	(120,  'PUERTO DE COTOS'), 
    28123002   :	(123,  'RIVAS-VACIAMADRID'), 
    28133002   :	(133,  'SAN MARTÍN DE VALDEIGLESIAS'), 
    28148004   :	(148,  'TORREJÓN DE ARDOZ'), 
    28161001   :	(161,  'VALDEMORO'), 
    28171001   :	(171,  'VILLA DEL PRADO'), 
    28180001   :	(180,  'VILLAREJO DE SALVANÉS')
    }
    
    # Listado de magnitudes
    # ---------------------
    maglist = {
    # código     magnitud                unidades    
    81 :	('Velocidad del viento',     'm/s'), 
    82 :	('Dirección del viento',     'º'), 
    83 :	('Temperatura',              'ºC'), 
    86 :	('Humedad relativa',         '%'), 
    87 :	('Presión atmosférica',      'hPa'), 
    88 :	('Radiación solar',          'W/m2'), 
    89 :	('Precipitación',            'mm')
    }


    # Lectura de datos
    # -------------------------------------------
    df = pd.read_csv(ifile,sep=';', decimal='.')
    
    # Selección de estación y contaminante
    # --------------------------------------
    df = df[ (df['estacion']  == int(str(codigo_estacion)[-3:])) 
           & (df['magnitud']  == codigo_magnitud) 
           & (df['municipio'] == estalist[codigo_estacion][0])]
    
    # Tamaño de la muestra
    # -------------------------
    print(' -Info: encontrados datos de %d días' % len(df))
    
    # Eliminamos información innecesaria
    # -----------------------------------------
    df = df.drop(columns=['provincia','municipio',
                          'estacion','punto_muestreo','magnitud'])
    
    # Pasamos los días de columnas a filas con
    # el contaminante como valor
    # -----------------------------------------
    df1 = df.melt(id_vars=['ano','mes','dia'],
                 value_vars = [ 'h%02d' % i for i in range(1,25)],
                 var_name='hora',
                 value_name='valor',  
                 )
    
    
    # Convertimos la hora a valor numérico
    # --------------------------------------------------
    df1['hora'] = df1['hora'].apply(lambda x : int(x[1:]))
    
 
    # Pasamos los días de columnas a filas con
    # el flag de calidad como valor
    # -----------------------------------------
    df2 = df.melt(id_vars=['ano','mes','dia'],
                 value_vars = [ 'v%02d' % i for i in range(1,25)],
                 var_name='hora',
                 value_name='flag',  
                 )
    
    # Convertimos el día a valor numérico
    # --------------------------------------------------
    df2['hora'] = df2['hora'].apply(lambda x : int(x[1:]))
    
    # Combinamos filas de columnas iguales
    # --------------------------------------------
    df = df1.merge(df2)
    
    # Retenemos solo valores válidos
    # -----------------------------------------------
    df = df[df['flag'] == 'V'].drop(columns='flag')
    
    # Generamos una fecha a partir de las columnas
    # -----------------------------------------------
    df['fecha'] = pd.to_datetime({'year':df.ano,'month':df.mes,'day':df.dia,'hour':df.hora})
    
    # Eliminamos colunas innecesarias
    # -------------------------------------
    df = df.drop(columns=['ano','mes','dia','hora'])

    return df, *maglist[codigo_magnitud], estalist[codigo_estacion][1]




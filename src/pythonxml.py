import os
import xml.etree.ElementTree as ET

BRANCH_A_BUSCAR = 'v_20230331'
TIPO_OBJETO_A_BUSCAR = 'DataSource'
RUTA_DE_LOS_XMLS = '..\\formato'

for root, dirs, files in os.walk(RUTA_DE_LOS_XMLS):
    if TIPO_OBJETO_A_BUSCAR in dirs and BRANCH_A_BUSCAR in root:
        ruta_con_datasources = root+"\\DataSource"
        lista_archivos_en_ruta = os.listdir(root+"\\DataSource")
        print("## DATASOURCES ENCONTRADOS EN LA RUTA ", root)
        print("LISTA DATASOURCE EN RUTA :")
        print(lista_archivos_en_ruta)
        for archivo in lista_archivos_en_ruta:
            if archivo.endswith('.xml'):
                # Construir ruta completa del archivo
                file_path=ruta_con_datasources+"\\"+archivo
                # Procesar el archivo XML capturando el error
                try:
                    tree = ET.parse(file_path)
                    root_xml = tree.getroot()
                    # Buscar todas las etiquetas <name> y extraer su texto
                    nombreDS = root_xml.find(".//property[@name='name']").get('value')
                    if nombreDS :
                        print(f"\n--NOMBRE DATASOURCE : {nombreDS}")
                    else:
                        print("Etiqueta <property> encontrada, pero falta información en los atributos.")

                    for obj in root_xml.findall(".//object[@type='DataSource:field']"):
                        name_property = obj.find(".//property[@name='name']")
                        type_property = obj.find(".//property[@name='type']")
                        if name_property is not None:
                            nombre_campo = name_property.get('value')
                            tipo_campo = type_property.get('value')
                            print(f"----Nombre campo {nombre_campo} y el tipo {tipo_campo}")
                
                except ET.ParseError as e:
                    print(f"Error al procesar el archivo {archivo}: {e}")
        print("####################################################\n")
import xml.etree.ElementTree as ET
import sys
import re

class ProcessXML:
    def __init__(self):
        self.file_path = None

    def process_xml_file(self, file_path):        
        datafinal = []
        tree=ET.parse(file_path)
        root_xml=tree.getroot()
        nombre_ds=root_xml.find(".//property[@name='name']").get('value')
        project=file_path.split('/')[4]
        if nombre_ds:
            dataconsol = {'nombreDS':nombre_ds,'nombreCampo':'','tipoDeDato':'','longitud':'','id_campo':'', 'Proyecto Contenedor':project}
        else:
            print("Etiqueta <property> encontrada, pero falta información en los atributos.")
            return []
        print(f'Procesando DataSource {file_path}', file=sys.stdout)
        for obj in root_xml.findall(".//object[@type='DataSource:field']"):
            name_property = obj.find(".//property[@name='name']")
            type_property = obj.find(".//property[@name='type']")
            id_propery=obj.find(".//property[@name='id']")
            if name_property is not None:
                nombre_campo = name_property.get('value')
                tipo_campo = type_property.get('value')
                id_campo=id_propery.get('value')
                if tipo_campo=="VARCHAR":
                    size_property = obj.find(".//property[@name='size']")
                    size_campo = int(size_property.get('value'))
                else:
                    size_campo = 0

                dataconsol=dataconsol.copy()
                dataconsol['nombreCampo'] = nombre_campo
                dataconsol['tipoDeDato'] = tipo_campo
                dataconsol['longitud'] = size_campo
                dataconsol['id_campo'] = id_campo
                datafinal.append(dataconsol)

        return datafinal
    
    def process_xml_file_agg(self, file_path):        
        datafinal = []
        tree=ET.parse(file_path)
        root_xml=tree.getroot()
        nombre_obj=root_xml.find(".//property[@name='name']").get('value')
        tipo_objeto=root_xml.attrib['type']
        if nombre_obj:
            #dataconsol = {'nombreAGG':nombre_agg,'nombreCampo':'','tipoDeDato':'','longitud':'','Proyecto Contenedor':'','Branch':''}
            dataconsol = {'nombre_obj':nombre_obj,'tipo_obj':tipo_objeto,'nombreCampo':'','id_campo':''}
        else:
            print("Etiqueta <property> encontrada, pero falta información en los atributos.")
            return []
        
        if tipo_objeto in('Aggregation', 'Portfolio'):
            print(f'Procesando archivo {file_path}', file=sys.stdout)
            for obj in root_xml.findall(".//object[@type='DataModel:fieldReference']"):
                for fieldref in obj:
                    largo_url=len(str(fieldref.text).split('.'))
                    url=str(fieldref.text).split('.')[largo_url-1]
                    nombre_campo=re.findall(r'["\'](.*?)["\']', url)[0]
                    id_campo=re.findall(r'\{(.*?)\}', url)[0]
                    dataconsol=dataconsol.copy()
                    if id_campo not in dataconsol['id_campo']:
                        dataconsol['id_campo'] = id_campo
                        dataconsol['nombreCampo'] = nombre_campo
                        datafinal.append(dataconsol) 

        # elif tipo_objeto=='Portfolio':
        #     print(f'Procesando Portfolio {file_path}', file=sys.stdout)
        #     for obj in root_xml.findall(".//object[@type='DataModel:fieldReference']"):            
        #         for fieldref in obj:
        #             largo_url=len(str(fieldref.text).split('.'))
        #             url=str(fieldref.text).split('.')[largo_url-1]
        #             #url=str(fieldref.text).split('.')[3]
        #             nombre_campo=re.findall(r'["\'](.*?)["\']', url)[0]
        #             id_campo=re.findall(r'\{(.*?)\}', url)[0]
        #             dataconsol=dataconsol.copy()
        #             if id_campo not in dataconsol['id_campo']:                    
        #                 dataconsol['id_campo'] = id_campo
        #                 dataconsol['nombreCampo'] = nombre_campo
        #                 datafinal.append(dataconsol)                    

        return datafinal
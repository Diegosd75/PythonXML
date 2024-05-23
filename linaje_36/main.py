import pandas as pd
import sys
import read_path
import process_xml
import execute_export
import argparse
import zipfile

argparser = argparse.ArgumentParser(description='Procesa archivos XML')
argparser.add_argument('-p', '--project', help='Proyecto a procesar', required=True)
argparser.add_argument('-b', '--branch', help='Branch a procesar', required=True)
argparser.add_argument('-w', '--wf', help='Workflow a procesar', required=True)
args = argparser.parse_args()
project = args.project
branch = args.branch
wf_name = args.wf

def main(project, branch, obj_name):
    print(f'Leyendo path ./formato/{project}', file=sys.stdout)
    rp = read_path.ReadPath(f'./formato/{project}', '.xml')
    pxml = process_xml.ProcessXML()
    datafinal = []
    
    if obj_name == 'DataSource':
        print('Procesando XMLs de los DataSources...', file=sys.stdout)
        for file_path in rp.read(branch):            
            datafinal.extend(pxml.process_xml_file(file_path))

    elif obj_name == 'Aggregation':
        print('Procesando XMLs de las Agregaciones y Portfolios...', file=sys.stdout)
        for file_path in rp.read_agg(project, branch):
            datafinal.extend(pxml.process_xml_file_agg(file_path))
    
    return datafinal
if __name__ == "__main__":
    try:
        #print('Ejecutando API export...', file=sys.stdout)
        #execute_export.run_process(project,branch,wf_name)
        
        print('Descomprimiendo export...', file=sys.stdout)
        with zipfile.ZipFile(f'./export_{project}_{branch}.zip', 'r') as zip_ref:
            zip_ref.extractall(f'./formato/{project}')

        print('Generando data de los DataSources...', file=sys.stdout)
        datafinal=main(project, branch, 'DataSource')
        df = pd.DataFrame(datafinal)
        df.drop_duplicates(inplace=True)
        df.to_excel(f'./Fuentes_{project}_{branch}.xlsx', index=False)

        print('Generando data de las Agregaciones...', file=sys.stdout)
        datafinal_agg=main(project, branch, 'Aggregation')
        df_agg = pd.DataFrame(datafinal_agg)
        df_agg.drop_duplicates(inplace=True)
        df_agg.to_excel(f'./Campos_Agg_{project}_{branch}.xlsx', index=False)

        df_join=pd.merge(df, df_agg, how='inner', on='id_campo')
        df_join.drop(columns=['id_campo','nombreCampo_y'], inplace=True)
        df_join.to_excel(f'./Fuentes_{project}_{branch}_Join.xlsx', index=False)
        df_pivot=pd.pivot_table(df_join, values='longitud', index='nombreCampo_x', columns='nombre_obj', aggfunc='count').reset_index()

        for col in df_pivot.columns:
            if col != 'nombreCampo_x':
                df_pivot[col]=df_pivot[col].apply(lambda x: 'X' if x>0 else '')
                
        df_pivot.to_excel(f'./Pivot_{project}_{branch}.xlsx', index=False)
        print("Proceso finalizado correctamente.")

    except Exception as ex:
        print(f"Error: {ex}", file=sys.stderr)
        sys.exit(1)
import os


for root, dirs, files in os.walk('C:/REPOSITORIOS/PythonXML'):
    #print(root)
    if 'DataSource' in root:
        full_path = os.path.join(root)
        if 'v_20230331' in full_path:
            print(full_path)
            print(os.listdir(full_path))
            print("#############################################################")

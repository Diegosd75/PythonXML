import rsa
import requests
from requests.adapters import HTTPAdapter, Retry
import json
import sys
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

url='https://controllerview.bancolombia.corp:8443/cv'

def get_hdrs():
   '''

    Returns
    -------
    hdrs : Dictionary
        Headers con la autenticación para la petición.

    '''
   hdrs={'content-type':'text/xml',
            'directoryname':'LDAP',
            'username':get_user(),
            'password':get_password(),
            'Accept':'application/json'}
   return hdrs

def get_password():
    """Función para decodificar la contraseña del usuario de red

    Returns:
        password (string): contraseña desencriptada
    """
    try:
        with open('./Pass/privKey.txt') as f:
        #with open('/opt/axiom/certificados/privKey.txt') as f:
            private_key_reloaded = rsa.PrivateKey.load_pkcs1(f.read().encode('utf8'))
        with open('./Pass/pass.txt','rb') as f:
       #with open('/opt/axiom/certificados/pass.txt','rb') as f:
            password=rsa.decrypt(f.read(),private_key_reloaded).decode('utf8')
    except Exception as ex:
        raise FileExistsError('Error al obtener la contraseña: ',str(ex))

    return password

def get_user():
    """Función para obtener el usuario de red

    Returns:
        user (String): Nombre de usuario
    """
    try:        
        with open('./Pass/user.txt') as f:
        #with open('/opt/axiom/certificados/user.txt') as f:
            user=f.read()
    except Exception as ex:
        raise FileExistsError('Error al obtener el usuario: ',str(ex))

    return user

def create_request_body(project,branch,wf_name):
    """Función para generar el Body de la petición

    Args:
        project (String): Proyecto que contiene el WF ejecutar
        branch (String): Branch que contiene el WF a ejecutar
        asof_date (String): As Of Date de la ejecución
        name (String): Nombre del WF a ejecutar
        variables (String): Variables de ejecución del WF

    Returns:
        Body(String): Body para ser usado en la petición
    """    
    
    body=f'''
        <object type="ExportSpec" version="1.0">
    <property name="onlyValidObjects" value="true" valueType="boolean"/>
	<property name="components" valueType="table">
		<object type="ExportSpec:branchObjectComponent" version="1.0">
			<property name="projectName" value="{project}" valueType="string"/>
			<property name="branchName" value="{branch}" valueType="string"/>
			<property name="objectType" value="WorkFlow" valueType="string"/>
			<property name="objectName" value="{wf_name}" valueType="string"/>
            <property name="includeComponents" value="NONE" valueType="string"/>
            <property name="includeDependencies" value="ALL_BRANCHES" valueType="string"/>
		</object>
	</property>
</object>
            '''
    return body

def fn_start_task(body,project, branch):
    '''
    Parameters
    ----------
    body : String
        Body en XML de la petición para iniciar ejecución de WF.

    Returns
    -------
    taskId : String
        ID de la tarea y la Branch resultante de la ejecución.

    '''
    try:
        print('Iniciando API startExport', file=sys.stdout)
        link=f'{url}/rest/global/framework/startExport'
        headers=get_hdrs()
        session=requests.Session()
        retry=Retry(connect=5, backoff_factor=1)
        adapter=HTTPAdapter(max_retries=retry)
        session.mount('https://', adapter)
        r=session.post(link,body,headers=headers,verify=True)
        content_type=r.headers.get('content-type')
        response_status=False
        if content_type=='application/json':                
            response=json.loads(r.content)
            rs = response.get('PROPERTIES').get('responseStatus').get('value')
            rm = response.get('PROPERTIES').get('responseMessage').get('value')
            if rs==-1:
                raise ConnectionError(f'{rm}')
        elif content_type=='application/zip':
            print('Guardando export en la ruta...', file=sys.stdout)
            with open(f'./export_{project}_{branch}.zip','wb') as f:
                f.write(r.content)
            response_status=True

        return response_status
    
    except Exception as e:
        raise ConnectionError(f'{str(e)}')

def run_process(project_name,branch_name,wf_name):
    print('runProcess', file=sys.stdout)
    '''

    Parameters
    ----------
    project_name : string
        Proyecto que se va a exportar.
    branch_name : string
        Branch que se va a exportar.    
    
    Returns
    -------
    None
    '''            
    try:
        print('Creando body para el request...', file=sys.stdout)
        body=create_request_body(project_name,branch_name, wf_name)
        print('Iniciando tarea de export...', file=sys.stdout)
        response_status=fn_start_task(body,project_name,branch_name)
        if response_status:            
            print('Tarea finalizada con exito...', file=sys.stdout)
        else:
            raise RuntimeError('Tarea fallida')

    except Exception as ex:
        raise ConnectionError(f'{str(ex)}')
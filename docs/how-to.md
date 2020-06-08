# TP Redes

### Instalacion
- [Instalar Docker](https://docs.docker.com/engine/install/)
- [Instalar Kubernetes](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [Instalar kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)
- Descargar el [repositorio](https://github.com/alavarello/tp-redes)
```sh
git clone git@github.com:alavarello/tp-redes.git
```
### Pasos a seguir

Todos estos comandos se corren desde la carpeta inicial del repositorio
**Nota:** Agregar nota de como correr kind ./../
##### 1) Iniciar el cluster usando kind

Kind levanta nodos en docker. Usando el archivo **cluster.yml** podemos configurar como se estructura el cluster. Hay dos tipos de nodos: masters y workers.

```sh
# Para levantar el cluster
kind create cluster --config cluster.yml
# Para ver los contextos (el cluster deberia estar en el contexto kind-kind)
kubectl config get-contexts
```
 ##### 2) Levantar el dashboard
El dashboard sive para administrar y visualizar el cluster de Kubernetes de una mejor manera.
```sh
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.1/aio/deploy/recommended.yaml
# Crear permisos
kubectl create -f dashboard/config.yml
# Generar token y copiarlo para poder hacer login
kubectl -n kubernetes-dashboard describe secret $(kubectl -n kubernetes-dashboard get secret | grep admin-user | awk '{print $1}')
# Ejecutar en otra terminal o correrlo como un subproceso
kubectl proxy
```

Al correr el ultimo comando entrar [aqui](http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/login) y pegar el token

 ##### 3) Deployar la version alpha de la API

 La version alpha de la API se puede encontrar como una imagen de docker `alavarello/test-api:alpha`

 ```sh
# Primero se deployan los servicios
kubectl apply -f deployments/services.yml
# Despues se deploya la version alpha de la API
kubectl apply -f deployments/alpha.yml
```

 ##### 3) Levantar una base de datos local

Levantamos una base de datos postgresql en un docker. Este contenedor llamado **database** esta en la misma red (**kind**) que los nodos del cluster. De esta manera el cluster se puede comunicar con el servidor de la base de datos. La base de datos de portgres que se crea se llama **postgres** con un usuario **postgres** y contraseña **123456**

```sh
docker container run --network=kind --name database -e POSTGRES_PASSWORD=123456 -d postgres

```

 ##### 4) Creamos un host en la red para acceder a la API

Creamos una contenedor de docker dentro de la red **kind** para poder acceder mediante curl a la API. Este contenedor es efimero, cuando se cierre el programa bash se destruye el contenedor. El contenedor esta basado en una imagen que tiene ubuntu y curl

 ```sh
docker container run -it --network=kind alavarello/custom-curl
```

 ###### 4.1) Comandos curl

Si la base de datos es nueva, entonces es necesario aplicar las migraciones usando el endpoint de **/admin**. Este comando se deberia correr una sola vez en la prueba.

 ```sh
curl --data "secret=123456&migrate=true" kind-worker:32333/admin/
```

Para obtener los estudiantes o crearlos

 ```sh
# GET para obtener todos los estudiantes
curl kind-worker:32333/students/
# POST para crear un estudiante
curl --data "username=sebas&email=sabas@redes.com" kind-worker:32333/students/
```

 ##### 5) Subir la version beta de la API
Para la version beta de la API usamos la imagen de docker `alavarello/test-api:beta` que tiene unos cambios sobre como representar un estudiante.

```sh
# Subimos algunos Pods de la version beta y bajamos la cantidad de Pods de la version alpha
kubectl apply -f deployments/beta-canary.yml
# Subimos la cantidad total de nodos que queremos de la version beta
kubectl apply -f deployments/beta.yml
# Borramos el deployment de alpha
kubectl delete deployments alpha
```

**Nota:** Despues de correr el primer comando se pueden apreciar las dos API conviviendo en el cluster

 #### 6) Pruebas extras

 Algunos comandos extra que se corrieron en las pruebas

 ```sh
# Para detener el funcionamiento de un nodo
docker stop kind-worker
# Levantar el nodo que detuvimos anteriormente
docker start kind-worker
# Obtener los Pods corriendo
kubectl get pods
# Borrar un pod
kubectl delete pods  <pod> # Replazar <pod> por el nombre del Pod
```

 #### 7) Para finalizar

Para terminar y eliminar todo lo que se uso en la prueba

 ```sh
# Para borrar el cluster
kind delete cluster
# Eliminar la base de datos
docker rm -f database
```

**Nota**: El nodo que se uso para hacer los curls se remueve cuando se sale de la terminal.

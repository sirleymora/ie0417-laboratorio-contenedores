# Parte 8: Limpieza del ambiente

## Objetivo

Aprender a revisar y limpiar los contenedores, imágenes, volúmenes y redes que ya no se utilizan, para no acumular recursos innecesarios en Docker.

---

## Estado inicial: qué recursos quedaron creados

Antes de limpiar, revisé qué había en el sistema con cuatro comandos de listado.

### Contenedores: `docker ps -a`

```powershell
docker ps -a
```

```text
CONTAINER ID   IMAGE                   COMMAND           CREATED        STATUS                    PORTS     NAMES
f0c2e82db91d   laboratorio-flask:1.0   "python app.py"   6 hours ago    Exited (0) 6 hours ago              app-bind
317a494e04f4   ubuntu                  "bash"            32 hours ago   Exited (0) 31 hours ago             musing_shamir
fd0fcc96cf60   hello-world             "/hello"          32 hours ago   Exited (0) 31 hours ago             magical_sammet
```

Quedaban tres contenedores, todos detenidos (`Exited (0)`): `app-bind` (de la prueba de bind mounts) y dos contenedores con nombre aleatorio de las primeras partes, `musing_shamir` (Ubuntu) y `magical_sammet` (`hello-world`), que creé sin usar `--name`. Ninguno estaba en ejecución, pero seguían ocupando espacio y sus nombres.

### Imágenes: `docker images`

```powershell
docker images
```

```text
IMAGE                 ID             DISK USAGE
hello-world:latest    5e2309035332       25.9kB
laboratorio-flask:1.0 50554302642f        222MB
nginx:latest          abe47724e466        242MB
redis:latest          8aee6591ee8c        213MB
ubuntu:latest         f144425ff09b        162MB
```

Había cinco imágenes: las que descargué de Docker Hub (`hello-world`, `ubuntu`, `nginx` y `redis`) y la que construí yo (`laboratorio-flask:1.0`).

### Volúmenes: `docker volume ls`

```powershell
docker volume ls
```

```text
DRIVER    VOLUME NAME
local     datos-lab
```

Quedaba el volumen `datos-lab`, creado en la parte de volúmenes.

### Redes: `docker network ls`

```powershell
docker network ls
```

```text
NETWORK ID     NAME      DRIVER    SCOPE
2d03c3f294cd   bridge    bridge    local
df9ef500e2b5   host      host      local
5dec381846bf   none      null      local
```

Solo aparecían las tres redes que Docker trae por defecto. Las redes `red-lab` y `red-app` ya las había eliminado al final de las partes de redes con `docker network rm`.

---

## Comandos de limpieza ejecutados

### `docker container prune`

```powershell
docker container prune
```

#### Explicación

Elimina **todos los contenedores detenidos**. Antes de hacerlo pide confirmación.

#### Resultado obtenido

```text
WARNING! This will remove all stopped containers.
Are you sure you want to continue? [y/N] y
Deleted Containers:
f0c2e82db91d29cd84b6fed691fb056b1fad5f115ec704e47e232ad7b6990a2e
317a494e04f47d95bce69c2dd4e172975d9ba736fddca1c367244c3deebeac38
fd0fcc96cf60507a5624b77a761312c241e2cb37ae6ec280955d3e991ef7387c

Total reclaimed space: 217.1kB
```

#### Qué observé

Eliminó los tres contenedores que vi en `docker ps -a` y liberó solo 217.1 kB, porque un contenedor detenido ocupa muy poco; lo que pesa son las imágenes.

### `docker image prune`

```powershell
docker image prune
```

#### Explicación

Elimina las imágenes **colgantes** (*dangling*), es decir, las que no tienen nombre ni etiqueta y no están asociadas a ningún contenedor (suelen ser restos de construcciones anteriores). No elimina imágenes con nombre, como `ubuntu` o `laboratorio-flask:1.0`, aunque no estén en uso.

#### Resultado obtenido

```text
WARNING! This will remove all dangling images.
Are you sure you want to continue? [y/N] y
Total reclaimed space: 0B
```

#### Qué observé

No liberó nada (`0B`), porque todas mis imágenes tienen nombre y etiqueta, así que ninguna es colgante.

### `docker volume prune`

```powershell
docker volume prune
```

#### Explicación

Elimina los volúmenes locales que no están siendo usados por ningún contenedor. En esta versión de Docker, la advertencia indica que se eliminan los volúmenes **anónimos** los que Docker crea sin nombre que no están en uso.

#### Resultado obtenido

```text
WARNING! This will remove anonymous local volumes not used by at least one container.
Are you sure you want to continue? [y/N] y
Total reclaimed space: 0B
```

#### Qué observé

No eliminó nada (`0B`). Mi volumen `datos-lab` **no se borró**, porque es un volumen con nombre y no uno anónimo: el siguiente `docker system df` todavía lo muestra. Esto me confirma que hay que tener cuidado con esta clase de comandos, ya que cada versión de Docker puede tratar los volúmenes con nombre de forma distinta.

---

## Comando ejecutado: `docker system df`

```powershell
docker system df
```

### Explicación

Muestra cuánto espacio en disco usa Docker, desglosado por tipo de recurso, y cuánto de ese espacio se podría recuperar.

### Resultado obtenido

```text
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          5         0         721.1MB   603.5MB (83%)
Containers      0         0         0B        0B
Local Volumes   1         0         33B       33B (100%)
Build Cache     11        0         222.7MB   28.67kB
```

### Qué observé

- **Imágenes:** 5 en total y ninguna activa (ningún contenedor las usa ahora). Ocupan 721.1 MB, de los cuales 603.5 MB (83 %) se podrían recuperar. Son, con diferencia, el recurso que más espacio consume.
- **Contenedores:** 0, ya que el `container prune` los eliminó todos.
- **Volúmenes locales:** 1 (`datos-lab`), con apenas 33 bytes, que corresponden al pequeño archivo de la práctica.
- **Caché de construcción (*Build Cache*):** 11 elementos que suman 222.7 MB, generados por el `docker build` de mi imagen. Casi nada de eso es recuperable de inmediato (28.67 kB).

### Comandos que no ejecuté

No ejecuté `docker system prune`, que es el comando general de limpieza, ni, por supuesto, `docker system prune -a`. Este último eliminaría **todas** las imágenes que no estén siendo usadas por un contenedor, incluyendo `laboratorio-flask:1.0`, y habría que descargarlas o reconstruirlas de nuevo.

---

## Diferencia entre limpiar contenedores, imágenes y volúmenes

| Recurso | Qué se elimina | Efecto |
|---|---|---|
| **Contenedores** (`docker container prune`) | Los contenedores detenidos | Libera poco espacio; se pierden los datos que estaban solo dentro de esos contenedores. Las imágenes y volúmenes se conservan. |
| **Imágenes** (`docker image prune`) | Imágenes sin uso | Libera mucho espacio. Si se elimina una imagen que se necesita, hay que descargarla o reconstruirla. |
| **Volúmenes** (`docker volume prune`) | Volúmenes que ningún contenedor usa | Es la limpieza más delicada: puede borrar datos persistentes de forma definitiva. |

---

## Reflexión

La limpieza me mostró cuánto se va acumulando sin que lo note: contenedores con nombres aleatorios de las primeras partes, imágenes que descargué solo una vez para probar y caché de construcción. También me llamó la atención que los contenedores casi no pesan, mientras que las imágenes ocupan la mayor parte del espacio. Y comprobé que los comandos `prune` piden confirmación por una razón: lo que eliminan no se recupera.

---

## Preguntas de reflexión

**1. ¿Por qué Docker puede consumir mucho espacio en disco?**

Porque cada imagen descargada o construida se guarda completa en el disco, y además se acumulan contenedores detenidos, volúmenes y caché de construcción. En mi caso, con solo cinco imágenes ya había 721 MB, y 603 MB eran recuperables. Como es tan fácil crear contenedores e imágenes nuevos, si no se limpia con frecuencia el espacio crece sin que uno lo note.

**2. ¿Qué diferencia hay entre eliminar un contenedor y eliminar una imagen?**

Eliminar un contenedor borra solo esa instancia, pero la imagen sigue disponible para crear contenedores nuevos. Eliminar una imagen borra la plantilla: ya no se pueden crear contenedores a partir de ella hasta descargarla o reconstruirla de nuevo, y Docker no deja eliminarla mientras algún contenedor la esté usando. Lo vi en `docker system df`: después de borrar los contenedores, las imágenes seguían ahí.

**3. ¿Por qué se debe tener cuidado al eliminar volúmenes?**

Porque los volúmenes guardan datos persistentes, como el contenido de una base de datos, y eliminarlos los borra de forma definitiva: no están dentro de ningún contenedor ni se pueden reconstruir con un `docker build`. Por eso `docker volume prune` pide confirmación, y por eso conviene revisar con `docker volume ls` qué se va a eliminar antes de confirmar.

**4. ¿Qué buenas prácticas aplicaría para mantener limpio su ambiente local?**

- Usar `--rm` en contenedores temporales para que se eliminen solos al terminar.
- Ponerles nombre a los contenedores con `--name`, para identificarlos y eliminarlos fácilmente.
- Revisar de forma periódica con `docker ps -a`, `docker images`, `docker volume ls` y `docker system df` qué se está acumulando.
- Eliminar los contenedores y las redes que ya no uso apenas termino una práctica.
- Revisar la lista antes de confirmar un `prune`, y no ejecutar `docker system prune -a` ni `docker volume prune` sin entender qué se va a perder.
- Conservar el `Dockerfile` y el código en el repositorio, para poder reconstruir cualquier imagen cuando haga falta.

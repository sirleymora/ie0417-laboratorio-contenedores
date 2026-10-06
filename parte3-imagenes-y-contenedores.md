# Parte 3: Imágenes y contenedores

## Objetivo

Comprender la diferencia entre una imagen y un contenedor. Una imagen es una plantilla inmutable con lo necesario para ejecutar una aplicación, y un contenedor es una instancia creada a partir de esa imagen, que puede estar en ejecución o detenida.

---

## Comando ejecutado: `docker pull ubuntu`

```powershell
docker pull ubuntu
```

### Explicación

Este comando descarga una imagen desde un registro (por defecto Docker Hub) hacia mi computadora, **sin crear ni ejecutar ningún contenedor**. Como no indiqué una versión, Docker usó la etiqueta `latest` por defecto (`Using default tag: latest`). La imagen se descarga en capas (cada línea `Pull complete` o `Download complete` corresponde a una capa).

### Resultado obtenido

```text
Using default tag: latest
latest: Pulling from library/ubuntu
06ad70e463aa: Pull complete
4e07a0f12b2c: Pull complete
8f70d2bfe91a: Download complete
Digest: sha256:f144425ff09be612d6d9ad965196e9cdc23dae1f42110a8a11a3e9a8198759f7
Status: Downloaded newer image for ubuntu:latest
docker.io/library/ubuntu:latest
```

### Reflexión

A diferencia de `docker run`, aquí solo se descarga la imagen. Me sirve para entender que descargar y ejecutar son dos acciones distintas: primero tengo la plantilla, y después puedo crear contenedores a partir de ella.

---

## Comando ejecutado: `docker images`

```powershell
docker images
```

### Explicación

Este comando lista las imágenes que están almacenadas localmente en mi computadora. Muestra el nombre y etiqueta de cada imagen (`IMAGE`), su identificador (`ID`) y el espacio que ocupa en disco (`DISK USAGE`).

### Resultado obtenido

```text
IMAGE                ID             DISK USAGE
hello-world:latest   5e2309035332       25.9kB
ubuntu:latest        f144425ff09b        162MB
```

### Qué observé

Aparecen dos imágenes: `hello-world`, que descargué en la Parte 2 y es diminuta (25.9 kB), y `ubuntu`, que acabo de descargar y ocupa 162 MB. Aun así, 162 MB es muy poco para un sistema operativo completo, lo que muestra que es una versión mínima.

### Reflexión

Este comando es la forma de saber qué plantillas tengo disponibles antes de crear contenedores. También me deja ver cuánto espacio consume cada imagen.

---

## Comando ejecutado: `docker run -it ubuntu bash`

```powershell
docker run -it ubuntu bash
```

### Explicación

Este comando crea un contenedor a partir de la imagen `ubuntu` y ejecuta dentro de él el programa `bash` (una terminal). Las opciones significan:

- `-i` (interactivo): mantiene abierta la entrada estándar, para que pueda escribir comandos.
- `-t` (tty): asigna una terminal, para que se vea como una consola normal.

### Qué significa ejecutar un contenedor en modo interactivo

Significa que no solo se inicia el contenedor, sino que quedo conectada a él: lo que escribo en mi teclado llega a un programa dentro del contenedor, y su salida se muestra en mi terminal. En este caso, al ejecutar el comando el prompt cambió a `root@317a494e04f4:/#`, lo que indica que estoy dentro del contenedor, como usuario `root`, y que `317a494e04f4` es su identificador.

### Qué observé dentro del contenedor Ubuntu

Dentro del contenedor ejecuté:

```text
root@317a494e04f4:/# ls
bin   etc   lib64  opt   run   sys  var
boot  home  media  proc  sbin  tmp
dev   lib   mnt    root  srv   usr

root@317a494e04f4:/# pwd
/

root@317a494e04f4:/# cat/etc/os-release
bash: cat/etc/os-release: No such file or directory

root@317a494e04f4:/# cat /etc/os-release
PRETTY_NAME="Ubuntu 26.04.1 LTS"
NAME="Ubuntu"
VERSION_ID="26.04"
VERSION="26.04.1 LTS (Resolute Raccoon)"
VERSION_CODENAME=resolute
ID=ubuntu
ID_LIKE=debian
...
```

- `ls` mostró la estructura típica de directorios de Linux (`bin`, `etc`, `home`, `usr`, `var`, etc.).
- `pwd` mostró que estoy en `/`, la raíz del sistema de archivos del contenedor.
- `cat /etc/os-release` confirmó que el contenedor se comporta como **Ubuntu 26.04.1 LTS**.
- En un primer intento escribí `cat/etc/os-release` sin el espacio y `bash` respondió `No such file or directory`, porque interpretó todo como una sola ruta. Al corregirlo (`cat /etc/os-release`) funcionó.

### Qué ocurrió al salir del contenedor

Al ejecutar `exit`, la terminal volvió a PowerShell. Como `bash` era el único proceso principal del contenedor, al terminar `bash` el contenedor se detuvo. Lo comprobé con `docker ps -a`.

### Reflexión

Fue interesante ver que, aunque estoy en Windows, dentro del contenedor tengo un entorno Linux completo con su propio sistema de archivos. También me dejó claro que el contenedor vive solo mientras su proceso principal esté activo.

---

## Comando ejecutado: `docker ps -a`

```powershell
docker ps -a
```

### Explicación

Lista todos los contenedores, tanto los que están en ejecución como los detenidos.

### Resultado obtenido

```text
CONTAINER ID   IMAGE         COMMAND    CREATED              STATUS                     PORTS     NAMES
317a494e04f4   ubuntu        "bash"     About a minute ago   Exited (0) 8 seconds ago             musing_shamir
fd0fcc96cf60   hello-world   "/hello"   9 minutes ago        Exited (0) 9 minutes ago             magical_sammet
```

### Qué observé

Aparecen dos contenedores, ambos con estado `Exited (0)`: el de `hello-world` (de la Parte 2) y el nuevo de `ubuntu`, que ejecutó `bash`. Docker les asignó nombres aleatorios (`musing_shamir` y `magical_sammet`) porque no usé `--name`.

### Reflexión

Ver los dos contenedores junto a las dos imágenes me ayudó a notar la diferencia: cada vez que uso `docker run` se crea un contenedor **nuevo**, pero las imágenes se reutilizan.

---

## Preguntas de reflexión

**1. ¿La imagen Ubuntu es lo mismo que una máquina virtual Ubuntu?**

No. La imagen de Ubuntu es solo una plantilla con los archivos y librerías de Ubuntu necesarios para ejecutar programas; no incluye su propio kernel ni arranca como un sistema completo. Una máquina virtual incluye un sistema operativo completo con su kernel, que se ejecuta sobre un hipervisor y reserva recursos propios. La imagen que descargué pesa solo 162 MB, mucho menos que una máquina virtual típica.

**2. ¿Por qué el contenedor puede parecer un sistema Linux si no es una máquina virtual completa?**

Porque dentro del contenedor tengo el sistema de archivos, las herramientas y las librerías de Ubuntu, por lo que al usar `ls` o `cat /etc/os-release` veo exactamente lo mismo que vería en un Ubuntu real. Lo que no tiene es un kernel propio: usa el del sistema anfitrión, y está aislado del resto del sistema, así que da la apariencia de ser una máquina separada.

**3. ¿Qué significa que el contenedor comparta el kernel con el host?**

Significa que los procesos del contenedor se ejecutan directamente sobre el mismo kernel que usa el host, en lugar de arrancar uno propio. Esto los hace ligeros y rápidos de iniciar. En mi caso lo vi en `docker info`, que mostró un kernel `...microsoft-standard-WSL2`: como trabajo en Windows, Docker Desktop usa un kernel de Linux proporcionado por WSL 2, y mis contenedores comparten ese kernel.

**4. ¿Qué diferencia hay entre una imagen descargada y un contenedor creado?**

La imagen descargada es la plantilla de solo lectura, que queda guardada en mi computadora y puede reutilizarse muchas veces. El contenedor es una instancia creada a partir de esa imagen: tiene su propio estado y puede estar en ejecución o detenido. En mi caso, la imagen `ubuntu` se descargó una sola vez con `docker pull`, pero cada `docker run` crea un contenedor nuevo; por eso en `docker ps -a` veo contenedores distintos con nombres distintos que salen de la misma imagen.

---

## Administración de contenedores

### Objetivo

Aprender a crear, nombrar, detener, iniciar y eliminar contenedores.

### Comando ejecutado: `docker run -it --name mi-ubuntu ubuntu bash`

```powershell
docker run -it --name mi-ubuntu ubuntu bash
```

#### Explicación

Es el mismo comando de la sección anterior, pero con la opción `--name mi-ubuntu`, que le asigna un nombre que yo elijo al contenedor, en lugar del nombre aleatorio que Docker genera por defecto (como `musing_shamir`). Con ese nombre luego puedo referirme al contenedor en otros comandos sin tener que copiar su ID.

#### Resultado obtenido

Dentro del contenedor creé un archivo y verifiqué que existía:

```text
root@41190ac2b0a5:/# echo "Hola desde el contenedor" > mensaje.txt
root@41190ac2b0a5:/# cat mensaje.txt
Hola desde el contenedor
root@41190ac2b0a5:/# exit
exit
```

### Comando ejecutado: `docker ps -a` (después de salir)

```powershell
docker ps -a
```

#### Resultado obtenido

```text
CONTAINER ID   IMAGE         COMMAND    CREATED              STATUS                      PORTS     NAMES
41190ac2b0a5   ubuntu        "bash"     About a minute ago   Exited (0) 19 seconds ago             mi-ubuntu
317a494e04f4   ubuntu        "bash"     4 minutes ago        Exited (0) 3 minutes ago              musing_shamir
fd0fcc96cf60   hello-world   "/hello"   13 minutes ago       Exited (0) 13 minutes ago             magical_sammet
```

#### Qué observé

El contenedor `mi-ubuntu` aparece con el nombre que le asigné y con estado `Exited (0)`: se detuvo al salir de `bash`, pero sigue existiendo.

### Comando ejecutado: `docker start mi-ubuntu`

```powershell
docker start mi-ubuntu
```

#### Explicación

Inicia un contenedor **ya existente** que estaba detenido. No crea uno nuevo ni usa la imagen para crear otro contenedor: reutiliza el que ya tenía.

#### Resultado obtenido

```text
mi-ubuntu
```

Al iniciarlo, el contenedor corre en segundo plano y no queda conectado a mi terminal.

### Comando ejecutado: `docker exec -it mi-ubuntu bash`

```powershell
docker exec -it mi-ubuntu bash
```

#### Explicación

Ejecuta un comando **dentro de un contenedor que ya está en ejecución**. En este caso abre una terminal `bash` en `mi-ubuntu`. Es la forma de "entrar" a un contenedor que ya está corriendo. Las opciones `-it` cumplen la misma función que en `docker run`.

#### Resultado obtenido

```text
root@41190ac2b0a5:/# cat mensaje.txt
Hola desde el contenedor
root@41190ac2b0a5:/# exit
exit
```

#### Qué pasó con el archivo creado dentro del contenedor

El archivo `mensaje.txt` **seguía existiendo** después de salir, detener e iniciar nuevamente el contenedor. Además, el identificador del contenedor era el mismo (`41190ac2b0a5`), lo que confirma que `docker start` reutilizó el contenedor original y no creó uno nuevo. Esto muestra que los datos escritos dentro de un contenedor se conservan mientras el contenedor exista, aunque esté detenido.

### Comandos ejecutados: `docker stop mi-ubuntu` y `docker rm mi-ubuntu`

```powershell
docker stop mi-ubuntu
docker rm mi-ubuntu
docker ps -a
```

#### Explicación

- `docker stop` detiene un contenedor que está en ejecución. El contenedor sigue existiendo, solo queda inactivo.
- `docker rm` elimina un contenedor que ya está detenido, junto con su sistema de archivos interno.

#### Resultado obtenido

```text
mi-ubuntu
mi-ubuntu

CONTAINER ID   IMAGE         COMMAND    CREATED          STATUS                      PORTS     NAMES
317a494e04f4   ubuntu        "bash"     6 minutes ago    Exited (0) 5 minutes ago              musing_shamir
fd0fcc96cf60   hello-world   "/hello"   15 minutes ago   Exited (0) 15 minutes ago             magical_sammet
```

#### Qué observé

Después de `docker rm`, `mi-ubuntu` ya no aparece en `docker ps -a`. Como el contenedor se eliminó, también se eliminó su contenido, incluyendo `mensaje.txt`.

### Resumen de lo aprendido

- **Uso de `--name`:** permite darle al contenedor un nombre fácil de recordar y usarlo en comandos como `start`, `exec`, `stop` y `rm`.
- **Diferencia entre `docker start` y `docker run`:** `docker run` **crea** un contenedor nuevo a partir de una imagen y lo ejecuta; `docker start` **reinicia** un contenedor que ya existe y está detenido.
- **Uso de `docker exec`:** ejecuta un comando dentro de un contenedor que ya está corriendo, por ejemplo para abrir una terminal en él.
- **Diferencia entre detener y eliminar:** detener (`docker stop`) apaga el contenedor pero lo conserva, con sus archivos, y puede volver a iniciarse; eliminar (`docker rm`) lo borra definitivamente junto con sus datos.
- **Archivo creado dentro del contenedor:** se conservó mientras el contenedor existió (incluso al detenerlo e iniciarlo), pero se perdió junto con el contenedor al eliminarlo.

### Reflexión

Esta parte me ayudó a entender el ciclo de vida de un contenedor: se crea, se ejecuta, se detiene, puede reiniciarse y finalmente se elimina. También me di cuenta de que detener un contenedor no borra nada, pero eliminarlo sí, y que por eso los datos importantes no deberían guardarse únicamente dentro de él.

### Preguntas de reflexión

**1. ¿Qué ventaja tiene asignar nombres a los contenedores?**

Facilita identificarlos y manejarlos. Un nombre como `mi-ubuntu` es más fácil de recordar y escribir que un ID como `41190ac2b0a5` o un nombre aleatorio como `musing_shamir`. Además, evita confusiones cuando hay varios contenedores de la misma imagen.

**2. ¿Qué diferencia hay entre crear un contenedor nuevo y reiniciar uno existente?**

Crear un contenedor nuevo (`docker run`) genera una instancia nueva y limpia a partir de la imagen, sin los cambios de contenedores anteriores. Reiniciar uno existente (`docker start`) vuelve a activar el mismo contenedor, con su mismo ID y con los archivos que tenía. Lo comprobé porque `mensaje.txt` seguía ahí después de `docker start`.

**3. ¿Qué sucede con los datos creados dentro de un contenedor si este se elimina?**

Se pierden, porque viven en el sistema de archivos del propio contenedor, que se borra junto con él. Por eso, cuando se necesita conservar información más allá de la vida del contenedor, se usan volúmenes (que veremos más adelante en el laboratorio).

**4. ¿Por qué se dice que los contenedores son desechables?**

Porque están pensados para crearse, usarse y eliminarse con facilidad, sin perder nada importante. Como la imagen se conserva, siempre se puede crear otro contenedor idéntico en segundos. Esto implica que no conviene depender de los datos guardados dentro de un contenedor, sino tratarlo como algo reemplazable.
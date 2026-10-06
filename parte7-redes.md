# Parte 7: Redes de Docker

## Objetivo

Crear una red personalizada y comunicar contenedores entre sí usando sus nombres.

Docker crea por defecto una red de tipo `bridge`, pero también se pueden crear redes propias. Los contenedores conectados a la misma red pueden comunicarse entre sí, e incluso usar el nombre del contenedor como dirección.

---

## Qué es una red en Docker

Una red en Docker es una red virtual que conecta contenedores entre sí y, según su configuración, con el exterior. Cada contenedor conectado a una red recibe una dirección IP dentro de ella. Los contenedores que están en la misma red pueden comunicarse; los que están en redes distintas quedan aislados unos de otros.

---

## Comando ejecutado: `docker network create red-lab`

```powershell
docker network create red-lab
```

### Explicación

Crea una red nueva llamada `red-lab`. Como no indiqué un tipo, Docker usó el predeterminado, `bridge`, que es una red virtual interna dentro de mi máquina. Al terminar, devuelve el identificador de la red.

### Resultado obtenido

```text
5159f2b434eaa49a15d953f940ebf0b517185ea2888f925eae8b3b5950b6e1c1
```

---

## Comando ejecutado: `docker network ls`

```powershell
docker network ls
```

### Explicación

Lista las redes que existen en Docker, con su identificador, nombre, tipo (driver) y alcance.

### Resultado obtenido

```text
NETWORK ID     NAME      DRIVER    SCOPE
22477876d121   bridge    bridge    local
df9ef500e2b5   host      host      local
5dec381846bf   none      null      local
5159f2b434ea   red-lab   bridge    local
```

### Qué observé

Aparecen las tres redes que Docker trae por defecto (`bridge`, `host` y `none`) y, además, mi nueva red `red-lab`, de tipo `bridge` y alcance `local`. El identificador `5159f2b434ea` coincide con los primeros caracteres del ID que devolvió `docker network create`.

---

## Comando ejecutado: `docker run -d --name servidor-web --network red-lab nginx`

```powershell
docker run -d --name servidor-web --network red-lab nginx
```

### Explicación

Crea un contenedor llamado `servidor-web` a partir de la imagen `nginx` (un servidor web), en segundo plano (`-d`), y lo conecta a mi red `red-lab` con la opción `--network red-lab`. No publiqué ningún puerto con `-p`, así que este servidor no es accesible desde mi navegador, solo desde dentro de la red.

### Resultado obtenido

```text
Unable to find image 'nginx:latest' locally
latest: Pulling from library/nginx
46243d3234ed: Pull complete
f802f27d954b: Pull complete
2056b40bae09: Pull complete
f1169c633cbc: Pull complete
3326c3817340: Pull complete
afa8dec48454: Pull complete
37d8c7707e42: Download complete
e40088050cb6: Download complete
Digest: sha256:abe47724e466aeab9a345d8e46a221c2fa8953c7848bb4a3bd9976a7199f8cf2
Status: Downloaded newer image for nginx:latest
f8bd7f547d25424fca321e62ce8619eb8e1f27281fa2dddde205be6516d11e52
```

### Qué observé

Como la imagen `nginx` no estaba en mi computadora, Docker la descargó automáticamente. Al final devolvió el ID del contenedor, que quedó corriendo en segundo plano.

---

## Comando ejecutado: `docker run -it --name cliente --network red-lab ubuntu bash`

```powershell
docker run -it --name cliente --network red-lab ubuntu bash
```

### Explicación

Crea un segundo contenedor, interactivo, llamado `cliente`, a partir de la imagen `ubuntu`, y lo conecta a la **misma red** `red-lab`. Este contenedor hace de cliente: desde él voy a intentar comunicarme con `servidor-web`.

### Qué significa conectar contenedores a la misma red

Significa que ambos contenedores pueden verse y comunicarse directamente entre sí a través de la red virtual, sin necesidad de publicar puertos hacia mi computadora. Un contenedor que no esté en `red-lab` no podría alcanzar a `servidor-web` de esa forma.

---

## Dentro del contenedor `cliente`

### Instalación de `curl`

```bash
apt update
apt install -y curl
```

#### Explicación

La imagen `ubuntu` es mínima y no trae `curl`, que es la herramienta que uso para hacer peticiones web desde la terminal. `apt update` actualiza la lista de paquetes disponibles y `apt install -y curl` instala `curl` (la opción `-y` responde "sí" automáticamente a la confirmación).

#### Resultado obtenido 

```text
root@f4f8c789b669:/# apt update
Get:1 http://archive.ubuntu.com/ubuntu resolute InRelease [136 kB]
...
Fetched 26.5 MB in 6s (4179 kB/s)
2 packages can be upgraded. Run 'apt list --upgradable' to see them.

root@f4f8c789b669:/# apt install -y curl
Installing:
  curl
...
Summary:
  Upgrading: 0, Installing: 30, Removing: 0, Not Upgrading: 2
  Download size: 6617 kB
...
Setting up curl (8.18.0-1ubuntu2.7) ...
...
```

#### Qué observé

`curl` se instaló junto con 29 paquetes de los que depende. Durante la instalación aparecieron avisos de `debconf` (por ejemplo, `unable to initialize frontend: Dialog`). No son errores de la instalación: solo indican que la imagen mínima no tiene programas para mostrar menús interactivos, y `apt` continuó con normalidad.

### Prueba de conexión: `curl http://servidor-web`

```bash
curl http://servidor-web
```

#### Explicación

Hace una petición HTTP al contenedor `servidor-web`, usando su **nombre** en lugar de una dirección IP.

#### Resultado obtenido

```text
root@f4f8c789b669:/# curl http://servidor-web
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, nginx is successfully installed and working.
Further configuration is required for the web server, reverse proxy,
API gateway, load balancer, content cache, or other features.</p>

<p>For online documentation and support please refer to
<a href="https://nginx.org/">nginx.org</a>.<br/>
To engage with the community please visit
<a href="https://community.nginx.org/">community.nginx.org</a>.<br/>
For enterprise grade support, professional services, additional
security features and capabilities please refer to
<a href="https://f5.com/nginx">f5.com/nginx</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

Después salí del contenedor con `exit`.

#### Qué ocurrió al ejecutar `curl http://servidor-web`

El contenedor `cliente` recibió como respuesta el HTML de la página de bienvenida de Nginx ("Welcome to nginx!"). Eso demuestra que logró comunicarse con el contenedor `servidor-web` a través de la red `red-lab`.

#### Por qué se pudo usar el nombre `servidor-web`

Porque en una red creada por mí, Docker incluye un servicio de resolución de nombres (DNS interno) que asocia el nombre de cada contenedor con su dirección IP dentro de la red. Así, cuando `curl` busca `servidor-web`, Docker lo traduce a la IP correcta del contenedor, sin que yo tenga que averiguarla ni escribirla. Esto me evita depender de direcciones IP, que pueden cambiar cada vez que se crea un contenedor.

---

## Comandos de limpieza

```powershell
docker stop servidor-web
docker rm servidor-web
docker rm cliente
docker network rm red-lab
```

### Resultado obtenido

```text
servidor-web
servidor-web
cliente
red-lab
```

### Explicación

- `docker stop servidor-web` detiene el servidor Nginx, que seguía corriendo en segundo plano.
- `docker rm servidor-web` y `docker rm cliente` eliminan los dos contenedores. El cliente no necesitó `stop` porque ya se había detenido al salir con `exit`.
- `docker network rm red-lab` elimina la red. Solo se puede eliminar cuando ya no hay contenedores conectados a ella, por eso se hace al final.

---

## Reflexión

Lo que más me llamó la atención es que el servidor Nginx nunca publicó ningún puerto hacia mi computadora, y aun así el cliente pudo llegar a él sin problema, solo por estar en la misma red. También me gustó poder usar un nombre en lugar de una dirección IP: bastó con escribir `servidor-web`. Entiendo que así es como se conectan los distintos servicios de una aplicación hecha con varios contenedores.

---

## Preguntas de reflexión

**1. ¿Por qué los contenedores necesitan redes?**

Porque los contenedores están aislados unos de otros por defecto, y las aplicaciones reales suelen estar formadas por varios servicios que deben comunicarse, por ejemplo, una aplicación web con una base de datos. Las redes permiten conectar solo a los contenedores que deben hablar entre sí y mantener aislados a los demás.

**2. ¿Qué ventaja tiene usar nombres de contenedor en lugar de direcciones IP?**

Los nombres son más fáciles de recordar y no cambian, mientras que las direcciones IP pueden variar cada vez que se crea o reinicia un contenedor. Usando nombres, una aplicación puede configurarse una sola vez (por ejemplo, conectarse a `servidor-web`) y seguir funcionando aunque la IP del contenedor sea otra.

**3. ¿Qué diferencia hay entre publicar un puerto hacia el host y comunicarse dentro de una red Docker?**

Publicar un puerto (`-p`) abre una entrada desde mi computadora (el host) hacia un contenedor, y sirve para que yo, o cualquier programa en mi máquina, lo use desde el navegador. La comunicación dentro de una red Docker ocurre solo entre contenedores y no requiere publicar nada hacia afuera. En esta práctica, `servidor-web` no tenía ningún `-p` y aun así `cliente` pudo acceder a él, porque estaban en la misma red. Por eso, lo normal es publicar solo los puertos que deben ser accesibles desde afuera, y dejar los demás servicios accesibles únicamente dentro de la red.

**4. ¿Qué ejemplos reales podrían usar una red Docker?**

Una aplicación web que se conecta a una base de datos (MySQL, PostgreSQL o Redis); una API que atiende a un frontend; un servidor web que distribuye tráfico entre varios contenedores de una aplicación; o un sistema de microservicios en el que cada servicio corre en su propio contenedor y todos comparten una red.

---

## Comunicación entre servicios

### Objetivo

Comprender cómo una aplicación podría comunicarse con otro servicio dentro de una red Docker, sin usar todavía Docker Compose. Para eso uso Redis, que en este ejemplo hace el papel de una base de datos simulada.

### Qué es Redis en este ejemplo

Redis es una base de datos muy rápida que guarda la información en forma de pares clave-valor (por ejemplo, la clave `curso` con el valor `IE0417`). En este laboratorio funciona como el "otro servicio" al que se conecta un cliente, igual que una aplicación web se conectaría a su base de datos. Corre en su propio contenedor y yo me conecto a él desde un segundo contenedor.

---

## Comando ejecutado: `docker network create red-app`

```powershell
docker network create red-app
```

### Explicación

Crea una red nueva llamada `red-app`, donde van a convivir el servidor y el cliente de Redis.

### Resultado obtenido

```text
5c760d900ba026c439dbf0380fb4ad5c249c540bc5eea0c55b78801fc4128a63
```

---

## Comando ejecutado: `docker run -d --name redis-lab --network red-app redis`

```powershell
docker run -d --name redis-lab --network red-app redis
```

### Explicación

Crea y ejecuta en segundo plano un contenedor llamado `redis-lab` a partir de la imagen oficial `redis`, conectado a la red `red-app`. Este contenedor es el **servidor** de Redis.

### Qué representa `redis-lab`

Representa el servicio de base de datos de este ejemplo. Su nombre (`redis-lab`) es el que el cliente va a usar para encontrarlo dentro de la red.

### Resultado obtenido

```text
Unable to find image 'redis:latest' locally
latest: Pulling from library/redis
0a3621ec1dd4: Pull complete
c30201c9cd3c: Pull complete
4ac6ba6b019e: Pull complete
ecc510c1e359: Pull complete
f55e02ea8cde: Pull complete
dc611c1ed116: Pull complete
4f4fb700ef54: Pull complete
e6c2a7c7d56e: Download complete
edf7d95c5d27: Download complete
Digest: sha256:8aee6591ee8c2b26e9e01ad4913fbc804ea6b79a9bc675ee1824d80ea5dd9856
Status: Downloaded newer image for redis:latest
880d71c9e7585f24d7f395fcf7b03da75de7272131f0b8986500ea0ea6347667
```

La imagen `redis` no estaba en mi computadora, así que Docker la descargó automáticamente.

---

## Comando ejecutado: `docker ps`

```powershell
docker ps
```

### Resultado obtenido

```text
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS         PORTS      NAMES
880d71c9e758   redis     "docker-entrypoint.s…"   9 seconds ago   Up 8 seconds   6379/tcp   redis-lab
```

### Qué observé

`redis-lab` está en ejecución (`Up`). En `PORTS` aparece solo `6379/tcp`, el puerto en el que escucha Redis dentro del contenedor, sin ningún mapeo hacia mi computadora. Igual que con Nginx, el servidor solo es accesible desde la red de Docker.

---

## Problema que tuve: el cliente se ejecutó como un segundo servidor

### Comando que ejecuté

```powershell
docker run -it --name cliente-redis --network red-app redis
```

### Qué ocurrió

A este comando le faltó la parte final (`redis-cli -h redis-lab`). Como no indiqué ningún comando, Docker ejecutó el que la imagen `redis` trae por defecto, que es arrancar un **servidor** Redis. En lugar de un cliente, se levantó un segundo servidor, y la terminal quedó ocupada mostrando sus mensajes de arranque (fragmento):

```text
Starting Redis Server
1:C 06 Oct 2026 04:35:21.973 * Redis version=8.10.2, bits=64, commit=00000000, modified=1, pid=1, just started
...
1:M 06 Oct 2026 04:35:22.001 * Server initialized
1:M 06 Oct 2026 04:35:22.001 * Ready to accept connections tcp
1:M 06 Oct 2026 04:35:22.002 # WARNING: Redis does not require authentication and is not protected by network restrictions. Redis will accept connections from any IP address on any network interface.
```

Lo detuve con `Ctrl + C`, y el servidor se apagó de forma ordenada:

```text
^C1:signal-handler (1791261489) Received SIGINT scheduling shutdown...
1:M 06 Oct 2026 04:38:09.861 * User requested shutdown...
1:M 06 Oct 2026 04:38:09.864 * BGSAVE done, 0 keys saved, 0 keys skipped, 89 bytes written.
1:M 06 Oct 2026 04:38:09.898 # Redis is now ready to exit, bye bye...
```

Al volver a ejecutar el comando correcto, Docker mostró un conflicto de nombre:

```text
docker: Error response from daemon: Conflict. The container name "/cliente-redis" is already in use by container "d8f223d71c91d563e548a2c8007cde279a0b03af5c80a4b460cc943f571b9a85". You have to remove (or rename) that container to be able to reuse that name.
```

El contenedor equivocado ya estaba detenido, pero **seguía existiendo**, así que su nombre estaba ocupado. Lo eliminé y verifiqué que el servidor `redis-lab` siguiera activo:

```powershell
docker rm cliente-redis
docker ps
```

```text
cliente-redis
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS         PORTS      NAMES
880d71c9e758   redis     "docker-entrypoint.s…"   7 minutes ago   Up 7 minutes   6379/tcp   redis-lab
```

### Qué aprendí de este error

- Lo que va después del nombre de la imagen en `docker run` es el **comando que se ejecuta dentro del contenedor**. Si no lo indico, se usa el comando por defecto de la imagen.
- Un contenedor detenido sigue existiendo y conserva su nombre hasta que se elimina con `docker rm`.

---

## Comando ejecutado: `docker run -it --name cliente-redis --network red-app redis redis-cli -h redis-lab`

```powershell
docker run -it --name cliente-redis --network red-app redis redis-cli -h redis-lab
```

### Explicación

Crea un contenedor interactivo y temporal llamado `cliente-redis`, en la misma red `red-app`, a partir de la imagen `redis`, pero esta vez ejecutando `redis-cli`, el programa cliente de Redis. La opción `-h redis-lab` le indica el **host**  al que debe conectarse: el nombre del contenedor del servidor.

### Cómo se conectó el cliente al servidor

Ambos contenedores están en la misma red (`red-app`), y el cliente usó el nombre `redis-lab` para encontrar al servidor. Docker tradujo ese nombre a la dirección IP del contenedor, igual que ocurrió con `servidor-web` en la sección anterior. No tuve que averiguar ninguna IP ni publicar ningún puerto en mi computadora.

### Resultado obtenido

```text
redis-lab:6379> ping
PONG
redis-lab:6379> set curso IE0417
OK
redis-lab:6379> get curso
"IE0417"
redis-lab:6379> exit
```

### Qué significa recibir `PONG`

`ping` es una prueba de conectividad: el cliente le pregunta al servidor "¿estás ahí?" y el servidor responde `PONG`. Recibirlo confirma que el cliente logró comunicarse con el servidor a través de la red y que el servidor está funcionando.

### Qué hicieron los otros comandos

- `set curso IE0417` guardó en Redis el valor `IE0417` bajo la clave `curso`, y Redis respondió `OK`.
- `get curso` leyó esa clave y devolvió `"IE0417"`, es decir, el dato quedó guardado en el servidor `redis-lab` y lo pude recuperar desde el cliente.

El prompt `redis-lab:6379>` también es una prueba: muestra que el cliente está conectado al host `redis-lab`, en el puerto 6379.

---

## Comandos de limpieza

```powershell
docker stop redis-lab
docker rm redis-lab
docker rm cliente-redis
docker network rm red-app
```

### Resultado obtenido

```text
redis-lab
redis-lab
cliente-redis
red-app
```

### Explicación

Detuve y eliminé el servidor, eliminé el contenedor cliente  y, al final, eliminé la red, que solo puede borrarse cuando ya no hay contenedores conectados.

---

## Qué enseñanza deja este ejemplo sobre aplicaciones con varios contenedores

Que una aplicación puede dividirse en servicios independientes, cada uno en su propio contenedor, y que se comunican entre sí a través de una red de Docker usando nombres. Solo hace falta que los contenedores estén en la misma red; no es necesario publicar los puertos del servicio hacia mi computadora. También dejó ver una limitación: tuve que crear la red, el servidor y el cliente con varios comandos escritos a mano, y un error en uno de ellos complica todo el proceso.

## Reflexión

Este ejemplo me ayudó a ver cómo se vería una aplicación real: un servicio que usa otro, cada uno aislado en su contenedor y conectados por una red. El error que cometí con el comando incompleto me enseñó algo útil: lo que va después del nombre de la imagen es lo que realmente se ejecuta dentro del contenedor. También entendí por qué conviene eliminar los contenedores que ya no uso: un contenedor detenido igual conserva su nombre.

## Preguntas de reflexión

**1. ¿Por qué una aplicación web podría necesitar comunicarse con una base de datos?**

Porque una aplicación necesita guardar y consultar información que no debe perderse cuando termina de ejecutarse, como usuarios, productos, pedidos o configuraciones. La base de datos se encarga de almacenar esos datos, y la aplicación solo se encarga de la lógica y de mostrar la información.

**2. ¿Por qué ambos contenedores deben estar en la misma red?**

Porque los contenedores están aislados entre sí por defecto, y solo pueden verse y comunicarse directamente si comparten una red. Además, en una red creada por mí, Docker permite usar el nombre del contenedor como dirección. En este ejemplo, el cliente pudo encontrar a `redis-lab` por estar en `red-app`.

**3. ¿Qué ventaja tiene separar servicios en contenedores distintos?**

Cada servicio queda aislado, con sus propias dependencias, y puede actualizarse, reiniciarse o reemplazarse sin afectar a los demás. También permite reutilizar imágenes oficiales (como `redis`) en lugar de instalar el servicio a mano, y escalar o probar cada parte por separado.

**4. ¿Qué limitación tiene hacerlo manualmente con varios comandos `docker run`?**

Hay que escribir y recordar cada comando, con sus opciones, en el orden correcto, y cualquier error o descuido complica todo el proceso, como me pasó con el comando incompleto. Además, es difícil repetir la misma configuración en otra máquina o compartirla con otras personas. Docker Compose resuelve esto describiendo todos los servicios en un solo archivo.

# Parte 5: Publicación de puertos

## Objetivo

Comprender cómo exponer una aplicación que corre dentro de un contenedor para poder accederla desde la máquina anfitriona (mi computadora).

---

## Primera ejecución: `-p 5000:5000`

### Comando ejecutado

```powershell
docker run --name app-puertos -p 5000:5000 laboratorio-flask:1.0
```

### Explicación

Crea y ejecuta un contenedor llamado `app-puertos` a partir de la imagen `laboratorio-flask:1.0`, y además **publica un puerto**: la opción `-p 5000:5000` conecta el puerto 5000 de mi computadora con el puerto 5000 del contenedor. Gracias a eso, ahora puedo abrir la aplicación desde el navegador.

### Resultado obtenido

Con el contenedor en ejecución, `docker ps` mostró:

```text
CONTAINER ID   IMAGE                   COMMAND           CREATED         STATUS         PORTS                                         NAMES
00283bd789ca   laboratorio-flask:1.0   "python app.py"   2 minutes ago   Up 2 minutes   0.0.0.0:5000->5000/tcp, [::]:5000->5000/tcp   app-puertos
```

### Qué observé

En la columna `PORTS` aparece `0.0.0.0:5000->5000/tcp`. Antes, cuando ejecuté el contenedor sin `-p`, esa columna solo mostraba `5000/tcp`, que es el puerto declarado por `EXPOSE` pero sin conexión hacia mi máquina. Ahora el puerto sí está publicado: lo que llegue al puerto 5000 de mi computadora se redirige al puerto 5000 del contenedor. (El `[::]` es lo mismo pero para direcciones IPv6.)

### Captura del navegador

En las siguientes imágenes se evidencia que ambas páginas están corriendo correctamente:

![Aplicación en localhost:5000](evidencias/parte5-puertos-5000.png)

![Ruta /info en localhost:5000](evidencias/parte5-puertos-5000-info.png)

### Detener y eliminar el contenedor

```powershell
docker stop app-puertos
docker rm app-puertos
```

Resultado:

```text
app-puertos
app-puertos
```

---

## Segunda ejecución: `-p 8080:5000`

### Comando ejecutado

```powershell
docker run --name app-puertos-2 -p 8080:5000 laboratorio-flask:1.0
```

### Explicación

Es el mismo contenedor y la misma aplicación, pero ahora con `-p 8080:5000`: el puerto **8080** de mi computadora se conecta con el puerto **5000** del contenedor. La aplicación sigue escuchando en el 5000 dentro del contenedor, no cambió nada en el código ni en la imagen; solo cambié por dónde la accedo desde mi computadora.

### Resultado obtenido

```text
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000
Press CTRL+C to quit
172.17.0.1 - - [04/Oct/2026 23:35:18] "GET / HTTP/1.1" 200 -
172.17.0.1 - - [04/Oct/2026 23:35:18] "GET /favicon.ico HTTP/1.1" 404 -
```

Con el contenedor en ejecución, `docker ps` mostró:

```text
CONTAINER ID   IMAGE                   COMMAND           CREATED         STATUS         PORTS                                         NAMES
ff74cb27e613   laboratorio-flask:1.0   "python app.py"   2 minutes ago   Up 2 minutes   0.0.0.0:8080->5000/tcp, [::]:8080->5000/tcp   app-puertos-2
```

### Qué observé

- En `PORTS` aparece `0.0.0.0:8080->5000/tcp`: el 8080 es el puerto de mi computadora y el 5000 es el del contenedor.
- Los logs registran la petición `GET /` con código `200` al abrir `http://localhost:8080`. La petición `GET /favicon.ico` devolvió `404`, algo normal porque el navegador pide automáticamente el ícono de la pestaña y la aplicación no lo define.
- Las peticiones aparecen con origen `172.17.0.1`, que es la dirección de la puerta de enlace de la red interna de Docker. Es decir, desde el punto de vista del contenedor, mis peticiones llegan a través de Docker y no directamente desde mi navegador.
- Dentro del contenedor la aplicación sigue diciendo `Running on http://172.17.0.2:5000`: no sabe nada del puerto 8080. Ese mapeo lo hace Docker por fuera.
- Mientras este contenedor estaba en ejecución, intenté abrir de nuevo `http://localhost:5000` (y `/info`) y **no funcionó**: la página no cargó. Tiene sentido porque en esta ejecución solo publiqué el puerto 8080 del host; el puerto 5000 de mi computadora ya no está conectado a ningún contenedor, aunque la aplicación siga escuchando en el 5000 por dentro. La aplicación solo es accesible por el puerto del host que yo elegí en `-p`, en este caso `http://localhost:8080`.

### Captura del navegador

En la siguiente imagen se evidencia que l local host no responde: 

![localhost:5000 sin respuesta mientras el contenedor usa 8080:5000](evidencias/parte5-puertos-5000-sin-respuesta.png)

### Detener y eliminar el contenedor

```powershell
docker stop app-puertos-2
docker rm app-puertos-2
```

Resultado:

```text
app-puertos-2
app-puertos-2
```

Al detener el contenedor desde otra terminal, la terminal donde corría `docker run` terminó y mostró un mensaje de sugerencia de Docker ("What's next: Debug this container error with Gordon"). No fue un error de la aplicación: es una sugerencia que Docker Desktop muestra cuando el contenedor termina por una señal de parada.

---

## Qué significa cada mapeo

### Qué significa `-p 5000:5000`

Que el puerto 5000 de mi computadora (host) se conecta con el puerto 5000 del contenedor. Cualquier petición que llegue a `localhost:5000` se redirige a la aplicación dentro del contenedor.

### Qué significa `-p 8080:5000`

Que el puerto 8080 de mi computadora se conecta con el puerto 5000 del contenedor. Cualquier petición a `localhost:8080` se redirige a la misma aplicación, que sigue escuchando en el 5000 por dentro.

### Cuál puerto pertenece al host y cuál al contenedor

El formato es `-p PUERTO_HOST:PUERTO_CONTENEDOR`:

| Opción | Puerto del host (mi computadora) | Puerto del contenedor |
|---|---|---|
| `-p 5000:5000` | 5000 | 5000 |
| `-p 8080:5000` | 8080 | 5000 |

El número de la **izquierda** es el del host; el de la **derecha** es el del contenedor.

---

## Reflexión

Lo más importante de esta parte es que la aplicación no cambió en ningún momento: usé la misma imagen y el mismo código, y solo con la opción `-p` decidí por dónde acceder a ella. Me ayudó mucho comparar la columna `PORTS` de `docker ps` antes y después de publicar el puerto, porque se ve claramente la diferencia entre un puerto que solo está declarado (`5000/tcp`) y uno realmente publicado (`0.0.0.0:5000->5000/tcp`).

---

## Preguntas de reflexión

**1. ¿Por qué no basta con que la aplicación escuche en el puerto 5000 dentro del contenedor?**

Porque el contenedor está aislado en su propia red interna, y un puerto abierto dentro de ella no es visible desde mi computadora. Lo comprobé al ejecutar el contenedor sin `-p`: Flask estaba escuchando en el 5000, pero `docker ps` solo mostraba `5000/tcp` y la aplicación no era accesible desde el navegador. Hace falta publicar el puerto para que el tráfico de mi máquina llegue al contenedor.

**2. ¿Qué función cumple el mapeo de puertos?**

Conecta un puerto de la máquina anfitriona con un puerto del contenedor. Docker recibe las conexiones que llegan al puerto del host y las redirige al puerto indicado dentro del contenedor, lo que permite acceder desde afuera a los servicios que corren adentro.

**3. ¿Cuál es la diferencia entre el puerto del host y el puerto del contenedor?**

El puerto del host pertenece a mi computadora y es por donde accedo desde el navegador (por ejemplo, 8080). El puerto del contenedor es el que usa la aplicación dentro de su propio entorno aislado (5000, el que definí en `app.py`). No tienen que ser iguales: en la segunda ejecución usé 8080 en el host y 5000 en el contenedor, y funcionó sin modificar la aplicación.

**4. ¿Qué pasaría si dos contenedores intentan usar el mismo puerto del host?**

El segundo no podría iniciar, porque un puerto del host solo puede estar asignado a un servicio a la vez. Docker mostraría un error indicando que el puerto ya está en uso (algo como "port is already allocated"). Para evitarlo, se asigna un puerto distinto del host a cada contenedor; por ejemplo, `-p 5000:5000` para uno y `-p 8080:5000` para el otro, aunque ambos escuchen en el 5000 por dentro. Por eso detuve y eliminé `app-puertos` antes de iniciar el segundo contenedor.

---

## Logs e inspección

### Objetivo

Aprender a observar el comportamiento de un contenedor usando comandos de inspección: `docker logs`, `docker logs -f`, `docker inspect` y `docker stats`.

### Comando ejecutado: `docker run -d --name app-logs -p 5000:5000 laboratorio-flask:1.0`

```powershell
docker run -d --name app-logs -p 5000:5000 laboratorio-flask:1.0
```

#### Explicación

Es el mismo contenedor de la sección anterior, pero con la opción `-d` (*detached*), que lo ejecuta **en segundo plano**. La terminal queda libre y Docker solo imprime el ID completo del contenedor.

#### Resultado obtenido

```text
1b720b4267c60415844aed2931309b400675dd13aff11aa4e46bb1bbed6635de
```

---

### Comando ejecutado: `docker logs app-logs`

```powershell
docker logs app-logs
```

#### Explicación

Muestra lo que el contenedor ha escrito en su salida estándar y en su salida de errores hasta el momento. En este caso, son los mensajes que imprime Flask al arrancar. Como el contenedor está en segundo plano, es la forma de ver qué está pasando dentro de él.

#### Resultado obtenido

```text
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000
Press CTRL+C to quit
```

#### Qué observé

Se ve el arranque de Flask completo, sin ninguna petición todavía, porque en ese momento no había abierto la página en el navegador.

---

### Comando ejecutado: `docker logs -f app-logs`

```powershell
docker logs -f app-logs
```

#### Explicación

La opción `-f` (*follow*) hace que la terminal quede **siguiendo los logs en tiempo real**: además de mostrar lo anterior, imprime las líneas nuevas apenas se generan. Se detiene con `Ctrl + C`, lo cual solo deja de seguir los logs, sin detener el contenedor.

#### Resultado obtenido

Mientras el comando estaba activo, abrí `http://localhost:5000` y `http://localhost:5000/info` en el navegador, y aparecieron las nuevas líneas:

```text
 * Serving Flask app 'app'
 * Debug mode: off
...
Press CTRL+C to quit
172.17.0.1 - - [04/Oct/2026 23:44:18] "GET / HTTP/1.1" 200 -
172.17.0.1 - - [04/Oct/2026 23:44:28] "GET /info HTTP/1.1" 200 -
```

#### Qué observé

Cada visita desde el navegador generó una línea nueva en los logs: `GET /` a las 23:44:18 y `GET /info` a las 23:44:28, ambas con código `200` (respuesta exitosa). Esto me permitió ver, en tiempo real, cómo el contenedor recibía y atendía mis peticiones.

---

### Comando ejecutado: `docker inspect app-logs`

```powershell
docker inspect app-logs
```

#### Explicación

Devuelve, en formato JSON, toda la información detallada de la configuración y el estado del contenedor. Es una salida muy larga, así que a continuación copio solo los fragmentos más relevantes.

#### Resultado obtenido (parcial)

**Estado del contenedor (`State`):**

```json
"State": {
    "Status": "running",
    "Running": true,
    "Paused": false,
    "Restarting": false,
    "OOMKilled": false,
    "Dead": false,
    "Pid": 395,
    "ExitCode": 0,
    "Error": "",
    "StartedAt": "2026-10-04T23:43:35.075923144Z"
}
```

**Comando que ejecuta, directorio de trabajo e imagen (`Config`):**

```json
"Config": {
    "Cmd": [
        "python",
        "app.py"
    ],
    "Image": "laboratorio-flask:1.0",
    "WorkingDir": "/app",
    "ExposedPorts": {
        "5000/tcp": {}
    }
}
```

**Publicación de puertos y modo de red (`HostConfig`):**

```json
"NetworkMode": "bridge",
"PortBindings": {
    "5000/tcp": [
        {
            "HostIp": "",
            "HostPort": "5000"
        }
    ]
}
```

**Red y dirección IP (`NetworkSettings`):**

```json
"Ports": {
    "5000/tcp": [
        { "HostIp": "0.0.0.0", "HostPort": "5000" },
        { "HostIp": "::", "HostPort": "5000" }
    ]
},
"Networks": {
    "bridge": {
        "Gateway": "172.17.0.1",
        "IPAddress": "172.17.0.2",
        "MacAddress": "de:20:de:23:d2:66"
    }
}
```

#### Qué observé

- `"Status": "running"` confirma que el contenedor está activo, y `"ExitCode": 0` y `"OOMKilled": false` indican que no ha fallado ni se quedó sin memoria.
- `Cmd` (`python app.py`) y `WorkingDir` (`/app`) coinciden con lo que definí en el `Dockerfile` con `CMD` y `WORKDIR`.
- `PortBindings` y `Ports` muestran el mapeo del puerto 5000 del contenedor al puerto 5000 de mi computadora, el mismo que aparece en `docker ps`.
- El contenedor está en la red `bridge` (la red por defecto) con la IP `172.17.0.2`, y el gateway `172.17.0.1` es la dirección que vi como origen de las peticiones en los logs.
- `"Mounts": []` indica que no tiene volúmenes montados, y `"Memory": 0` que no tiene un límite de memoria configurado.

Para confirmar un dato puntual sin leer todo el JSON, usé la opción `--format`:

```powershell
docker inspect --format "{{.State.Status}}" app-logs
```

```text
running
```

---

### Comando ejecutado: `docker stats`

```powershell
docker stats
```

#### Explicación

Muestra, en tiempo real, el consumo de recursos de los contenedores en ejecución: CPU, memoria, tráfico de red, lectura y escritura en disco y cantidad de procesos. Se actualiza continuamente hasta que se detiene con `Ctrl + C`.

#### Resultado obtenido

```text
CONTAINER ID   NAME       CPU %     MEM USAGE / LIMIT     MEM %     NET I/O          BLOCK I/O        PIDS
1b720b4267c6   app-logs   0.03%     22.77MiB / 7.447GiB   0.30%     4.64kB / 1.9kB   24.7MB / 147kB   2
```

#### Qué observé

- **CPU:** 0.03 %, casi nada, porque la aplicación está esperando peticiones.
- **Memoria:** 22.77 MiB usados de 7.447 GiB disponibles (0.30 %). Es muy poco, y el límite que muestra es la memoria total asignada a Docker, no un límite del contenedor.
- **Red (`NET I/O`):** 4.64 kB recibidos y 1.9 kB enviados, lo que corresponde a las peticiones que hice desde el navegador.
- **`PIDS`:** 2 procesos corriendo dentro del contenedor.

---

### Detener y eliminar el contenedor

```powershell
docker stop app-logs
docker rm app-logs
```

Resultado:

```text
app-logs
app-logs
```

---

### Resumen de lo aprendido

- **Qué muestra `docker logs`:** lo que el contenedor ha escrito en su salida estándar y de errores hasta ese momento. En este caso, el arranque de Flask y las peticiones recibidas.
- **Para qué sirve `docker logs -f`:** para seguir los logs en vivo, viendo aparecer cada nueva línea apenas ocurre.
- **Qué tipo de información muestra `docker inspect`:** la configuración y el estado detallado del contenedor en JSON: estado, imagen, comando, directorio de trabajo, variables de entorno, puertos, red, IP, montajes y límites de recursos.
- **Qué información muestra `docker stats`:** el uso de CPU, memoria, red, disco y cantidad de procesos de cada contenedor en ejecución, en tiempo real.

### Reflexión

Lo que más me gustó fue ver cómo aparecían en `docker logs -f` mis propias visitas al navegador, con la hora y el código de respuesta. También me sorprendió que `docker inspect` contiene todos los datos que fui definiendo en distintos pasos del laboratorio (el `CMD`, el `WORKDIR`, el puerto publicado), todo reunido en un solo lugar. Cuando un contenedor se comporte mal, sé que estos comandos son los primeros que debo usar.

### Preguntas de reflexión

**1. ¿Por qué los logs son importantes al trabajar con contenedores?**

Porque un contenedor, sobre todo si está en segundo plano, no muestra directamente lo que pasa adentro. Los logs son la forma principal de saber si la aplicación arrancó bien, si recibe peticiones o si hay errores. Como los contenedores se crean y destruyen con facilidad, los logs son muchas veces la única pista para entender por qué algo falló.

**2. ¿Qué diferencia hay entre ver logs históricos y logs en tiempo real?**

`docker logs` muestra lo que ya ocurrió hasta el momento y termina; sirve para revisar qué pasó, por ejemplo al arrancar o antes de un error. `docker logs -f` se queda activo y muestra además las líneas nuevas a medida que se generan; sirve para observar el comportamiento mientras se prueba la aplicación. En mi caso, vi aparecer `GET /` y `GET /info` justo cuando las abrí en el navegador.

**3. ¿Qué información útil se puede obtener con `docker inspect`?**

El estado del contenedor (si está corriendo, su código de salida, si fue terminado por falta de memoria), la imagen de la que viene, el comando que ejecuta, el directorio de trabajo, las variables de entorno, los puertos publicados, la red y su dirección IP, los volúmenes montados y los límites de recursos. Es útil para verificar que el contenedor quedó configurado como esperaba y para diagnosticar problemas.

**4. ¿Por qué es importante observar el consumo de recursos?**

Porque los contenedores comparten los recursos de la máquina anfitriona, y uno que consuma demasiada CPU o memoria puede afectar a los demás o a todo el sistema. Con `docker stats` puedo detectar contenedores que se comportan mal, dimensionar cuántos recursos necesita una aplicación y decidir si hace falta ponerles límites. En mi caso, la aplicación consumía muy poco (0.03 % de CPU y unos 22 MiB de memoria).

---

## Variables de entorno

### Objetivo

Configurar el comportamiento de un contenedor usando variables de entorno, sin modificar el código ni la imagen.

En `app.py`, la página principal toma el mensaje de la variable de entorno `MENSAJE`:

```python
mensaje = os.environ.get("MENSAJE", "Hola desde Flask en Docker")
```

Si la variable existe, se usa su valor; si no, se usa el texto por defecto "Hola desde Flask en Docker".

### Primera ejecución

#### Comando ejecutado

```powershell
docker run --name app-env -p 5000:5000 -e MENSAJE="Hola desde una variable de entorno" laboratorio-flask:1.0
```

#### Explicación

Crea y ejecuta el contenedor `app-env` publicando el puerto 5000, y además le pasa una variable de entorno con la opción `-e`: `MENSAJE="Hola desde una variable de entorno"`.

#### Resultado obtenido

```text
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000
Press CTRL+C to quit
172.17.0.1 - - [04/Oct/2026 23:48:41] "GET / HTTP/1.1" 200 -
```

#### Captura del navegador

Al abrir `http://localhost:5000`, la página mostró el título **"Hola desde una variable de entorno"** y debajo el texto "Esta aplicación se está ejecutando dentro de un contenedor."

![Primera ejecución con variable de entorno](evidencias/parte5-entorno-1.png)

#### Detener y eliminar el contenedor

```powershell
docker stop app-env
docker rm app-env
```

```text
app-env
app-env
```

### Segunda ejecución, con otro mensaje

#### Comando ejecutado

```powershell
docker run --name app-env-2 -p 5000:5000 -e MENSAJE="Configuración cambiada sin modificar la imagen" laboratorio-flask:1.0
```

#### Resultado obtenido

```text
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000
Press CTRL+C to quit
172.17.0.1 - - [04/Oct/2026 23:51:25] "GET / HTTP/1.1" 200 -
```

#### Captura del navegador

![Página con el mensaje "Configuración cambiada sin modificar la imagen"](evidencias/parte5-entorno-2.png)

#### Detener y eliminar el contenedor

```powershell
docker stop app-env-2
docker rm app-env-2
```

```text
app-env-2
app-env-2
```

### Qué hace la opción `-e`

Define una variable de entorno dentro del contenedor al momento de crearlo, con el formato `-e NOMBRE="valor"`. El programa que corre adentro puede leerla como cualquier variable de entorno del sistema; en este caso, `app.py` la lee con `os.environ.get("MENSAJE", ...)`.

### Qué cambió en la aplicación

El mensaje que muestra la página principal. En la primera ejecución apareció "Hola desde una variable de entorno", y en la segunda se usó otro texto ("Configuración cambiada sin modificar la imagen"). Los logs de ambas ejecuciones muestran que la página principal respondió correctamente (`GET / ... 200`). El resto de la aplicación se comportó igual: las mismas rutas, el mismo puerto y la misma imagen.

### Por qué no fue necesario reconstruir la imagen

Porque el mensaje no está escrito dentro de la imagen: el código solo indica que debe leer la variable `MENSAJE` cuando se ejecuta. El valor se entrega al momento de crear cada contenedor, no al construir la imagen. Por eso usé exactamente la misma imagen, `laboratorio-flask:1.0`, en las dos ejecuciones, y solo cambié el valor de `-e`. No tuve que editar `app.py` ni volver a ejecutar `docker build`.

### Reflexión

Esta parte me mostró que una misma imagen puede comportarse de forma distinta según la configuración que reciba al arrancar. Me llamó la atención lo sencillo que fue cambiar el mensaje: bastó con otro valor en `-e`, sin tocar el código ni reconstruir nada. Entiendo que esta es la forma habitual de configurar aplicaciones en contenedores.

### Preguntas de reflexión

**1. ¿Por qué es útil configurar aplicaciones mediante variables de entorno?**

Porque permite cambiar el comportamiento de una aplicación sin modificar su código ni reconstruir la imagen. La misma imagen se puede ejecutar con configuraciones distintas según el contexto (desarrollo, pruebas, producción), y los valores quedan separados del código.

**2. ¿Qué tipo de información podría configurarse así?**

Datos que cambian según el entorno: la dirección y el puerto de una base de datos, el nombre de usuario o contraseña de un servicio, claves de acceso o tokens de una API, el modo de ejecución (desarrollo o producción), el nivel de detalle de los logs o, como en este laboratorio, un mensaje que se muestra en pantalla.

**3. ¿Por qué no es buena práctica guardar contraseñas directamente dentro del código?**

Porque el código se comparte, se versiona y se guarda en repositorios, así que cualquier persona con acceso podría ver las contraseñas. También quedarían dentro de la imagen, de modo que quien la obtenga las tendría. Además, para cambiar una contraseña habría que modificar el código y reconstruir la imagen. Es mejor entregarlas desde afuera, por ejemplo con variables de entorno o con mecanismos de manejo de secretos.

**4. ¿Qué ventaja tiene usar la misma imagen con diferentes configuraciones?**

Se prueba y se distribuye una sola imagen, y se ejecuta igual en cualquier entorno; solo cambian los valores que se le pasan. Eso reduce errores, ahorra tiempo (no hay que reconstruir) y asegura que lo que se probó es lo mismo que se despliega. En este laboratorio lo vi directamente: dos contenedores con mensajes distintos salieron de la misma imagen `laboratorio-flask:1.0`.
# Parte 2: Primer contenedor

## Objetivo

Ejecutar mi primer contenedor usando una imagen existente en Docker Hub y aprender a consultar el estado de los contenedores.

---

## Comando ejecutado: `docker run hello-world`

```powershell
docker run hello-world
```

### Explicación

Este comando crea y ejecuta un contenedor a partir de la imagen `hello-world`. Hace varias cosas en una sola orden:

1. Busca la imagen `hello-world` en mi computadora.
2. Si no la encuentra, la descarga desde Docker Hub (el registro público de imágenes).
3. Crea un contenedor nuevo a partir de esa imagen.
4. Lo ejecuta. El programa que lleva dentro imprime un mensaje y termina.

### Qué ocurrió porque la imagen no estaba descargada

Como era mi primera vez usando Docker (`Images: 0` en `docker info`), la imagen no estaba en mi máquina. Docker mostró `Unable to find image 'hello-world:latest' locally`, y automáticamente la descargó desde Docker Hub (`Pulling from library/hello-world`). Al terminar indicó `Status: Downloaded newer image for hello-world:latest`. Es decir, no tuve que ejecutar un `docker pull` por separado: `docker run` lo hizo solo. Además, como no indiqué una versión, Docker usó la etiqueta `latest` por defecto.

### Resultado obtenido

```text
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
4f55086f7dd0: Pull complete
d5e71e642bf5: Download complete
Digest: sha256:5e23090353324d887c48ad5e5c56d294eab81588df9605b07d1afe895f9cc8f8
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.
...
```

### Evidencias

En la siguiente imagen se nota como estan funcionando adecuadamente los comandos de Docker:
![Ejecución de comandos](evidencias/parte2-hello-world.png)

### Reflexión

Me sorprendió que un solo comando hiciera todo el recorrido: buscar la imagen, descargarla, crear el contenedor y ejecutarlo. El mensaje de salida además explica los pasos que Docker siguió, lo cual ayuda a entender la relación entre el cliente, el daemon y Docker Hub.

---

## Comando ejecutado: `docker ps`

```powershell
docker ps
```

### Explicación

Este comando lista los contenedores que están **actualmente en ejecución**.

### Resultado obtenido

```text
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

### Reflexión

La lista salió vacía, solo con los encabezados de las columnas. Esto no significa que el contenedor no se haya creado, sino que ya no estaba en ejecución: terminó apenas imprimió su mensaje.

---

## Comando ejecutado: `docker ps -a`

```powershell
docker ps -a
```

### Explicación

La opción `-a` (de *all*) hace que el comando muestre **todos** los contenedores, tanto los que están en ejecución como los que ya terminaron o están detenidos.

### Resultado obtenido

```text
CONTAINER ID   IMAGE         COMMAND    CREATED          STATUS                      PORTS     NAMES
fd0fcc96cf60   hello-world   "/hello"   48 seconds ago   Exited (0) 48 seconds ago             magical_sammet
```

### Qué observé

- El contenedor `fd0fcc96cf60` fue creado a partir de la imagen `hello-world`.
- Ejecutó el comando `"/hello"`, que es el programa que imprime el mensaje.
- Su estado es `Exited (0)`: terminó, y el código `0` indica que lo hizo sin errores.
- Docker le asignó un nombre aleatorio (`magical_sammet`) porque yo no usé `--name`.

### Reflexión

Este comando me permitió ver que los contenedores no desaparecen cuando terminan: siguen existiendo en estado detenido hasta que se eliminan. Es útil para revisar el historial de lo que se ha ejecutado.

---

## Diferencia entre `docker ps` y `docker ps -a`

| Comando | Qué muestra | En mi caso |
|---|---|---|
| `docker ps` | Solo contenedores en ejecución | Lista vacía |
| `docker ps -a` | Todos los contenedores (en ejecución y detenidos) | Apareció el contenedor de `hello-world` con estado `Exited (0)` |

---

## Preguntas de reflexión

**1. ¿Qué es la imagen `hello-world`?**

Es una imagen muy pequeña, publicada oficialmente en Docker Hub, creada para comprobar que Docker funciona. Contiene un único programa que imprime un mensaje de bienvenida y termina. No es una aplicación útil por sí misma; su propósito es verificar que el cliente, el daemon y la descarga de imágenes están funcionando bien.

**2. ¿El contenedor quedó ejecutándose después de imprimir el mensaje?**

No. El contenedor vive mientras el programa que ejecuta siga corriendo. En este caso el programa solo imprime el mensaje y termina, así que el contenedor se detuvo de inmediato. Lo comprobé porque `docker ps` salió vacío y en `docker ps -a` aparece con estado `Exited (0)`.

**3. ¿Por qué aparece en `docker ps -a` pero no necesariamente en `docker ps`?**

Porque `docker ps` solo muestra contenedores que están en ejecución, y `docker ps -a` muestra todos, incluidos los detenidos. Como este contenedor ya terminó, aparece únicamente con la opción `-a`. Si el contenedor siguiera corriendo, aparecería en ambos.

**4. ¿Qué demuestra este primer ejemplo sobre Docker?**

Demuestra que con un solo comando puedo descargar una imagen desde un registro, crear un contenedor a partir de ella y ejecutarlo, sin instalar nada manualmente. También muestra que un contenedor está ligado al proceso que ejecuta (cuando el proceso termina, el contenedor se detiene) y que la imagen y el contenedor son cosas distintas: la imagen quedó descargada y el contenedor quedó creado aparte.
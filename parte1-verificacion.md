# Parte 1: Verificación de la instalación de Docker

## Objetivo

Comprobar que Docker quedó instalado correctamente y que puedo ejecutar comandos básicos desde la terminal.

## Entorno utilizado

- **Sistema operativo:** Windows (con Docker Desktop usando WSL 2)
- **Terminal:** PowerShell integrada en Visual Studio Code
- **Versión de Docker instalada:** 29.8.1 (build 4a63305)

---

## Comando ejecutado: `docker --version`

```powershell
docker --version
```

### Explicación

Este comando muestra la versión del cliente de Docker instalada en mi computadora. Sirve para confirmar que el programa existe, que la terminal lo reconoce y qué versión estoy usando.

### Resultado obtenido

```text
Docker version 29.8.1, build 4a63305
```

### Reflexión

Al principio la terminal no reconocía el comando `docker`. Eso pasó porque la terminal ya estaba abierta cuando instalé Docker, y no había cargado todavía la ruta del programa. Después de cerrar y volver a abrir VS Code, el comando funcionó. Esto me mostró que una instalación recién hecha no siempre se refleja de inmediato en una terminal que ya estaba abierta.

---

## Comando ejecutado: `docker info`

```powershell
docker info
```

### Explicación

Este comando muestra información general del cliente y del servidor (daemon) de Docker. Del lado del cliente aparecen la versión, el contexto de conexión y los plugins instalados. Del lado del servidor aparecen cuántos contenedores e imágenes hay, el controlador de almacenamiento, las redes y volúmenes disponibles, el kernel, el sistema operativo del host, la arquitectura, los CPUs y la memoria asignada.

Que aparezca la sección **Server** es importante: significa que el cliente logró comunicarse con el daemon y que Docker está realmente en ejecución.

### Resultado obtenido (parcial)

```text
Client:
 Version:    29.8.1
 Context:    desktop-linux
 Debug Mode: false
 Plugins:
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.37.1
  compose: Docker Compose (Docker Inc.)
    Version:  v5.5.1
  ...

Server:
 Containers: 0
  Running: 0
  Paused: 0
  Stopped: 0
 Images: 0
 Server Version: 29.8.1
 Storage Driver: overlayfs
 Logging Driver: json-file
 Cgroup Version: 2
 Plugins:
  Volume: local
  Network: bridge host ipvlan macvlan null overlay
 Swarm: inactive
 Runtimes: io.containerd.runc.v2 nvidia runc
 Default Runtime: runc
 Kernel Version: 6.6.87.2-microsoft-standard-WSL2
 Operating System: Docker Desktop
 OSType: linux
 Architecture: x86_64
 CPUs: 16
 Total Memory: 7.447GiB
 Name: docker-desktop
 ...
```

### Qué observé en esta salida

- **Containers: 0** e **Images: 0**: la instalación es nueva y todavía no he creado ni descargado nada.
- **OSType: linux** y **Kernel Version: ...microsoft-standard-WSL2**: aunque trabajo en Windows, los contenedores corren sobre un kernel Linux que proporciona WSL 2.
- **Network: bridge host ...**: Docker ya trae tipos de red disponibles, entre ellos `bridge`, que se usa por defecto.
- **Volume: local**: los volúmenes se manejan localmente.

### Reflexión

`docker info` me pareció el comando más útil de esta parte, porque no solo confirma que Docker funciona, sino que también muestra con qué recursos cuenta (CPUs, memoria) y sobre qué sistema corren los contenedores. Me llamó la atención ver que en Windows Docker usa un kernel Linux por debajo.

---

## Comando ejecutado: `docker help`

```powershell
docker help
```

### Explicación

Este comando muestra la lista de comandos de Docker y sus opciones globales, junto con una descripción corta de cada uno. Sirve como referencia rápida cuando no recuerdo cómo se llama un comando. Además, con `docker COMANDO --help` se puede ver la ayuda específica de cada uno.

### Resultado obtenido 

```text
Usage:  docker [OPTIONS] COMMAND

A self-sufficient runtime for containers

Common Commands:
  run         Create and run a new container from an image
  exec        Execute a command in a running container
  ps          List containers
  build       Build an image from a Dockerfile
  pull        Download an image from a registry
  push        Upload an image to a registry
  images      List images
  login       Authenticate to a registry
  logout      Log out from a registry
  search      Search Docker Hub for images
  version     Show the Docker version information
  info        Display system-wide information
  ...
```

### Evidencias

En la siguiente imagen se evidencia la instalación correcta de Docker:
![Docker instalado](evidencias/parte1-docker-instalado.png)

### Reflexión

Los comandos comunes (`run`, `ps`, `build`, `pull`, `images`) son justamente los que voy a usar en el resto del laboratorio. Ver la lista completa me da una idea de todo lo que Docker puede hacer, incluso si en este laboratorio solo voy a usar una parte.

---

## Por qué es importante verificar la instalación antes de continuar

Todas las partes siguientes dependen de que Docker esté instalado y funcionando. Si no verifico esto primero, un error más adelante (por ejemplo, al descargar una imagen o construir una) podría ser difícil de interpretar, porque no sabría si el problema está en el comando que escribí o en la instalación. Verificarlo al inicio permite descartar esa causa desde el comienzo.

---

## Preguntas de reflexión

**1. ¿Qué diferencia hay entre instalar Docker y tener Docker ejecutándose correctamente?**

Instalar Docker solo coloca los programas en la computadora. Tenerlo ejecutándose correctamente significa que el servicio (daemon) está activo y que el cliente puede comunicarse con él. En mi caso lo viví directamente: primero la terminal no reconocía `docker`, y aun después de instalarlo, necesité abrir Docker Desktop para que el motor arrancara. Solo cuando `docker info` mostró la sección *Server* pude confirmar que todo funcionaba.

**2. ¿Qué información útil muestra el comando `docker info`?**

Muestra la versión del cliente y del servidor, el contexto de conexión, la cantidad de contenedores (en ejecución, pausados y detenidos) y de imágenes, el controlador de almacenamiento, los tipos de red y de volumen disponibles, el kernel y sistema operativo donde corre el motor, la arquitectura, y los recursos (CPUs y memoria). Es útil tanto para verificar que Docker funciona como para diagnosticar problemas.

**3. ¿Por qué Docker necesita un servicio o daemon ejecutándose en segundo plano?**

Porque el comando `docker` que escribo en la terminal es solo un cliente: envía órdenes, pero quien realmente crea y administra los contenedores, las imágenes, las redes y los volúmenes es el daemon. Este debe estar activo permanentemente para mantener los contenedores en ejecución, gestionar los recursos y responder a las órdenes del cliente en cualquier momento. Si el daemon no está activo, el cliente no tiene con quién comunicarse y los comandos fallan.

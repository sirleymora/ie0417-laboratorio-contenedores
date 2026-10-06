# Laboratorio 2: Laboratorio de Contenedores

**Curso:** IE0417 - Diseño de Software para Ingeniería

**Universidad de Costa Rica, Escuela de Ingeniería Eléctrica**

**Docente:** Rafael Esteban Badilla Alvarado

**Estudiante:** Sirley Mora Chavarría


En este laboratorio practiqué el uso de contenedores con Docker: ejecutar contenedores, construir una imagen propia con un `Dockerfile`, publicar puertos, usar variables de entorno, persistir datos con volúmenes y bind mounts, y comunicar contenedores mediante redes. Todo el trabajo se hizo en Windows con Docker Desktop y PowerShell, dentro de Visual Studio Code.

---

## Índice

| Archivo | Contenido |
|---|---|
| [parte1-verificacion.md](parte1-verificacion.md) | Verificación de la instalación de Docker (`docker --version`, `docker info`, `docker help`) |
| [parte2-comandos-basicos.md](parte2-comandos-basicos.md) | Primer contenedor con `hello-world`, `docker ps` y `docker ps -a` |
| [parte3-imagenes-y-contenedores.md](parte3-imagenes-y-contenedores.md) | Imágenes y contenedores con Ubuntu; administración básica de contenedores (`--name`, `start`, `exec`, `stop`, `rm`) |
| [parte4-dockerfile.md](parte4-dockerfile.md) | Aplicación Flask, prueba local y construcción de la imagen con un `Dockerfile` |
| [parte5-puertos.md](parte5-puertos.md) | Publicación de puertos, logs e inspección de contenedores, y variables de entorno |
| [parte6-volumenes.md](parte6-volumenes.md) | Persistencia con volúmenes y bind mounts |
| [parte7-redes.md](parte7-redes.md) | Redes de Docker y comunicación entre servicios con Nginx y Redis |
| [parte8-limpieza.md](parte8-limpieza.md) | Limpieza de contenedores, imágenes y volúmenes; uso de espacio con `docker system df` |
| [app/](epp/) | Código de la aplicación: `app.py`, `requirements.txt` y `Dockerfile` |
| [evidencias/](Evidencias/) | Capturas de pantalla usadas como evidencia |

## Estructura del repositorio

```text
laboratorio-contenedores/
├── README.md
├── parte1-verificacion.md
├── parte2-comandos-basicos.md
├── parte3-imagenes-y-contenedores.md
├── parte4-dockerfile.md
├── parte5-puertos.md
├── parte6-volumenes.md
├── parte7-redes.md
├── parte8-limpieza.md
├── Evidencias/
└── App/
    ├── Dockerfile
    ├── app.py
    └── requirements.txt
```

---

## Reflexión final

**1. ¿Qué es un contenedor?**

Es una forma de ejecutar una aplicación junto con lo que necesita (librerías, configuración) en un entorno aislado y ligero. No incluye un sistema operativo completo, sino que comparte el kernel con la máquina anfitriona, por eso arranca rápido y ocupa poco. Lo vi en la práctica: un contenedor de Ubuntu parece un Linux completo, pero se crea en segundos y se elimina con un comando.

**2. ¿Qué problema resuelve Docker?**

Resuelve el problema de que una aplicación funcione en una computadora y no en otra por diferencias en el entorno. Al empaquetar la aplicación y sus dependencias en una imagen, esta se ejecuta igual en cualquier máquina que tenga Docker. En mi caso lo noté con Flask: pude ejecutarlo en un contenedor sin depender de lo que tuviera instalado en mi computadora.

**3. ¿Qué diferencia hay entre una imagen y un contenedor?**

La imagen es la plantilla, solo de lectura, que contiene lo necesario para ejecutar la aplicación. El contenedor es una instancia creada a partir de esa imagen, que puede estar en ejecución o detenida. De una misma imagen puedo crear muchos contenedores: por ejemplo, de `laboratorio-flask:1.0` salieron `app-lab`, `app-puertos`, `app-env` y otros más, todos independientes.

**4. ¿Qué diferencia hay entre un contenedor y una máquina virtual?**

Una máquina virtual incluye un sistema operativo completo con su propio kernel y reserva recursos para él, por lo que es más pesada y lenta de iniciar. Un contenedor comparte el kernel del anfitrión y solo incluye la aplicación y sus dependencias, por lo que es mucho más liviano y rápido. En `docker info` vi que mis contenedores usan el kernel de WSL 2, y la imagen de Ubuntu pesa solo 162 MB.

**5. ¿Qué aprendí sobre puertos?**

Aprendí que aunque la aplicación escuche en un puerto dentro del contenedor, no es accesible desde mi computadora hasta que lo publico con `-p PUERTO_HOST:PUERTO_CONTENEDOR`. Comprobé la diferencia en `docker ps`: `5000/tcp` cuando solo estaba declarado y `0.0.0.0:5000->5000/tcp` cuando estaba publicado. También vi que puedo usar otro puerto del host (8080) sin cambiar la aplicación, y que entonces `localhost:5000` deja de funcionar.

**6. ¿Qué aprendí sobre volúmenes?**

Aprendí que lo que se guarda dentro de un contenedor se pierde cuando este se elimina, y que los volúmenes permiten conservar datos fuera del contenedor. Lo comprobé con el archivo de `datos-lab`: eliminé el primer contenedor y un segundo contenedor lo siguió leyendo. También aprendí que un bind mount conecta una carpeta de mi computadora con el contenedor, lo cual sirve para desarrollar, aunque puede ocultar lo que la imagen tenía en esa ruta (como me pasó al ejecutarlo desde la carpeta equivocada).

**7. ¿Qué aprendí sobre redes?**

Aprendí que los contenedores conectados a la misma red pueden comunicarse entre sí usando el nombre del contenedor, sin necesidad de conocer su IP ni de publicar puertos hacia mi computadora. Lo vi con `curl http://servidor-web`, que devolvió la página de Nginx, y con `redis-cli -h redis-lab`, que respondió `PONG`. Entendí que así se conectan, por ejemplo, una aplicación y su base de datos.

**8. ¿En qué casos usaría Docker en un proyecto de software?**

Lo usaría para tener el mismo entorno de desarrollo en todo el equipo, para ejecutar servicios auxiliares (una base de datos, Redis o un servidor web) sin instalarlos en mi computadora, para probar aplicaciones en entornos limpios y para desplegar una aplicación de forma reproducible en otro servidor. También para proyectos con varios servicios que deben comunicarse entre sí.

**9. ¿Qué parte del laboratorio me pareció más útil?**

La parte que me pareció más importante fue ver la aplicación funcionando en `localhost` y cómo la página cambia al modificar `app.py` desde mi computadora, con el bind mount. Me ayudó a entender cómo se puede desarrollar con Docker sin reconstruir la imagen cada vez que cambio el código, y a ver de forma concreta cómo el contenedor usa los archivos de mi carpeta.

**10. ¿Qué parte me pareció más confusa?**

La parte 7, la de redes. Me costó entender cómo el nombre de un contenedor funciona como dirección dentro de la red, y fue donde más me confundí con los comandos: en el ejemplo con Redis ejecuté el cliente sin la parte final (`redis-cli -h redis-lab`), lo que levantó un segundo servidor en lugar de un cliente, y tuve que corregirlo. Me di cuenta de que lo que va después del nombre de la imagen es el comando que se ejecuta dentro del contenedor.

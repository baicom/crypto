# CRYPTO

Intercambio de mensajes seguros

## Porque

La idea de esta aplicacion nacio porque nuestros clientes no tenian conocimientos de criptografia asimetrica (por ejemplo gpg) y necesitabamos intercambiar mensajes de manera segura, con una interface simple para que puediera usarla cualquiera.

De esta manera no enviaban un password de un server en un mail en texto plano.

## Ayuda

El sistema posee dos modalidades: ONLINE generar un mensaje encriptado y guardarlo para compartir el link, TRADICIONAL interface para encriptar o desencriptar un texto sin almacenamiento. Para ambos modos hay que usar una clave para intercambiar información.

Los mensajes en modalidad ONLINE no son almacenados en texto plano, ya que al hacer click en el boton "Grabar" el navegador primero encripta los datos y luego los envia para generar el link de intercambio.

Ademas dicha modalidad permite darle un tiempo de expiración al mensaje y activar que sea destruido al leer, de esa manera la persona que recibe el link solo tendra esa oportunidad para leer el mensaje.

## Importante

Renombrar app.cfg-sample a app.cfg y editar con los parametros apropiados

El archivo app.wsgi esta pensado para correr con un servidor apache con la extension libapache2-mod-wsgi 

## TODO

- Cambiar el javascript para hacer 100% single page application
- Agregar mas documentacion 

## Autor

@agramajo


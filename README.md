# Gestor de Reparaciones para Técnicos

## 📍Introducción
  Esta página cuenta con un inicio a modo de publicidad, como si se tratara de una tienda en específico, pero cuenta con un sistema que por medio de un logueo o registro se puede acceder a la base de datos propia de la página, donde se puede cargar datos de reparaciones y actualizar su estado en: Pendiente, Finalizado o Cancelado. 
  
  Primero se crea un Cliente con sus correspondientes datos, al cual se le va a atribuir la reparación, y luego se crea esta última, la cual guarda el usuario que le dió inicio. Cada reparación contiene: fecha, descripción, costo y estado.
  
  También se puede editar tanto los datos del cliente como el de la reparación. Si se le cambia el nombre al cliente, la reparación se actualiza con el nuevo nombre ya que está vinculado por el id con el que se registró en la Base de Datos.
  - Es un CRUD aplicado a las reparaciones, se puede Crear, Leer, Actualizar y Borrar (En este último caso cambia el estado de Existencia de 1 a 0, para que siga estando en la BD).
  - Cuenta con diferencia de permisos según usuario o administrador.
  - 
  - Se le hicieron correcciones y quedan algunas cosas por mejorar, como la vista mobile.
  - Se puede crear un usuario en register, por defecto sin permisos admin. Un usuario de prueba es:
  - Permisos de usuario -> user: pablo Contraseña: pablo
  - Permisos de admin -> user: rodris Contraseña: admin

## 🔍URL
 La página de Gestoría para reparaciones se encuentra online en https://rodma99.pythonanywhere.com/

##  🚀Instalación
 Se puede instalar esta aplicación de manera local de diferentes maneras, mis pasos son:
 - En una Carpeta nueva clona el repositorio con GitBash:
 - git clone https://github.com/RodrigoMamaniF/GestorReparaciones.git
 - Abre la carpeta con Visual Studio Code, en la terminal crea un entorno virtual para instalar los requerimientos del proyecto:
 - virtualenv -p python3 GestorEnv (u otro nombre, es para el entorno)
 - pip install -r requirementsGestor.txt
 - Con XAMPP, activamos Apache y MySQL, y vamos al administrador desde el navegador: localhost/phpmyadmin/
 - Creamos una nueva BD desde phpMyAdmin y lo llamamos 'flask_login' para que lo tome el archivo python config, e importamos ...\GestorReparaciones\src\bd\flask_login 
 - Listo!
## Capturas:
 - Vista Usuario:
   <img width="1346" height="682" alt="3" src="https://github.com/user-attachments/assets/4454f230-9b87-4b01-bd29-f216ddf9a447" />
 - Vista Admin:
   <img width="1346" height="674" alt="5 admin" src="https://github.com/user-attachments/assets/6cdacd56-d16c-47b0-9c59-dfd89656be00" />
 - Agregar Reparación:
   <img width="1334" height="678" alt="10 Agregar reparación" src="https://github.com/user-attachments/assets/84c34450-300b-4a0e-8a25-f8b8fe4940fa" />

   


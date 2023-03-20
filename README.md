# Módulo para gestión de actividades mediante to do list y modelo GTD

## Hecho por Enrique Carretero Tato

### Descripción
En este módulo podemos gestionar actividades en base al Modelo GTD, el cual funciona de la siguiente manera:
- Hay que realizar una tarea, así que se apunta en la lista de tareas.
- Al terminar la jornada laboral, se revisa las tareas apuntadas y se asignan según su prioridad, estado y tipo de actividad GTD.
- Si la tarea se ha de realizar al día siguiente, se incluye en la lista de tareas ejecutables, que será la lista de tareas a realizar ese día.
- Si la tarea se ha de realizar dentro de un tiempo (menos de un mes) debido a un evento externo, se incluye en la lista Tickler File de corto plazo con una fecha un día antes de cuando se deba realizar. En cuanto llegue el día, se pasa a la lista de tareas ejecutables del día siguiente.
- Si la tarea se ha de realizar dentro de un tiempo mayor a un mes debido a un evento externo o no se conoce fecha de este último, se incluye en la lista Tickler File de largo plazo con una fecha un día antes de cuando se deba realizar (si se conoce). En cuanto llegue el día, se mira si hay fecha y se pasa a Ejecutables o Corto Plazo.
- Si la tarea es recurrente, se pasa al Tickler File de tareas recurrentes.
- Si es una tarea que no esté previsto realizar y no es urgente, se puede pasar a la incubadora. Al final del día laboral, se revisa la incubadora y se ve si hay espacio en la lista de ejecutables para incluir alguna de las tareas.

### Características
- Visualizar las tareas a realizar en base al Modelo GTD.
- Crear nuevas tareas y asignarlas según su prioridad, estado y tipo de actividad GTD.
- Marcar tareas realizadas y tenerlas guardadas.
- Ver las tareas que los usuarios tienen asignadas.
- Crear, modificar o borrar tipos de actividades, según las necesidades de la empresa.

### Basado en el siguiente módulo
- https://apps.odoo.com/apps/modules/14.0/todo_list/, creado por Cybrosys Techno Solutions.
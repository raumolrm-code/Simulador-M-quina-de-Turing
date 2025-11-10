Descripción general
Este ejecutable abre una aplicación de escritorio que permite observar, de manera visual y paso a paso, cómo una Máquina de Turing decide si una cadena pertenece a uno de diez lenguajes regulares predefinidos. La interfaz muestra la cinta, el cabezal de lectura/escritura y el estado actual de la máquina. Durante la ejecución, cada símbolo procesado se marca con ε para que la persona usuaria pueda seguir el rastro de lo que ya fue leído. Al finalizar, la aplicación informa si la cadena fue ACEPTADA o RECHAZADA y, en caso de error, explica qué símbolo se esperaba en ese punto.

Qué hace el programa
El programa simula una Máquina de Turing sin utilizar expresiones regulares ni librerías externas. Todas las decisiones se toman con una tabla de transiciones interna (listas paralelas: estActua, lecturas, escribeC, estsigui, mueveCab). La persona puede avanzar transición por transición con el botón Paso o activar la animación automática con Correr. Cuando una cadena es aceptada, el cabezal realiza un rebobinado visual de regreso a la posición inicial para cerrar la demostración de forma clara.

Por qué es útil
El ejecutable ayuda a comprender la relación entre lenguajes regulares, autómatas y máquinas de Turing desde una perspectiva práctica. Es una herramienta pensada para cursos de Lenguajes Formales y Autómatas, porque permite “ver” los estados como filtros, entender por qué se rechaza una cadena y comprobar, con ejemplos concretos, cómo la estructura del lenguaje guía el reconocimiento.

Cómo comenzar a usarlo
Al ejecutar el programa se muestra la ventana principal. La persona elige un lenguaje en el selector, escribe la cadena que desea evaluar y presiona Iniciar. A partir de allí, puede usar Paso para avanzar de a una transición o Correr para que el simulador se mueva automáticamente. Si la cadena es válida, aparecerá ACEPTADO en color verde y el cabezal volverá al inicio. Si no es válida, se mostrará RECHAZADO en color rojo y, justo debajo de la cinta, un mensaje “Se esperaba un:” indicando qué símbolo(s) eran válidos en ese punto. La barra de desplazamiento horizontal y un autoenfoque mantienen visible el cabezal cuando la cinta es larga.

Lenguajes incluidos (10)

(ab)*: vacía o repeticiones exactas de ab.
a(a|b)*b: empieza con a y termina con b.
01: ceros seguidos de unos (la vacía también vale).
a+b+c+: al menos una a, luego al menos una b, luego al menos una c.
Contiene “101” en binario.
Número par de ‘a’ sobre {a,b}.
(0|1)*00: termina exactamente en 00.
Longitud exacta 3 sobre {a,b,c}.
abc*: bloques en ese orden (la vacía vale).
(a|b)*a: termina en a.

Flujo de uso recomendado:

1) Seleccionar un lenguaje en el menú.
2) Escribir la cadena de entrada.
3) Presionar Iniciar.
4) Avanzar con Paso o animar con Correr.
5) Observar el resultado y, de ser necesario, leer “Se esperaba un: …” para comprender el rechazo.
6) Usar Reiniciar para probar otra cadena o cambiar de lenguaje.

Buenas prácticas y límites
Se recomienda comenzar con cadenas cortas y aumentar la longitud gradualmente. Si un símbolo no pertenece al alfabeto de un lenguaje, el simulador lo rechazará en el punto exacto y explicará qué se esperaba. Para efectos demostrativos y de claridad visual, la máquina solo se mueve hacia la derecha durante el reconocimiento y no modifica realmente el contenido de la cinta (más allá del marcado visual con ε). La longitud de la cinta está pensada para ejercicios de aula; si la cadena es muy larga, el desplazamiento horizontal y el autoenfoque mantienen el cabezal a la vista, aunque el desempeño visual puede variar según el equipo.

Mensajes y estados
• ACEPTADO (verde): la cadena pertenece al lenguaje seleccionado; el cabezal rebobina al inicio.
• RECHAZADO (rojo): la cadena no cumple el lenguaje; debajo de la cinta se muestra “Se esperaba un: …”.
• Fin de cadena en estado no final: el mensaje aclara que faltó un símbolo o que no es permitido terminar en ese punto.

import numpy as np
import matplotlib.pyplot as plt


# Parámetros de la simulación
mediaN = 5
desviacionN = 3
personas = 100
nroCajas = 3
tiempo_llegada_media = 3
pagarEfectivo = 0.4

# Verificación de número de cajas
if nroCajas > 5:
    print("El numero de cajas es muy grande, se recomienda un numero menor a 5")
    exit()

# Definición de la clase Cliente
class Cliente:
    def __init__(self, id, productos):
        self.id = id
        self.productos = productos
        self.tiempo_atencion = self.generar_tiempo_atencion()
        self.tiempo_pago = self.generar_tiempo_pago(pagarEfectivo)

    def generar_tiempo_atencion(self):
        # Genera el tiempo de atención basado en una distribución normal
        tiempo = np.random.normal(5,3) # Escala el tiempo según la cantidad de productos
        while tiempo <= 0:
            tiempo = np.random.normal(5,3) # Asegura que el tiempo no sea negativo
        return tiempo


    def generar_tiempo_pago(self, pagarEfectivo):
        # Determina el tiempo de pago basado en si paga en efectivo o no
        if np.random.rand() < pagarEfectivo:
            return 2  # Pago en efectivo (2 minutos)
        else:
            return (70 / 60)  # Pago con otro medio (en minutos)

# Definición de la clase Caja
class Caja:
    def __init__(self):
        self.clientes = []
        self.tiempo_libre = 0  # Tiempo en que la caja estará libre para el siguiente cliente

    def atender_cliente(self, cliente, tiempo_actual):
        # Calcula el tiempo de espera basado en la disponibilidad de la caja
        tiempo_espera = max(0, self.tiempo_libre - tiempo_actual)
        
        # Actualiza el tiempo libre de la caja
        self.tiempo_libre = max(self.tiempo_libre, tiempo_actual) + cliente.tiempo_atencion + cliente.tiempo_pago
        
        # Devuelve el tiempo de espera
        return tiempo_espera

def asignarMejorCaja(cajas, tiempo_actual):
    # Selecciona la caja con menos tiempo libre
    caja = cajas[0]
    for c in cajas:
        if c.tiempo_libre < tiempo_actual:
            caja = c
            break
    return caja

# Función para simular la atención de los clientes
def simular(personas, nroCajas, tiempo_llegada_media):
    cajas = [Caja() for _ in range(nroCajas)]
    tiempos_espera = []
    tiempos_atencion = [[] for _ in range(nroCajas)]
    tiempo_actual = 0  # Variable para llevar el tiempo acumulado de llegada
    tiempos_llegada = []  # Lista para guardar los tiempos de llegada de cada cliente

    # Iteración para simular la llegada de cada cliente
    for i in range(personas):
        # Generar el tiempo de llegada del cliente con una distribución Poisson
        tiempo_llegada = np.random.poisson(tiempo_llegada_media)
        tiempo_actual += tiempo_llegada  # Acumular tiempo de llegada
        tiempos_llegada.append(tiempo_actual)  # Guardar el tiempo de llegada acumulado
        
        productos = int(np.random.normal(mediaN, desviacionN))
        while productos <= 0:
            productos = int(np.random.normal(mediaN, desviacionN))
        
        cliente = Cliente(i, productos)
        # print(f'Cliente {i+1} llega en el minuto {tiempo_actual} con {productos} productos y tardara "{cliente.tiempo_atencion} + {cliente.tiempo_pago}" minutos en finalizar la compra')
        # for i in range(nroCajas):
        #     print(f'Caja {i+1} va a estar libre en el minuto {cajas[i].tiempo_libre}, es decir que debe esperar {max(0, cajas[i].tiempo_libre - tiempo_actual)} minutos')

        # Seleccionar la caja con menos tiempo libre (la más disponible)
        caja = asignarMejorCaja(cajas, tiempo_actual)


        # Calcular el tiempo de espera del cliente en la caja seleccionada
        tiempo_espera = caja.atender_cliente(cliente, tiempo_actual)
        tiempos_espera.append(tiempo_espera)
        
        # Registrar el tiempo de atención de este cliente
        tiempos_atencion[cajas.index(caja)].append(cliente.tiempo_atencion + cliente.tiempo_pago)

    return tiempos_espera, tiempos_atencion, tiempos_llegada

# Función para visualizar los resultados
def visualizar(tiempos_espera, tiempos_atencion):
    # Crear subgráficas
    nroCajas = len(tiempos_atencion)
    total_graficas = nroCajas + 1  # Total de gráficos: uno por cada caja y uno para el tiempo de espera

    # Determinar el número de filas y columnas necesario para acomodar todas las subgráficas
    columnas = 2
    filas = (total_graficas + 1) // columnas

    # Crear subgráficas dinámicamente
    fig, axs = plt.subplots(filas, columnas, figsize=(12, filas * 5))
    axs = axs.flatten()  # Aplanar los ejes para un acceso más fácil

    # Graficar tiempos de atención por caja
    for i, tiempos in enumerate(tiempos_atencion):
        axs[i].plot(tiempos, label=f'Tiempos de Atención - Caja {i+1}')
        axs[i].set_title(f'Tiempo de Atención por Caja {i+1}')
        axs[i].set_xlabel('Cliente')
        axs[i].set_ylabel('Tiempo de Atención (min)')
        axs[i].legend()

    # Graficar tiempos de espera en el siguiente eje disponible
    axs[nroCajas].plot(tiempos_espera, label='Tiempo de Espera', color='orange')
    axs[nroCajas].set_title('Tiempo de Espera de Clientes')
    axs[nroCajas].set_xlabel('Cliente')
    axs[nroCajas].set_ylabel('Tiempo de Espera (min)')
    axs[nroCajas].legend()

    # Ocultar cualquier eje adicional no utilizado
    for j in range(total_graficas, len(axs)):
        fig.delaxes(axs[j])

    plt.tight_layout()  # Ajustar el espacio entre subgráficas
    plt.show()

# Ejecución de la simulación
tiempos_espera, tiempos_atencion, tiempos_llegada = simular(personas, nroCajas, tiempo_llegada_media)

# Visualizar resultados
visualizar(tiempos_espera, tiempos_atencion)

# Imprimir resultados
print(f'Simulacion hecha con los siguientes valores:')
print(f'Numero de personas: {personas}')
print(f'Numero de cajas: {nroCajas}')
print(f'Tiempo de llegada medio: {tiempo_llegada_media}')
print(f'Tiempo de espera promedio: {np.mean(tiempos_espera)} minutos')

# Imprimir los tiempos de espera y atención
# print(f'Tiempos de espera de los clientes: {tiempos_espera}')
# print(f'Tiempos de atencion de los clientes: {tiempos_atencion}')
# print(f'Tiempos de llegada de cada cliente: {tiempos_llegada}')
for i in range(nroCajas):
    print(f'Cantidad de clientes atendidos por Caja {i+1}: {len(tiempos_atencion[i])}')
import numpy as np
import matplotlib.pyplot as plt

class Cliente:
    def __init__(self, id, productos):
        self.id = id
        self.productos = productos
        self.tiempo_atencion = self.generar_tiempo_atencion()
        self.tiempo_pago = self.generar_tiempo_pago()

    def generar_tiempo_atencion(self):
        tiempo = np.random.normal(5, 3)
        return max(tiempo, 0)

    def generar_tiempo_pago(self, p=0.4):
        if np.random.rand() < p:
            return 2  # Pago en efectivo
        else:
            return 70 / 60  # Pago en otro medio (en minutos)

class Caja:
    def __init__(self):
        self.clientes = []
        self.tiempo_libre = 0

    def atender_cliente(self, cliente):
        self.clientes.append(cliente)
        self.tiempo_libre += cliente.tiempo_atencion + cliente.tiempo_pago

def simular(personas=5, nroCajas=4, tiempo_llegada_media=3):
    cajas = [Caja() for _ in range(nroCajas)]
    tiempos_espera = []
    tiempos_atencion = [[] for _ in range(nroCajas)]
    
    for i in range(personas):
        tiempo_llegada = np.random.poisson(tiempo_llegada_media)
        productos = np.random.randint(1, 11)
        cliente = Cliente(i, productos)

        caja = min(cajas, key=lambda c: len(c.clientes))

        tiempos_espera.append(caja.tiempo_libre)
        caja.atender_cliente(cliente)
        caja.tiempo_libre += tiempo_llegada
        tiempos_atencion[cajas.index(caja)].append(cliente.tiempo_atencion + cliente.tiempo_pago)

    return tiempos_espera, tiempos_atencion

# Función para visualizar resultados
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
tiempos_espera_fila_unica, tiempos_atencion_fila_unica = simular()

# Visualizar resultados
visualizar(tiempos_espera_fila_unica, tiempos_atencion_fila_unica)

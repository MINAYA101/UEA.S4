"""
Programa para calcular el promedio semanal del clima usando Programación Tradicional
"""

# CONSTANTES
DIAS_SEMANA = 7  # Número de días en una semana

def obtener_temperatura_diaria(dia):
    """
    Solicita al usuario la temperatura para un día específico.
    
    Args:
        dia (int): Número del día (1-7)
    
    Returns:
        float: Temperatura ingresada por el usuario
    """
    while True:
        try:
            temperatura = float(input(f"Ingrese la temperatura del día {dia} (°C): "))
            return temperatura
        except ValueError:
            print("Error: Por favor ingrese un número válido.")

def ingresar_temperaturas_semanales():
    """
    Recopila las temperaturas para los 7 días de la semana.
    
    Returns:
        list: Lista con las temperaturas de la semana
    """
    temperaturas = []
    print("\n" + "="*50)
    print("INGRESO DE TEMPERATURAS SEMANALES")
    print("="*50)
    
    for dia in range(1, DIAS_SEMANA + 1):
        temp = obtener_temperatura_diaria(dia)
        temperaturas.append(temp)
    
    return temperaturas

def calcular_promedio_semanal(temperaturas):
    """
    Calcula el promedio de temperaturas para la semana.
    
    Args:
        temperaturas (list): Lista de temperaturas
    
    Returns:
        float: Promedio semanal de temperaturas
    """
    if not temperaturas:  # Verifica si la lista está vacía
        return 0.0
    
    suma = sum(temperaturas)
    promedio = suma / len(temperaturas)
    return round(promedio, 2)  # Redondea a 2 decimales

def mostrar_resultados(temperaturas, promedio):
    """
    Muestra las temperaturas ingresadas y el promedio calculado.
    
    Args:
        temperaturas (list): Lista de temperaturas
        promedio (float): Promedio semanal
    """
    print("\n" + "="*50)
    print("RESULTADOS DEL PROMEDIO SEMANAL")
    print("="*50)
    
    # Mostrar temperaturas diarias
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    for i, (dia, temp) in enumerate(zip(dias, temperaturas), 1):
        print(f"Día {i} ({dia}): {temp}°C")
    
    # Mostrar promedio
    print("\n" + "-"*30)
    print(f"PROMEDIO SEMANAL: {promedio}°C")
    print("-"*30)
    
    # Clasificación del clima según el promedio
    if promedio < 10:
        clasificacion = "Muy frío"
    elif promedio < 20:
        clasificacion = "Frío"
    elif promedio < 25:
        clasificacion = "Templado"
    elif promedio < 30:
        clasificacion = "Cálido"
    else:
        clasificacion = "Muy cálido"
    
    print(f"Clasificación: {clasificacion}")

def main():
    """
    Función principal que coordina la ejecución del programa.
    """
    print("PROGRAMA PARA CALCULAR EL PROMEDIO SEMANAL DEL CLIMA")
    print("(Programación Tradicional)")
    
    # Paso 1: Ingresar temperaturas
    temperaturas = ingresar_temperaturas_semanales()
    
    # Paso 2: Calcular promedio
    promedio = calcular_promedio_semanal(temperaturas)
    
    # Paso 3: Mostrar resultados
    mostrar_resultados(temperaturas, promedio)
    
    # Opcional: Permitir al usuario repetir el proceso
    while True:
        respuesta = input("\n¿Desea calcular otro promedio? (s/n): ").lower()
        if respuesta == 's':
            main()  # Reiniciar el programa
            break
        elif respuesta == 'n':
            print("\n¡Gracias por usar el programa!")
            break
        else:
            print("Por favor ingrese 's' o 'n'.")

# Punto de entrada del programa
if __name__ == "__main__":
    main()
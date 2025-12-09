import sys
import io

try:
    # Python 3.7+ tiene reconfigure
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    try:
        # Fallback para versiones antiguas / entornos donde reconfigure no está disponible
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except Exception:
        # Si no podemos forzar UTF-8, continuamos (evita crash en import)
        pass

class CriaturaMagica:
    """
    Clase base que representa una criatura mágica genérica.
    Define los atributos básicos y comportamientos comunes.
    """
    
    def __init__(self, nombre, potencia, sabiduria, resistencia, salud):
        """
        Inicializa una nueva criatura mágica.
        
        Args:
            nombre (str): Nombre de la criatura
            potencia (int): Poder de ataque físico
            sabiduria (int): Poder de habilidades mágicas
            resistencia (int): Capacidad para reducir daño
            salud (int): Puntos de vida
        """
        self.nombre = nombre
        self.potencia = potencia
        self.sabiduria = sabiduria
        self.resistencia = resistencia
        self.salud = salud
    
    def mostrar_estadisticas(self):
        """
        Muestra todas las estadísticas de la criatura de forma formateada.
        """
        print(f"\n═══ ESTADÍSTICAS DE {self.nombre.upper()} ═══")
        print(f"• Potencia: {self.potencia}")
        print(f"• Sabiduría: {self.sabiduria}")
        print(f"• Resistencia: {self.resistencia}")
        print(f"• Salud: {self.salud}")
    
    def evolucionar(self, aumento_potencia, aumento_sabiduria, aumento_resistencia):
        """
        Mejora los atributos de la criatura después de ganar experiencia.
        
        Args:
            aumento_potencia (int): Incremento en potencia
            aumento_sabiduria (int): Incremento en sabiduría
            aumento_resistencia (int): Incremento en resistencia
        """
        self.potencia += aumento_potencia
        self.sabiduria += aumento_sabiduria
        self.resistencia += aumento_resistencia
        print(f"{self.nombre} ha evolucionado! +{aumento_potencia}POT, +{aumento_sabiduria}SAB, +{aumento_resistencia}RES")
    
    def esta_con_vida(self):
        """
        Verifica si la criatura aún tiene salud positiva.
        
        Returns:
            bool: True si la criatura está viva, False en caso contrario
        """
        return self.salud > 0
    
    def derrotar(self):
        """
        Establece la salud a cero, indicando que la criatura ha sido derrotada.
        """
        self.salud = 0
        print(f"{self.nombre} ha sido derrotado!")
    
    def calcular_dano(self, oponente):
        """
        Calcula el daño base que inflige esta criatura al oponente.
        
        Args:
            oponente (CriaturaMagica): La criatura que recibe el daño
            
        Returns:
            int: Puntos de daño calculados
        """
        # Daño base = Potencia - Resistencia del oponente
        return self.potencia - oponente.resistencia
    
    def ejecutar_ataque(self, oponente):
        """
        Realiza un ataque contra otra criatura.
        
        Args:
            oponente (CriaturaMagica): La criatura objetivo del ataque
        """
        dano_infligido = self.calcular_dano(oponente)
        
        # Asegurar que el daño sea al menos 1
        dano_infligido = max(1, dano_infligido)

        # Reducir la salud del oponente y asegurar que no quede negativa
        oponente.salud -= dano_infligido
        oponente.salud = max(0, oponente.salud)

        # Mostrar información del ataque
        print(f"{self.nombre} ataca a {oponente.nombre} causando {dano_infligido} puntos de daño")
        
        # Verificar estado del oponente
        if oponente.esta_con_vida():
            print(f"Salud de {oponente.nombre}: {oponente.salud}")
        else:
            # Si la salud es 0 o menor, normalizamos y anunciamos la derrota
            oponente.derrotar()


class Dragon(CriaturaMagica):
    """
    Representa un dragón, criatura poderosa que utiliza garras y aliento de fuego.
    Su daño se multiplica por la longitud de sus garras.
    """
    
    def __init__(self, nombre, potencia, sabiduria, resistencia, salud, longitud_garras):
        """
        Inicializa un dragón con sus atributos especiales.
        
        Args:
            longitud_garras (int): Longitud de las garras que multiplica el daño
        """
        super().__init__(nombre, potencia, sabiduria, resistencia, salud)
        self.longitud_garras = longitud_garras
    
    def cambiar_garras(self):
        """
        Permite cambiar el tipo de garras del dragón, afectando su multiplicador de daño.
        """
        print(f"\nSelecciona nuevas garras para {self.nombre}:")
        print("1. Garras de Obsidiana - Multiplicador x6")
        print("2. Garras de Diamante - Multiplicador x8")
        print("3. Garras de Fénix - Multiplicador x10")
        
        try:
            seleccion = int(input("Opción (1-3): "))
            
            if seleccion == 1:
                self.longitud_garras = 6
                print(f"{self.nombre} ahora tiene Garras de Obsidiana (x6)")
            elif seleccion == 2:
                self.longitud_garras = 8
                print(f"{self.nombre} ahora tiene Garras de Diamante (x8)")
            elif seleccion == 3:
                self.longitud_garras = 10
                print(f"{self.nombre} ahora tiene Garras de Fénix (x10)")
            else:
                print("Opción inválida. Se mantienen las garras actuales.")
        except ValueError:
            print("Entrada no válida. Se mantienen las garras actuales.")
    
    def mostrar_estadisticas(self):
        """
        Muestra estadísticas incluyendo el atributo especial del dragón.
        """
        super().mostrar_estadisticas()
        print(f"• Longitud de Garras: {self.longitud_garras} (multiplicador de daño)")
    
    def calcular_dano(self, oponente):
        """
        Sobrescribe el cálculo de daño para incluir el multiplicador de garras.
        
        Args:
            oponente (CriaturaMagica): La criatura que recibe el daño
            
        Returns:
            int: Daño calculado con multiplicador
        """
        # Daño del dragón = Potencia × Longitud de garras - Resistencia del oponente
        return (self.potencia * self.longitud_garras) - oponente.resistencia


class Hechicero(CriaturaMagica):
    """
    Representa un hechicero, criatura mágica que utiliza grimorios para potenciar sus hechizos.
    Su daño se multiplica por el poder de su grimorio.
    """
    
    def __init__(self, nombre, potencia, sabiduria, resistencia, salud, poder_grimorio):
        """
        Inicializa un hechicero con su grimorio mágico.
        
        Args:
            poder_grimorio (int): Poder del grimorio que multiplica el daño mágico
        """
        super().__init__(nombre, potencia, sabiduria, resistencia, salud)
        self.poder_grimorio = poder_grimorio
    
    def mostrar_estadisticas(self):
        """
        Muestra estadísticas incluyendo el atributo especial del hechicero.
        """
        super().mostrar_estadisticas()
        print(f"• Poder del Grimorio: {self.poder_grimorio} (multiplicador de hechizos)")
    
    def calcular_dano(self, oponente):
        """
        Sobrescribe el cálculo de daño para utilizar sabiduría y grimorio.
        
        Args:
            oponente (CriaturaMagica): La criatura que recibe el daño
            
        Returns:
            int: Daño mágico calculado
        """
        # Daño del hechicero = Sabiduría × Poder del grimorio - Resistencia del oponente
        return (self.sabiduria * self.poder_grimorio) - oponente.resistencia


def ejecutar_combate(combatiente_1, combatiente_2):
    """
    Simula un combate por turnos entre dos criaturas mágicas.
    
    Args:
        combatiente_1 (CriaturaMagica): Primer participante del combate
        combatiente_2 (CriaturaMagica): Segundo participante del combate
    """
    turno_actual = 1
    
    print(f"\n{'='*60}")
    print(f"¡COMBATE MÁGICO: {combatiente_1.nombre} vs {combatiente_2.nombre}!")
    print(f"{'='*60}")
    
    # Ciclo de combate mientras ambos combatientes estén con vida
    while combatiente_1.esta_con_vida() and combatiente_2.esta_con_vida():
        print(f"\n{'~'*30} TURNO {turno_actual} {'~'*30}")
        
        # Turno del primer combatiente
        print(f"\n Acción de {combatiente_1.nombre}:")
        combatiente_1.ejecutar_ataque(combatiente_2)
        
        # Si el segundo combatiente sigue con vida, tiene su turno
        if combatiente_2.esta_con_vida():
            print(f"\n Acción de {combatiente_2.nombre}:")
            combatiente_2.ejecutar_ataque(combatiente_1)
        
        turno_actual += 1
    
    # Mostrar resultado final del combate
    print(f"\n{'='*60}")
    print("RESULTADO FINAL DEL COMBATE")
    print(f"{'='*60}")
    
    if combatiente_1.esta_con_vida() and combatiente_2.esta_con_vida():
        print("¡Empate! Ambas criaturas permanecen en pie.")
    elif combatiente_1.esta_con_vida():
        print(f"¡{combatiente_1.nombre} es el vencedor!")
    elif combatiente_2.esta_con_vida():
        print(f"¡{combatiente_2.nombre} es el vencedor!")
    else:
        print("¡Ambas criaturas han caído en combate!")


# ============================================
# PROGRAMA PRINCIPAL - DEMOSTRACIÓN DEL SISTEMA
# ============================================

def main():
    """
    Función principal que demuestra el sistema de criaturas mágicas.
    """
    print("="*60)
    print("SISTEMA DE CRIATURAS MÁGICAS - DEMOSTRACIÓN")
    print("="*60)
    
    # Creación de las criaturas
    dragon_fuego = Dragon("Ignarius", 18, 8, 5, 120, 7)
    hechicero_arcano = Hechicero("Merlina", 6, 22, 4, 100, 4)
    
    # Mostrar estadísticas iniciales
    print("\nESTADÍSTICAS INICIALES DE LAS CRIATURAS:")
    dragon_fuego.mostrar_estadisticas()
    hechicero_arcano.mostrar_estadisticas()
    
    # Demostración de evolución (mejora de atributos)
    print("\nDEMOSTRACIÓN DE EVOLUCIÓN:")
    dragon_fuego.evolucionar(3, 1, 2)
    hechicero_arcano.evolucionar(1, 4, 1)
    
    # Mostrar estadísticas después de evolucionar
    print("\nESTADÍSTICAS DESPUÉS DE EVOLUCIONAR:")
    dragon_fuego.mostrar_estadisticas()
    hechicero_arcano.mostrar_estadisticas()
    
    # Ejecutar combate
    ejecutar_combate(dragon_fuego, hechicero_arcano)
    
    print("\n" + "="*60)
    print("FIN DE LA DEMOSTRACIÓN")
    print("="*60)

# Punto de entrada del programa
if __name__ == "__main__":
    main()

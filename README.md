# GSPH Toolkit – Heurísticas Educativas para el Problema del Viajante (TSP)

## ¿Qué es el TSP (Travelling Salesman Problem / Problema del Vendedor Viajero)?

El **TSP (Travelling Salesman Problem)** es uno de los problemas más clásicos e importantes en la optimización combinatoria. Consiste en encontrar la **ruta más corta posible** que recorra un conjunto de ciudades **una sola vez** y regrese al punto de origen, **minimizando la distancia total recorrida**.

---

### Ejemplo aplicado:
> Un camión de reparto debe entregar paquetes en 15 comunas de una región. Si no planifica bien su ruta, podría recorrer muchos kilómetros extra. Además, la planificación debe realizarse rápidamente para ser práctica en la vida real.

---
## 📏 Parámetros a evaluar

A continuación se describen las métricas que utilizamos para comparar las heurísticas.  

| Parámetro | ¿Qué mide? | Fórmula / Cálculo | Unidades |
|-----------|------------|-------------------|----------|
| **Longitud total del tour** | Suma de todas las distancias entre nodos consecutivos (incluyendo el regreso al origen). Refleja la **calidad** de la solución: cuanto más corta, mejor. | $L = \sum_{i=1}^{n} d(p_i, p_{i+1})$, donde $p_{n+1}=p_1$ | metros, kilómetros o unidades TSPLIB |
| **Tiempo de ejecución** | Tiempo que el algoritmo tarda en construir la solución. Indica la **eficiencia computacional**. | $t = t_{fin} - t_{inicio}$ | segundos (s) |
| **BKS (Best Known Solution)** | La mejor longitud reportada en la literatura o repositorios oficiales para la instancia. Sirve como referencia de "piso". | — (dato externo) | mismas que *Longitud* |
| **GAP** | Diferencia relativa entre nuestra longitud y el BKS; indica **qué tan lejos** estamos del óptimo conocido. | $GAP = \frac{L_{heur} - L_{BKS}}{L_{BKS}} \times 100\%$ | porcentaje (%) |

> **Resumen:**  
> 1. *Longitud* evalúa la **calidad** del tour.  
> 2. *Tiempo de ejecución* evalúa la **velocidad** del algoritmo.  
> 3. *BKS* nos da un punto de referencia externo.  
> 4. *GAP* combina ambos valores para medir el **desempeño relativo** de la heurística.

## Nuestra Propuesta: GSPH (Gómez Spatial Partition Heuristic)

### ¿Qué es GSPH?

GSPH es una heurística que resuelve el TSP utilizando una estrategia **espacial**: divide el plano geográfico en subzonas según la densidad de ciudades, resuelve rutas locales dentro de cada subzona y luego **conecta las subrutas** de manera inteligente.

### ¿Por qué esta estrategia?

- **Reduce la complejidad** del problema completo.
- **Acelera los tiempos de ejecución.**
- **Imita cómo los humanos resuelven rutas:** por sectores o zonas.

---

### Ejemplo ilustrativo:
> Imagina que tienes que visitar 50 clientes en una ciudad. Lo natural sería dividir por zonas: primero los del centro, luego los del norte, después los del sur, etc. GSPH automatiza esta idea utilizando geometría y densidad.
---

## Mejora de la Propuesta: GSPH‑FC (GSPH con Filtro de Clústeres)

### ¿Qué es GSPH‑FC?

GSPH-FC es una **extensión mejorada de GSPH** que incorpora un sistema de penalización para evitar agrupaciones ineficientes. Controla que los clústeres generados:
- no sean demasiado desbalanceados,
- no incluyan puntos aislados o alejados,
- sean más compactos y cohesionados.

---

### ¿Qué mejora respecto a GSPH?

- Utiliza un parámetro llamado `cluster_factor` para regular la cohesión de los grupos.
- Penaliza agrupaciones pobres o dispersas.
- Mejora la calidad del tour final con una ruta más balanceada.

---

### Ejemplo aplicado:
> Supongamos que el algoritmo agrupa dos comunas muy lejanas en una misma zona: eso aumenta la distancia del tour. GSPH-FC corrige este tipo de situaciones, actuando como un "supervisor" de las zonas generadas por GSPH.

---

## 🚀 Cómo ejecutar una instancia manualmente

Para probar cualquiera de las heurísticas con un conjunto de datos específico, se puede utilizar el script `manual_test.py` que facilita la ejecución y comparación:

```bash
python manual_test.py <nombre_de_la_heuristica> instances/<nombre_instancia_tsp.tsp> --plot
```

### Parámetros:

1. **nombre_de_la_heuristica**: Algoritmo a utilizar. Opciones disponibles:
   - `tsp_clasico`: Implementación básica con mejora 2-opt
   - `gsph_fc`: Nuestra propuesta mejorada GSPH con Filtro de Clústeres

2. **nombre_instancia_tsp.tsp**: Archivo de instancia en formato TSPLIB ubicado en la carpeta `instances/`

3. **--plot**: Parámetro opcional que genera una visualización gráfica de la solución

### Ejemplo de uso:

```bash
python manual_test.py gsph_fc instances/a280.tsp --plot
```

### Resultados:

Al ejecutar el comando, se genera:

1. Una carpeta llamada `results_manual_test_<nombre_instancia>` que contiene:
   - Un archivo de texto `resultado.txt` con información sobre:
     - Algoritmo utilizado
     - Nombre de la instancia
     - Longitud total del tour
     - Tiempo de ejecución
   - Si se usa la opción `--plot`, un archivo PNG `grafico_<algoritmo>.png` que muestra visualmente el tour encontrado

También se muestra en la terminal un resumen con los datos principales de la ejecución.

---

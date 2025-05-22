# GSPH Toolkit – Heurísticas Educativas para el Problema del Viajante (TSP)

## ¿Qué es el TSP (Travelling Salesman Problem / Problema del Vendedor Viajero)?

El **TSP (Travelling Salesman Problem)** es uno de los problemas más clásicos e importantes en la optimización combinatoria. Consiste en encontrar la **ruta más corta posible** que recorra un conjunto de ciudades **una sola vez** y regrese al punto de origen, **minimizando la distancia total recorrida**.

---

### Ejemplo aplicado:
> Un camión de reparto debe entregar paquetes en 15 comunas de una región. Si no planifica bien su ruta, podría recorrer muchos kilómetros extra. Además, la planificación debe realizarse rápidamente para ser práctica en la vida real.

**Imagen sugerida:**  
Mapa de las municipalidades de la Región Metropolitana de Santiago mostrando una ruta TSP tradicional.

---

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

**Imagen sugerida:**  
Visualización de GSPH aplicado a la Región Metropolitana, con zonas diferenciadas y subrutas conectadas.

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
> Supongamos que el algoritmo agrupa dos comunas muy lejanas en una misma zona: eso aumenta la distancia del tour. GSPH-FC corrige este tipo de situaciones, actuando como un “supervisor” de las zonas generadas por GSPH.

**Imagen sugerida:**  
Mapa de la Región Metropolitana con agrupaciones optimizadas por GSPH-FC, mostrando mejoras respecto al caso anterior.

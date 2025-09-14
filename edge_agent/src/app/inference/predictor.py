def edge_predict(data):
    entrada = data.entrada
    # Simulación distinta del cloud
    if "urgente" in entrada.lower():
        return "prioridad_alta"
    return "edge_normal"

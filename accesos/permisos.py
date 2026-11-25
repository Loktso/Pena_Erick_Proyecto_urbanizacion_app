def es_administrador(usuario):
    """True si es superusuario o pertenece al grupo 'administradores'."""
    if not usuario.is_authenticated:
        return False
    return usuario.is_superuser or usuario.groups.filter(name='administradores').exists()


def puede_modificar(usuario, objeto):
    """Regla de propiedad: el administrador modifica todo; los demás, solo lo que crearon."""
    return es_administrador(usuario) or objeto.creado_por_id == usuario.id
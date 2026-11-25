from accesos.urls.visitante_urls import urlpatterns as visitante_urls
from accesos.urls.registro_acceso_urls import urlpatterns as registro_urls

# Aquí se suman las rutas de cada entidad
urlpatterns = []
urlpatterns += registro_urls
urlpatterns += visitante_urls
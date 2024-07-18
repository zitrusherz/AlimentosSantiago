from gestion_pedidos.models import Plato

platos_data = [
    {'nombre': 'arroz', 'imagen': 'images/platos/arroz.png'},
    {'nombre': 'bebida', 'imagen': 'images/platos/bebida.png'},
    {'nombre': 'chupedelocos', 'imagen': 'images/platos/chupedelocos.png'},
    {'nombre': 'congrioalaplancha', 'imagen': 'images/platos/congrioalaplancha.png'},
    {'nombre': 'congriofrio', 'imagen': 'images/platos/congriofrio.png'},
    {'nombre': 'corona', 'imagen': 'images/platos/corona.png'},
    {'nombre': 'costillarahumado', 'imagen': 'images/platos/costillarahumado.png'},
    {'nombre': 'empanadaqueso', 'imagen': 'images/platos/empanadaqueso.png'},
    {'nombre': 'empanaditadeplateada', 'imagen': 'images/platos/empanaditadeplateada.png'},
    {'nombre': 'ensaladachilena', 'imagen': 'images/platos/ensaladachilena.png'},
    {'nombre': 'escalopaElcomilon', 'imagen': 'images/platos/escalopaElcomilon.png'},
    {'nombre': 'filetealajillo', 'imagen': 'images/platos/filetealajillo.png'},
    {'nombre': 'filetealaparrilla', 'imagen': 'images/platos/filetealaparrilla.png'},
    {'nombre': 'fileteelcomilon', 'imagen': 'images/platos/fileteelcomilon.png'},
    {'nombre': 'filetetiroles', 'imagen': 'images/platos/filetetiroles.png'},
    {'nombre': 'lecheasada', 'imagen': 'images/platos/lecheasada.png'},
    {'nombre': 'merluzaaustralalaplancha', 'imagen': 'images/platos/merluzaaustralalaplancha.png'},
    {'nombre': 'mixempanada', 'imagen': 'images/platos/mixempanada.png'},
    {'nombre': 'papasduquesas', 'imagen': 'images/platos/papasduquesas.png'},
    {'nombre': 'papafritas', 'imagen': 'images/platos/papafritas.png'},
    {'nombre': 'pasteldechoclo', 'imagen': 'images/platos/pasteldechoclo.png'},
    {'nombre': 'pechugadepollo', 'imagen': 'images/platos/pechugadepollo.png'},
    {'nombre': 'plateadaalhorno', 'imagen': 'images/platos/plateadaalhorno.png'},
    {'nombre': 'purepicante', 'imagen': 'images/platos/purepicante.png'},
    {'nombre': 'pure', 'imagen': 'images/platos/pure.png'},
    {'nombre': 'salmonalaplancha', 'imagen': 'images/platos/salmonalaplancha.png'},
    {'nombre': 'torobayobeer', 'imagen': 'images/platos/torobayobeer.png'},
    {'nombre': 'tortatresleches', 'imagen': 'images/platos/tortatresleches.png'}
]

for plato_data in platos_data:
    plato, created = Plato.objects.get_or_create(nombre=plato_data['nombre'])
    plato.imagen = plato_data['imagen']
    plato.save()

print("Platos actualizados con éxito")

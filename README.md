# Pokedex API Middleware
Este proyecto implementa un middleware para una Pokedex API utilizando Django Rest Framework. Permite consultar la información de Pokémon desde una API pública [api_oak](https://pokeapi.co/api/v2/pokemon), con la opción de cargar los datos de los Pokémon en una base de datos local para poder editarlos.

## Funcionalidades
- **Consultar Pokémon**: Permite realizar consultas a la API externa de Pokémon para obtener información filtrada (nombre y URL de recurso).
- **Cargar Pokémon**: Carga información de Pokémon desde la API pública de Oak y la almacena en la base de datos local.
- **Editar Pokémon**: Permite a los usuarios modificar la información de un Pokémon almacenado en la base de datos.
- **Middleware**: Implementa un middleware para interceptar y procesar las solicitudes a la API externa.

## Requisitos
Antes de comenzar, asegúrate de tener los siguientes requisitos instalados:

- Python 3.7+
- Django 3.0+
- Django Rest Framework
- PostgreSQL (u otra base de datos, opcionalmente)

## Instalación
Sigue estos pasos para configurar y ejecutar el proyecto en tu entorno local.

1. Clonar el repositorio
```
git clone https://github.com/Omarleonardo/andes.git
cd andes
```


3. Crear un entorno virtual
```
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

4. Instalar dependencias
```
pip install -r requirements.txt
```



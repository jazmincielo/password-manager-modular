import os
from config.settings import settings
from database.connection import init_db
from ui.views import render_vault_ui
from nicegui import ui

# Validar variables de entorno al iniciar
settings.validate()

# Inicializar tablas de la base de datos en Supabase
init_db()

# Renderizar la interfaz gráfica
render_vault_ui()

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title=settings.TITLE, port=settings.PORT, reload=False)

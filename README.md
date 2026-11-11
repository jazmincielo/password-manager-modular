# Secure Vault - Gestor de Contraseñas (Estructura Modular)

Aplicación estructurada respetando los principios de **diseño modular, separación de responsabilidades (SOLID) y arquitectura por capas**.

## Estructura del Proyecto:
```text
laboratorio_password_manager_modular/
├── config/             # Configuración centralizada y variables de entorno (.env)
│   ├── settings.py
│   └── __init__.py
├── database/           # Conexión al ORM SQLModel y Supabase PostgreSQL
│   ├── connection.py
│   └── __init__.py
├── models/             # Modelos de datos (tablas SQLModel)
│   ├── vault.py
│   └── __init__.py
├── services/           # Lógica de negocio (Cifrado Fernet y Operaciones de Bóveda)
│   ├── crypto_service.py
│   ├── vault_service.py
│   └── __init__.py
├── ui/                 # Interfaz de usuario (Componentes NiceGUI)
│   ├── views.py
│   └── __init__.py
├── main.py             # Punto de entrada de la aplicación
├── Dockerfile          # Imagen contenerizada
├── docker-compose.yml  # Orquestación con contenedor Docker
├── .env.example        # Plantilla de secretos (Pooler Supabase Puerto 6543)
├── .gitignore
└── requirements.txt
```

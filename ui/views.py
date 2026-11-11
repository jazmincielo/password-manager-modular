from nicegui import ui
from services.vault_service import vault_service
from services.crypto_service import crypto_service

def render_vault_ui():
    ui.colors(primary='#0F172A', secondary='#2563EB', accent='#10B981')

    # Encabezado
    with ui.header().classes('items-center justify-between bg-slate-900 text-white p-4 shadow-lg'):
        with ui.row().classes('items-center gap-3'):
            ui.icon('lock', size='md').classes('text-emerald-400')
            ui.label('Secure Vault - Gestor de Contraseñas').classes('text-2xl font-bold tracking-wide')
        ui.label('Arquitectura Modular: Config | DB | Models | Services | UI').classes('text-sm text-slate-300')

    with ui.column().classes('w-full max-w-5xl mx-auto my-6 p-4 gap-6'):

        # Card: Registro de Credenciales
        with ui.card().classes('w-full p-6 shadow-md border border-slate-200 bg-white rounded-xl'):
            ui.label('Registrar Nueva Credencial Encriptada').classes('text-xl font-bold text-slate-800 mb-1')
            ui.label('La contraseña se procesa a través de VaultService y se cifra con AES antes de persistirse en Supabase.').classes('text-sm text-slate-500 mb-4')
            
            with ui.column().classes('w-full gap-4'):
                with ui.row().classes('w-full items-center gap-4'):
                    service_input = ui.input(label='Servicio / Sitio Web', placeholder='Ej. GitHub, Gmail, AWS').classes('flex-1')
                    user_input = ui.input(label='Usuario / Email', placeholder='usuario@correo.com').classes('flex-1')
                
                with ui.row().classes('w-full items-center gap-4'):
                    pass_input = ui.input(label='Contraseña', password=True, password_toggle_button=True).classes('flex-2')
                    
                    def set_gen_pass():
                        pass_input.value = crypto_service.generate_random_password()
                        ui.notify('Contraseña segura generada automáticamente', type='positive')

                    ui.button('Generar Clave Segura', on_click=set_gen_pass, icon='auto_awesome').props('outline color=primary').classes('flex-1')

                notes_input = ui.input(label='Notas Adicionales (Opcional)', placeholder='Instrucciones de recuperación o 2FA').classes('w-full')

                def save_entry():
                    service = service_input.value.strip()
                    username = user_input.value.strip()
                    password = pass_input.value.strip()
                    notes = notes_input.value.strip()

                    if not service or not username or not password:
                        ui.notify('Por favor completa los campos obligatorios.', type='warning')
                        return

                    vault_service.create_entry(
                        service_name=service,
                        username=username,
                        raw_password=password,
                        notes=notes
                    )

                    ui.notify(f'Credencial para {service} guardada encriptada en Supabase', type='positive')
                    service_input.value = ''
                    user_input.value = ''
                    pass_input.value = ''
                    notes_input.value = ''
                    refresh_vault()

                ui.button('Guardar Credencial Encriptada', on_click=save_entry, icon='security').classes('bg-slate-900 text-white font-semibold py-2 px-6 rounded-lg w-full')

        # Card: Bóveda de Contraseñas
        with ui.card().classes('w-full p-6 shadow-md border border-slate-200 bg-white rounded-xl'):
            with ui.row().classes('w-full justify-between items-center mb-4'):
                ui.label('Bóveda de Credenciales Almacenadas').classes('text-xl font-bold text-slate-800')
                ui.button('Actualizar Bóveda', on_click=lambda: refresh_vault(), icon='refresh').props('outline color=primary')

            vault_container = ui.column().classes('w-full gap-3')

            def refresh_vault():
                vault_container.clear()
                entries = vault_service.get_all_entries()
                
                if not entries:
                    with vault_container:
                        ui.label('No hay credenciales registradas en la bóveda.').classes('text-slate-400 italic py-6 text-center w-full')
                    return

                for item in entries:
                    with vault_container:
                        with ui.card().classes('w-full p-4 border border-slate-200 rounded-lg flex-row items-center justify-between bg-slate-50'):
                            with ui.column().classes('gap-1 flex-1'):
                                with ui.row().classes('items-center gap-2'):
                                    ui.icon('key', size='sm').classes('text-slate-700')
                                    ui.label(item.service_name).classes('text-lg font-bold text-slate-900')
                                ui.label(f"Usuario: {item.username}").classes('text-sm text-slate-600')
                                
                                hash_preview = item.encrypted_password[:25] + "..."
                                ui.label(f"Texto Cifrado en BD: {hash_preview}").classes('text-xs font-mono text-slate-400')
                            
                            with ui.row().classes('items-center gap-2'):
                                def reveal_password(enc_pwd=item.encrypted_password):
                                    plain = crypto_service.decrypt(enc_pwd)
                                    with ui.dialog() as dialog, ui.card().classes('p-6 gap-4'):
                                        ui.label('🔒 Contraseña Descifrada').classes('text-lg font-bold text-slate-800')
                                        ui.input(value=plain).props('readonly outlineref').classes('w-full text-lg font-mono')
                                        ui.button('Cerrar', on_click=dialog.close).classes('bg-slate-800 text-white')
                                    dialog.open()

                                def delete_entry(entry_id=item.id):
                                    vault_service.delete_entry(entry_id)
                                    ui.notify('Credencial eliminada de la bóveda', type='info')
                                    refresh_vault()

                                ui.button('Ver Clave', on_click=reveal_password, icon='visibility').classes('bg-emerald-600 text-white')
                                ui.button(icon='delete', on_click=delete_entry).props('flat color=red')

            refresh_vault()

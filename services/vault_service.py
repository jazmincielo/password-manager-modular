from sqlmodel import select
from database.connection import get_session
from models.vault import VaultEntry
from services.crypto_service import crypto_service
from typing import List

class VaultService:
    @staticmethod
    def create_entry(service_name: str, username: str, raw_password: str, notes: str = "") -> VaultEntry:
        """Cifra la contraseña y guarda el registro en Supabase."""
        encrypted_pwd = crypto_service.encrypt(raw_password)
        entry = VaultEntry(
            service_name=service_name,
            username=username,
            encrypted_password=encrypted_pwd,
            notes=notes
        )
        with get_session() as session:
            session.add(entry)
            session.commit()
            session.refresh(entry)
            return entry

    @staticmethod
    def get_all_entries() -> List[VaultEntry]:
        """Obtiene todas las credenciales ordenadas por ID descendente."""
        with get_session() as session:
            return session.exec(select(VaultEntry).order_by(VaultEntry.id.desc())).all()

    @staticmethod
    def delete_entry(entry_id: int) -> bool:
        """Elimina una credencial por su ID."""
        with get_session() as session:
            db_entry = session.get(VaultEntry, entry_id)
            if db_entry:
                session.delete(db_entry)
                session.commit()
                return True
            return False

vault_service = VaultService()

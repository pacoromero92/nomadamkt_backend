from enum import Enum
class Role(str, Enum):
    ADMIN = "Administrador"
    USER = "Usuario"
    MANAGER = "Manager"
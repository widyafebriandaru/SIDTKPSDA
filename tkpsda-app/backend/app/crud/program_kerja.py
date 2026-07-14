from app.crud.base import CRUDBase
from app.models.program_kerja import ProgramKerja
from app.schemas.program_kerja import ProgramKerjaCreate, ProgramKerjaUpdate


class CRUDProgramKerja(CRUDBase[ProgramKerja, ProgramKerjaCreate, ProgramKerjaUpdate]):
    pass


program_kerja = CRUDProgramKerja(ProgramKerja)

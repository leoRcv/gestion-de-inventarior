from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import schemas
from repositories import categoria_repo # Ojo con la mayúscula si tu carpeta es "Repositories"

router = APIRouter(prefix="/categorias", tags=["Categorías"])

@router.post("/", response_model=schemas.Categoria)
def crear_nueva_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    return categoria_repo.crear_categoria(db=db, categoria=categoria)

@router.get("/", response_model=list[schemas.Categoria])
def listar_categorias(db: Session = Depends(get_db)):
    return categoria_repo.obtener_categorias(db=db)
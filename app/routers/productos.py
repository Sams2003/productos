from fastapi import APIRouter, HTTPException
from app.database import get_conexion
from typing import Optional
from pydantic import BaseModel

class Producto(BaseModel):
    nombre_producto: str
    marca: str
    descripcion: Optional[str] = None
    precio: float
    stock: int
    estado_producto: str
    imagen_url: Optional[str] = None

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)

@router.get("/")
def obtener_productos():
    try:
        cone =  get_conexion()
        cursor = cone.cursor()
        cursor.execute("SELECT sku, nombre_producto, marca, descripcion, precio, stock, estado_producto , imagen_url FROM productos")
        productos = []
        for sku, nombre_producto, marca, descripcion, precio, stock, estado_producto, imagen_url  in cursor:
            productos.append({
                "sku" : sku,
                "nombre_producto" : nombre_producto,
                "marca" : marca,
                "descripcion" : descripcion,
                "precio" : precio,
                "stock" : stock,
                "estado_producto" : estado_producto,
                "imagen_url": imagen_url
            })
        cursor.close()
        cone.close()
        return productos
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    



@router.get("/{sku_buscar}")

def obtener_producto( sku_buscar: int):
    try:
        cone =  get_conexion()
        cursor = cone.cursor()
        cursor.execute("SELECT * FROM productos WHERE sku = :sku", {"sku": sku_buscar})#, { :buscar })

        productos= cursor.fetchone()
        cursor.close()
        cone.close()
        if not productos:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        else:
            return {
                "sku" : sku_buscar,
                "nombre_producto" : productos[1],
                "marca" : productos[2],
                "descripcion" : productos[3],
                "precio" : productos[4],
                "stock" : productos [5],
                "estado_producto" : productos [6],
                "imagen_url": productos [7]
            }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))



@router.post("/")
# La función ahora espera un único argumento 'producto' que es del tipo de nuestro modelo Pydantic.
# FastAPI entiende que debe tomar el JSON del 'body' y validarlo contra este modelo.
def agregar_productos(producto: Producto):
    try:
        cone = get_conexion()
        cursor = cone.cursor()
        # Ahora usamos los datos del objeto recibido: producto.nombre_producto, etc.
        cursor.execute("""INSERT INTO productos(nombre_producto, marca, descripcion, precio, stock, estado_producto, imagen_url)
                          VALUES(:nombre_producto, :marca, :descripcion, :precio, :stock, :estado_producto, :imagen_url)""",
                       {
                           "nombre_producto": producto.nombre_producto,
                           "marca": producto.marca,
                           "descripcion": producto.descripcion,
                           "precio": producto.precio,
                           "stock": producto.stock,
                           "estado_producto": producto.estado_producto,
                           "imagen_url": producto.imagen_url
                       })
        cone.commit()
        cursor.close()
        cone.close()
        return {"mensaje": "Producto agregado con éxito"}
    except Exception as ex:
        # Es una buena práctica registrar el error en la consola del servidor para depuración
        print(f"Error al agregar producto: {ex}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {ex}")



@router.put("/{sku_actualizar}")

def actualizar_producto(sku:int, nombre_producto: str, marca: str, descripcion: str, precio:int, stock :int, estado_producto : str , imagen_url: Optional[str] = None):
    try:
        cone =  get_conexion()
        cursor = cone.cursor()
        cursor.execute("""UPDATE productos SET sku = :sku, nombre_producto = :nombre_producto, marca = :marca, 
                       descripcion = :descripcion, precio = :precio, stock = :stock, estado_producto = :estado_producto, imagen_url = :imagen_url
                          WHERE sku = :sku""",
                        {"sku":sku, "nombre_producto":nombre_producto, "marca":marca, 
                         "descripcion":descripcion, "precio":precio, "stock": stock, "estado_producto" : estado_producto, "imagen_url" : imagen_url})
        if cursor.rowcount ==0:
            cursor.close()
            cone.close()
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        cone.commit()
        cursor.close()
        cone.close()
        return{"mensaje" :"Producto actualizado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    
@router.delete("/{sku_eliminar}")
def eliminar_producto(sku_eliminar : int):
    try:
        cone =  get_conexion()
        cursor = cone.cursor()
        cursor.execute("DELETE FROM productos WHERE sku = :sku", {"sku": sku_eliminar})
        
        if cursor.rowcount == 0:
            cursor.close()
            cone.close()
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        cone.commit()
        cursor.close()
        cone.close()
        return{"mensaje" :"Producto eliminado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


from typing import Optional

@router.patch("/{sku_actualizar}")
def actualizar_parcial(sku_actualizar:int, nombre_producto:Optional[str]=None, marca:Optional[str]=None, 
                       descripcion:Optional[str] = None, precio:Optional[int] = None, 
                       stock:Optional[int] = None, estado_producto:Optional[str] = None,
                       imagen_url: Optional[str] = None):
    try:
        if not nombre_producto:
            raise HTTPException(status_code=400, detail="Debe enviar al menos 1 dato")
        cone = get_conexion()
        cursor = cone.cursor()

        campos = []
        valores = {"sku": sku_actualizar}
        if nombre_producto:
            campos.append("nombre_producto = :nombre_producto")
            valores["nombre_producto"] = nombre_producto
        if marca:
            campos.append("marca = :marca")
            valores["marca"] = marca
        if descripcion:
            campos.append("descripcion = :descripcion")
            valores["descripcion"] = descripcion
        if precio:
            campos.append("precio = :precio")
            valores["precio"] = precio
        if stock:
            campos.append("stock = :stock")
            valores["stock"] = stock
        if estado_producto:
            campos.append("estado_producto = :estado_producto")
            valores["estado_producto"] = estado_producto
        if imagen_url:
            campos.append("imagen_url = :imagen_url")
            valores["imagen_url"] = imagen_url


        cursor.execute(f"UPDATE productos SET {', '.join(campos)} WHERE sku = :sku"
                       ,valores)
        if cursor.rowcount==0:
            cursor.close()
            cone.close()
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        cone.commit()
        cursor.close()
        cone.close()        
        return {"mensaje": "Producto actualizado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
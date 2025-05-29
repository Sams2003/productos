from fastapi import APIRouter, HTTPException
from app.database import get_conexion

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)

@router.get("/")
def obtener_productos():
    try:
        cone =  get_conexion()
        cursor = cone.cursor()
        cursor.execute("SELECT sku, nombre_producto, marca, descripcion, precio, stock, estado_producto FROM productos")
        productos = []
        for sku, nombre_producto, marca, descripcion, precio, stock, estado_producto in cursor:
            productos.append({
                "sku" : sku,
                "nombre_producto" : nombre_producto,
                "marca" : marca,
                "descripcion" : descripcion,
                "precio" : precio,
                "stock" : stock,
                "estado_producto" : estado_producto
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
                "nombre_producto" : productos[0],
                "marca" : productos[1],
                "descripcion" : productos[2],
                "precio" : productos[3],
                "stock" : productos [4],
                "estado_producto" : productos [5]
            }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))



@router.post("/")

def agregar_productos (nombre_producto: str, marca: str, descripcion: str, precio:int, stock:int, estado_producto:str) :
    try:
        cone =  get_conexion()
        cursor = cone.cursor()
        cursor.execute("""INSERT INTO productos(nombre_producto, marca, descripcion, precio, stock, estado_producto )
                          VALUES(:nombre_producto, :marca, :descripcion, :precio, :stock, :estado_producto)""",
                          {"nombre_producto":nombre_producto, "marca":marca, "descripcion":descripcion, 
                           "precio":precio, "stock" :stock, "estado_producto" :estado_producto})
        cone.commit()
        cursor.close()
        cone.close()
        return{"Producto agregado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))



@router.put("/{sku_actualizar}")

def actualizar_producto(sku:int, nombre_producto: str, marca: str, descripcion: str, precio:int, stock :int, estado_producto : str ):
    try:
        cone =  get_conexion()
        cursor = cone.cursor()
        cursor.execute("""UPDATE productos SET sku = :sku, nombre_producto = :nombre_producto, marca = :marca, 
                       descripcion = :descripcion, precio = :precio, stock = :stock, estado_producto = :estado_producto
                          WHERE sku = :sku""",
                        {"sku":sku, "nombre_producto":nombre_producto, "marca":marca, 
                         "descripcion":descripcion, "precio":precio, "stock": stock, "estado_producto" : estado_producto})
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
                       stock:Optional[int] = None, estado_producto:Optional[str] = None):
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
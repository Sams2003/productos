from fastapi import APIRouter, HTTPException
from app.database import get_conexion

router=  APIRouter(
    prefix = "/productos",
    tag= ["Productos"]
)

@router.get("/")

def obtener_productos():
    try:
        cone =  get_conexion
        cursor = cone.cursor()
        cursor.execute("SELECT FROM")
        productos = []
        for x in cursor:
            productos.append({
                print ("poner aqui los datos que va a guardar")
            })
        cursor.close()
        cone.close()
        return productos
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    
@router.get("/{buscar}")

def buscar_productos( buscar: int):
    try:
        cone =  get_conexion
        cursor = cone.cursor()
        cursor.execute("SELECT FROM WHERE")#, { :buscar })
        productos= cursor.fetchone()
        cursor.close()
        cone.close()
        if not productos:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        else:
            return {
                "hola" : buscar
            }
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.post("/")

def agregar_productos () :
    try:
        cone =  get_conexion
        cursor = cone.cursor()
        cursor.execute("""INSERT INTO 
                          VALUES(:)""",
                        {})
        cone.commit()
        cursor.close()
        cone.close()
        return{"Producto agregado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    
@router.put("/{actualizar}")

def actualizar_producto():
    try:
        cone =  get_conexion
        cursor = cone.cursor()
        cursor.execute("""UPDATE 
                          SET(:)
                          WHERE""",
                        {"actualizar al final"})
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
    
@router.delete("/{eliminar}")

def eliminar_producto(eliminar : int):
    try:
        cone =  get_conexion
        cursor = cone.cursor()
        cursor.execute("DELETE FROM WHERE ")
        if cone.rowcount == 0:
            cursor.close()
            cone.close()
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        cone.commit()
        cursor.close()
        cone.close()
        return{"mensaje" :"Producto eliminado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@router.patch("/{actualizar_par}")

#from typing import Optional

def actualizar_parcial():
    try:
        if not "producto" and not "producto":
            raise HTTPException(status_code=400, detail="Debe enviar a menos 1 dato")
        cone =  get_conexion
        cursor = cone.cursor()
        campos = []
        valores = { " " :actualizar_par}
        if "hola":
            campos.append("")
            valores= [""] = ""
        if "adios":
            campos.append("")
            valores = [""] = ""

        cursor.execute(f"""UPDATE 
                          SET{',' .join(campos)}
                          WHERE""",
                        valores)
        if cone.rowcount == 0:
            cursor.close()
            cone.close()
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        cone.commit()
        cursor.close()
        cone.close()
        return{"mensaje" :"Producto modificado con éxito"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


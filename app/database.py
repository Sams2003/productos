import oracledb

def get_conexion ():
    conexion = oracledb.connect(
        user = "ferreteria",
        password = "ferreteria",
        dsn = "localhost:1521/orcl"
    )
    return conexion

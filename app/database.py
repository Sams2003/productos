import oracledb

def get_conexion ():
    conexion = oracledb.connect(
        user = "my_ferre",
        password = "my_ferre",
        dsn = "localhost:1521/orcl"
    )
    return conexion

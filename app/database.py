import oracledb

def get_conexion ():
    conexion = oracledb.connect(
        user = " ",
        password = " ",
        dsn = "localhost/orcl"
    )
    return conexion

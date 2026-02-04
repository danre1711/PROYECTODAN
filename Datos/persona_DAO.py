from Datos.conexion import Conexion
from Dominio.persona import Persona

import pyodbc as bd

class PersonaDAO:
    _INSERT = ("INSERT INTO Personas (nombres, apellidos, cedula, sexo, email,edad) "
               "VALUES (?, ?, ?, ?, ? ,?)")
    _SELECT = ("SELECT idPersona, nombres, apellidos, cedula, sexo, email, edad "
               "FROM Personas WHERE cedula = ?")

    @classmethod
    def insertar_persona(cls, persona):
        try:
            with Conexion.obtener_cursor() as cursor:
                datos = (persona.nombre, persona.apellido, persona.cedula, persona.sexo,persona.email,persona.edad,)
                cursor.execute(cls._INSERT, datos)
                respuesta = cursor.rowcount
                if respuesta == 1:
                    return {'ejecuto':True, 'mensaje':'Se guardo con exito.'}
        except bd.IntegrityError as e_bb:
            print(f'Error en la cedula: {e_bb}')
            if 'UQ_Cedula' in e_bb.__str__():
                return {'ejecuto':False, 'mensaje':'Cedula ya existe.'}
            elif 'UQ_Email' in e_bb.__str__():
                return {'ejecuto': False, 'mensaje': 'Email ya existe.'}
        except Exception as e:
            print(f'Error general: {e}')
            print(type(e))
            return {'ejecuto':False, 'mensaje':'Error al guardar los datos, comuncarse sistemas.'}

    @classmethod
    def seleccionar_persona(cls, cedula):
        persona = None
        try:
            with Conexion.obtener_cursor() as cursor:
                datos = (cedula,)
                cursor.execute(cls._SELECT, datos)
                registros = cursor.fetchall()
                for registro in registros:
                    persona = Persona(nombre=registro[1], apellido=registro[2],
                                      cedula=registro[3], sexo=registro[4], email=registro[5], edad =registro[6])
                return persona
        except Exception as e:
            print(f'Error general: {e}')
            print(type(e))
            return persona


if __name__ == "__main__":
    # p1 = Persona(cedula="999999999", nombre="Enrique", apellido="Perez", sexo="Masculino")
    # print(PersonaDAO.insertar_persona(p1))
    print(PersonaDAO.seleccionar_persona('333333'))

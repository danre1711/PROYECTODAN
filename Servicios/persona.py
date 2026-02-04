import re
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QMainWindow, QMessageBox
from datetime import datetime

from Dominio.persona import Persona
from UI.vtnPrincipal import Ui_vtnPrincipal


class PersonaServicio(QMainWindow):
    ''''
    Clase que genera la logica de los objetos persona
    '''

    def __init__(self):
        super(PersonaServicio, self).__init__()
        self.ui = Ui_vtnPrincipal()
        self.ui.setupUi(self)
        self.ui.btnGuardar.clicked.connect(self.guardar)
        self.ui.txtCedula.setValidator(QIntValidator())
        self.ui.btnLimpiar.clicked.connect(self.limpiar)
        self.ui.btnBuscar.clicked.connect(self.buscar)
        # validacion del correo
        patron = r"(?!.*.{2})"
        self.regex_email = QRegularExpression(patron)
        self.email_validator = QRegularExpressionValidator(self.regex_email, self)
        self.ui.txtEmaill.setValidator(self.email_validator)

        self.ui.txtFechaNacimiento.setPlaceholderText("dd/MM/yyyy")

    def _es_email_valido(self, email):
        return self.regex_email.match(email).hasMatch()

    def guardar(self):
        nombre = self.ui.txtNombre.text()
        apellido = self.ui.txtApellido.text()
        cedula = self.ui.txtCedula.text()
        email = self.ui.txtEmaill.text().strip()
        sexo = self.ui.cbSexo.currentText()
        fecha_texto = self.ui.txtFechaNacimiento.text()

        # validacion de los datos del formulario
        if nombre == "":
            QMessageBox.warning(self, "Advertencia", "Debe ingresar el nombre")
        elif apellido == "":
            QMessageBox.warning(self, "Advertencia", "Debe ingresar el apellido")
        elif len(cedula) < 10:
            QMessageBox.warning(self, "Advertencia", "Debe ingresar la cedula")
        elif not self._es_email_valido(email):
            QMessageBox.warning(self, "Advertencia", "Debe ingresar el email")
        elif sexo == "Seleccionar":
            QMessageBox.warning(self, "Advertencia", "Debe ingresar el sexo")
        else:
            try:
                fecha_nacimiento = datetime.strptime(fecha_texto, "%d/%m/%Y").date()
            except:
                QMessageBox.warning(self, "Advertencia", "formato de fecha inválida, ingrese un formato correcto")
                return

            persona = Persona(cedula=cedula, nombre=nombre, apellido=apellido, email=email, sexo=sexo,
                              fecha_nacimiento=fecha_nacimiento)
            print(nombre)
            print(apellido)
            print(cedula)
            print(sexo)
            print(fecha_nacimiento)

            self.guardar_en_bd(persona)

            self.ui.statusbar.showMessage('Se guardo la información', 500)
            # borrar campos del formulario
            self.ui.txtNombre.setText('')
            self.ui.txtApellido.setText('')
            self.ui.txtCedula.setText('')
            self.ui.txtEmaill.setText('')
            self.ui.cbSexo.setCurrentText('')
            self.ui.txtFechaNacimiento.setText('')

    def limpiar(self):
        self.ui.txtNombre.clear()
        self.ui.txtApellido.clear()
        self.ui.txtCedula.clear()
        self.ui.txtEmaill.clear()
        self.ui.txtFechaNacimiento.clear()
        self.ui.cbSexo.setCurrentIndex(0)
        self.ui.statusbar.showMessage('informacion eliminada correctamente', 500)


    def buscar(self):
        cedula = self.ui.txtBuscarCedula.text().strip()

        if len(cedula) < 10:
            QMessageBox.warning(self, "Advertencia", "Cédula incorrecta, digite nuevamente")
            return

        try:
            import sqlite3
            conn = sqlite3.connect('personas.db')
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM personas WHERE cedula = ?', (cedula,))
            resultado = cursor.fetchone()

            if resultado:
                self.ui.txtNombre.setText(resultado[1])
                self.ui.txtApellido.setText(resultado[2])
                self.ui.txtCedula.setText(resultado[0])
                self.ui.txtEmaill.setText(resultado[3])
                self.ui.cbSexo.setCurrentText(resultado[4])
                fecha = datetime.strptime(resultado[5], '%Y-%m-%d').strftime('%d/%m/%Y')
                self.ui.txtFechaNacimiento.setText(fecha)
                self.ui.statusbar.showMessage('Persona encontrada', 3000)
            else:
                QMessageBox.information(self, "Advertencia", "No se encontró ninguna persona con la cédula ingresada")

            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al buscar: {str(e)}")

    def guardar_en_bd(self, persona):
        try:
            import sqlite3
            conn = sqlite3.connect('personas.db')
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS personas (
                    cedula TEXT PRIMARY KEY,
                    nombre TEXT,
                    apellido TEXT,
                    email TEXT,
                    sexo TEXT,
                    fecha_nacimiento DATE
                )
            ''')

            cursor.execute('''
                INSERT OR REPLACE INTO personas 
                (cedula, nombre, apellido, email, sexo, fecha_nacimiento)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (persona.cedula, persona.nombre, persona.apellido,
                  persona.email, persona.sexo, str(persona.fecha_nacimiento)))

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error al guardar: {e}")
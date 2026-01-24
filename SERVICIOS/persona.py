from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QMainWindow, QMessageBox

from DOMINIO.persona import Persona
from UI.vtnPrincipal import Ui_vtnPrincipal



class PersonaServicio(QMainWindow):
    '''
    clase que genera la logica de los objetos persona
    '''
    def __init__(self):
        super(PersonaServicio, self).__init__()
        self.ui = Ui_vtnPrincipal()
        self.ui.setupUi(self)
        self.ui.btnGuardar.clicked.connect(self.guardar)
        self.ui.btnLimpiar.clicked.connect(self.limpiar)
        self.ui.txtCedula.setValidator(QIntValidator())

    def guardar(self):
        nombre = self.ui.txtNombre.text()
        apellido = self.ui.txtApellido.text()
        cedula = self.ui.txtCedula.text()
        sexo = self.ui.cbSexo.currentText()
        email = self.ui.txtEmail.text()

        # validacion de datos del formulario
        if nombre == "":
            QMessageBox.warning(self, 'Advertencia', 'Debe ingresar el nombre')
        elif apellido == "":
            QMessageBox.warning(self, 'Advertencia', 'Debe ingresar el apellido')
        elif len(cedula) < 10:
            QMessageBox.warning(self, 'Advertencia', 'Debe ingresar la cedula')
        elif sexo == "Seleccionar":
            QMessageBox.warning(self, 'Advertencia', 'Debe seleccionar el sexo')
        elif email == "":
            QMessageBox.warning(self, 'Advertencia', 'Debe ingresar el email')
        else:
            try:
                persona = Persona(cedula=cedula, nombre=nombre, apellido=apellido, sexo=sexo, email=email)
                print(persona)

                # mostrar confirmacion de que se guardo
                self.ui.statusbar.showMessage('Se guardó la información', 3000)

                # Borrar los campos del formulario
                self.ui.txtNombre.setText('')
                self.ui.txtApellido.setText('')
                self.ui.txtCedula.setText('')
                self.ui.txtEmail.setText('')
                self.ui.cbSexo.setCurrentText('Seleccionar')

            except ValueError as e:
                # Captura errores de validación de la clase Persona
                QMessageBox.warning(self, 'Error de validación', str(e))

    def limpiar(self):
        self.ui.txtNombre.clear()
        self.ui.txtApellido.clear()
        self.ui.txtCedula.clear()
        self.ui.txtEmail.clear()
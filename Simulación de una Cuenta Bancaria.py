import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import random

# Definimos la clase CuentaBancaria, que representa una cuenta bancaria
class CuentaBancaria:
    def __init__(self, numero_cuenta, titular, saldo=0.0, tipo_cuenta="Ahorros"):
        # Atributos de la cuenta bancaria: número de cuenta, titular, saldo y tipo de cuenta
        self.numero_cuenta = numero_cuenta
        self.titular = titular
        self.saldo = saldo
        self.tipo_cuenta = tipo_cuenta
        self.historial_transacciones = []  # Lista para guardar el historial de transacciones

    # Método para consultar el saldo de la cuenta
    def consultar_saldo(self):
        return self.saldo

    # Método para depositar dinero en la cuenta
    def depositar(self, monto):
        if monto > 0:  # Verificamos si el monto es positivo
            self.saldo += monto  # Aumentamos el saldo con el monto depositado
            self.historial_transacciones.append(f"Depósito de ${monto}")  # Guardamos el depósito en el historial
            return True  # Retornamos True para indicar que el depósito fue exitoso
        return False  # Si el monto es negativo, retornamos False

    # Método para retirar dinero de la cuenta
    def retirar(self, monto):
        if monto > 0 and self.saldo >= monto:  # Verificamos que el monto sea positivo y que haya suficiente saldo
            self.saldo -= monto  # Restamos el monto al saldo
            self.historial_transacciones.append(f"Retiro de ${monto}")  # Guardamos el retiro en el historial
            return True  # Retornamos True si el retiro fue exitoso
        return False  # Si no se cumple la condición, retornamos False

    # Método para transferir dinero a otra cuenta
    def transferir(self, monto, cuenta_destino):
        if monto > 0 and self.saldo >= monto and self.numero_cuenta != cuenta_destino.numero_cuenta:  # Verificamos que el monto sea válido y que no se transfiera a la misma cuenta
            self.saldo -= monto  # Restamos el monto de la cuenta origen
            cuenta_destino.saldo += monto  # Sumamos el monto a la cuenta destino
            self.historial_transacciones.append(f"Transferencia de ${monto} a la cuenta {cuenta_destino.numero_cuenta}")  # Registramos la transferencia
            return True  # Transferencia exitosa
        return False  # Si alguna condición falla, retornamos False

    # Método para mostrar el historial de transacciones
    def mostrar_historial(self):
        return "\n".join(self.historial_transacciones)  # Devolvemos el historial de transacciones como un texto


# Clase principal de la aplicación (que maneja la interfaz gráfica)
class BancoApp:
    def __init__(self, root):
        self.root = root  # Creamos la ventana principal
        self.root.title("Simulación de Cuenta Bancaria")  # Titulo de la ventana
        self.cuentas = {}  # Diccionario que guardará todas las cuentas bancarias creadas
        self.cuenta_activa = None  # Variable que guardará la cuenta actualmente activa

        # Llamamos al método para crear los elementos de la interfaz
        self.create_widgets()

    def create_widgets(self):
        # Elementos de la interfaz gráfica (etiquetas y campos de entrada)
        self.label_titular = tk.Label(self.root, text="Nombre del Titular:")
        self.label_titular.grid(row=0, column=0)

        self.entry_titular = tk.Entry(self.root)
        self.entry_titular.grid(row=0, column=1)

        self.label_saldo = tk.Label(self.root, text="Saldo Inicial:")
        self.label_saldo.grid(row=1, column=0)

        self.entry_saldo = tk.Entry(self.root)
        self.entry_saldo.grid(row=1, column=1)

        self.label_tipo = tk.Label(self.root, text="Tipo de Cuenta:")
        self.label_tipo.grid(row=2, column=0)

        self.entry_tipo = tk.Entry(self.root)
        self.entry_tipo.grid(row=2, column=1)

        # Botones para interactuar con la interfaz
        self.button_crear_cuenta = tk.Button(self.root, text="Crear Cuenta", command=self.crear_cuenta)
        self.button_crear_cuenta.grid(row=3, columnspan=2)

        self.button_seleccionar_cuenta = tk.Button(self.root, text="Seleccionar Cuenta Activa", command=self.seleccionar_cuenta)
        self.button_seleccionar_cuenta.grid(row=4, columnspan=2)

        self.button_consultar_saldo = tk.Button(self.root, text="Consultar Saldo", command=self.consultar_saldo)
        self.button_consultar_saldo.grid(row=5, columnspan=2)

        self.button_depositar = tk.Button(self.root, text="Depositar Dinero", command=self.depositar)
        self.button_depositar.grid(row=6, columnspan=2)

        self.button_retirar = tk.Button(self.root, text="Retirar Dinero", command=self.retirar)
        self.button_retirar.grid(row=7, columnspan=2)

        self.button_transferir = tk.Button(self.root, text="Transferir Dinero", command=self.transferir)
        self.button_transferir.grid(row=8, columnspan=2)

        self.button_historial = tk.Button(self.root, text="Mostrar Historial", command=self.mostrar_historial)
        self.button_historial.grid(row=9, columnspan=2)

        self.button_mostrar_cuentas = tk.Button(self.root, text="Mostrar Cuentas Activas", command=self.mostrar_cuentas_activas)
        self.button_mostrar_cuentas.grid(row=10, columnspan=2)

    def crear_cuenta(self):
        try:
            # Obtenemos los valores de los campos de texto
            nombre = self.entry_titular.get()
            saldo_inicial = float(self.entry_saldo.get())
            tipo_cuenta = self.entry_tipo.get()

            # Validamos que todos los campos sean correctos
            if not nombre or saldo_inicial < 0 or not tipo_cuenta:
                messagebox.showerror("Error", "Por favor, complete todos los campos con valores válidos.")
                return

            # Generamos un número de cuenta aleatorio
            numero_cuenta = random.randint(1000000000, 9999999999)
            # Creamos la cuenta bancaria
            cuenta = CuentaBancaria(numero_cuenta, nombre, saldo_inicial, tipo_cuenta)
            # Guardamos la cuenta en el diccionario de cuentas
            self.cuentas[numero_cuenta] = cuenta
            # Mostramos un mensaje confirmando la creación de la cuenta
            messagebox.showinfo("Cuenta Creada", f"Cuenta creada con éxito.\nNúmero de cuenta: {numero_cuenta}")

            # Limpiamos los campos para crear una nueva cuenta
            self.entry_titular.delete(0, tk.END)
            self.entry_saldo.delete(0, tk.END)
            self.entry_tipo.delete(0, tk.END)

        except ValueError:
            # Si el valor de saldo no es un número, mostramos un error
            messagebox.showerror("Error", "El saldo inicial debe ser un número válido.")

    def seleccionar_cuenta(self):
        if not self.cuentas:
            messagebox.showerror("Error", "No hay cuentas disponibles. Debe crear una cuenta primero.")
            return

        # Pedimos al usuario que ingrese el número de cuenta
        seleccion = simpledialog.askstring("Seleccionar Cuenta", "Ingrese el número de cuenta:")
        if seleccion:
            numero_cuenta = int(seleccion)
            if numero_cuenta in self.cuentas:
                # Si la cuenta existe, la seleccionamos
                self.cuenta_activa = self.cuentas[numero_cuenta]
                messagebox.showinfo("Cuenta Seleccionada", f"Cuenta activa seleccionada: {numero_cuenta}")
            else:
                messagebox.showerror("Error", "La cuenta seleccionada no existe.")

    def consultar_saldo(self):
        if self.cuenta_activa:
            saldo = self.cuenta_activa.consultar_saldo()
            messagebox.showinfo("Saldo", f"Saldo disponible: ${saldo}")
        else:
            messagebox.showerror("Error", "Debe seleccionar una cuenta activa primero.")

    def depositar(self):
        if self.cuenta_activa:
            monto = simpledialog.askfloat("Depositar", "Ingrese el monto a depositar:")
            if monto and monto > 0:
                if self.cuenta_activa.depositar(monto):
                    messagebox.showinfo("Depósito", f"${monto} depositados con éxito.")
                else:
                    messagebox.showerror("Error", "Monto no válido para depósito.")
            else:
                messagebox.showerror("Error", "El monto debe ser mayor que cero.")
        else:
            messagebox.showerror("Error", "Debe seleccionar una cuenta activa primero.")

    def retirar(self):
        if self.cuenta_activa:
            monto = simpledialog.askfloat("Retirar", "Ingrese el monto a retirar:")
            if monto and monto > 0:
                if self.cuenta_activa.retirar(monto):
                    messagebox.showinfo("Retiro", f"${monto} retirados con éxito.")
                else:
                    messagebox.showerror("Error", "Fondos insuficientes o monto no válido.")
            else:
                messagebox.showerror("Error", "El monto debe ser mayor que cero.")
        else:
            messagebox.showerror("Error", "Debe seleccionar una cuenta activa primero.")

    def transferir(self):
        if self.cuenta_activa:
            numero_destino = simpledialog.askstring("Transferir", "Ingrese el número de cuenta destino:")
            if numero_destino:
                try:
                    numero_destino = int(numero_destino)
                    if numero_destino in self.cuentas:
                        monto = simpledialog.askfloat("Transferir", "Ingrese el monto a transferir:")
                        if monto and monto > 0:
                            cuenta_destino = self.cuentas[numero_destino]
                            if self.cuenta_activa.transferir(monto, cuenta_destino):
                                messagebox.showinfo("Transferencia", f"${monto} transferidos con éxito.")
                            else:
                                messagebox.showerror("Error", "Fondos insuficientes o monto no válido.")
                        else:
                            messagebox.showerror("Error", "El monto debe ser mayor que cero.")
                    else:
                        messagebox.showerror("Error", "La cuenta destino no existe.")
                except ValueError:
                    messagebox.showerror("Error", "El número de cuenta debe ser válido.")
            else:
                messagebox.showerror("Error", "Debe ingresar un número de cuenta destino.")
        else:
            messagebox.showerror("Error", "Debe seleccionar una cuenta activa primero.")

    def mostrar_historial(self):
        if self.cuenta_activa:
            historial = self.cuenta_activa.mostrar_historial()
            messagebox.showinfo("Historial de Transacciones", historial)
        else:
            messagebox.showerror("Error", "Debe seleccionar una cuenta activa primero.")

    def mostrar_cuentas_activas(self):
        if not self.cuentas:
            messagebox.showinfo("Cuentas Activas", "No hay cuentas activas.")
            return

        cuentas_info = "\n".join([f"Cuenta: {cuenta.numero_cuenta} | Titular: {cuenta.titular}" for cuenta in self.cuentas.values()])
        messagebox.showinfo("Cuentas Activas", cuentas_info)


if __name__ == "__main__":
    # Creamos la ventana principal y ejecutamos la aplicación
    root = tk.Tk()
    app = BancoApp(root)
    root.mainloop()

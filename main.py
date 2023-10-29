import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.scrolledtext as tkst
from tkinter.scrolledtext import ScrolledText
import subprocess
from AnalizadorLexico import *
from AnalizadorSintactico import *
from Instrucciones.Texto import *


class app:
    content = ''
    current_file_path = ''

    def __init__(self, root):
        self.root = root
        self.root.title("Analizador BizData")
        self.root.geometry("800x600")

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side=tk.TOP, fill=tk.X)

        self.open_button = tk.Button(self.button_frame, text="Abrir Archivo", command=self.open_file)
        self.open_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(self.button_frame, text="Guardar", command=self.save_file_current)
        self.save_button.pack(side=tk.LEFT)

        self.save_as_button = tk.Button(self.button_frame, text="Guardar Como", command=self.save_file)
        self.save_as_button.pack(side=tk.LEFT)

        self.analyze_button = tk.Button(self.button_frame, text="Analizar", command=self.analyze_code)
        self.analyze_button.pack(side=tk.LEFT)

        self.analyze_button = tk.Button(self.button_frame, text="Reporte Errores", command=self.errores)
        self.analyze_button.pack(side=tk.LEFT)

        self.analyze_button = tk.Button(self.button_frame, text="Reporte Tokens", command=self.reporte)
        self.analyze_button.pack(side=tk.LEFT)

        self.exit_button = tk.Button(self.button_frame, text="Salir",width=6, command=root.quit)
        self.exit_button.pack(side=tk.RIGHT)


        self.line_number_bar = tk.Text(root, width=4, padx=4, takefocus=0, border=0, background='DarkOliveGreen1',state='disabled')
        self.line_number_bar.pack(side=tk.LEFT, fill=tk.Y)

        self.text_widget = ScrolledText(self.root, wrap=tk.WORD, background='LightSteelBlue3')
        self.text_widget.pack(expand=True, fill='both')

        # Consola de salida
        self.output_console = tkst.ScrolledText(self.root, wrap=tk.WORD)
        self.output_console.pack(expand=True, fill='both')
        self.output_console.config(state='disabled')

        self.current_line = 1

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos con Formato bizdata", "*.bizdata")])
        if file_path:
            self.current_file_path = file_path
            with open(file_path, 'r') as file:
                self.content = file.read()
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, self.content)
            self.update_line_numbers()
        self.data = self.text_widget.get(1.0, tk.END)

    def save_file_current(self):
        if self.current_file_path:
            self.content = self.text_widget.get(1.0, tk.END)
            with open(self.current_file_path, 'w') as file:
                file.write(self.content)
            messagebox.showinfo("Guardado", "Archivo guardado exitosamente.")
        else:
            messagebox.showerror("Error", "No se ha abierto ningún archivo para guardar.")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".bizdata", filetypes=[("Archivos de con Formato BIZDATA", "*.bizdata")])
        if file_path:
            self.content = self.text_widget.get(1.0, tk.END)
            with open(file_path, 'w') as file:
                file.write(self.content)
            messagebox.showinfo("Guardado", "Archivo guardado exitosamente.")

    def update_line_numbers(self, event=None):
        line_count = self.text_widget.get('1.0', tk.END).count('\n')
        if line_count != self.current_line:
            self.line_number_bar.config(state=tk.NORMAL)
            self.line_number_bar.delete(1.0, tk.END)
            for line in range(1, line_count + 1):
                self.line_number_bar.insert(tk.END, f"{line}\n")
            self.line_number_bar.config(state=tk.DISABLED)
            self.current_line = line_count

    def analyze_code(self):
        # Obtén el código del área de texto
        code = self.text_widget.get(1.0, tk.END)
        imprimir_consola = ''
        try:
            # Ejecuta el análisis léxico
            instrucciones_lexico = instruccion(code)
            lista_instrucciones = []
            while True:
                instrucciones_lenguaje = instrucciones_sintactico(instrucciones_lexico)
                if instrucciones_lenguaje:
                    lista_instrucciones.append(instrucciones_lenguaje)
                else:
                    break

            #! Ejecutar instrucciones

            for elemento in lista_instrucciones:
                if isinstance(elemento, DeclaracionClaves):
                    continue
                elif isinstance(elemento, Imprimir):
                    imprimir_consola += elemento.ejecutarT()
                elif isinstance(elemento, Imprimirln):
                    imprimir_consola += elemento.ejecutarT()

            print(imprimir_consola)
            for error in lista_errores:
                print(error.operar(None))

            for lis in lista_lexemas:
                print(lis.operar(None))

            # Muestra el resultado en la consola de salida
            self.output_console.config(state='normal')
            self.output_console.delete(1.0, tk.END)
            self.output_console.insert(tk.END, imprimir_consola)
            self.output_console.config(state='disabled')
            messagebox.showinfo("Análisis exitoso", "El código se analizó exitosamente.")

        except Exception as e:
            messagebox.showerror(f"Ocurrió un error al analizar el código: {str(e)}")
            print("Ocurrió un error al analizar el código: ", e)


    def errores(self):
        print("Mostrando errores...")
        self.generar_reporte_errores(lista_errores)
        messagebox.showinfo("Mensaje:","Reporte de Errores Generados!")

    def reporte(self):
        self.generar_html_tokens(lista_lexemas)
        messagebox.showinfo("Mensaje:","Reporte Generado!")

    def ver_lista_lexemas(self):
        for lis in lista_lexemas:
            print(lis.lexema, lis.getFila, lis.getColumna, lis.tipo)


    def run_analysis(self, code):
        
        try:
            result = subprocess.check_output(["python", "-c", code], universal_newlines=True, stderr=subprocess.STDOUT)
            return result
        except subprocess.CalledProcessError as e:
            return f"Error: {e.returncode}\n{e.output}"
        except Exception as e:
            return f"Error inesperado: {str(e)}"



    def generar_reporte_errores(self, lista_errores):
        # Encabezado de la tabla
        tabla_html = """
        <table border="1">
            <tr>
                <th>Error</th>
                <th>Tipo</th>
                <th>Fila</th>
                <th>Columna</th>
            </tr>
        """

        # Itera sobre la lista de errores y crea filas en la tabla
        for error in lista_errores:
            fila_html = f"""
            <tr>
                <td>{error.lexema}</td>
                <td>{error.tipo}</td>
                <td>{error.getFila()}</td>
                <td>{error.getColumna()}</td>
            </tr>
            """
            tabla_html += fila_html

        # Cierra la tabla
        tabla_html += "</table>"

        # Encabezado y estilos adicionales
        header = """
        <html>
        <head>
            <style>
                table {
                    width: 80%;
                    border-collapse: collapse;
                    margin: 20px auto;
                }
                th, td {
                    padding: 8px 12px;
                    text-align: left;
                }
            </style>
        </head>
        <body>
        """

        footer = """
        </body>
        </html>
        """

        # Concatena todas las partes
        reporte_html = header + "<h2>Reporte HTML de Errores</h2>" + tabla_html + footer

        # Guarda el reporte en un archivo HTML
        with open("Reporte_Errores_201902672.html", "w") as f:
            f.write(reporte_html)


    def generar_html_tokens(self, lista_lexemas):

        with open('reporte_lexemas.html', 'w') as file:
            file.write('<html>\n')
            file.write('<head>\n')
            file.write('<title>Reporte HTML de Lexemas</title>\n')
            file.write('</head>\n')
            file.write('<body>\n')
            file.write('<h1>Reporte HTML de Lexemas</h1>\n')
            file.write('<table border="1">\n')
            file.write('<tr>\n')
            file.write('<th>No</th><th>Lexema</th><th>Tipo</th><th>Fila</th><th>Columna</th>\n')
            file.write('</tr>\n')

            for i, lexema in enumerate(lista_lexemas, start=1):
                file.write('<tr>\n')
                file.write(f'<td>{i}</td><td>{lexema.lexema}</td><td>{lexema.tipo}</td><td>{lexema.fila}</td><td>{lexema.columna}</td>\n')
                file.write('</tr>\n')

            file.write('</table>\n')
            file.write('</body>\n')
            file.write('</html>')



if __name__ == "__main__":
    root = tk.Tk()
    app = app(root)
    root.mainloop()
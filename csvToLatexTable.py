import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def seleccionar_carpeta(titulo="Selecciona una carpeta"):
    carpeta = filedialog.askdirectory(title=titulo)
    return carpeta

def csv_a_latex(archivo_csv, carpeta_destino, carpeta_origen, decimales):
    df = pd.read_csv(archivo_csv)

    # Redondear los valores numéricos
    df = df.round(decimales)

    nombre_archivo = os.path.splitext(os.path.basename(archivo_csv))[0]
    nombre_archivo_escapado = nombre_archivo.replace("_", "\\_")

    n_cols = len(df.columns)
    align = "l" + "r" * (n_cols - 1) if n_cols > 0 else ""
    header_cols = [col.replace("_", "\\_") for col in df.columns]
    header_row = " & ".join(header_cols) + " \\\\"

    data_rows = []
    for _, row in df.iterrows():
        row_str = " & ".join(str(x) for x in row) + " \\\\"
        data_rows.append(row_str)

    lines = []
    lines.append(f"\\begin{{longtable}}{{{align}}}")
    lines.append(f"\\caption{{Archivo: {nombre_archivo_escapado}}}\\label{{tab:{nombre_archivo}}} \\\\")
    lines.append("\\toprule")
    lines.append(header_row)
    lines.append("\\midrule")
    lines.append("\\endfirsthead")
    lines.append("\\toprule")
    lines.append(header_row)
    lines.append("\\midrule")
    lines.append("\\endhead")
    lines.append("\\midrule")
    lines.append(f"\\multicolumn{{{n_cols}}}{{r}}{{Continued on next page}} \\\\")
    lines.append("\\midrule")
    lines.append("\\endfoot")
    lines.append("\\bottomrule")
    lines.append("\\endlastfoot")
    lines.extend(data_rows)
    lines.append("\\end{longtable}")

    tabla_latex = "\n".join(lines)

    ruta_relativa = os.path.relpath(archivo_csv, carpeta_origen)
    nueva_ruta = os.path.join(carpeta_destino, os.path.dirname(ruta_relativa))
    os.makedirs(nueva_ruta, exist_ok=True)
    archivo_salida = os.path.join(nueva_ruta, f"{nombre_archivo}.tex")

    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write(tabla_latex)

def procesar_csvs(carpeta_origen, carpeta_destino, decimales):
    encontrados = 0
    for root, _, files in os.walk(carpeta_origen):
        for file in files:
            if file.endswith(".csv"):
                encontrados += 1
                archivo_csv = os.path.join(root, file)
                csv_a_latex(archivo_csv, carpeta_destino, carpeta_origen, decimales)
    return encontrados

def ejecutar():
    try:
        decimales = int(entrada_decimales.get())
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa un número entero para los decimales.")
        return

    carpeta_origen = seleccionar_carpeta("Selecciona la carpeta de origen (CSV)")
    if not carpeta_origen:
        return

    carpeta_destino = seleccionar_carpeta("Selecciona la carpeta de destino (LaTeX)")
    if not carpeta_destino:
        return

    cantidad = procesar_csvs(carpeta_origen, carpeta_destino, decimales)
    messagebox.showinfo("Proceso completado", f"Se procesaron {cantidad} archivos CSV.")

# Interfaz
ventana = tk.Tk()
ventana.title("CSV a LaTeX Longtable")
ventana.geometry("420x250")
ventana.resizable(False, False)

label = tk.Label(ventana, text="Conversor de CSV a LaTeX (formato longtable)", font=("Arial", 12))
label.pack(pady=15)

frame_dec = tk.Frame(ventana)
frame_dec.pack()

label_decimales = tk.Label(frame_dec, text="Número de decimales:", font=("Arial", 10))
label_decimales.pack(side="left", padx=5)

entrada_decimales = tk.Entry(frame_dec, width=5)
entrada_decimales.insert(0, "6")  # Valor por defecto
entrada_decimales.pack(side="left", padx=5)

boton = tk.Button(ventana, text="Seleccionar carpetas y ejecutar", font=("Arial", 11), command=ejecutar)
boton.pack(pady=20)

ventana.mainloop()

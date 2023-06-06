import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox

class ImageGalleryApp:
    def __init__(self, root):
        self.root = root
        self.current_image_index = 0
        self.images = []
        self.current_directory = ""
        self.current_image_label = None

        # Configurar la ventana principal
        self.root.title("Image Gallery")
        self.root.geometry("800x600")

        # Crear la galeria de imagenes en el lado izquierdo
        self.image_canvas = tk.Canvas(self.root, width=550, height=600)
        self.image_canvas.pack(side=tk.LEFT)

        # Agregar boton para seleccionar el directorio de imagenes
        select_dir_button = tk.Button(self.root, text="Select Directory", command=self.select_directory)
        select_dir_button.pack(side=tk.TOP)

        # Agregar boton para crear una nueva carpeta
        create_folder_button = tk.Button(self.root, text="Create Folder", command=self.create_folder)
        create_folder_button.pack(side=tk.TOP)

        # Agregar lista de carpetas en el lado derecho
        self.folder_listbox = tk.Listbox(self.root, width=30)
        self.folder_listbox.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.folder_listbox.bind("<<ListboxSelect>>", self.move_image_to_folder)


    def select_directory(self):
        # Abrir el dialogo para seleccionar el directorio de imagenes
        self.current_directory = filedialog.askdirectory()

        # Obtener la lista de archivos de imagen en el directorio
        self.images = [file for file in os.listdir(self.current_directory) if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        self.current_image_index = 0

        # Actualizar la galeria de imagenes
        self.show_current_image()

        # Actualizar la lista de carpetas en el lado derecho
        self.update_folder_list()

    def update_folder_list(self):
        # Limpiar la lista de carpetas
        self.folder_listbox.delete(0, tk.END)

        # Obtener la lista de carpetas en el directorio actual
        folders = [folder for folder in os.listdir(self.current_directory) if os.path.isdir(os.path.join(self.current_directory, folder))]

        # Agregar las carpetas a la lista
        for folder in folders:
            self.folder_listbox.insert(tk.END, folder)

    def show_current_image(self):
        # Eliminar la imagen actual si existe
        if self.current_image_label:
            self.image_canvas.delete(self.current_image_label)

        # Obtener la ruta completa de la imagen actual
        current_image_path = os.path.join(self.current_directory, self.images[self.current_image_index])

        # Cargar la imagen utilizando Pillow
        image = Image.open(current_image_path)
        image.thumbnail((500, 500))  # Ajustar el tamano de la imagen para que se ajuste en el lienzo

        # Convertir la imagen a un objeto compatible con Tkinter
        tk_image = ImageTk.PhotoImage(image)

        # Mostrar la imagen en el lienzo
        self.current_image_label = self.image_canvas.create_image(10, 10, anchor=tk.NW, image=tk_image)
        self.image_canvas.image = tk_image

    def show_next_image(self):
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.show_current_image()

    def show_previous_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_current_image()

    def move_image_to_folder(self, event):
        # Obtener el indice de la carpeta seleccionada en la lista
        selected_index = self.folder_listbox.curselection()

        if selected_index:
            selected_folder = self.folder_listbox.get(selected_index)
            selected_folder_path = os.path.join(self.current_directory, selected_folder)

            # Mover la imagen actual a la carpeta seleccionada
            try:
                current_image_path = os.path.join(self.current_directory, self.images[self.current_image_index])
                new_image_path = os.path.join(selected_folder_path, self.images[self.current_image_index])
                os.makedirs(selected_folder_path, exist_ok=True)
                os.rename(current_image_path, new_image_path)
                self.show_next_image()  # Mostrar la siguiente imagen despues de moverla
                self.update_folder_list()  # Actualizar la lista de carpetas despues de mover la imagen
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def create_folder(self):
        # Abrir el cuadro de dialogo para ingresar el nombre de la nueva carpeta
        folder_name = tk.simpledialog.askstring("Create Folder", "Enter folder name:")
        if folder_name:
            new_folder_path = os.path.join(self.current_directory, folder_name)
            try:
                os.makedirs(new_folder_path, exist_ok=True)
                messagebox.showinfo("Folder Created", "New folder created successfully.")
                self.update_folder_list()  # Actualizar la lista de carpetas despues de crear una nueva carpeta
            except Exception as e:
                messagebox.showerror("Error", str(e))

root = tk.Tk()
app = ImageGalleryApp(root)
root.mainloop()
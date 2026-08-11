import flet as ft

def main(page: ft.Page):
    # Configuration de la fenêtre
    page.title = "Mini Compteur"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 300
    page.window_height = 250

    # Élément de texte pour afficher la valeur
    txt_number = ft.Text(value="0", size=40, weight=ft.FontWeight.BOLD)

    # Fonctions pour gérer les clics
    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    # Ajout des composants graphiques à la page
    page.add(
        ft.Text("Mon Compteur Flet", size=20, color=ft.Colors.BLUE),
        ft.Row(
            controls=[
                ft.IconButton(ft.Icons.REMOVE, on_click=minus_click, icon_color=ft.Colors.RED),
                txt_number,
                ft.IconButton(ft.Icons.ADD, on_click=plus_click, icon_color=ft.Colors.GREEN),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

# Lancer l'application
ft.app(target=main)

import flet as ft
from congress import all_lists, move_to_next_list, add_person_to_list


class RecencyTrackerApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Recency Tracker"
        self.page.window_width = 900
        self.page.window_height = 700
        
        # PO Info state
        self.po_name = ""
        self.po_round = ""
        self.po_room = ""
        
        self.build_ui()
    
    def build_ui(self):
        """Build the main UI layout."""
        # PO Info Input Section
        self.po_name_input = ft.TextField(label="P.O. Name", width=250)
        self.po_round_input = ft.TextField(label="Round Name", width=250)
        self.po_room_input = ft.TextField(label="Room Number", width=250)
        
        po_info_section = ft.Column(
            [
                ft.Text("P.O. Information", size=18, weight="bold"),
                self.po_name_input,
                self.po_round_input,
                self.po_room_input,
                ft.ElevatedButton(
                    "Save P.O. Info",
                    on_click=self.save_po_info
                ),
            ],
            spacing=10,
            visible=True
        )
        
        # Person entry section
        self.new_person_input = ft.TextField(
            label="Enter person name",
            width=250,
            on_submit=self.add_person_handler
        )
        
        person_entry_section = ft.Column(
            [
                ft.Text("Add Person to List", size=18, weight="bold"),
                self.new_person_input,
                ft.ElevatedButton(
                    "Add Person",
                    on_click=self.add_person_handler
                ),
            ],
            spacing=10,
            visible=True
        )
        
        # Lists display section
        self.lists_container = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)
        
        lists_section = ft.Column(
            [
                ft.Text("Current Lists", size=18, weight="bold"),
                self.lists_container,
            ],
            spacing=10,
            expand=True
        )
        
        # Main layout
        main_column = ft.Column(
            [
                po_info_section,
                ft.Divider(),
                person_entry_section,
                ft.Divider(),
                lists_section,
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        
        self.page.add(main_column)
        self.refresh_lists_display()
    
    def save_po_info(self, e):
        """Save P.O. information."""
        self.po_name = self.po_name_input.value
        self.po_round = self.po_round_input.value
        self.po_room = self.po_room_input.value
        
        if self.po_name and self.po_round and self.po_room:
            self.show_snackbar("P.O. information saved successfully!")
        else:
            self.show_snackbar("Please fill in all P.O. fields!")
    
    def add_person_handler(self, e):
        """Handle adding a person to the list."""
        person_name = self.new_person_input.value.strip()
        
        if not self.po_name:
            self.show_snackbar("Please save P.O. info first!")
            return
        
        if person_name:
            add_person_to_list(person_name)
            self.new_person_input.value = ""
            self.refresh_lists_display()
            self.show_snackbar(f"Added {person_name} to the list!")
        else:
            self.show_snackbar("Please enter a person's name!")
        
        self.page.update()
    
    def move_person_handler(self, list_index, person_index):
        """Handle moving a person to the next list."""
        def on_click(e):
            if move_to_next_list(list_index, person_index):
                self.show_snackbar(f"Person moved from list {list_index} successfully!")
                self.refresh_lists_display()
            else:
                self.show_snackbar("Error moving person!")
            self.page.update()
        
        return on_click
    
    def refresh_lists_display(self):
        """Refresh the display of all lists."""
        self.lists_container.controls.clear()
        
        if not self.po_name:
            self.lists_container.controls.append(
                ft.Text("Enter P.O. information first", color="gray")
            )
            self.page.update()
            return
        
        # Display P.O. info header
        po_info_text = ft.Text(
            f"P.O: {self.po_name} | Round: {self.po_round} | Room: {self.po_room}",
            size=14,
            weight="bold"
        )
        self.lists_container.controls.append(po_info_text)
        self.lists_container.controls.append(ft.Divider(height=10))
        
        # Display each list
        if not any(all_lists):
            self.lists_container.controls.append(
                ft.Text("No people in lists yet", color="gray")
            )
        else:
            for list_index, current_list in enumerate(all_lists):
                list_card = self.build_list_card(list_index, current_list)
                self.lists_container.controls.append(list_card)
        
        self.page.update()
    
    def build_list_card(self, list_index, current_list):
        """Build a card displaying a single list."""
        list_items = ft.Column(spacing=8)
        
        for person_index, person in enumerate(current_list):
            person_row = ft.Row(
                [
                    ft.Text(f"{person_index}: {person}", expand=True, size=13),
                    ft.ElevatedButton(
                        "Move →",
                        size=ft.ButtonSize.SMALL,
                        on_click=self.move_person_handler(list_index, person_index)
                    ),
                ],
                spacing=10,
            )
            list_items.controls.append(person_row)
        
        list_card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"List {list_index}", size=14, weight="bold", color="blue"),
                        ft.Divider(height=5),
                        list_items,
                    ],
                    spacing=5,
                ),
                padding=15,
            ),
            margin=5,
        )
        
        return list_card
    
    def show_snackbar(self, message):
        """Display a snackbar notification."""
        snack = ft.SnackBar(ft.Text(message))
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()


def main():
    def create_app(page: ft.Page):
        app = RecencyTrackerApp(page)
    
    ft.app(target=create_app)


if __name__ == "__main__":
    main()

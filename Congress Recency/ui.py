import flet as ft
from congress import all_lists, move_to_next_list, add_person_to_list


class RecencyTrackerApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Recency Tracker"
        self.page.window_width = 900
        self.page.window_height = 700
        
        # Role state
        self.user_role = None  # "po" or "speaker"
        
        # PO Info state
        self.po_name = ""
        self.po_round = ""
        self.po_room = ""
        
        self.build_ui()
    
    def build_ui(self):
        """Build the main UI layout with role-based menu."""
        self.page.clean()
        self.show_role_menu()
    
    def show_role_menu(self):
        """Display the initial role selection menu."""
        menu_column = ft.Column(
            [
                ft.Text("Welcome to Recency Tracker", size=28, weight="bold"),
                ft.Text("Please select your role:", size=16),
                ft.SizedBox(height=20),
                ft.ElevatedButton(
                    "P.O. (Presiding Officer)",
                    on_click=lambda e: self.set_role("po"),
                    width=300,
                    height=60,
                    style=ft.ButtonStyle(text_style=ft.TextStyle(size=14))
                ),
                ft.SizedBox(height=15),
                ft.ElevatedButton(
                    "Speaker",
                    on_click=lambda e: self.set_role("speaker"),
                    width=300,
                    height=60,
                    style=ft.ButtonStyle(text_style=ft.TextStyle(size=14))
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            spacing=15,
        )
        
        self.page.add(menu_column)
    
    def set_role(self, role):
        """Set the user role and show appropriate interface."""
        self.user_role = role
        self.page.clean()
        
        if role == "po":
            self.build_po_interface()
        else:
            self.build_speaker_interface()
    
    def logout(self, e=None):
        """Return to role selection menu."""
        self.user_role = None
        self.page.clean()
        self.show_role_menu()
    
    def build_po_interface(self):
        """Build the P.O. only interface with edit capabilities."""
        # P.O. Info Input Section
        self.po_name_input = ft.TextField(label="P.O. Name", width=250, value=self.po_name)
        self.po_round_input = ft.TextField(label="Round Name", width=250, value=self.po_round)
        self.po_room_input = ft.TextField(label="Room Number", width=250, value=self.po_room)
        
        po_info_section = ft.Column(
            [
                ft.Text("P.O. Only Area - Edit Information", size=18, weight="bold", color="darkred"),
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
            label="Enter speaker name",
            width=250,
            on_submit=self.add_person_handler
        )
        
        person_entry_section = ft.Column(
            [
                ft.Text("Add Speaker to Queue", size=18, weight="bold"),
                self.new_person_input,
                ft.ElevatedButton(
                    "Add Speaker",
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
                ft.Text("Current Speaker Lists", size=18, weight="bold"),
                self.lists_container,
            ],
            spacing=10,
            expand=True
        )
        
        # Logout button
        logout_button = ft.ElevatedButton(
            "Logout",
            on_click=self.logout,
            style=ft.ButtonStyle(bgcolor="lightgray")
        )
        
        # Main layout
        main_column = ft.Column(
            [
                po_info_section,
                ft.Divider(),
                person_entry_section,
                ft.Divider(),
                lists_section,
                ft.Divider(),
                logout_button,
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        
        self.page.add(main_column)
        self.refresh_lists_display()
    
    def build_speaker_interface(self):
        """Build the Speaker read-only interface."""
        # Round Info Display (read-only)
        self.round_info_display = ft.Column(spacing=10)
        
        round_info_section = ft.Column(
            [
                ft.Text("Round Info", size=18, weight="bold", color="darkblue"),
                self.round_info_display,
            ],
            spacing=10,
        )
        
        # Lists display section (read-only)
        self.lists_container_speaker = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)
        
        lists_section = ft.Column(
            [
                ft.Text("Speaker Queue & Lists", size=18, weight="bold"),
                self.lists_container_speaker,
            ],
            spacing=10,
            expand=True
        )
        
        # Logout button
        logout_button = ft.ElevatedButton(
            "Logout",
            on_click=self.logout,
            style=ft.ButtonStyle(bgcolor="lightgray")
        )
        
        # Main layout
        main_column = ft.Column(
            [
                round_info_section,
                ft.Divider(),
                lists_section,
                ft.Divider(),
                logout_button,
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        
        self.page.add(main_column)
        self.refresh_speaker_display()
    
    def save_po_info(self, e):
        """Save P.O. information."""
        self.po_name = self.po_name_input.value
        self.po_round = self.po_round_input.value
        self.po_room = self.po_room_input.value
        
        if self.po_name and self.po_round and self.po_room:
            self.show_snackbar("P.O. information saved successfully!")
            self.refresh_lists_display()
        else:
            self.show_snackbar("Please fill in all P.O. fields!")
    
    def add_person_handler(self, e):
        """Handle adding a speaker to the queue (P.O. only)."""
        person_name = self.new_person_input.value.strip()
        
        if not self.po_name:
            self.show_snackbar("Please save P.O. info first!")
            return
        
        if person_name:
            add_person_to_list(person_name)
            self.new_person_input.value = ""
            self.refresh_lists_display()
            self.show_snackbar(f"Added {person_name} to the queue!")
        else:
            self.show_snackbar("Please enter a speaker's name!")
        
        self.page.update()
    
    def move_person_handler(self, list_index, person_index):
        """Handle moving a speaker to the next round (P.O. only)."""
        def on_click(e):
            if move_to_next_list(list_index, person_index):
                self.show_snackbar(f"Speaker moved to next round!")
                self.refresh_lists_display()
            else:
                self.show_snackbar("Error moving speaker!")
            self.page.update()
        
        return on_click
    
    def refresh_lists_display(self):
        """Refresh the P.O. display of all lists with edit buttons."""
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
            weight="bold",
            color="darkblue"
        )
        self.lists_container.controls.append(po_info_text)
        self.lists_container.controls.append(ft.Divider(height=10))
        
        # Display each list
        if not any(all_lists):
            self.lists_container.controls.append(
                ft.Text("No speakers in queue yet", color="gray")
            )
        else:
            for list_index, current_list in enumerate(all_lists):
                list_card = self.build_po_list_card(list_index, current_list)
                self.lists_container.controls.append(list_card)
        
        self.page.update()
    
    def build_po_list_card(self, list_index, current_list):
        """Build a card displaying a single list for P.O. (with edit buttons)."""
        list_items = ft.Column(spacing=8)
        
        for person_index, person in enumerate(current_list):
            person_row = ft.Row(
                [
                    ft.Text(f"{person_index + 1}: {person}", expand=True, size=13),
                    ft.ElevatedButton(
                        "Move →",
                        on_click=self.move_person_handler(list_index, person_index),
                        width=80,
                        height=35
                    ),
                ],
                spacing=10,
            )
            list_items.controls.append(person_row)
        
        list_card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"List {list_index + 1}", size=14, weight="bold", color="blue"),
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
    
    def refresh_speaker_display(self):
        """Refresh the Speaker view with round info and speaker queue (read-only)."""
        # Update round info display
        self.round_info_display.controls.clear()
        
        if not self.po_name:
            self.round_info_display.controls.append(
                ft.Text("Waiting for P.O. to enter round information...", color="gray", italic=True)
            )
        else:
            self.round_info_display.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(f"Presiding Officer: {self.po_name}", size=14, weight="bold"),
                                ft.Text(f"Round: {self.po_round}", size=14),
                                ft.Text(f"Room: {self.po_room}", size=14),
                            ],
                            spacing=8,
                        ),
                        padding=15,
                    ),
                    margin=5,
                )
            )
        
        # Update speaker lists display (read-only)
        self.lists_container_speaker.controls.clear()
        
        if not any(all_lists):
            self.lists_container_speaker.controls.append(
                ft.Text("No speakers in queue yet", color="gray", italic=True)
            )
        else:
            # Show current speaker (first person in first list)
            if all_lists[0]:
                current_speaker = all_lists[0][0]
                self.lists_container_speaker.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Currently Speaking:", size=12, weight="bold", color="green"),
                                    ft.Text(current_speaker, size=16, weight="bold", color="darkgreen"),
                                ],
                                spacing=5,
                            ),
                            padding=15,
                            bgcolor="lightgreen"
                        ),
                        margin=5,
                    )
                )
            
            # Show remaining speaker queues
            for list_index, current_list in enumerate(all_lists):
                list_card = self.build_speaker_list_card(list_index, current_list)
                self.lists_container_speaker.controls.append(list_card)
        
        self.page.update()
    
    def build_speaker_list_card(self, list_index, current_list):
        """Build a read-only card displaying a speaker list."""
        list_items = ft.Column(spacing=8)
        
        for person_index, person in enumerate(current_list):
            person_row = ft.Row(
                [
                    ft.Text(f"{person_index + 1}: {person}", expand=True, size=13),
                ],
                spacing=10,
            )
            list_items.controls.append(person_row)
        
        list_card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"List {list_index + 1}", size=14, weight="bold", color="blue"),
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

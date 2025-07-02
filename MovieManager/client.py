import tkinter as tk
from tkinter import messagebox
import json
import socket
from typing import Dict, List, Tuple
from datetime import datetime
import ttkbootstrap as ttk

class ModernSocketClient:
    def __init__(self, host='54.165.166.21', port=8000):
        self.host = host
        self.port = port
        self.socket = None
        self.timeout = 5
        
    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.host, self.port))
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False
            
    def disconnect(self):
        if self.socket:
            try:
                self.socket.close()
            except Exception as e:
                print(f"Error closing socket: {e}")
            finally:
                self.socket = None
            
    def send_message(self, message: dict) -> dict:
        if not self.socket:
            return {"status": "error", "message": "Not connected to server"}
            
        try:
            message_data = json.dumps(message).encode()
            self.socket.sendall(message_data)
            response_data = self.socket.recv(4096)
            if not response_data:
                return {"status": "error", "message": "Empty response from server"}
            return json.loads(response_data.decode())
        except Exception as e:
            return {"status": "error", "message": f"Communication error: {str(e)}"}

class ModernMovieBookingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Movie Booking System")
        self.root.geometry("1000x700")
        
        # Define the new color palette
        self.light_grey_bg = "#F0F0F0"      # Primary background
        self.medium_grey_bg = "#E0E0E0"     # Secondary background for panels/frames
        self.vibrant_teal = "#00ADB5"       # Accent color for interactive elements
        self.dark_charcoal = "#393E46"      # Dark text color
        self.bright_orange = "#FF8C00"      # Highlight/warning color
        
        # Configure ttkbootstrap styles
        self.style = ttk.Style()
        
        # Configure the root window's background
        self.root.configure(background=self.light_grey_bg)

        # Custom styles for Frames
        self.style.configure("LightGrey.TFrame", background=self.light_grey_bg)
        self.style.configure("MediumGrey.TFrame", background=self.medium_grey_bg)
        
        # Custom styles for Labels
        self.style.configure("Header.TLabel", 
                             background=self.light_grey_bg, 
                             foreground=self.dark_charcoal,
                             font=("Helvetica", 24, "bold"))
        self.style.configure("Standard.TLabel", 
                             background=self.medium_grey_bg, # Labels inside frames
                             foreground=self.dark_charcoal,
                             font=("Helvetica", 12))
        self.style.configure("Panel.TLabel", # Labels on panels
                             background=self.light_grey_bg,
                             foreground=self.dark_charcoal,
                             font=("Helvetica", 12))

        # Custom styles for LabelFrames
        self.style.configure("MediumGrey.TLabelframe", 
                             background=self.medium_grey_bg,
                             foreground=self.dark_charcoal,
                             bordercolor=self.vibrant_teal) # Border color for labelframe
        self.style.configure("MediumGrey.TLabelframe.Label", # The actual label text (e.g. "Movie Selection")
                             background=self.medium_grey_bg, 
                             foreground=self.dark_charcoal, 
                             font=("Helvetica", 12, "bold"))

        # Custom style for Buttons
        self.style.configure("Custom.TButton", 
                             background=self.vibrant_teal,
                             foreground=self.light_grey_bg, # Light text on dark button
                             padding=10,
                             font=("Helvetica", 10, "bold"))
        self.style.map("Custom.TButton",
                       background=[("active", self.bright_orange)], # Hover effect
                       foreground=[("active", self.dark_charcoal)]) # Text changes on hover

        # Custom style for Entry widgets
        self.style.configure("Custom.TEntry", 
                             fieldbackground=self.light_grey_bg, # Input area background
                             foreground=self.dark_charcoal,   # Text color
                             insertcolor=self.vibrant_teal,  # Cursor color
                             bordercolor=self.vibrant_teal,  # Border color
                             relief="flat",
                             padding=5)
        self.style.map("Custom.TEntry",
                       fieldbackground=[("focus", self.medium_grey_bg)]) # Focus effect

        # Custom style for Combobox
        self.style.configure("Custom.TCombobox",
                             fieldbackground=self.light_grey_bg, # Input area background
                             foreground=self.dark_charcoal,
                             selectbackground=self.vibrant_teal, # Background of selected item in dropdown
                             selectforeground=self.light_grey_bg, # Foreground of selected item in dropdown
                             background=self.light_grey_bg, # Button part of combobox
                             arrowcolor=self.vibrant_teal, # Arrow color
                             bordercolor=self.vibrant_teal, # Border
                             padding=5)
        self.style.map("Custom.TCombobox",
                       fieldbackground=[("readonly", self.light_grey_bg)],
                       background=[("readonly", self.light_grey_bg)],
                       foreground=[("readonly", self.dark_charcoal)],
                       selectbackground=[("readonly", self.vibrant_teal)],
                       selectforeground=[("readonly", self.light_grey_bg)])


        # Initialize socket client
        self.socket_client = ModernSocketClient()
        if not self.socket_client.connect():
            messagebox.showerror("Connection Error", "Failed to connect to server")
            root.destroy()
            return
            
        # Initialize data
        self.movies = {}
        self.initialize_variables()
        self.setup_gui()
        self.load_movies()
        
    def initialize_variables(self):
        self.movie_var = tk.StringVar()
        self.customer_var = tk.StringVar()
        self.ticket_var = tk.StringVar()
        self.add_name_var = tk.StringVar()
        self.add_price_var = tk.StringVar()
        self.add_tickets_var = tk.StringVar()
        self.add_room_var = tk.StringVar()
        self.add_release_date_var = tk.StringVar()
        self.add_end_date_var = tk.StringVar()
        self.update_price_var = tk.StringVar()
        self.update_tickets_var = tk.StringVar()
        self.update_room_var = tk.StringVar()
        self.update_release_date_var = tk.StringVar()
        self.update_end_date_var = tk.StringVar()
        
    def setup_gui(self):
        # Main container with specific background
        self.main_container = ttk.Frame(self.root, style="LightGrey.TFrame", padding="20")
        self.main_container.pack(fill="both", expand=True)
        
        # Header
        self.setup_header()
        
        # Content area
        self.content_frame = ttk.Frame(self.main_container, style="LightGrey.TFrame")
        self.content_frame.pack(fill="both", expand=True, pady=20)
        
        # Left panel (Movie Info)
        self.setup_left_panel()
        
        # Right panel (Booking)
        self.setup_right_panel()
        
        # Management frames (initially hidden)
        self.setup_management_frames()
        
    def setup_header(self):
        header_frame = ttk.Frame(self.main_container, style="LightGrey.TFrame")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Title with modern font and text color
        title_label = ttk.Label(header_frame, 
                              text="Movie Ticket Booking System",
                              style="Header.TLabel") # Use custom style for header label
        title_label.pack(side="left", padx=10)
        
        # Navigation buttons
        nav_frame = ttk.Frame(header_frame, style="LightGrey.TFrame")
        nav_frame.pack(side="right", padx=10)
        
        buttons = [
            ("Add Movie", self.show_add_movie),
            ("Update Movie", self.show_update_movie),
            ("Delete Movie", self.delete_movie)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(nav_frame, 
                           text=text,
                           command=command,
                           style="Custom.TButton") # Use custom style for buttons
            btn.pack(side="left", padx=5)
            
    def setup_left_panel(self):
        left_panel = ttk.Frame(self.content_frame, style="LightGrey.TFrame")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Movie selection
        self.setup_movie_selection(left_panel)
        
        # Movie info
        self.setup_movie_info(left_panel)
        
    def setup_right_panel(self):
        right_panel = ttk.Frame(self.content_frame, style="LightGrey.TFrame")
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Booking form
        booking_frame = ttk.LabelFrame(right_panel, 
                                     text="Book Tickets",
                                     padding="15",
                                     style="MediumGrey.TLabelframe") # Use custom style for LabelFrame
        booking_frame.pack(fill="x", pady=(0, 10))
        
        # Customer name
        ttk.Label(booking_frame, 
                 text="Customer Name:",
                 style="Standard.TLabel").pack(fill="x", pady=(0, 5)) # Use standard label style
        ttk.Entry(booking_frame, 
                 textvariable=self.customer_var,
                 style="Custom.TEntry", # Use custom entry style
                 font=("Helvetica", 12)).pack(fill="x", pady=(0, 10))
        
        # Number of tickets
        ttk.Label(booking_frame, 
                 text="Number of Tickets:",
                 style="Standard.TLabel").pack(fill="x", pady=(0, 5)) # Use standard label style
        self.ticket_entry = ttk.Entry(booking_frame, 
                                    textvariable=self.ticket_var,
                                    style="Custom.TEntry", # Use custom entry style
                                    font=("Helvetica", 12))
        self.ticket_entry.pack(fill="x", pady=(0, 10))
        
        # Purchase button
        ttk.Button(booking_frame,
                  text="Purchase Tickets",
                  command=self.calculate_total,
                  style="Custom.TButton").pack(fill="x", pady=10) # Use custom button style
                  
    def setup_management_frames(self):
        # Add Movie Form
        self.add_movie_frame = ttk.LabelFrame(self.main_container,
                                            text="Add New Movie",
                                            padding="15",
                                            style="MediumGrey.TLabelframe") # Use custom style for LabelFrame
        
        # Add movie form fields
        add_grid = ttk.Frame(self.add_movie_frame, style="MediumGrey.TFrame") # Use custom style for inner frame
        add_grid.pack(fill="x", padx=5, pady=5)
        
        fields = [
            ("Movie Name:", self.add_name_var),
            ("Price:", self.add_price_var),
            ("Available Tickets:", self.add_tickets_var),
            ("Cinema Room:", self.add_room_var),
            ("Release Date (YYYY-MM-DD):", self.add_release_date_var),
            ("End Date (YYYY-MM-DD):", self.add_end_date_var)
        ]
        
        for i, (label, var) in enumerate(fields):
            ttk.Label(add_grid, text=label, 
                      style="Standard.TLabel").grid(row=i, column=0, sticky="w", padx=5, pady=2) # Use standard label style
            ttk.Entry(add_grid, textvariable=var, width=30, style="Custom.TEntry").grid(row=i, column=1, sticky="w", padx=5, pady=2) # Use custom entry style
        
        ttk.Button(add_grid, text="Save Movie", command=self.save_new_movie, style="Custom.TButton").grid(row=len(fields), column=0, columnspan=2, pady=10) # Use custom button style
        
        # Update Movie Form
        self.update_movie_frame = ttk.LabelFrame(self.main_container,
                                               text="Update Movie",
                                               padding="15",
                                               style="MediumGrey.TLabelframe") # Use custom style for LabelFrame
        
        # Grid layout for update movie form
        update_grid = ttk.Frame(self.update_movie_frame, style="MediumGrey.TFrame") # Use custom style for inner frame
        update_grid.pack(fill="x", padx=5, pady=5)
        
        fields = [
            ("New Price:", self.update_price_var),
            ("Available Tickets:", self.update_tickets_var),
            ("Cinema Room:", self.update_room_var),
            ("Release Date (YYYY-MM-DD):", self.update_release_date_var),
            ("End Date (YYYY-MM-DD):", self.update_end_date_var)
        ]
        
        for i, (label, var) in enumerate(fields):
            ttk.Label(update_grid, text=label,
                      style="Standard.TLabel").grid(row=i, column=0, sticky="w", padx=5, pady=2) # Use standard label style
            ttk.Entry(update_grid, textvariable=var, width=30, style="Custom.TEntry").grid(row=i, column=1, sticky="w", padx=5, pady=2) # Use custom entry style
        
        ttk.Button(update_grid, text="Update Movie", command=self.save_updated_movie, style="Custom.TButton").grid(row=len(fields), column=0, columnspan=2, pady=10) # Use custom button style
                                               
    def setup_movie_selection(self, parent):
        # Movie selection frame
        movie_frame = ttk.LabelFrame(parent, 
                                    text="Movie Selection",
                                    padding="15",
                                    style="MediumGrey.TLabelframe") # Use custom style for LabelFrame
        movie_frame.pack(fill="x", pady=(0, 10))
        
        # Movie dropdown
        ttk.Label(movie_frame, 
                 text="Select Movie:",
                 style="Standard.TLabel").pack(side="left", padx=5) # Use standard label style
        self.movie_dropdown = ttk.Combobox(movie_frame, 
                                         textvariable=self.movie_var,
                                         width=30,
                                         font=("Helvetica", 12),
                                         state="readonly",
                                         style="Custom.TCombobox") # Use custom combobox style
        self.movie_dropdown.pack(side="left", padx=5, fill="x", expand=True)
        self.movie_dropdown.bind('<<ComboboxSelected>>', self.update_movie_info)

    def setup_movie_info(self, parent):
        # Movie info frame
        info_frame = ttk.LabelFrame(parent, 
                                   text="Movie Information",
                                   padding="15",
                                   style="MediumGrey.TLabelframe") # Use custom style for LabelFrame
        info_frame.pack(fill="x", pady=(0, 10))
        
        # Grid layout for movie info
        info_grid = ttk.Frame(info_frame, style="MediumGrey.TFrame") # Use custom style for inner frame
        info_grid.pack(fill="x", padx=5, pady=5)
        
        # First row
        ttk.Label(info_grid, 
                 text="Price:",
                 style="Standard.TLabel").grid(row=0, column=0, sticky="w", padx=5, pady=2) # Use standard label style
        self.cost_label = ttk.Label(info_grid, 
                                  text="R0.00",
                                  font=("Helvetica", 12),
                                  style="Standard.TLabel") # Use standard label style
        self.cost_label.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(info_grid, 
                 text="Cinema Room:",
                 style="Standard.TLabel").grid(row=0, column=2, sticky="w", padx=7, pady=2) # Use standard label style
        self.room_label = ttk.Label(info_grid, 
                                  text="0",
                                  font=("Helvetica", 12),
                                  style="Standard.TLabel") # Use standard label style
        self.room_label.grid(row=0, column=3, sticky="w", padx=5, pady=2)
        
        # Second row
        ttk.Label(info_grid, 
                 text="Tickets:",
                 style="Standard.TLabel").grid(row=1, column=0, sticky="w", padx=5, pady=2) # Use standard label style
        self.tickets_left_label = ttk.Label(info_grid, 
                                         text="0",
                                         font=("Helvetica", 12),
                                         style="Standard.TLabel") # Use standard label style
        self.tickets_left_label.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(info_grid, 
                 text="Release Date:",
                 style="Standard.TLabel").grid(row=1, column=2, sticky="w", padx=7, pady=2) # Use standard label style
        self.release_date_label = ttk.Label(info_grid, 
                                         text="",
                                         font=("Helvetica", 12),
                                         style="Standard.TLabel") # Use standard label style
        self.release_date_label.grid(row=1, column=3, sticky="w", padx=5, pady=2)
        
        # Third row
        ttk.Label(info_grid, 
                 text="End Date:",
                 style="Standard.TLabel").grid(row=2, column=0, sticky="w", padx=5, pady=2) # Use standard label style
        self.end_date_label = ttk.Label(info_grid, 
                                      text="",
                                      font=("Helvetica", 12),
                                      style="Standard.TLabel") # Use standard label style
        self.end_date_label.grid(row=2, column=1, columnspan=3, sticky="w", padx=5, pady=2)
            
    def validate_numeric_input(self, value: str, min_value: float = 0) -> tuple[bool, float]:
        try:
            num_value = float(value)
            if num_value < min_value:
                return False, num_value
            return True, num_value
        except ValueError:
            return False, 0
            
    def load_movies(self):
        response = self.socket_client.send_message({
            "action": "load"
        })
        
        if response.get("status") == "ok":
            records = response.get("record", [])
            if isinstance(records, list):
                self.movies = {}
                for movie in records:
                    if isinstance(movie, dict):
                        title = movie.get("title")
                        if title:
                            self.movies[title] = [
                                float(movie.get("ticket_price", 0)),
                                int(movie.get("tickets_available", 0)),
                                int(movie.get("cinema_room", 1)),
                                movie.get("release_date", ""),
                                movie.get("end_date", "")
                            ]
                            
                self.movie_dropdown['values'] = list(self.movies.keys())
                if self.movies:
                    self.movie_var.set(list(self.movies.keys())[0])
                    self.update_movie_info()
        else:
            messagebox.showerror("Error", response.get("message", "Failed to load movies"))
            
    def show_add_movie(self):
        self.add_movie_frame.pack(fill="x", pady=10)
        self.update_movie_frame.pack_forget()
        
    def show_update_movie(self):
        selected_movie = self.movie_var.get()
        if not selected_movie:
            messagebox.showerror("Error", "Please select a movie to update")
            return
            
        self.update_movie_frame.pack(fill="x", pady=10)
        self.add_movie_frame.pack_forget()
        
        # Set current values
        price, tickets, room, release_date, end_date = self.movies[selected_movie]
        self.update_price_var.set(str(price))
        self.update_tickets_var.set(str(tickets))
        self.update_room_var.set(str(room))
        self.update_release_date_var.set(release_date)
        self.update_end_date_var.set(end_date)
        
    def update_movie_info(self, event=None):
        selected_movie = self.movie_var.get()
        if selected_movie in self.movies:
            price, tickets, room, release_date, end_date = self.movies[selected_movie]
            self.tickets_left_label.config(text=str(tickets))
            self.cost_label.config(text=f"R{price:.2f}")
            self.room_label.config(text=str(room))
            self.release_date_label.config(text=release_date)
            self.end_date_label.config(text=end_date)
            
    def calculate_total(self):
        selected_movie = self.movie_var.get()
        if not selected_movie:
            messagebox.showerror("Error", "Please select a movie")
            return
            
        customer_name = self.customer_var.get().strip()
        if not customer_name:
            messagebox.showerror("Error", "Please enter customer name")
            return
            
        quantity_str = self.ticket_var.get()
        if not quantity_str:
            messagebox.showerror("Error", "Please enter number of tickets")
            return
            
        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                messagebox.showerror("Error", "Please enter a valid quantity")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of tickets")
            return
            
        # Get movie_id from the selected movie
        movie_id = None
        for movie in self.movies:
            if movie == selected_movie:
                movie_id = str(list(self.movies.keys()).index(movie) + 1)
                break
        
        if not movie_id:
            messagebox.showerror("Error", "Invalid movie selection")
            return
            
        response = self.socket_client.send_message({
            "action": "sale",
            "payload": {
                "movie_id": movie_id,
                "customer_name": customer_name,
                "number_of_tickets": quantity
            }
        })
        
        if response.get("status") == "ok":
            # Update the UI with the new ticket count
            if selected_movie in self.movies:
                current_tickets = self.movies[selected_movie][1]
                new_tickets = current_tickets - quantity
                self.movies[selected_movie][1] = new_tickets
                self.tickets_left_label.config(text=str(new_tickets))
                
            # Clear the form
            self.customer_var.set("")
            self.ticket_var.set("")
            
            messagebox.showinfo("Success", f"Successfully purchased {quantity} tickets for {selected_movie}")
        else:
            error_msg = response.get("error", "Failed to process sale")
            messagebox.showerror("Error", error_msg)
        
    def save_new_movie(self):
        name = self.add_name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a movie name")
            return
            
        # Validate numeric inputs
        price_valid, price = self.validate_numeric_input(self.add_price_var.get(), 0.01)
        tickets_valid, tickets = self.validate_numeric_input(self.add_tickets_var.get(), 1)
        room_valid, room = self.validate_numeric_input(self.add_room_var.get(), 1)
        
        if not all([price_valid, tickets_valid, room_valid]):
            messagebox.showerror("Error", "Please enter valid numbers for price, tickets, and room")
            return
            
        # Validate dates
        release_date = self.add_release_date_var.get().strip()
        end_date = self.add_end_date_var.get().strip()
        
        if not release_date or not end_date:
            messagebox.showerror("Error", "Please enter both release and end dates")
            return
            
        if name in self.movies:
            messagebox.showerror("Error", "A movie with this name already exists")
            return
            
        # Print the request payload for debugging
        payload = {
            "action": "create",
            "payload": {
                "title": name,
                "cinema_room": str(int(room)),  # Ensure it's string, and int
                "release_date": release_date,
                "end_date": end_date,
                "tickets_available": int(tickets),
                "ticket_price": float(price)
            }
        }
        print("Sending request to server:", payload)
        
        response = self.socket_client.send_message(payload)
        print("Server response:", response)
        
        if response.get("status") == "ok":
            # Update local movies dictionary
            self.movies[name] = [float(price), int(tickets), int(room), release_date, end_date]
            
            # Update UI
            self.movie_dropdown['values'] = list(self.movies.keys())
            self.movie_var.set(name)
            self.add_movie_frame.pack_forget() # Hide add movie frame, not management_frame
            
            # Clear form fields
            self.add_name_var.set("")
            self.add_price_var.set("")
            self.add_tickets_var.set("")
            self.add_room_var.set("")
            self.add_release_date_var.set("")
            self.add_end_date_var.set("")
            
            # Update movie info display
            self.update_movie_info()
            messagebox.showinfo("Success", "Movie added successfully!")
        else:
            error_msg = response.get("message", "Failed to add movie")
            print("Error adding movie:", error_msg)
            messagebox.showerror("Error", error_msg)
            
    def save_updated_movie(self):
        selected_movie = self.movie_var.get()
        if not selected_movie:
            messagebox.showerror("Error", "Please select a movie to update")
            return
            
        # Get movie_id from the selected movie
        movie_id = None
        for movie in self.movies:
            if movie == selected_movie:
                movie_id = str(list(self.movies.keys()).index(movie) + 1)  # Convert to 1-based index
                break
        
        if not movie_id:
            messagebox.showerror("Error", "Invalid movie selection")
            return
            
        # Validate numeric inputs
        price_valid, price = self.validate_numeric_input(self.update_price_var.get(), 0.01)
        tickets_valid, tickets = self.validate_numeric_input(self.update_tickets_var.get(), 0)
        room_valid, room = self.validate_numeric_input(self.update_room_var.get(), 1)
        
        if not all([price_valid, tickets_valid, room_valid]):
            messagebox.showerror("Error", "Please enter valid numbers for price, tickets, and room")
            return
            
        # Validate dates
        release_date = self.update_release_date_var.get().strip()
        end_date = self.update_end_date_var.get().strip()
        
        if not release_date or not end_date:
            messagebox.showerror("Error", "Please enter both release and end dates")
            return
            
        # Create newData dictionary with only changed values
        newData = {}
        current_data = self.movies[selected_movie]
        
        if float(price) != current_data[0]:
            newData["ticket_price"] = float(price)
        if int(tickets) != current_data[1]:
            newData["tickets_available"] = int(tickets)
        if int(room) != current_data[2]:
            newData["cinema_room"] = int(room)
        if release_date != current_data[3]:
            newData["release_date"] = release_date
        if end_date != current_data[4]:
            newData["end_date"] = end_date
        
        if not newData:
            messagebox.showinfo("Info", "No changes detected")
            return
        
        response = self.socket_client.send_message({
            "action": "update",
            "payload": {
                "movie_id": movie_id,
                "newData": newData
            }
        })
        
        if response.get("status") == "ok":
            # Update local movies dictionary with new values
            self.movies[selected_movie] = [float(price), int(tickets), int(room), release_date, end_date]
            self.update_movie_frame.pack_forget() # Hide update movie frame
            self.update_movie_info()
            messagebox.showinfo("Success", "Movie updated successfully!")
        else:
            messagebox.showerror("Error", response.get("message", "Failed to update movie"))
            
    def delete_movie(self):
        selected_movie = self.movie_var.get()
        if not selected_movie:
            messagebox.showerror("Error", "Please select a movie to delete")
            return
            
        # Get movie_id from the selected movie
        movie_id = None
        for movie in self.movies:
            if movie == selected_movie:
                movie_id = str(list(self.movies.keys()).index(movie) + 1)  # Convert to 1-based index
                break
        
        if not movie_id:
            messagebox.showerror("Error", "Invalid movie selection")
            return
            
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {selected_movie}?"):
            response = self.socket_client.send_message({
                "action": "delete",
                "payload": {
                    "movie_id": movie_id
                }
            })
            
            if response.get("status") == "ok":
                del self.movies[selected_movie]
                self.movie_dropdown['values'] = list(self.movies.keys())
                if self.movies:
                    self.movie_var.set(list(self.movies.keys())[0])
                else:
                    self.movie_var.set('')
                self.cost_label.config(text="R0.00")
                self.tickets_left_label.config(text="0")
                self.room_label.config(text="0")
                self.release_date_label.config(text="")
                self.end_date_label.config(text="")
                messagebox.showinfo("Success", "Movie deleted successfully!")
            else:
                messagebox.showerror("Error", response.get("message", "Failed to delete movie"))
                
    def on_closing(self):
        if self.socket_client:
            self.socket_client.disconnect()
        self.root.destroy()

if __name__ == "__main__":
    # Initialize with a ttkbootstrap theme. "flatly" or "journal" are light themes.
    root = ttk.Window(themename="flatly") 
    app = ModernMovieBookingSystem(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
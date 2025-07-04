import tkinter as tk
from tkinter import messagebox
import json
import socket
from typing import Dict, List, Tuple
from datetime import datetime

class ModernSocketClient:
    def __init__(self, host='localhost', port=12345):
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

class SimpleMovieBookingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Booking System")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")

        self.socket_client = ModernSocketClient()
        if not self.socket_client.connect():
            messagebox.showerror("Connection Error", "Failed to connect to server")
            root.destroy()
            return

        self.movies = {}
        self.initialize_variables()
        self.setup_gui()
        self.load_movies()

    def initialize_variables(self):
        self.movie_var = tk.StringVar()
        self.customer_var = tk.StringVar()
        self.ticket_var = tk.StringVar()

    def setup_gui(self):
        # Header
        header = tk.Frame(self.root, bg="#f0f0f0")
        header.pack(fill="x", pady=(10, 0))
        tk.Label(header, text="Movie Ticket Booking System", font=("Helvetica", 20, "bold"), bg="#f0f0f0").pack(side="left", padx=10)
        btn_frame = tk.Frame(header, bg="#f0f0f0")
        btn_frame.pack(side="right", padx=10)
        tk.Button(btn_frame, text="Add Movie", command=self.show_add_movie, width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Update Movie", command=self.show_update_movie, width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Delete Movie", command=self.delete_movie, width=12).pack(side="left", padx=5)

        # Main content
        content = tk.Frame(self.root, bg="#f0f0f0")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        left = tk.Frame(content, bg="#f0f0f0")
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        right = tk.Frame(content, bg="#f0f0f0")
        right.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # Movie selection
        movie_sel = tk.LabelFrame(left, text="Movie Selection", bg="#e0e0e0", padx=10, pady=10)
        movie_sel.pack(fill="x", pady=(0, 10))
        tk.Label(movie_sel, text="Select Movie:", bg="#e0e0e0").pack(side="left")
        self.movie_dropdown = tk.OptionMenu(movie_sel, self.movie_var, "", command=self.update_movie_info)
        self.movie_dropdown.config(width=30)
        self.movie_dropdown.pack(side="left", padx=5, fill="x", expand=True)

        # Movie info
        info = tk.LabelFrame(left, text="Movie Information", bg="#e0e0e0", padx=10, pady=10)
        info.pack(fill="x")
        self.cost_label = tk.Label(info, text="Price: R0.00", bg="#e0e0e0", anchor="w")
        self.cost_label.pack(fill="x")
        self.room_label = tk.Label(info, text="Cinema Room: 0", bg="#e0e0e0", anchor="w")
        self.room_label.pack(fill="x")
        self.tickets_left_label = tk.Label(info, text="Tickets: 0", bg="#e0e0e0", anchor="w")
        self.tickets_left_label.pack(fill="x")
        self.release_date_label = tk.Label(info, text="Release Date: ", bg="#e0e0e0", anchor="w")
        self.release_date_label.pack(fill="x")
        self.end_date_label = tk.Label(info, text="End Date: ", bg="#e0e0e0", anchor="w")
        self.end_date_label.pack(fill="x")

        # Booking form
        booking = tk.LabelFrame(right, text="Book Tickets", bg="#e0e0e0", padx=10, pady=10)
        booking.pack(fill="x")
        tk.Label(booking, text="Customer Name:", bg="#e0e0e0").pack(anchor="w")
        tk.Entry(booking, textvariable=self.customer_var).pack(fill="x", pady=(0, 10))
        tk.Label(booking, text="Number of Tickets:", bg="#e0e0e0").pack(anchor="w")
        self.ticket_entry = tk.Entry(booking, textvariable=self.ticket_var)
        self.ticket_entry.pack(fill="x", pady=(0, 10))
        tk.Button(booking, text="Purchase Tickets", command=self.calculate_total).pack(fill="x", pady=10)

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
                menu = self.movie_dropdown["menu"]
                menu.delete(0, "end")
                for m in self.movies.keys():
                    menu.add_command(label=m, command=lambda v=m: self.movie_var.set(v))
                if self.movies:
                    first = list(self.movies.keys())[0]
                    self.movie_var.set(first)
                    self.update_movie_info()
        else:
            messagebox.showerror("Error", response.get("message", "Failed to load movies"))

    def show_add_movie(self):
        self.add_movie_popup()

    def show_update_movie(self):
        selected_movie = self.movie_var.get()
        if not selected_movie:
            messagebox.showerror("Error", "Please select a movie to update")
            return
        self.update_movie_popup(selected_movie)

    def update_movie_info(self, event=None):
        selected_movie = self.movie_var.get()
        if selected_movie in self.movies:
            price, tickets, room, release_date, end_date = self.movies[selected_movie]
            self.tickets_left_label.config(text=f"Tickets: {tickets}")
            self.cost_label.config(text=f"Price: R{price:.2f}")
            self.room_label.config(text=f"Cinema Room: {room}")
            self.release_date_label.config(text=f"Release Date: {release_date}")
            self.end_date_label.config(text=f"End Date: {end_date}")

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
            if selected_movie in self.movies:
                current_tickets = self.movies[selected_movie][1]
                new_tickets = current_tickets - quantity
                self.movies[selected_movie][1] = new_tickets
                self.tickets_left_label.config(text=f"Tickets: {new_tickets}")
            self.customer_var.set("")
            self.ticket_var.set("")
            messagebox.showinfo("Success", f"Successfully purchased {quantity} tickets for {selected_movie}")
        else:
            error_msg = response.get("error", "Failed to process sale")
            messagebox.showerror("Error", error_msg)

    def add_movie_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Add New Movie")
        popup.geometry("350x350")
        popup.grab_set()
        fields = [
            ("Movie Name", tk.StringVar()),
            ("Price", tk.StringVar()),
            ("Available Tickets", tk.StringVar()),
            ("Cinema Room", tk.StringVar()),
            ("Release Date (YYYY-MM-DD)", tk.StringVar()),
            ("End Date (YYYY-MM-DD)", tk.StringVar()),
        ]
        entries = {}
        for i, (label, var) in enumerate(fields):
            tk.Label(popup, text=label).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            e = tk.Entry(popup, textvariable=var)
            e.grid(row=i, column=1, padx=10, pady=5)
            entries[label] = var
        def save():
            name = entries["Movie Name"].get().strip()
            price_valid, price = self.validate_numeric_input(entries["Price"].get(), 0.01)
            tickets_valid, tickets = self.validate_numeric_input(entries["Available Tickets"].get(), 1)
            room_valid, room = self.validate_numeric_input(entries["Cinema Room"].get(), 1)
            release_date = entries["Release Date (YYYY-MM-DD)"].get().strip()
            end_date = entries["End Date (YYYY-MM-DD)"].get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter a movie name", parent=popup)
                return
            if not all([price_valid, tickets_valid, room_valid]):
                messagebox.showerror("Error", "Please enter valid numbers for price, tickets, and room", parent=popup)
                return
            if not release_date or not end_date:
                messagebox.showerror("Error", "Please enter both release and end dates", parent=popup)
                return
            if name in self.movies:
                messagebox.showerror("Error", "A movie with this name already exists", parent=popup)
                return
            payload = {
                "action": "create",
                "payload": {
                    "title": name,
                    "cinema_room": str(int(room)),
                    "release_date": release_date,
                    "end_date": end_date,
                    "tickets_available": int(tickets),
                    "ticket_price": float(price)
                }
            }
            response = self.socket_client.send_message(payload)
            if response.get("status") == "ok":
                self.movies[name] = [float(price), int(tickets), int(room), release_date, end_date]
                menu = self.movie_dropdown["menu"]
                menu.add_command(label=name, command=lambda v=name: self.movie_var.set(v))
                self.movie_var.set(name)
                self.update_movie_info()
                popup.destroy()
                messagebox.showinfo("Success", "Movie added successfully!", parent=self.root)
            else:
                error_msg = response.get("message", "Failed to add movie")
                messagebox.showerror("Error", error_msg, parent=popup)
        tk.Button(popup, text="Save Movie", command=save).grid(row=len(fields), column=0, columnspan=2, pady=15)

    def update_movie_popup(self, selected_movie):
        popup = tk.Toplevel(self.root)
        popup.title("Update Movie")
        popup.geometry("350x320")
        popup.grab_set()
        price, tickets, room, release_date, end_date = self.movies[selected_movie]
        fields = [
            ("New Price", tk.StringVar(value=str(price))),
            ("Available Tickets", tk.StringVar(value=str(tickets))),
            ("Cinema Room", tk.StringVar(value=str(room))),
            ("Release Date (YYYY-MM-DD)", tk.StringVar(value=release_date)),
            ("End Date (YYYY-MM-DD)", tk.StringVar(value=end_date)),
        ]
        entries = {}
        for i, (label, var) in enumerate(fields):
            tk.Label(popup, text=label).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            e = tk.Entry(popup, textvariable=var)
            e.grid(row=i, column=1, padx=10, pady=5)
            entries[label] = var
        def save():
            price_valid, price_val = self.validate_numeric_input(entries["New Price"].get(), 0.01)
            tickets_valid, tickets_val = self.validate_numeric_input(entries["Available Tickets"].get(), 0)
            room_valid, room_val = self.validate_numeric_input(entries["Cinema Room"].get(), 1)
            release_date_val = entries["Release Date (YYYY-MM-DD)"].get().strip()
            end_date_val = entries["End Date (YYYY-MM-DD)"].get().strip()
            if not all([price_valid, tickets_valid, room_valid]):
                messagebox.showerror("Error", "Please enter valid numbers for price, tickets, and room", parent=popup)
                return
            if not release_date_val or not end_date_val:
                messagebox.showerror("Error", "Please enter both release and end dates", parent=popup)
                return
            movie_id = str(list(self.movies.keys()).index(selected_movie) + 1)
            newData = {}
            current_data = self.movies[selected_movie]
            if float(price_val) != current_data[0]:
                newData["ticket_price"] = float(price_val)
            if int(tickets_val) != current_data[1]:
                newData["tickets_available"] = int(tickets_val)
            if int(room_val) != current_data[2]:
                newData["cinema_room"] = int(room_val)
            if release_date_val != current_data[3]:
                newData["release_date"] = release_date_val
            if end_date_val != current_data[4]:
                newData["end_date"] = end_date_val
            if not newData:
                messagebox.showinfo("Info", "No changes detected", parent=popup)
                return
            response = self.socket_client.send_message({
                "action": "update",
                "payload": {
                    "movie_id": movie_id,
                    "newData": newData
                }
            })
            if response.get("status") == "ok":
                self.movies[selected_movie] = [float(price_val), int(tickets_val), int(room_val), release_date_val, end_date_val]
                self.update_movie_info()
                popup.destroy()
                messagebox.showinfo("Success", "Movie updated successfully!", parent=self.root)
            else:
                messagebox.showerror("Error", response.get("message", "Failed to update movie"), parent=popup)
        tk.Button(popup, text="Update Movie", command=save).grid(row=len(fields), column=0, columnspan=2, pady=15)

    def delete_movie(self):
        selected_movie = self.movie_var.get()
        if not selected_movie:
            messagebox.showerror("Error", "Please select a movie to delete")
            return
        movie_id = None
        for movie in self.movies:
            if movie == selected_movie:
                movie_id = str(list(self.movies.keys()).index(movie) + 1)
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
                menu = self.movie_dropdown["menu"]
                menu.delete(0, "end")
                for m in self.movies.keys():
                    menu.add_command(label=m, command=lambda v=m: self.movie_var.set(v))
                if self.movies:
                    self.movie_var.set(list(self.movies.keys())[0])
                else:
                    self.movie_var.set('')
                self.cost_label.config(text="Price: R0.00")
                self.tickets_left_label.config(text="Tickets: 0")
                self.room_label.config(text="Cinema Room: 0")
                self.release_date_label.config(text="Release Date: ")
                self.end_date_label.config(text="End Date: ")
                messagebox.showinfo("Success", "Movie deleted successfully!")
            else:
                messagebox.showerror("Error", response.get("message", "Failed to delete movie"))

    def on_closing(self):
        if self.socket_client:
            self.socket_client.disconnect()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleMovieBookingSystem(root)
    # Only set protocol and mainloop if root still exists
    if root.winfo_exists():
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        root.mainloop()
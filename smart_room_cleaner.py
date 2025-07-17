import tkinter as tk
import random
import time

class SmartRoomCleanerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("✨ Smart Room Cleaner AI Agent")
        self.master.geometry("1100x750")
        self.master.configure(bg="#f0f8ff")
        self.master.resizable(False, False)

        self.rooms = {
            "A": random.choice(["Clean", "Dirty"]),
            "B": random.choice(["Clean", "Dirty"]),
            "C": random.choice(["Clean", "Dirty"]),
            "D": random.choice(["Clean", "Dirty"]),
            "E": random.choice(["Clean", "Dirty"]),
            "F": random.choice(["Clean", "Dirty"]),
            "G": random.choice(["Clean", "Dirty"]),
            "H": random.choice(["Clean", "Dirty"]),
        }

        self.room_order = list(self.rooms.keys())
        self.current_location = self.find_first_dirty_room() or self.room_order[0]
        self.current_index = self.room_order.index(self.current_location)

        self.battery = 100
        self.cleaned_count = 0
        dirty_count = sum(1 for status in self.rooms.values() if status == "Dirty")
        self.total_cycles = dirty_count * 2 if dirty_count > 0 else 8  # Efficient adaptive cycle count
        self.cycles_remaining = self.total_cycles
        self.room_visit_history = {room: 0 for room in self.room_order}

        self.room_frames = {}
        self.room_labels = {}

        self.create_ui()

    def find_first_dirty_room(self):
        for room in self.room_order:
            if self.rooms[room] == "Dirty":
                return room
        return None

    def create_ui(self):
        tk.Label(self.master, text="🧠 AI Smart Room Cleaner", font=("Helvetica", 22, "bold"),
                 bg="#f0f8ff", fg="#1e3a8a").pack(pady=15)

        grid_frame = tk.Frame(self.master, bg="#f0f8ff")
        grid_frame.pack(pady=10)

        for i, room in enumerate(self.room_order):
            frame = tk.Frame(grid_frame, width=160, height=160, bg="#ffffff", bd=4, relief="ridge")
            frame.grid(row=i // 4, column=i % 4, padx=25, pady=20)
            label = tk.Label(frame, text="", font=("Helvetica", 14, "bold"), justify="center")
            label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.room_frames[room] = frame
            self.room_labels[room] = label

        self.status_label = tk.Label(self.master, text="Status: Ready", font=("Helvetica", 13, "bold"),
                                     bg="#f0f8ff", fg="#0d47a1")
        self.status_label.pack(pady=10)

        self.info_label = tk.Label(self.master, font=("Helvetica", 12), bg="#f0f8ff", fg="#374151")
        self.info_label.pack(pady=5)

        self.history_label = tk.Label(self.master, font=("Helvetica", 11), bg="#f0f8ff", fg="#374151")
        self.history_label.pack(pady=5)

        self.start_button = tk.Button(self.master, text="🚀 Start Cleaning", font=("Helvetica", 13, "bold"),
                                      bg="#2563eb", fg="white", padx=20, pady=10, command=self.start_agent)
        self.start_button.pack(pady=20)

        self.update_ui()

    def update_ui(self):
        for room, label in self.room_labels.items():
            status = self.rooms[room]
            is_agent_here = (room == self.current_location)
            emoji = "🤖\n" if is_agent_here else ""
            icon = "🧹" if status == "Dirty" else "✨"
            label.config(text=f"{emoji}Room {room}\n{status} {icon}")

            frame = self.room_frames[room]
            frame.config(bg="#c8e6c9" if status == "Clean" else "#ffcdd2")

        self.info_label.config(
            text=f"🔋 Battery: {self.battery}%   |   ✅ Cleaned: {self.cleaned_count}   |   ⏱️ Cycles Left: {self.cycles_remaining}"
        )

        history_text = "📊 Room Visits: " + " | ".join([f"{room}({self.room_visit_history[room]})" for room in self.room_order])
        self.history_label.config(text=history_text)

    def clean_room(self):
        if self.rooms[self.current_location] == "Dirty":
            self.status_label.config(text=f"🧼 Cleaning Room {self.current_location}...", fg="#2e7d32")
            self.rooms[self.current_location] = "Clean"
            self.cleaned_count += 1
            self.battery -= 5
        else:
            self.status_label.config(text=f"✅ Room {self.current_location} already clean.", fg="#616161")

    def move(self):
        self.status_label.config(text=f"➡️ Searching next dirty room...", fg="#ef6c00")

        for i in range(len(self.room_order)):
            next_index = (self.current_index + i + 1) % len(self.room_order)
            next_room = self.room_order[next_index]
            if self.rooms[next_room] == "Dirty":
                self.current_index = next_index
                self.current_location = next_room
                break
        else:
            self.current_index = (self.current_index + 1) % len(self.room_order)
            self.current_location = self.room_order[self.current_index]

        self.room_visit_history[self.current_location] += 1
        self.battery -= 2

    def run_step(self):
        if self.cycles_remaining > 0 and self.battery > 0:
            self.clean_room()
            self.update_ui()
            self.cycles_remaining -= 1
            self.master.after(800, self.next_move)
        else:
            self.status_label.config(
                text="✅ Cleaning Completed!" if self.battery > 0 else "❌ Battery Dead. Simulation Ended.",
                fg="green" if self.battery > 0 else "red"
            )
            self.update_ui()

    def next_move(self):
        self.move()
        self.update_ui()
        self.master.after(800, self.run_step)

    def start_agent(self):
        self.start_button.config(state=tk.DISABLED)
        self.run_step()

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartRoomCleanerGUI(root)
    root.mainloop()

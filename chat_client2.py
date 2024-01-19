import socket  # Import the socket module for handling network connections
import threading  # Import the threading module for managing multiple threads
import tkinter as tk  # Import the tkinter library for creating the GUI
from tkinter import scrolledtext, simpledialog, ttk  # Import specific components from tkinter
from ttkthemes import ThemedTk  # Import ThemedTk for themed tkinter windows

class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("DISCORD MORENO™")  # Set the title of the GUI window

        # Create a scrolled text widget for displaying chat history
        self.chat_history = scrolledtext.ScrolledText(self.master, wrap=tk.WORD)
        self.chat_history.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        # Create an entry widget for entering messages
        self.message_entry = ttk.Entry(self.master)
        self.message_entry.pack(pady=10, padx=(10, 5), side=tk.LEFT, expand=True, fill=tk.X)

        # Create a button for sending messages
        self.send_button = ttk.Button(self.master, text="Send", command=self.send_message, width=5)
        self.send_button.pack(pady=10, padx=(5, 10), side=tk.RIGHT)

        # Create a socket for the client
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Prompt the user to enter their name
        self.name = simpledialog.askstring("Name", "Enter your name:")

        # If a name is provided, connect to the server and start a thread to receive messages
        if self.name:
            self.client_socket.connect(('localhost', 6666))
            self.client_socket.send(self.name.encode('utf-8'))
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.start()

    def send_message(self):
        message = self.message_entry.get()  # Get the message from the entry widget
        self.client_socket.send(message.encode('utf-8'))  # Send the message to the server
        self.display_message(f"{self.name}: {message}", 'blue')  # Display the sent message in blue

    def display_message(self, message, color):
        self.chat_history.tag_configure(color, foreground=color)  # Configure a tag with the specified color
        self.chat_history.insert(tk.END, message + '\n', color)  # Insert the message into the chat history with the specified color
        self.chat_history.see(tk.END)  # Scroll to the end of the chat history

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')  # Receive a message from the server
                if not message:
                    break
                self.display_message(message, 'red')  # Display the received message in red
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

def main():
    root = ThemedTk(theme="ubuntu")  # Create a themed tkinter window
    client_gui = GUI(root)  # Create an instance of the GUI class
    root.mainloop()  # Start the tkinter event loop

if __name__ == "__main__":
    main()  # Run the main function when the script is executed

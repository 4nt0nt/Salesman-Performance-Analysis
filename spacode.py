import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class Salesman:
    def __init__(self, name):
        self.name = name
        self.clients = {}

    def add_client(self, day, client):
        if day not in self.clients:
            self.clients[day] = []
        self.clients[day].append(client)


def calculate_best_salesmen(salesmen):
    highest_average = 0
    best_salesmen = []

    for salesman in salesmen:
        total_clients = sum(len(clients) for clients in salesman.clients.values())
        average_clients = total_clients / len(salesman.clients)

        if average_clients > highest_average:
            highest_average = average_clients
            best_salesmen = [salesman]
        elif average_clients == highest_average:
            best_salesmen.append(salesman)

    return best_salesmen


def create_salesman():
    salesman_name = entry_name.get()
    salesman = Salesman(salesman_name)
    salesmen.append(salesman)
    update_salesman_list()


def add_client():
    selected_salesman = listbox_salesman.get(tk.ACTIVE)
    client_name = entry_client.get()
    selected_day = listbox_days.get(tk.ACTIVE)

    for salesman in salesmen:
        if salesman.name == selected_salesman:
            salesman.add_client(selected_day, client_name)
            break

    update_client_list()
    update_salesmen_table()


def add_day():
    day = entry_day.get()
    if day not in days:
        days.append(day)
        update_day_list()


def update_salesman_list():
    listbox_salesman.delete(0, tk.END)
    for salesman in salesmen:
        listbox_salesman.insert(tk.END, salesman.name)


def update_client_list():
    selected_salesman = listbox_salesman.get(tk.ACTIVE)
    selected_day = listbox_days.get(tk.ACTIVE)
    for salesman in salesmen:
        if salesman.name == selected_salesman:
            listbox_clients.delete(0, tk.END)
            if selected_day in salesman.clients:
                for client in salesman.clients[selected_day]:
                    listbox_clients.insert(tk.END, client)
            break


def update_day_list():
    listbox_days.delete(0, tk.END)
    for day in days:
        listbox_days.insert(tk.END, day)


def update_salesmen_table():
    tree.delete(*tree.get_children())
    for salesman in salesmen:
        for day, clients in salesman.clients.items():
            for client in clients:
                tree.insert("", tk.END, values=(salesman.name, day, client))


def find_best_salesmen():
    best_salesmen = calculate_best_salesmen(salesmen)
    if best_salesmen:
        best_salesmen_names = ', '.join([salesman.name for salesman in best_salesmen])
        label_best_salesman.config(text=f"Best Salesmen: {best_salesmen_names}")
    else:
        label_best_salesman.config(text="No salesmen available.")

    graph_display_frame = tk.Frame(window)
    graph_display_frame.pack(pady=20)

    for salesman in salesmen:
        G = nx.DiGraph()
        G.add_node(salesman.name)
        prev_node = salesman.name
        for day, clients in salesman.clients.items():
            day_node = f"{day} - {salesman.name}"
            G.add_node(day_node)
            G.add_edge(prev_node, day_node)
            prev_node = day_node
            for client in clients:
                G.add_node(client)
                G.add_edge(day_node, client)

        graph_frame = tk.Frame(graph_display_frame)
        graph_frame.pack(side=tk.LEFT, padx=10, pady=10)

        fig = Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, edge_color='b', node_color='lightblue', node_size=500, font_size=8,
                width=1.5, ax=ax)
        ax.set_title(salesman.name)
        ax.set_axis_off()

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    canvas.create_window((0, 0), window=graph_frame, anchor='nw')
    graph_frame.update_idletasks()

    canvas.config(scrollregion=canvas.bbox('all'))


window = tk.Tk()
window.title("Best Salesman Calculator")
window.geometry("1500x800")

label_name = tk.Label(window, text="Salesman Name:")
label_name.pack()
entry_name = tk.Entry(window, width=50)
entry_name.pack()

button_create_salesman = tk.Button(window, text="Create Salesman", command=create_salesman)
button_create_salesman.pack()

frame_salesman = tk.Frame(window)
frame_salesman.pack(side=tk.LEFT, padx=10)

label_salesman = tk.Label(frame_salesman, text="Salesmen")
label_salesman.pack()

listbox_salesman = tk.Listbox(frame_salesman)
listbox_salesman.pack(side=tk.LEFT)

frame_day = tk.Frame(window)
frame_day.pack(side=tk.LEFT, padx=10)

label_day = tk.Label(frame_day, text="Days")
label_day.pack()

listbox_days = tk.Listbox(frame_day)
listbox_days.pack(side=tk.LEFT)

frame_client = tk.Frame(window)
frame_client.pack(side=tk.LEFT, padx=10)

label_client = tk.Label(frame_client, text="Clients")
label_client.pack()

listbox_clients = tk.Listbox(frame_client)
listbox_clients.pack(side=tk.LEFT)

label_day = tk.Label(window, text="Day:")
label_day.pack()
entry_day = tk.Entry(window, width=50)
entry_day.pack()

button_add_day = tk.Button(window, text="Add Day", command=add_day)
button_add_day.pack()

label_client = tk.Label(window, text="Client:")
label_client.pack()
entry_client = tk.Entry(window, width=50)
entry_client.pack()

button_add_client = tk.Button(window, text="Add Client", command=add_client)
button_add_client.pack()

button_find_best_salesmen = tk.Button(window, text="Find Best Salesmen", command=find_best_salesmen)
button_find_best_salesmen.pack()

label_best_salesman = tk.Label(window, text="Best Salesmen: ")
label_best_salesman.pack()

salesmen = []
days = []

listbox_salesman.bind("<<ListboxSelect>>", lambda event: update_client_list())
listbox_days.bind("<<ListboxSelect>>", lambda event: update_client_list())

tree_frame = tk.Frame(window)
tree_frame.pack(pady=20)

tree = ttk.Treeview(tree_frame, columns=("Salesman", "Day", "Client"))
tree.heading("#0", text="Salesmen and Clients")
tree.heading("Salesman", text="Salesman")
tree.heading("Day", text="Day")
tree.heading("Client", text="Client")

tree.column("#0", width=200)
tree.column("Salesman", width=200)
tree.column("Day", width=100)
tree.column("Client", width=200)

tree.pack()

window.mainloop()

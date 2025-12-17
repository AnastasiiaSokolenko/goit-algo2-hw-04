from collections import deque
import pandas as pd

INF = 10**9  # large integer simulating infinity

# === Алгоритм Едмондса-Карпа ===
def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    visited = [False] * len(capacity_matrix)
    queue = deque([source])
    visited[source] = True

    while queue:
        current_node = queue.popleft()
        for neighbor in range(len(capacity_matrix)):
            if (
                not visited[neighbor]
                and capacity_matrix[current_node][neighbor]
                - flow_matrix[current_node][neighbor] > 0
            ):
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)
    return False


def edmonds_karp(capacity_matrix, source, sink):
    num_nodes = len(capacity_matrix)
    flow_matrix = [[0] * num_nodes for _ in range(num_nodes)]
    parent = [-1] * num_nodes
    max_flow = 0

    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        path_flow = INF
        current_node = sink

        while current_node != source:
            previous_node = parent[current_node]
            path_flow = min(
                path_flow,
                capacity_matrix[previous_node][current_node]
                - flow_matrix[previous_node][current_node],
            )
            current_node = previous_node

        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += path_flow
            flow_matrix[current_node][previous_node] -= path_flow
            current_node = previous_node

        max_flow += path_flow

    return max_flow, flow_matrix


# === Побудова графа ===
edges = [
    ("t1", "w1", 25), ("t1", "w2", 20), ("t1", "w3", 15),
    ("t2", "w3", 15), ("t2", "w4", 30), ("t2", "w2", 10),
    ("w1", "s1", 15), ("w1", "s2", 10), ("w1", "s3", 20),
    ("w2", "s4", 15), ("w2", "s5", 10), ("w2", "s6", 25),
    ("w3", "s7", 20), ("w3", "s8", 15), ("w3", "s9", 10),
    ("w4", "s10", 20), ("w4", "s11", 10), ("w4", "s12", 15),
    ("w4", "s13", 5), ("w4", "s14", 10),
]

# Унікальні вершини
nodes = sorted(set(u for u, _, _ in edges) | set(v for _, v, _ in edges))

# === Додаємо super_source і super_sink ===
super_source = "source"
super_sink = "sink"
nodes = [super_source] + nodes + [super_sink]

node_to_index = {name: i for i, name in enumerate(nodes)}
index_to_node = {i: name for name, i in node_to_index.items()}

size = len(nodes)

# Матриця пропускної здатності
capacity_matrix = [[0] * size for _ in range(size)]

for u, v, cap in edges:
    capacity_matrix[node_to_index[u]][node_to_index[v]] = cap

# З'єднуємо super_source з t1, t2
capacity_matrix[node_to_index["source"]][node_to_index["t1"]] = 60
capacity_matrix[node_to_index["source"]][node_to_index["t2"]] = 55

# З'єднуємо магазини з super_sink (обмеження = їх вхідна пропускна здатність)
for name in nodes:
    if name.startswith("s"):
        incoming_cap = sum(cap for u, v, cap in edges if v == name)
        capacity_matrix[node_to_index[name]][node_to_index["sink"]] = incoming_cap

# === Один запуск Edmonds–Karp ===
source_idx = node_to_index["source"]
sink_idx = node_to_index["sink"]

max_flow, flow_matrix = edmonds_karp(capacity_matrix, source_idx, sink_idx)

# === Формування таблиці результатів ===
results = []

# # Для кожного терміналу фіксуємо фактичний потік до кожного складу
terminal_to_warehouse_flow = {
    "t1": {},
    "t2": {}
}

for terminal in ["t1", "t2"]:
    t_idx = node_to_index[terminal]
    for w in nodes:
        if w.startswith("w"):
            w_idx = node_to_index[w]
            terminal_to_warehouse_flow[terminal][w] = flow_matrix[t_idx][w_idx]

# # Для кожного магазину визначаємо, від якого терміналу він отримав товар (через склад)
for w in nodes:
    if not w.startswith("w"):
        continue
    w_idx = node_to_index[w]

    for s in nodes:
        if not s.startswith("s"):
            continue
        s_idx = node_to_index[s]
        shop_flow = flow_matrix[w_idx][s_idx]
        if shop_flow == 0:
            continue

        # Визначаємо, з якого терміналу склад отримав потік
        for terminal in ["t1", "t2"]:
            if terminal_to_warehouse_flow[terminal][w] > 0:
                flow_contributed = min(shop_flow, terminal_to_warehouse_flow[terminal][w])
                results.append({
                    "Термінал": "Термінал 1" if terminal == "t1" else "Термінал 2",
                    "Магазин": s.upper(),
                    "Фактичний Потік": flow_contributed,
                })
                # Віднімаємо вже врахований потік, щоб уникнути подвоєння
                terminal_to_warehouse_flow[terminal][w] -= flow_contributed
                shop_flow -= flow_contributed
                if shop_flow == 0:
                    break   # Виходимо з циклу, якщо магазин отримав увесь призначений потік

df = pd.DataFrame(results).sort_values(by=["Термінал", "Магазин"])
print(df.to_string(index=False))

print(f"\nЗагальний максимальний потік: {max_flow}")



# from collections import deque
# import pandas as pd

# # === Алгоритм Едмондса-Карпа ===
# def bfs(capacity_matrix, flow_matrix, source, sink, parent):
#     visited = [False] * len(capacity_matrix)
#     queue = deque([source])
#     visited[source] = True

#     while queue:
#         current_node = queue.popleft()
#         for neighbor in range(len(capacity_matrix)):
#             if not visited[neighbor] and capacity_matrix[current_node][neighbor] - flow_matrix[current_node][neighbor] > 0:
#                 parent[neighbor] = current_node
#                 visited[neighbor] = True
#                 if neighbor == sink:
#                     return True
#                 queue.append(neighbor)
#     return False

# def edmonds_karp(capacity_matrix, source, sink):
#     num_nodes = len(capacity_matrix)
#     flow_matrix = [[0] * num_nodes for _ in range(num_nodes)]
#     parent = [-1] * num_nodes
#     max_flow = 0

#     while bfs(capacity_matrix, flow_matrix, source, sink, parent):
#         path_flow = float('inf')
#         current_node = sink
#         while current_node != source:
#             previous_node = parent[current_node]
#             path_flow = min(path_flow, capacity_matrix[previous_node][current_node] - flow_matrix[previous_node][current_node])
#             current_node = previous_node
#         current_node = sink
#         while current_node != source:
#             previous_node = parent[current_node]
#             flow_matrix[previous_node][current_node] += path_flow
#             flow_matrix[current_node][previous_node] -= path_flow
#             current_node = previous_node
#         max_flow += path_flow

#     return max_flow, flow_matrix

# # === Побудова графа ===
# edges = [
#     ("t1", "w1", 25), ("t1", "w2", 20), ("t1", "w3", 15),
#     ("t2", "w3", 15), ("t2", "w4", 30), ("t2", "w2", 10),
#     ("w1", "s1", 15), ("w1", "s2", 10), ("w1", "s3", 20),
#     ("w2", "s4", 15), ("w2", "s5", 10), ("w2", "s6", 25),
#     ("w3", "s7", 20), ("w3", "s8", 15), ("w3", "s9", 10),
#     ("w4", "s10", 20), ("w4", "s11", 10), ("w4", "s12", 15),
#     ("w4", "s13", 5), ("w4", "s14", 10),
# ]

# # Унікальні вершини
# nodes = sorted(set(u for u, _, _ in edges) | set(v for _, v, _ in edges))
# node_to_index = {name: i for i, name in enumerate(nodes)}
# index_to_node = {i: name for name, i in node_to_index.items()}

# # Додаємо super_sink
# super_sink = len(nodes)
# node_to_index["sink"] = super_sink
# index_to_node[super_sink] = "sink"
# size = super_sink + 1

# # Матриця пропускної здатності
# capacity_matrix = [[0] * size for _ in range(size)]
# for u, v, cap in edges:
#     i, j = node_to_index[u], node_to_index[v]
#     capacity_matrix[i][j] = cap

# # З'єднуємо магазини з super_sink
# for name in nodes:
#     if name.startswith("s"):
#         i = node_to_index[name]
#         capacity_matrix[i][super_sink] = float('inf')

# # Джерела
# t1 = node_to_index["t1"]
# t2 = node_to_index["t2"]

# # === Обчислення потоку від t1 і t2 ===
# flow1, flow_matrix1 = edmonds_karp(capacity_matrix, t1, super_sink)
# flow2, flow_matrix2 = edmonds_karp(capacity_matrix, t2, super_sink)

# # === Формування таблиці результатів ===
# results = []
# for name in nodes:
#     if name.startswith("s"):
#         idx = node_to_index[name]
#         flow_from_t1 = flow_matrix1[idx][super_sink]
#         flow_from_t2 = flow_matrix2[idx][super_sink]
#         if flow_from_t1 > 0:
#             results.append({"Термінал": "Термінал 1", "Магазин": name.upper(), "Фактичний Потік": flow_from_t1})
#         if flow_from_t2 > 0:
#             results.append({"Термінал": "Термінал 2", "Магазин": name.upper(), "Фактичний Потік": flow_from_t2})

# # Таблиця результатів
# df = pd.DataFrame(results).sort_values(by=["Термінал", "Магазин"])
# print(df.to_string(index=False))

# # Загальний потік
# print(f"\nЗагальний потік: {flow1 + flow2} (t1: {flow1}, t2: {flow2})")
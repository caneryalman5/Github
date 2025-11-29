#!/usr/bin/env python3
"""tsp_ortools.py

Converted from the user's notebook. Builds a small TSP with OR-Tools,
solves it and saves a plot `tsp_route.png` in the same folder.
"""
import sys
try:
    from ortools.constraint_solver import pywrapcp, routing_enums_pb2
except Exception as e:
    print("ERROR: OR-Tools not installed or failed to import. Please run:\n  python3 -m pip install --upgrade ortools")
    raise

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def euclidean(a, b):
    return np.linalg.norm(a - b)


def build_data(seed=42, n_customers=15, scale=100):
    np.random.seed(seed)
    coords = np.random.randint(0, 101, size=(1 + n_customers, 2))
    ids = ['Depo'] + [f'Müşteri {i+1}' for i in range(n_customers)]
    types = ['Depo'] + ['Müşteri'] * n_customers
    df = pd.DataFrame({'Nokta_ID': ids, 'Tip': types, 'X': coords[:, 0], 'Y': coords[:, 1]})

    coords_arr = df[['X', 'Y']].to_numpy().astype(float)
    n = coords_arr.shape[0]
    dist_matrix_float = [[euclidean(coords_arr[i], coords_arr[j]) for j in range(n)] for i in range(n)]
    dist_matrix = [[int(round(dist_matrix_float[i][j] * scale)) for j in range(n)] for i in range(n)]

    return df, coords_arr, dist_matrix, dist_matrix_float, scale


def solve_and_plot(df, coords_arr, dist_matrix, scale, output_path='tsp_route.png'):
    manager = pywrapcp.RoutingIndexManager(len(dist_matrix), 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return dist_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    search_parameters.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    search_parameters.time_limit.seconds = 20

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        index = routing.Start(0)
        route_nodes = []
        route_distance_int = 0
        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            route_nodes.append(node)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance_int += routing.GetArcCostForVehicle(previous_index, index, 0)
        route_nodes.append(manager.IndexToNode(index))

        route_distance = route_distance_int / scale
        visit_sequence = [df.loc[i, 'Nokta_ID'] for i in route_nodes]
        print('Bulunan ziyaret sırası (isim):', ' -> '.join(visit_sequence))
        print(f'Toplam mesafe (yaklaşık, scale bölünmüş): {route_distance:.2f}')

        # Plot
        route_coords = coords_arr[route_nodes]
        plt.figure(figsize=(8, 6))
        plt.scatter(df[df['Tip'] == 'Müşteri']['X'], df[df['Tip'] == 'Müşteri']['Y'], c='blue', label='Müşteriler')
        plt.scatter(df[df['Tip'] == 'Depo']['X'], df[df['Tip'] == 'Depo']['Y'], c='red', marker='s', s=100, label='Depo')
        for i in range(len(route_coords) - 1):
            x0, y0 = route_coords[i]
            x1, y1 = route_coords[i + 1]
            plt.arrow(x0, y0, x1 - x0, y1 - y0, length_includes_head=True, head_width=1.5, head_length=2.5,
                      fc='green', ec='green', alpha=0.7)

        # Place labels while avoiding overlaps using bounding-box checks in display (pixel) coords.
        ax = plt.gca()
        fig = plt.gcf()
        # draw once to initialize renderer and any text metrics
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()

        existing_bboxes = []  # list of matplotlib.transforms.Bbox in display coords

        # candidate offsets in pixels (try near the point first, then progressively farther)
        base_candidates = [(0, 0), (0, 14), (0, -14), (14, 0), (-14, 0), (10, 10), (-10, 10), (10, -10), (-10, -10)]

        for idx, node in enumerate(route_nodes):
            x, y = coords_arr[node]
            label = df.loc[node, 'Nokta_ID']

            disp = ax.transData.transform((x, y))
            placed = False

            # try base candidates first
            for cand in base_candidates:
                cand_disp = (disp[0] + cand[0], disp[1] + cand[1])
                data_label = ax.transData.inverted().transform(cand_disp)
                txt = ax.text(data_label[0], data_label[1], label, fontsize=8,
                              bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
                fig.canvas.draw()
                bb = txt.get_window_extent(renderer=renderer)

                # check overlap
                overlap = False
                for exbb in existing_bboxes:
                    if bb.overlaps(exbb):
                        overlap = True
                        break
                if not overlap:
                    existing_bboxes.append(bb)
                    placed = True
                    break
                else:
                    txt.remove()

            if placed:
                continue

            # fallback: spiral search for a non-overlapping spot
            step = 16
            max_tries = 48
            for t in range(1, max_tries + 1):
                angle = t * 25
                rad = (t // 6 + 1) * step
                cand_disp = (disp[0] + rad * np.cos(np.deg2rad(angle)), disp[1] + rad * np.sin(np.deg2rad(angle)))
                data_label = ax.transData.inverted().transform(cand_disp)
                txt = ax.text(data_label[0], data_label[1], label, fontsize=8,
                              bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
                fig.canvas.draw()
                bb = txt.get_window_extent(renderer=renderer)
                overlap = False
                for exbb in existing_bboxes:
                    if bb.overlaps(exbb):
                        overlap = True
                        break
                if not overlap:
                    existing_bboxes.append(bb)
                    placed = True
                    break
                else:
                    txt.remove()

            if not placed:
                # as last resort, place at a small offset with lower alpha
                data_label = ax.transData.inverted().transform((disp[0] + 8, disp[1] + 8))
                ax.text(data_label[0], data_label[1], label, fontsize=8, alpha=0.85,
                        bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))

        plt.title(f'Global Optimum Rotası - Toplam Mesafe: {route_distance:.2f}')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        try:
            plt.show()
        except Exception:
            # In headless environments show() can fail; we already saved the figure
            pass
        print(f'Rota grafiği kaydedildi: {output_path}')
    else:
        print('Çözüm bulunamadı.')


def main():
    df, coords_arr, dist_matrix, dist_matrix_float, scale = build_data(seed=42, n_customers=15, scale=100)
    print('Oluşan DataFrame:')
    print(df)
    solve_and_plot(df, coords_arr, dist_matrix, scale, output_path='tsp_route.png')


if __name__ == '__main__':
    main()

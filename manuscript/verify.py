import itertools
import json


VERTICES = frozenset(range(14))
EDGES = frozenset(
    tuple(sorted(edge))
    for index in range(7)
    for edge in (
        (index, (index + 1) % 7),
        (index, index + 7),
        (index + 7, 7 + (index + 2) % 7),
    )
)
ADJACENCY = {
    vertex: frozenset(
        second if first == vertex else first
        for first, second in EDGES
        if vertex in (first, second)
    )
    for vertex in VERTICES
}
REPRESENTATIVES = (
    (0, 2, 4, 8, 12),
    (0, 2, 4, 12, 13),
    (0, 2, 8, 11, 12),
    (0, 3, 8, 9, 12),
    (0, 3, 8, 11, 12),
)
PATHS = ((5, 6, 13, 11), (1, 8, 10, 3), (3, 4, 5, 6),
         (6, 5, 4, 11), (1, 2, 9, 7))
ODD_CYCLE_WITNESSES = (
    (4, (4, 5, 6, 13, 11)),
    (2, (2, 1, 8, 10, 3)),
    (11, (11, 4, 5, 6, 13)),
    (0, (4, 5, 6, 13, 11)),
    (0, (0, 1, 2, 9, 7)),
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def independent(vertices):
    return all(not {first, second} <= vertices for first, second in EDGES)


def components(vertices):
    remaining = set(vertices)
    result = []
    while remaining:
        queue = [min(remaining)]
        remaining.remove(queue[0])
        component = set(queue)
        while queue:
            vertex = queue.pop()
            neighbors = ADJACENCY[vertex] & remaining
            remaining.difference_update(neighbors)
            component.update(neighbors)
            queue.extend(sorted(neighbors))
        result.append(tuple(sorted(component)))
    return sorted(result, key=lambda component: (-len(component), component))


def union_find_orders(vertices):
    parent = {vertex: vertex for vertex in vertices}

    def root(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for first, second in EDGES:
        if first in vertices and second in vertices:
            parent[root(first)] = root(second)
    sizes = {}
    for vertex in vertices:
        representative = root(vertex)
        sizes[representative] = sizes.get(representative, 0) + 1
    return sorted(sizes.values(), reverse=True)


def bipartite(vertices):
    colors = {}
    for start in sorted(vertices):
        if start in colors:
            continue
        colors[start] = 0
        queue = [start]
        while queue:
            vertex = queue.pop()
            for neighbor in ADJACENCY[vertex] & vertices:
                if neighbor in colors:
                    if colors[neighbor] == colors[vertex]:
                        return False
                else:
                    colors[neighbor] = 1 - colors[vertex]
                    queue.append(neighbor)
    return True


def component_union_condition(selected):
    return all(
        bipartite(set(component) | {vertex})
        for component in components(VERTICES - selected)
        for vertex in selected
    )


def image(vertices, sign, shift):
    return tuple(sorted(
        (sign * (vertex % 7) + shift) % 7 + 7 * (vertex // 7)
        for vertex in vertices
    ))


def orbit(vertices):
    return {image(vertices, sign, shift)
            for sign in (-1, 1) for shift in range(7)}


def check_wagner():
    vertices = frozenset(range(8))
    edges = frozenset(tuple(sorted((vertex, (vertex + step) % 8)))
                      for vertex in vertices for step in (1, 4))
    adjacency = {vertex: {other for other in vertices
                         if tuple(sorted((vertex, other))) in edges}
                 for vertex in vertices}
    require(len(edges) == 12 and all(len(neighbors) == 3
                                    for neighbors in adjacency.values()),
            'Wagner cubic graph')
    require(not any(all(tuple(sorted(edge)) in edges
                        for edge in itertools.combinations(triple, 2))
                    for triple in itertools.combinations(vertices, 3)),
            'Wagner triangle exclusion')
    cycle = (0, 1, 2, 3, 4)
    require(all(tuple(sorted((cycle[index], cycle[(index + 1) % 5]))) in edges
                for index in range(5)), 'Wagner five-cycle')
    independent_count = 0
    valid_order_three = 0
    optimum = 8
    for mask in range(256):
        selected = frozenset(vertex for vertex in vertices if mask & (1 << vertex))
        if any(set(edge) <= selected for edge in edges):
            continue
        independent_count += 1
        remaining = set(vertices - selected)
        orders = []
        while remaining:
            start = min(remaining)
            remaining.remove(start)
            queue = [start]
            order = 0
            while queue:
                vertex = queue.pop()
                order += 1
                neighbors = adjacency[vertex] & remaining
                remaining.difference_update(neighbors)
                queue.extend(neighbors)
            orders.append(order)
        largest = max(orders, default=0)
        optimum = min(optimum, largest)
        valid_order_three += largest <= 3
    require(valid_order_three == 0 and optimum == 4, 'Wagner residual obstruction')
    return {'vertices': 8, 'edges': 12, 'subsets': 256,
            'independent_sets': independent_count,
            'odd_girth': 5,
            'partitions_with_residual_order_at_most_three': valid_order_three,
            'minimum_largest_residual_component_order': optimum}


def main():
    require(len(EDGES) == 21, 'edge count')
    require(all(first != second for first, second in EDGES), 'simplicity')
    require(all(len(neighbors) == 3 for neighbors in ADJACENCY.values()), 'degree')
    require(len(components(VERTICES)) == 1, 'connectedness')
    require(not any(
        all(tuple(sorted(edge)) in EDGES
            for edge in itertools.combinations(triple, 2))
        for triple in itertools.combinations(VERTICES, 3)
    ), 'triangle exclusion')
    cycle = (0, 1, 2, 9, 7)
    require(len(set(cycle)) == 5, 'five distinct cycle vertices')
    require(all(tuple(sorted((cycle[index], cycle[(index + 1) % 5]))) in EDGES
                for index in range(5)), 'five-cycle edges')
    for sign in (-1, 1):
        for shift in range(7):
            transformed = {tuple(sorted(image(edge, sign, shift))) for edge in EDGES}
            require(transformed == EDGES, 'dihedral automorphism')
    independent_count = 0
    histogram = {}
    maximal_sets = set()
    optimum = len(VERTICES)
    valid_order_three = 0
    component_union_solutions = []
    independent_sets = []
    for mask in range(1 << len(VERTICES)):
        selected = frozenset(vertex for vertex in VERTICES if mask & (1 << vertex))
        if not independent(selected):
            continue
        independent_count += 1
        independent_sets.append(selected)
        if component_union_condition(selected):
            component_union_solutions.append(sorted(selected))
        histogram[len(selected)] = histogram.get(len(selected), 0) + 1
        remaining = VERTICES - selected
        component_orders = sorted(map(len, components(remaining)), reverse=True)
        require(component_orders == union_find_orders(remaining), 'component agreement')
        largest = max(component_orders, default=0)
        optimum = min(optimum, largest)
        valid_order_three += largest <= 3
        if all(ADJACENCY[vertex] & selected for vertex in remaining):
            maximal_sets.add(tuple(sorted(selected)))
    expected_histogram = {0: 1, 1: 14, 2: 70, 3: 154, 4: 147, 5: 49}
    require(histogram == expected_histogram, 'independent-set size distribution')
    covered = set()
    rows = []
    for selected, path in zip(REPRESENTATIVES, PATHS):
        selected_set = frozenset(selected)
        require(selected in maximal_sets, 'maximal representative')
        require(len(path) == len(set(path)) == 4, 'four distinct path vertices')
        require(set(path) <= VERTICES - selected_set, 'residual path vertices')
        require(all(tuple(sorted(edge)) in EDGES for edge in zip(path, path[1:])),
                'residual path edges')
        images = orbit(selected)
        require(not covered & images, 'distinct symmetry classes')
        covered.update(images)
        rows.append({
            'independent_set': list(selected),
            'orbit_size': len(images),
            'residual_path': list(path),
            'component_orders': sorted(map(len, components(VERTICES - selected_set)),
                                       reverse=True),
        })
    require(covered == maximal_sets, 'complete maximal-independent-set classification')
    require(independent_count == 435 and len(maximal_sets) == 49, 'set counts')
    require(valid_order_three == 0 and optimum == 4, 'exact residual optimum')
    require(component_union_solutions == [[]], 'component-union condition solutions')
    require(not bipartite(VERTICES), 'nonbipartite graph')
    cycle_rows = []
    for selected, (vertex, cycle) in zip(REPRESENTATIVES, ODD_CYCLE_WITNESSES):
        require(vertex in selected, 'selected cycle attachment vertex')
        require(len(cycle) == len(set(cycle)) == 5, 'five distinct odd-cycle vertices')
        require(all(tuple(sorted((cycle[index], cycle[(index + 1) % 5]))) in EDGES
                    for index in range(5)), 'odd-cycle edges')
        require(any(set(cycle) <= set(component) | {vertex}
                    for component in components(VERTICES - set(selected))),
                'odd cycle in a residual component plus selected vertex')
        cycle_rows.append({'selected_vertex': vertex, 'odd_cycle': list(cycle)})
    extension_checks = 0
    for selected in independent_sets:
        if not selected or not component_union_condition(selected):
            continue
        for vertex in VERTICES - selected:
            if not ADJACENCY[vertex] & selected:
                require(component_union_condition(selected | {vertex}),
                        'nonempty condition preserved under independent extension')
                extension_checks += 1
    attaining = frozenset(REPRESENTATIVES[1])
    attaining_components = components(VERTICES - attaining)
    require(attaining_components == [(1, 3, 8, 10), (7, 9, 11), (5, 6)],
            'attaining partition')
    print(json.dumps({
        'graph': 'GP(7,2)',
        'labels': 'a_i=i; b_i=7+i; indices modulo 7',
        'vertices': 14,
        'edges': 21,
        'connected': True,
        'degree': 3,
        'odd_girth': 5,
        'subsets': 16384,
        'independent_sets': independent_count,
        'independent_set_size_distribution': histogram,
        'maximal_independent_sets': len(maximal_sets),
        'dihedral_classes': rows,
        'partitions_with_residual_order_at_most_three': valid_order_three,
        'minimum_largest_residual_component_order': optimum,
        'attaining_independent_set': sorted(attaining),
        'attaining_components': attaining_components,
        'component_methods_agree': True,
        'earlier_wagner_graph': check_wagner(),
        'component_union_bipartiteness': {
            'independent_solutions': component_union_solutions,
            'nonempty_independent_solutions': 0,
            'maximal_class_odd_cycles': cycle_rows,
            'extension_checks_on_satisfying_nonempty_sets': extension_checks,
            'extension_property': 'Written proof; the nonempty satisfying-set family is empty on this graph.',
        },
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

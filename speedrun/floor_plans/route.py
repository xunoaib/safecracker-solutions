from collections import defaultdict, deque

from dependencies import dependency_graph


def topological_sort(dependency_graph):
    in_degree = defaultdict(int)
    for node in dependency_graph:
        in_degree[node]
        for dep in dependency_graph[node]:
            in_degree[dep] += 1

    queue = deque([node for node in in_degree if in_degree[node] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in dependency_graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(result) != len(in_degree):
        raise ValueError('Cycle detected - no valid ordering exists')

    return result


def find_cycle(graph):
    visited = set()
    path = []
    path_set = set()

    def dfs(node):
        visited.add(node)
        path.append(node)
        path_set.add(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in path_set:
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                print('Cycle found:', ' -> '.join(cycle))
                return True

        path.pop()
        path_set.remove(node)
        return False

    for node in graph:
        if node not in visited:
            if dfs(node):
                return


def main():
    find_cycle(dependency_graph)
    result = topological_sort(dependency_graph)[::-1]
    print(', '.join(result))


if __name__ == '__main__':
    main()

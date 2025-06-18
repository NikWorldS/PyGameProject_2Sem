import heapq

class PathFinder:
    def heuristic(self, a, b):
        """Возвращает значение Манхэттенской эвристики"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star_search(self, grid, start, goal):
        direction = [
            (-1, 0),  # вверх
            (1, 0),  # вниз
            (0, -1),  # влево
            (0, 1),  # вправо
            (-1, -1),  # влево-вверх
            (-1, 1),  # вправо-вправо
            (1, -1),  # влево-вниз
            (1, 1),  # вправо-вниз
        ]

        open_set = []
        heapq.heappush(open_set, (0, start))

        came_from = {}
        cost_so_far = {start: 0}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                break

            for dx, dy in direction:
                next = (current[0] + dx, current[1] + dy)
                if 0 <= next[0] < len(grid[0]) and 0 <= next[1] < len(grid):
                    if grid[next[1]][next[0]] == 1:
                        continue

                    new_cost = cost_so_far[current] + 1
                    if next not in cost_so_far or new_cost < cost_so_far[next]:
                        cost_so_far[next] = new_cost
                        priority = new_cost + self.heuristic(goal, next)
                        heapq.heappush(open_set, (priority, next))
                        came_from[next] = current

        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from.get(current)
            if current is None:
                return []

        path.append(start)
        path.reverse()
        return path
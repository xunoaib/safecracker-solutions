#include <algorithm>
#include <array>
#include <cmath>
#include <iostream>
#include <queue>
#include <random>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using Grid = std::array<std::array<int, 5>, 5>;

// Coordinates for each 2x2 intersection (total 16 possible 2x2 blocks in 5x5
// grid)
const std::vector<std::pair<int, int>> ROTATIONS = {
    {0, 0}, {0, 1}, {0, 2}, {0, 3}, {1, 0}, {1, 1}, {1, 2}, {1, 3},
    {2, 0}, {2, 1}, {2, 2}, {2, 3}, {3, 0}, {3, 1}, {3, 2}, {3, 3},
};

// Tiles to be marked as blank (-1)
const std::unordered_set<int> BLANK_IDS = {3, 4, 9, 15, 20, 21};

// Print the grid
void print_grid(const Grid &grid) {
    for (auto &row : grid) {
        for (auto val : row) {
            if (val == -1)
                std::cout << "  *";
            else
                std::cout << ' ' << (val < 10 ? " " : "") << val;
        }
        std::cout << '\n';
    }
    std::cout << "\n";
}

// Rotate a 2x2 block clockwise
void rotate(Grid &grid, int r, int c) {
    int temp = grid[r][c];
    grid[r][c] = grid[r + 1][c];
    grid[r + 1][c] = grid[r + 1][c + 1];
    grid[r + 1][c + 1] = grid[r][c + 1];
    grid[r][c + 1] = temp;
}

// Create the solved state
Grid create_goal() {
    Grid grid;
    for (int i = 0; i < 5; ++i) {
        for (int j = 0; j < 5; ++j) {
            int id = i * 5 + j;
            grid[i][j] = BLANK_IDS.count(id) ? -1 : id;
        }
    }
    return grid;
}

// Shuffle the grid by applying random rotations
Grid shuffle_grid(const Grid &goal, int steps = 12) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dist(0, ROTATIONS.size() - 1);

    Grid shuffled = goal;
    for (int i = 0; i < steps; ++i) {
        auto [r, c] = ROTATIONS[dist(gen)];
        rotate(shuffled, r, c);
    }
    return shuffled;
}

// For hashing a grid state
struct GridHasher {
    std::size_t operator()(const Grid &g) const {
        std::size_t h = 0;
        for (auto &row : g)
            for (int val : row)
                h ^= std::hash<int>()(val) + 0x9e3779b9 + (h << 6) + (h >> 2);
        return h;
    }
};

// Heuristic: sum of Manhattan distances for all non-blank tiles
int heuristic(const Grid &a, const Grid &goal) {
    std::unordered_map<int, std::pair<int, int>> goal_pos;
    for (int i = 0; i < 5; ++i)
        for (int j = 0; j < 5; ++j)
            if (goal[i][j] != -1)
                goal_pos[goal[i][j]] = {i, j};

    int h = 0;
    for (int i = 0; i < 5; ++i) {
        for (int j = 0; j < 5; ++j) {
            int val = a[i][j];
            if (val != -1 && goal_pos.count(val)) {
                auto [gi, gj] = goal_pos[val];
                h += std::abs(i - gi) + std::abs(j - gj);
            }
        }
    }
    return h * 0.5;
}

// A* to find shortest path to solution
std::vector<std::pair<int, int>> solve(const Grid &start, const Grid &goal) {
    using State =
        std::tuple<int, int, Grid,
                   std::vector<std::pair<int, int>>>; // f, g, grid, path
    auto cmp = [](const State &a, const State &b) {
        return std::get<0>(a) > std::get<0>(b);
    };

    std::priority_queue<State, std::vector<State>, decltype(cmp)> pq(cmp);
    std::unordered_set<Grid, GridHasher> visited;

    int h0 = heuristic(start, goal);
    pq.emplace(h0, 0, start, std::vector<std::pair<int, int>>{});
    visited.insert(start);

    while (!pq.empty()) {
        auto [f, g, state, path] = pq.top();
        pq.pop();

        if (state == goal)
            return path;

        for (auto [r, c] : ROTATIONS) {
            Grid new_state = state;
            rotate(new_state, r, c);
            if (!visited.count(new_state)) {
                auto new_path = path;
                new_path.emplace_back(r, c);
                int g_new = g + 1;
                int f_new = g_new + heuristic(new_state, goal);
                pq.emplace(f_new, g_new, new_state, new_path);
                visited.insert(new_state);
            }
        }
    }

    return {}; // No solution found
}

int main() {
    Grid goal = create_goal();
    Grid start = shuffle_grid(goal);

    std::cout << "Initial state:\n";
    print_grid(start);
    std::cout << "Goal state:\n";
    print_grid(goal);

    auto solution = solve(start, goal);
    std::cout << "Solution in " << solution.size() << " moves:\n";
    for (auto [r, c] : solution)
        std::cout << "Rotate at (" << r << ", " << c << ")\n";

    return 0;
}

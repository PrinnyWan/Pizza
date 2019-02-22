class inputmap:
    def __init__(self, filename):
        f = open(filename, "r")
        require = f.readline().split(' ')
        self.R, self.C, self.L, self.H = int(require[0]), int(require[1]), int(require[2]), int(require[3])
        self.pizza = []
        self.mushrooms_map = [[0] * self.C for _ in range(self.R)]
        self.tomato_map = [[0] * self.C for _ in range(self.R)]
        self.sxy = []
        for x in range(self.H):
            for y in range(self.H):
                if 2 * self.L <= (x + 1) * (y + 1) <= self.H:
                    self.sxy.append((x, y))
        self.sxy.sort(key=lambda a: a[0] * a[1])

        for _ in range(self.R):
            self.pizza.append(f.readline())
        f.close()
        for x in range(self.R):
            mushrooms_count = 0
            tomato_count = 0
            for y in range(self.C):
                if x >= 1:
                    self.mushrooms_map[x][y] += self.mushrooms_map[x-1][y]
                    self.tomato_map[x][y] += self.tomato_map[x-1][y]
                if self.pizza[x][y] == 'M':
                    mushrooms_count += 1
                if self.pizza[x][y] == 'T':
                    tomato_count += 1
                self.mushrooms_map[x][y] += mushrooms_count
                self.tomato_map[x][y] += tomato_count
        print('Initialization Done')


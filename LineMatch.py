import copy

class LMProcess:
    def __init__(self, inputData):
        self.R, self.C = inputData.R, inputData.C
        self.L, self.H = inputData.L, inputData.H
        self.sxy = inputData.sxy
        self.mushrooms_map = inputData.mushrooms_map
        self.tomato_map = inputData.tomato_map
        self.visited = inputData.visited
        self.totalSlices = 0
        self.stack = []
        self.ansStack = []

        self.maxArea = 0
        self.curArea = 0
        self.totalArea = 0

        self.bound_l = 0
        self.bound_r = 0
        self.bound_t = 0
        self.bound_b = 0
        self.waitPoint = []
        self.backupStartPoint = []
        self.waitLine = set()


    def lineMatch(self, position = (0, 0)):

        self.waitPoint.append(position)

        self.temp = position
        ######
        self.lineMatchHelp(True)
        self.outputans()

        while True:
            self.Check2Backup()
            self.waitLine.add((self.bound_b, self.bound_r))
            if not self.backupStartPoint:
                break
            self.waitPoint.append(self.backupStartPoint.pop(0))
            self.temp = (self.bound_b, self.bound_r)

            self.lineMatchHelp(True)
            self.waitLine.remove((self.bound_b, self.bound_r))
            self.outputans()

        return

    def lineMatchHelp(self, start = False):
        if not self.waitPoint:
            if self.curArea >= self.maxArea and self.curArea > self.H :
                self.maxArea = self.curArea
                self.write2temp()
                self.ansStack = copy.deepcopy(self.stack)
            return

        curx, cury = self.waitPoint.pop()
        if start:
            self.maxArea = 0
            self.curSlices = 0
            self.ansStack = []
            self.botlimit = curx + 30
            self.rightlimit = cury + 30
            for slice_x, slice_y in self.sxy:
                if curx + slice_x < self.R and cury + slice_y < self.C and 2 * self.L <= (slice_x + 1) * (
                        slice_y + 1) <= self.H and self.valid(curx, cury, slice_x, slice_y):
                    self.waitPoint.append((curx, cury + slice_y + 1))
                    self.waitPoint.append((curx + slice_x + 1, cury))
                    self.waitLine.add((curx + slice_x, cury + slice_y))
                    self.changevisited(curx, cury, slice_x, slice_y, self.visited)
                    self.curArea += (slice_x + 1) * (slice_y + 1)
                    self.stack.append((curx, cury, curx + slice_x, cury + slice_y))
                    self.lineMatchHelp()
                    self.stack.pop()
                    self.curArea -= (slice_x + 1) * (slice_y + 1)
                    self.changevisited(curx, cury, slice_x, slice_y, self.visited, 0)
                    self.waitLine.remove((curx + slice_x, cury + slice_y))
            return

        else:
            match = False
            for slice_x, slice_y in self.sxy:
                if (curx + slice_x, cury - 1) in self.waitLine or (curx - 1, cury + slice_y) in self.waitLine:
                    if curx + slice_x < self.R and curx + slice_x < self.botlimit and cury + slice_y < self.C and cury + slice_y < self.rightlimit and 2 * self.L <= (slice_x + 1) * (
                            slice_y + 1) <= self.H and self.valid(curx, cury, slice_x, slice_y):

                        if (curx + slice_x, cury - 1) in self.waitLine:
                            endx, endy = curx + slice_x, cury - 1
                        else:
                            endx, endy = curx - 1, cury + slice_y
                            # find the used end line
                        match = True
                        if endx != curx - 1 and endy != cury + slice_y:
                            self.waitPoint.append((curx, cury + slice_y + 1))
                        else:
                            self.waitPoint.append((curx + slice_x + 1, cury))
                        self.waitLine.remove((endx, endy))
                        self.waitLine.add((curx + slice_x, cury + slice_y))
                        self.changevisited(curx, cury, slice_x, slice_y, self.visited)
                        self.curArea += (slice_x + 1) * (slice_y + 1)
                        self.stack.append((curx, cury, curx + slice_x, cury + slice_y))
                        self.lineMatchHelp()
                        self.stack.pop()
                        self.curArea -= (slice_x + 1) * (slice_y + 1)
                        self.changevisited(curx, cury, slice_x, slice_y, self.visited, 0)
                        self.waitLine.remove((curx + slice_x, cury + slice_y))
                        self.waitLine.add((endx, endy))
            if not match:
                self.lineMatchHelp()
            return

    def changevisited(self, cx, cy, sx, sy, visited, changeTo = 1):
        for x in range(cx, cx + sx + 1):
            for y in range(cy, cy + sy + 1):
                visited[x][y] = changeTo

    def valid(self, curx, cury, sx, sy):
        map1 = self.tomato_map
        map2 = self.mushrooms_map

        count1 = map1[curx + sx][cury + sy]
        count2 = map2[curx + sx][cury + sy]
        if curx >= 1:
            count1 -= map1[curx - 1][cury + sy]
            count2 -= map2[curx - 1][cury + sy]
        if cury >= 1:
            count1 -= map1[curx + sx][cury - 1]
            count2 -= map2[curx + sx][cury - 1]
        if curx >= 1 and cury >= 1:
            count1 += map1[curx - 1][cury - 1]
            count2 += map2[curx - 1][cury - 1]
        if count1 < self.L or count2 < self.L:
            return False
        for x in range(curx, curx + sx + 1):
            for y in range(cury, cury + sy + 1):
                if self.visited[x][y] == 1:
                    return False
        return True

    def write2temp(self):
        f = open('temp.txt', 'w')
        self.curSlices = len(self.stack)
        for _ in self.stack:
            f.writelines(str(_[0]) + ' ' + str(_[1]) + ' ' + str(_[2]) + ' ' + str(_[3]) + '\n')
        f.close()

    def outputans(self):
        with open('out.txt', 'a') as f:
            with open('temp.txt', 'r') as t:
                f.write(t.read())
        self.bound_b = -2
        self.bound_t = 1000
        self.bound_r = -2
        self.bound_l = 1000
        self.totalSlices += len(self.ansStack)
        self.totalArea += self.maxArea

        for startx, starty, endx, endy in self.ansStack:
            for x in range(startx, endx + 1):
                for y in range(starty, endy + 1):
                    self.visited[x][y] = 1
                    self.bound_b = max(x, self.bound_b)
                    self.bound_t = min(x, self.bound_t)
                    self.bound_r = max(y, self.bound_r)
                    self.bound_l = min(y, self.bound_l)

    def Check2Backup(self):
        if -1 < self.bound_r + 1 < self.C:
            for y in range(self.bound_r + 1, self.bound_l, -1):
                if (y == 0 or self.visited[self.bound_t][y -1]) and (self.bound_t == 0 or self.visited[self.bound_t - 1][y]):
                    if y + 1 >= self.C or self.visited[self.bound_t][y + 1] or self.bound_t + 1 >= self.R or self.visited[self.bound_t + 1][y]:
                        break
                    self.backupStartPoint.append((self.bound_t, y))
                    break
        if -1 < self.bound_b + 1 < self.R:
            for x in range(self.bound_b + 1, self.bound_t, -1):
                if (x == 0 or self.visited[x-1][self.bound_l]) and (self.bound_l == 0 or self.visited[x][self.bound_l-1]):
                    if x + 1 >= self.R or self.visited[x + 1][self.bound_l] or self.bound_l + 1 >= self.C or self.visited[x][self.bound_l + 1]:
                        break
                    self.backupStartPoint.append((x, self.bound_l))
                    break









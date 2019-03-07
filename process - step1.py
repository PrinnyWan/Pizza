import copy


class Process:

    def __init__(self, inputdata):
        self.R, self.C = inputdata.R, inputdata.C
        self.sxy = inputdata.sxy
        self.mushrooms_map = inputdata.mushrooms_map
        self.tomato_map = inputdata.tomato_map
        self.L, self.H = inputdata.L, inputdata.H
        self.stack = []
        self.maxarea = 0
        self.leftBound = 0
        self.curSlices = 0

        self.cut = 10
        # define block size

    def run(self):
        visited = [[0] * self.C for _ in range(self.R)]
        f = open('out.txt', 'w')
        f.close()
        # create a new output file
        slices = 0
        totalcell = 0
        cR = min(self.R, self.cut)
        cC = min(self.C, self.cut)
        # when the whole pizza smaller than one block, change size of the first block
        for x in range(0, self.R, self.cut):
            for y in range(0, self.C, self.cut):
                self.stack = []
                self.leftBound = y
                curarea = self.count(x, y, min(x + cR, self.R), min(y + cC, self.C), visited)
                self.maxarea = 0
                self.runhelper(x, y, curarea, cR * cC - curarea, [], min(x + cR, self.R), min(y + cC, self.C), self.L, self.H, visited, self.mushrooms_map, self.tomato_map)
                self.outputans(visited)
                slices += self.curSlices
                totalcell += self.maxarea
                print('block', (y // self.cut + 1) + ((x // self.cut) * (self.C // self.cut)), ':',
                      self.maxarea / (cR * cC), 'percent used,',
                      ((y // self.cut + 1) + ((x // self.cut) * (self.C // self.cut))) / (
                                  ((self.R + 9)// self.cut) * ((self.C + 9) // self.cut)), '% finished')
        print('total', totalcell, '/', self.R * self.C, totalcell / self.R / self.C)
        with open('out.txt', 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(str(slices) + '\n' + content)

    def count(self, startx, starty, endx, endy, visited):
        count = 0
        for x in range(startx, endx):
            for y in range(starty, endy):
                count += visited[x][y]
        return count

    def valid(self, curx, cury, sx, sy, L, H, map1, map2, visited):
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
        if count1 < L or count2 < L:
            return False

        for x in range(curx, curx + sx + 1):
            for y in range(cury, cury + sy + 1):
                if visited[x][y] == 1:
                    return False
        return True

    def changevisited(self, curx, cury, sx, sy, visited, changeto = 1):
        for x in range(curx, curx + sx + 1):
            for y in range(cury, cury + sy + 1):
                visited[x][y] = changeto

    def runhelper(self, curx, cury, curarea, restarea, stack, R, C, L, H, visited, map1, map2):
        if curx == R and cury == C:
            if curarea > self.maxarea:
                self.stack = copy.deepcopy(stack)
                self.maxarea = curarea
                self.write2temp(stack)
            return
        if curarea + restarea <= self.maxarea:
            return

        if visited[curx][cury]:
            nx, ny = self.findnextpoint(curx, cury, R, C, visited)
            self.runhelper(nx, ny, curarea, restarea - 1, stack, R, C, L, H, visited, map1, map2)
            return

        for slice_x , slice_y in self.sxy:
            if curx + slice_x < self.R and cury + slice_y < self.C and 2*L <= (slice_x + 1) * (slice_y + 1) <= H and self.valid(curx, cury, slice_x, slice_y, L, H, map1, map2, visited):
                stack.append((curx, cury, curx + slice_x, cury + slice_y))
                self.changevisited(curx, cury, slice_x, slice_y, visited)
                nx, ny = self.findnextpoint(curx, cury, R, C, visited)
                newarea = (min(R - curx, slice_x + 1)) * (min(C - cury, slice_y + 1))
                self.runhelper(nx, ny, curarea + newarea, restarea - newarea, stack, R, C, L, H, visited, map1, map2)
                self.changevisited(curx, cury, slice_x, slice_y, visited, 0)
                stack.pop()
        visited[curx][cury] = 1
        nx, ny = self.findnextpoint(curx, cury, R, C, visited)
        self.runhelper(nx, ny, curarea, restarea - 1, stack, R, C, L, H, visited, map1, map2)
        visited[curx][cury] = 0

    def findnextpoint(self, curx, cury, R, C, visited):
        while curx < R and cury < C:
            if not visited[curx][cury]:
                return curx, cury
            cury += 1
            if cury == C:
                cury = self.leftBound
                curx += 1
        return R, C

    def write2temp(self, stack):
        f = open('temp.txt', 'w')
        self.curSlices = len(stack)
        for _ in stack:
            f.writelines(str(_[0]) + ' ' + str(_[1]) + ' ' + str(_[2]) + ' ' + str(_[3]) + '\n')
        f.close()

    def outputans(self, visited):
        with open('out.txt', 'a') as f:
            with open('temp.txt', 'r') as t:
                f.write(t.read())
        for startx, starty, endx, endy in self.stack:
            for x in range(startx, endx + 1):
                for y in range(starty, endy + 1):
                    visited[x][y] = 1



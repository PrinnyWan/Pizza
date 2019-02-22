class processdata:

    def run(self, inputdata):
        mushrooms_map = inputdata.mushrooms_map
        tomato_map = inputdata.tomato_map
        L, H = inputdata.L, inputdata.H
        R, C = inputdata.R, inputdata.C
        visited = [[0] * C for _ in range(R)]
        f = open('out.txt', 'w')
        f.close()
        self.sxy = inputdata.sxy
        slices = 0
        self.curslices = 0
        cut = 10
        cR = min(R, cut)
        cC = min(C, cut)
        for x in range(0, R, 10):
            for y in range(0, C, 10):
                self.left = y
                self.maxarea = 0
                self.runhelper(x, y, 0, cR * cC, [], x + cR, y + cC, L, H, visited, mushrooms_map, tomato_map)
                self.outputans(x, y, cR, cC, R, C)
                slices += self.curslices
        with open('out.txt', 'r+') as f:
            content = f.read()
            f.seek(0,0)
            f.write(str(slices) + '\n' + content)

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
        if curx == R - 1 and cury == C - 1:
            if curarea > self.maxarea:
                self.maxarea = curarea
                self.write2temp(stack)
            return
        if curarea + restarea <= self.maxarea:
            return

        for slice_x , slice_y in self.sxy:
            if curx + slice_x < R and cury + slice_y < C and 2*L <= (slice_x + 1) * (slice_y + 1) <= H and self.valid(curx, cury, slice_x, slice_y, L, H, map1, map2, visited):
                stack.append((curx, cury, curx + slice_x, cury + slice_y))
                self.changevisited(curx, cury, slice_x, slice_y, visited)
                nx, ny = self.findnextpoint(curx, cury, R, C, visited)
                self.runhelper(nx, ny, curarea + (slice_x + 1) * (slice_y + 1), restarea - (slice_x + 1) * (slice_y + 1), stack, R, C, L, H, visited, map1, map2)
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
                cury = self.left
                curx += 1
        return R - 1, C - 1

    def write2temp(self, stack):
        f = open('temp.txt', 'w')
        self.curslices = len(stack)
        for _ in stack:
            f.writelines(str(_[0]) + ' ' + str(_[1]) + ' ' + str(_[2]) + ' ' + str(_[3]) + '\n')
        f.close()

    def outputans(self, x, y, cR, cC, R, C):
        print('block', (y//10+1)+((x//10)*(C//10)),':', self.maxarea / (cR * cC), 'percent used,', ((y//10+1)+((x//10)*(C//10))) / ((R//10+1)*(C//10+1)), '% finished')
        with open('out.txt', 'a') as f:
            with open('temp.txt', 'r') as t:
                f.write(t.read())




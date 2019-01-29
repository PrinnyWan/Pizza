class processdata:

    def run(self, inputdata):
        mushrooms_map = inputdata.mushrooms_map
        tomato_map = inputdata.tomato_map
        pizza = inputdata.pizza
        visited = [0] * inputdata.R * inputdata.C
        L, H = inputdata.L, inputdata.H
        R, C = inputdata.R, inputdata.C
        self.C = inputdata.C
        self.maxarea = 0
        self.runhelper(0, 0, 0, R * C, [], R, C, L, H, visited, mushrooms_map, tomato_map)

    def valid(self, curx, cury, sx, sy, L, H, map1, map2, visited):
        count1 = map1[curx + sx][cury + sy]
        count2 = map2[curx + sx][cury + sy]
        if curx >= 1:
            count1 -= map1[curx - 1][cury + sy]
            count2 -= map2[curx - 1][cury + sy]
        if cury >= 1:
            count1 -= map1[curx +sx][cury - 1]
            count2 -= map2[curx +sx][cury - 1]
        if curx >= 1 and cury >= 1:
            count1 -= map1[curx - 1][cury - 1]
            count2 -= map2[curx - 1][cury - 1]
        if count1 < L or count1 > H or count2 < L or count2 > H:
            return False

        for x in range(curx, curx + sx + 1):
            for y in range(cury, cury + sy + 1):
                if visited[self.getid(x, y)] == 1:
                    return False
        return True

    def getid(self, x, y):
        return x * self.C + y

    def changevisited(self, curx, cury, sx, sy, visited, changeto = 1):
        for x in range(curx, curx + sx + 1):
            for y in range(cury, cury + sy + 1):
                visited[self.getid(x, y)] = changeto

    def runhelper(self, curx, cury, curarea, restarea, stack, R, C, L, H, visited, map1, map2):
        if curx == R - 1 and cury == C - 1:
            if curarea > self.maxarea:
                self.maxarea = curarea
                self.outputans(stack)
            return
        if curarea + restarea < self.maxarea:
            return

        for slice_x in range(H + 1):
            for slice_y in range(H + 1):
                if curx + slice_x < R and cury + slice_y < C and 2*L <= (slice_x + 1) * (slice_y + 1) <= 2*H and self.valid(curx, cury, slice_x, slice_y, L, H, map1, map2, visited):
                    stack.append((curx, cury, curx + slice_x, cury + slice_y))
                    self.changevisited(curx, cury, slice_x, slice_y, visited)
                    nx, ny = self.findnextpoint(curx, cury, R, C, visited)
                    self.runhelper(nx, ny, curarea + (slice_x + 1) * (slice_y + 1), restarea - (slice_x + 1) * (slice_y + 1), stack, R, C, L, H, visited, map1, map2)
                    self.changevisited(curx, cury, slice_x, slice_y, visited, 0)
                    stack.pop()
        visited[self.getid(curx, cury)] = 1
        nx, ny = self.findnextpoint(curx, cury, R, C, visited)
        self.runhelper(nx, ny, curarea, restarea - 1, stack, R, C, L, H, visited, map1, map2)
        visited[self.getid(curx, cury)] = 0

    def findnextpoint(self, curx, cury, R, C, visited):
        while curx < R and cury < C:
            if not visited[self.getid(curx, cury)]:
                return  curx, cury
            cury += 1
            if cury == C:
                cury = 0
                curx += 1
        return R - 1, C - 1

    def outputans(self, stack):
        print(len(stack), stack)
        f = open('out.txt', 'w')
        f.writelines(str(len(stack)) + '\n')
        for _ in stack:
            f.writelines(str(_[0]) + ' ' + str(_[1]) + ' ' + str(_[2]) + ' ' + str(_[3]) + '\n')
        f.close()




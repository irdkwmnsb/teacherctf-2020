import random


class Player():
    def __init__(self, canvas_size):
        self.canvas_size = canvas_size

    def place(self, cur_img):
        raise NotImplementedError()


class ImagePlayer(Player):
    def __init__(self, canvas_size, goal_img):
        super().__init__(canvas_size)
        self.goal_img = goal_img
        self.check_pattern = [(i, j) for i in range(canvas_size[0]) for j in range(canvas_size[1])]
        random.shuffle(self.check_pattern)

    def place(self, cur_img):
        for i, j in self.check_pattern:
            if cur_img[i][j] != self.goal_img[i][j]:
                return (i, j, self.goal_img[i][j])


class ChaoticPlayer(Player):
    def __init__(self, canvas_size):
        super().__init__(canvas_size)

    def place(self, cur_img):
        x, y = random.randint(0, self.canvas_size[0] - 1), random.randint(0, self.canvas_size[1] - 1)
        col = not cur_img[x][y]
        return (x, y, col)


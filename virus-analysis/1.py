# 导入所需的库
import numpy as np
import matplotlib.pyplot as plt

# 创建扩散模型类


class Diffusion:

    # 初始化
    def __init__(self, N):
        self.N = N
        self.NI = N**2
        self.indivduals = None
        self.df = None
        self.NoP = 0

    # 初始化个体位置
    def init_pos(self, df):
        self.df = df
        N = self.N
        x, y = np.linspace(0, (N - 1) * df, N), np.linspace(0, (N - 1) * df, N)
        vx, vy = np.meshgrid(x, y)
        self.ix, self.iy = vx.flatten(), vy.flatten()
        self.iix, self.iiy = vx.flatten(), vy.flatten()

    # 设置模型参数
    def init_para(self, D0, P0, W, d_step=0.05, t_step=0.01, A=np.e):
        self.D0 = np.asarray(D0)
        self.P0 = np.asarray(P0)
        self.W = np.asarray(W)
        self.A = np.asarray(A)

        d0 = np.max(self.D0)
        p0 = np.min(self.P0)
        w = np.min(self.W)
        a = np.min(self.A)

        self.t_step = t_step
        self.d_step = d_step
        df = self.df
        self.p_min = (1 + w) * p0 / (a ** (df - d0))
        self.patients = np.zeros(self.NI, dtype=int)

    # 放置感染源
    def place_source(self, source):
        self.patients[source] = 1

    # 个体游走
    def walk(self, t):
        t_step = self.t_step
        d_step = self.d_step
        NI = self.NI
        step_d = d_step * self.df
        n_step = int(t // t_step)
        moves = np.random.random_integers(1, 4, n_step * NI).reshape(n_step, NI)
        ix, iy = self.ix, self.iy
        iix, iiy = self.iix, self.iiy
        UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4
        for step in range(n_step):
            this = moves[step]
            ix += np.where(this == RIGHT, d_step, 0.0)
            ix -= np.where(this == LEFT, d_step, 0.0)
            iy += np.where(this == UP, d_step, 0.0)
            iy -= np.where(this == DOWN, d_step, 0.0)

            if np.any(self.patients):
                self.update_patients()
        self.NoP = np.nonzero(self.patients)[0].shape[0]

    # 更新感染者
    def update_patients(self):
        df = self.df
        current_patients = np.nonzero(self.patients)[0]
        for patient in current_patients:
            Dx = self.ix[patient] - self.ix
            Dy = self.iy[patient] - self.iy
            Dxy = np.hypot(Dx, Dy)
            Dxy = np.where(Dxy > df, df, Dxy)
            Dij = Dxy - self.D0
            WP0 = (1 + self.W) * self.P0
            WP1 = (1 + self.W) * self.P0 / (self.A ** (Dij))
            Pij0 = np.where(Dij <= 0, WP0, 0.0)
            Pij1 = np.where(Dij > 0, WP1, 0.0)
            Pij = Pij0 + Pij1
            Pr = np.random.uniform(self.p_min, 1, self.NI)
            DP = Pr - Pij
            infected = np.argwhere(DP < 0)
            self.patients[infected] = 1

    def plot(self):
        ix, iy = self.ix, self.iy
        patients = self.patients
        x_max, x_min = np.max(ix), np.min(ix)
        y_max, y_min = np.max(iy), np.min(iy)
        x_max, x_min = x_max + 10, x_min - 10
        y_max, y_min = y_max + 10, y_min - 10
        infected = np.where(patients == 1.0)
        noninfected = np.where(patients != 1.0)

        iix = ix[infected]
        iiy = iy[infected]
        nix = ix[noninfected]
        niy = iy[noninfected]
        plt.axis([x_min, x_max, y_min, y_max])
        plt.scatter(iix, iiy, marker="*", color="b")
        plt.scatter(nix, niy, marker=".", color="r")
        plt.show()


if __name__ == "__main__":
    N = 20
    NI = N * N
    D0 = 2.0
    P0 = 0.3
    W = 0
    df = 6.0

    t_step = 0.01
    d_step = 0.05
    m = Diffusion(N)
    m.init_pos(df)
    m.init_para(D0, P0, W, t_step=t_step, d_step=d_step)
    m.place_source(153)
    numbers = []
    m.plot()
    for t in [1, 2, 3, 4, 5, 6, 7]:
        m.walk(t)
        m.plot()
        numbers.append(m.NoP)

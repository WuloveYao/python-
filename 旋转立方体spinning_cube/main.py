import numpy as np  # 导入 NumPy 库，用于数值计算和处理多维数组
import pygame  # 导入 Pygame 库，用于游戏开发和图形界面设计

# 定义屏幕的宽度和高度
WIDTH = 800
HEIGHT = 800

# 定义颜色常量
BLACK = (0, 0, 0)  # 黑色
WHITE = (255, 255, 255)  # 白色


class Cube:
    """
    表示一个立方体。
    """

    def __init__(self, pos: np.ndarray, a: float) -> None:
        """
        初始化立方体。
        :param pos: 立方体的中心位置，是一个包含三个元素的 NumPy 数组。
        :param a: 立方体的边长。
        """
        self.pos = pos  # 立方体的中心位置
        self.angle = np.pi / 4  # 立方体的旋转角度，初始化为 45 度
        self.center_offset = np.array([-a / 2, -a / 2, -a / 2])  # 立方体顶点到中心的偏移量
        self.edges = np.array([  # 立方体的边，是一个包含 12 条边的数组
            # 前脸的四条边
            np.array([np.array([0, 0, 0]), np.array([a, 0, 0])]),
            np.array([np.array([a, 0, 0]), np.array([a, a, 0])]),
            np.array([np.array([a, a, 0]), np.array([0, a, 0])]),
            np.array([np.array([0, a, 0]), np.array([0, 0, 0])]),
            # 右脸的四条边
            np.array([np.array([0, 0, 0]), np.array([0, 0, a])]),
            np.array([np.array([a, a, 0]), np.array([a, a, a])]),
            np.array([np.array([a, 0, 0]), np.array([a, 0, a])]),
            np.array([np.array([0, a, 0]), np.array([0, a, a])]),
            # 上脸的四条边
            np.array([np.array([0, 0, a]), np.array([a, 0, a])]),
            np.array([np.array([a, 0, a]), np.array([a, a, a])]),
            np.array([np.array([a, a, a]), np.array([0, a, a])]),
            np.array([np.array([0, a, a]), np.array([0, 0, a])]),
        ])

    def draw(self, screen: pygame.surface.Surface, rotation_rate: float) -> None:
        """
        在屏幕上绘制立方体。
        :param screen: 要绘制立方体的 Pygame 屏幕对象。
        :param rotation_rate: 立方体的旋转速率，用于控制立方体旋转的速度。
        """
        # 将立方体的边加上中心偏移量，得到实际的顶点位置
        rotated_cube = np.add(self.edges, self.center_offset)

        # 计算绕 X、Y、Z 轴旋转的矩阵
        rotation_matrix_x = np.array([
            [1, 0, 0],
            [0, np.cos(self.angle), -np.sin(self.angle)],
            [0, np.sin(self.angle), np.cos(self.angle)]
        ])
        rotation_matrix_y = np.array([
            [np.cos(self.angle), 0, np.sin(self.angle)],
            [0, 1, 0],
            [-np.sin(self.angle), 0, np.cos(self.angle)]
        ])
        rotation_matrix_z = np.array([
            [np.cos(self.angle), -np.sin(self.angle), 0],
            [np.sin(self.angle), np.cos(self.angle), 0],
            [0, 0, 1],
        ])

        # 对立方体进行旋转
        rotated_cube = np.matmul(rotated_cube, rotation_matrix_x)
        rotated_cube = np.matmul(rotated_cube, rotation_matrix_y)
        rotated_cube = np.matmul(rotated_cube, rotation_matrix_z)

        # 将旋转后的立方体移动到正确的位置
        moved_cube = np.add(self.pos, rotated_cube)

        # 在屏幕上绘制立方体的边
        for edge in moved_cube:
            # 获取边的两个端点的屏幕坐标
            start_pos = edge[0][0:2]
            end_pos = edge[1][0:2]
            # 绘制边
            pygame.draw.line(screen, WHITE, start_pos, end_pos)

        # 更新立方体的旋转角度
        self.angle += rotation_rate


def main():
    """
    主函数，启动 Pygame 并创建旋转的立方体。
    """
    # 初始化 Pygame
    pygame.init()
    # 创建屏幕对象
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # 设置窗口标题
    pygame.display.set_caption("旋转立方体 By stormsha")
    # 创建立方体对象，中心位于 (400, 400, 200)，边长为 200
    cube = Cube(np.array([400, 400, 200]), 200)

    # 主循环
    running = True
    while running:
        # 处理 Pygame 事件，如关闭窗口等
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 清空屏幕
        screen.fill(BLACK)
        # 绘制立方体
        cube.draw(screen, 0.001)
        # 更新屏幕
        pygame.display.flip()


if __name__ == "__main__":
    # 如果脚本被直接运行，则执行主函数
    main()

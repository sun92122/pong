import tkinter as  tk

class Game(tk.Frame):
    def __init__(self, master):
        super(Game, self).__init__(master)
        # 初始生命
        self.lives = 3
        # 畫布寬度
        self.width = 610
        # 畫布高度
        self.height = 400
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg='#aaaaff')

        self.canvas.pack()
        self.pack()

        # 初始化
        # 建立空的dict用以儲存
        self.items = {}
        '''
        TODO
        將.ball設為None
        將.paddle設為新Paddle
        以key=.paddle.item將.paddle加入.items
        已迴圈調用.add_brick()新增所有磚塊
        '''

        self.hub = None
        self.setup_game()
        self.canvas.focus_set()
        # 移動鍵綁定
        self.canvas.bind('<Left>', lambda _: self.paddle.move(-10))
        self.canvas.bind('<Right>', lambda _: self.paddle.move(10))

    # 初始化遊戲
    def setup_game(self):
        self.add_ball()
        self.update_lives_text()
        self.text = self.draw_text(300, 200, 'Press Space to start')
        self.canvas.bind('<space>', lambda _: self.start_game())

    # 新增球於paddle上方
    def add_ball(self):
        if self.ball is not None:
            self.ball.delete()
        '''
        TODO
        用.paddle.get_position()取得滑桿座標
        將.ball設為x=滑桿中心的球
        用.paddle.set_ball(self.ball)使球對滑桿參考
        '''

    # 新增磚塊
    def add_brick(self, x, y, hits):
        '''
        TODO
        新增一個新的Brick
        並以key=.item將其加入self.items
        '''

    #繪製文字
    def draw_text(self, x, y, text, size=40):
        font = ('Helvetica', size)
        return self.canvas.create_text(x, y, text=text, font=font)
    
    # 更新生命值
    def update_lives_text(self):
        text = 'Lives: %s' % self.lives
        if self.hub is None:
            self.hub = self.draw_text(50, 20, text, 15)
        else:
            self.canvas.itemconfig(self.hub, text=text)

    #開始遊戲
    def start_game(self):
        # 解除空白鍵綁定
        self.canvas.unbind('<space>')
        # 刪除畫布上的文字
        self.canvas.delete(self.text)
        # 解除paddle-ball鎖定
        self.paddle.ball = None
        # 進入主迴圈
        self.game_loop()

    # 主迴圈
    def game_loop(self):
        # 碰撞檢查
        self.check_collisions()
        # 檢查剩餘方塊
        num_bricks = len(self.canvas.find_withtag('brick'))
        # 檢查勝利條件
        if num_bricks == 0:
            self.ball.speed = None
            self.draw_text(300, 200, 'You win!')
        # 球落地檢查
        elif self.ball.get_position()[3] >= self.height:
            self.ball.speed = None
            self.lives -= 1
            # 遊戲失敗檢查
            if self.lives < 0:
                self.draw_text(300, 200, 'Game Over')
            else:
                self.after(1000, self.setup_game)
        else:
            self.ball.update()
            self.after(50, self.game_loop)

    # 碰撞檢查
    def check_collisions(self):
        ball_coords = self.ball.get_position()
        items = self.canvas.find_overlapping(*ball_coords)
        objects = [self.items[x] for x in items if x in self.items]
        self.ball.collide(objects)
        
# 物件父型態
class GameObject(object):
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    # 取得位置
    def get_position(self):
        return self.canvas.coords(self.item)
    
    # 移動物件
    def move(self, x, y):
        self.canvas.move(self.item, x, y)
    
    # 刪除物件
    def delete(self):
        self.canvas.delete(self.item)

# 定義類別 Ball
class Ball(GameObject):
    def __init__(self, canvas, x, y):
        # 球半徑
        self.radius = 10
        # 初始動量
        self.direction = [1, -1]
        # 球速度
        self.speed = 10
        item = canvas.create_oval(x-self.radius, y-self.radius,
                                  x+self.radius, y+self.radius,
                                  fill='white')
        super(Ball, self).__init__(canvas, item)

    # 附邊界檢查的位置更新
    def update(self):
        '''
        TODO
        使用 .get_positio() 取得球座標
        了解 get_positio() 回傳值分別代表的意義
        使用 .canvas.winfo_width() 取得畫布寬度
        對球的位置作邊界檢查

        若遇左右邊界將x方向動量反轉
        若遇上邊界將y方向動量反轉

        調用.move使球移動 (動量*速度) 單位
        '''

    # 碰撞處理
    def collide(self, game_objects):
        coords = self.get_position()
        x = (coords[0]+coords[2])*0.5
        if len(game_objects) > 1:
            self.direction[1] *= -1
        elif len(game_objects) == 1:
            game_object = game_objects[0]
            coords = game_object.get_position()
            if x > coords[2]:
                self.direction[0] = 1
            elif x < coords[0]:
                self.direction[0] = -1
            else:
                self.direction[1] *= -1
        for game_object in game_objects:
            if isinstance(game_object, Brick):
                game_object.hit()

# 定義類別 Paddle
class Paddle(GameObject):
    def __init__(self, canvas, x, y):
        # 寬
        self.width = 80
        # 高
        self.height = 10
        # 上方的球
        self.ball = None
        item = canvas.create_rectangle(x-self.width/2, y-self.height/2,
                                       x+self.width/2, y+self.height/2,
                                       fill='blue')
        super(Paddle, self).__init__(canvas, item)

    def set_ball(self, ball):
        self.ball = ball

    # 移動
    def move(self, offset):
        '''
        TODO
        使用 .get_positio() 取得滑桿座標
        了解 get_positio() 回傳值分別代表的意義
        使用 .canvas.winfo_width() 取得畫布寬度
        對滑桿的移動作邊界檢查

        了解調用父類別中同名(.move)的方法
        如果滑桿對球仍有參考(.ball 非 None)
        '''

class Brick(GameObject):
    # 以Brick.COLORS[剩餘碰撞次數]調用該磚塊顏色
    COLORS = {1: '#999999', 2: '#555555', 3: '#222222'}

    def __init__(self, canvas, x, y, hits):
        # 磚塊寬
        self.width = 75
        # 磚塊高
        self.height = 20
        # 磚塊的剩餘碰撞次數
        self.hits = hits
        # 磚塊顏色
        color = Brick.COLORS[hits]
        item = canvas.create_rectangle(x-self.width/2, y-self.height/2,
                                       x+self.width/2, y+self.height/2,
                                       fill=color,
                                       tag='brick')
        super(Brick, self).__init__(canvas, item)    

    # 磚塊被碰撞處理
    def hit(self):
        '''
        TODO
        將自身剩餘碰撞次數減一
        如果剩餘碰撞次數為0則調用self.delete刪除該磚塊
        否則調用self.canvas.itemconfig(self.item, fill=?)改變磚塊顏色
        '''
    

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Hello, Pong!')
    game = Game(root)
    game.mainloop()
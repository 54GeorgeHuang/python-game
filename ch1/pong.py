import tkinter as tk
from GameObject import Ball, Paddle, Brick


# Game類別宣告
class Game(tk.Frame):
	# 物件建構子
	def __init__(self, master):
		# 畫框初始化
		super(Game, self).__init__(master)
		self.width = 910
		self.height = 600
		self.canvas = tk.Canvas(self, bg='#aaaaff', width=self.width, height=self.height)
		self.canvas.pack()
		self.pack()

		#遊戲初始化
		self.lives = 3
		self.ball = None
		self.paddleSpeed = 30
		self.paddle = Paddle(self.canvas, self.width/2, self.height-40)

		# items 用來存可和球碰撞的物件，後面會用到
		self.items = {}
		self.items[self.paddle.item] = self.paddle
		for x in range(5, self.width - 5, 75):
			self.add_brick(x+37.5, 50, 3)
			self.add_brick(x+37.5, 70, 2)
			self.add_brick(x+37.5, 90, 1)

		self.hud = None
		self.setup_game()
		self.canvas.focus_set()
		self.canvas.bind('<Left>', lambda _: self.paddle.move(-1*self.paddleSpeed))
		self.canvas.bind('<Right>', lambda _: self.paddle.move(self.paddleSpeed))


	# 建立積木
	def add_brick(self, x, y, hits):
		brick = Brick(self.canvas, x, y, hits)
		self.items[brick.item] = brick


	# 遊戲進入預備狀態
	def setup_game(self):
		self.add_ball()
		self.update_lives_text()
		self.text = self.draw_text(self.width/2, self.height/2, 'Press Space to start')
		self.canvas.bind('<space>', lambda _: self.start_game())


	# 建立球
	def add_ball(self):

		# 刪除舊的球
		if self.ball is not None:
			self.ball.delete()

		# 放球在板子上
		paddle_coords = self.paddle.get_position()
		x = (paddle_coords[0] + paddle_coords[2]) * 0.5
		y = (paddle_coords[1] + paddle_coords[3]) * 0.5 - 26
		self.ball = Ball(self.canvas, x, y)
		self.paddle.set_ball(self.ball)


	# 印出訊息
	def draw_text(self, x, y, text, size='60'):
		font = ('Helvetica', size)
		return self.canvas.create_text(x, y, text=text, font=font)


	# 生命顯示及更新
	def update_lives_text(self):
		text = 'Lives: %s' % self.lives
		if self.hud is None:
			self.hud = self.draw_text(50, 20, text, 15)
		else:
			self.canvas.itemconfig(self.hud, text=text)


	# 遊戲開始
	def start_game(self):
		self.canvas.unbind('<space>')
		self.canvas.delete(self.text)
		self.paddle.ball = None
		self.game_loop()


	# 遊戲主迴圈
	def game_loop(self):
		# 檢查碰撞
		self.check_collisions()
		
		# 檢查是否勝利
		num_bricks = len(self.canvas.find_withtag('brick'))
		if num_bricks == 0:
			self.ball.speed = None
			self.draw_text(self.width/2, self.height/2, 'You win!')
		
		# 檢查是否漏球
		elif self.ball.get_position()[3] >= self.height:
			self.ball.speed = None
			self.lives -= 1

			# 沒命就結束，否則再發球
			if self.lives < 0:
				self.draw_text(self.width/2, self.height/2, 'Game Over')
			else:
				self.after(500, self.setup_game)
		
		# 若以上皆沒發生，球移動，並再呼叫主迴圈
		else:
			self.ball.update()
			self.after(50, self.game_loop)


	# 碰撞檢查
	def check_collisions(self):
		ball_coords = self.ball.get_position()

		# 找和球重疊的物件
		items = self.canvas.find_overlapping(*ball_coords)

		# 以上物件若能和球碰撞，則呼叫碰撞方法
		objects = []
		for x in items:
			if x in self.items:
				objects.append(self.items[x])
		self.ball.collide(objects)


# main
if __name__ == '__main__':
	root = tk.Tk()
	root.title('Hello, Pong!')
	game = Game(root)
	game.mainloop()
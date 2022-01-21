# 基本遊戲類別宣告
class GameObject(object):
	def __init__(self, canvas, item):
		self.canvas = canvas
		self.item = item

	# 取得物件位置
	def get_position(self):
		return self.canvas.coords(self.item)

	# 移動物件
	def move(self, x, y):
		self.canvas.move(self.item, x, y)

	# 刪除物件
	def delete(self):
		self.canvas.delete(self.item)



# 球類別宣告
class Ball(GameObject):
	# 球基本性質設定
	def __init__(self, canvas, x, y):
		self.radius = 15
		self.direction = [1, -1]
		self.speed = 15
		item = canvas.create_oval(x-self.radius, y-self.radius, x+self.radius, y+self.radius, fill='white')
		super(Ball, self).__init__(canvas, item)


	# 球邊界反彈偵測及位置更新
	def update(self):
		coords = self.get_position()
		width = self.canvas.winfo_width()
		# 得到新方向
		if coords[0] <= 0 or coords[2] >= width:
			self.direction[0] *= -1
		if coords[1] <= 0:
			self.direction[1] *= -1
		# 計算移動距離
		x = self.direction[0] * self.speed
		y = self.direction[1] * self.speed
		# 移動
		self.move(x, y)


	# 球碰撞
	def collide(self, game_objects):
		coords = self.get_position()
		x = (coords[0] + coords[2]) * 0.5

		# 若撞兩個以上積木，直接垂直反彈
		if len(game_objects) > 1:
			self.direction[1] *= -1
		
		# 若撞一個，要計算如何反彈
		elif len(game_objects) == 1:
			game_object = game_objects[0]
			coords = game_object.get_position()
			# 撞到右邊，水平反彈
			if x > coords[2]:
				self.direction[0] = 1
			# 撞到左邊，水平反彈
			elif x < coords[0]:
				self.direction[0] = -1
			# 撞到上下，垂直反彈
			else:
				self.direction[1] *= -1

		# 若積木被撞到，則呼叫方法
		for game_object in game_objects:
			if isinstance(game_object, Brick):
				game_object.hit()



# 木板類別宣告
class Paddle(GameObject):
	# 木板基本性質設定
	def __init__(self, canvas, x, y):
		self.width = 200
		self.height = 20
		self.ball = None
		item = canvas.create_rectangle(x - self.width/2, y - self.height/2, x + self.width/2, y + self.height/2, fill='blue')
		super(Paddle, self).__init__(canvas, item)

	# 是否與球連結設定（一起移動）
	def set_ball(self, ball):
		self.ball = ball

	# 移動
	def move(self, offset):
		coords = self.get_position()
		width = self.canvas.winfo_width()
		if coords[0] + offset >= 0 and coords[2] + offset <= width:
			super(Paddle, self).move(offset, 0)
			if self.ball is not None:
				self.ball.move(offset, 0)



# 積木類別設定
class Brick(GameObject):
	COLORS = {1: '#999999', 2:'#555555', 3:'#222222'}

	# 積木基本性質設定
	def __init__(self, canvas, x, y, hits):
		self.width = 75
		self.height = 20
		self.hits = hits
		color = Brick.COLORS[hits]
		item = canvas.create_rectangle(x - self.width/2, y - self.height/2, x + self.width/2, y + self.height/2, fill=color, tags='brick')
		super(Brick, self).__init__(canvas, item)
	# 積木被打到，更新積木
	def hit(self):
		self.hits -= 1
		if self.hits == 0:
			self.delete()
		else:
			self.canvas.itemconfig(self.item, fill=Brick.COLORS[self.hits])

import cocos

class MainLayer(cocos.layer.Layer):
	def __init__(self):
		super(MainLayer, self).__init__()
		self.player = cocos.sprite.Sprite("ball.png")
		self.player.color = (0, 0, 255)
		self.player.position = (320, 400)
		self.add(self.player)

if __name__ == "__main__":
	cocos.director.director.init(caption="Hellos, Cocos")
	layer = MainLayer()
	scene = cocos.scene.Scene(layer)
	cocos.director.director.run(scene)
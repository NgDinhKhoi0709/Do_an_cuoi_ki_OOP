class Button():
	"""
    Lớp Button đại diện cho một nút bấm tương tác trên giao diện người dùng trong trò chơi.
    Lớp này cung cấp các phương thức để hiển thị nút, kiểm tra sự tương tác của người dùng,
    và thay đổi màu sắc của văn bản khi di chuột qua nút.
	"""
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		"""
        Thiết lập các thuộc tính ban đầu cho nút bấm, bao gồm hình ảnh, vị trí, văn bản, màu sắc, và font chữ.
        Args:
            image (pygame.Surface): Hình ảnh của nút. Nếu None, sử dụng văn bản làm nút.
            pos (tuple): Tọa độ (x, y) của nút trên màn hình.
            text_input (str): Văn bản hiển thị trên nút.
            font (pygame.font.Font): Font chữ dùng để hiển thị văn bản trên nút.
            base_color (tuple): Màu sắc cơ bản của văn bản.
            hovering_color (tuple): Màu sắc của văn bản khi di chuột qua nút.
        """
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		"""
        Hiển thị nút và văn bản của nó lên màn hình.
        Nếu nút có hình ảnh, hiển thị hình ảnh đó. Nếu không, chỉ hiển thị văn bản.
        Args:
            screen (pygame.Surface): Bề mặt màn hình để hiển thị nút.
        """
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		"""
        Kiểm tra xem vị trí của con trỏ chuột có nằm trong vùng của nút không.
        Args:
            position (tuple): Vị trí (x, y) của con trỏ chuột trên màn hình.
        Returns:
            bool: True nếu vị trí của con trỏ chuột nằm trong vùng của nút, False nếu không.
        """
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		"""
        Thay đổi màu sắc của văn bản khi di chuột qua nút.
        Nếu con trỏ chuột nằm trong vùng của nút, văn bản sẽ đổi sang màu `hovering_color`.
        Nếu không, văn bản sẽ có màu `base_color`.
        Args:
            position (tuple): Vị trí (x, y) của con trỏ chuột trên màn hình.
        """
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)
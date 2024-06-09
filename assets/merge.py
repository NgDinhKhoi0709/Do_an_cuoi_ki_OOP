from PIL import Image

idle = Image.open("assets/images/hero/Sprites/Idle.png")
run = Image.open("assets/images/hero/Sprites/Run.png")
jump = Image.open("assets/images/hero/Sprites/Jump.png")
attack_1 = Image.open("assets/images/hero/Sprites/Attack1.png")
attack_2 = Image.open("assets/images/hero/Sprites/Attack2.png")
hit = Image.open("assets/images/hero/Sprites/Take Hit.png")
death = Image.open("assets/images/hero/Sprites/Death.png")
sprite_sheet = [idle, run, jump, attack_1, attack_2, hit, death]

sprite_width = 126
sprite_height = 126

columns = 11
rows = 7

result_width = sprite_width * columns
result_height = sprite_height * rows
result_image = Image.new("RGBA", (result_width, result_height))

for row in range(rows):
    if row < len(sprite_sheet): 
        for col in range(columns):
            box = (col * sprite_width, 0, (col + 1) * sprite_width, sprite_height)
            sprite = sprite_sheet[row].crop(box)
            position = (col * sprite_width, row * sprite_height)
            result_image.paste(sprite, position)
    else:
        break 

result_path = "assets/images/hero/Sprites/hero.png"
result_image.save(result_path)
result_image.show()

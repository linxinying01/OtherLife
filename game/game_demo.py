import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

x, y = 400, 300
speed_x = 5
speed_y = 5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 更新位置
    x += speed_x
    y += speed_y
    
    # 边界检测
    if x < 0 or x > 750:
        speed_x = -speed_x
    if y < 0 or y > 550:
        speed_y = -speed_y
        
    # 绘制
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 50, 50))
    pygame.display.flip()
    clock.tick(60) # 设置帧率为60 FPS

pygame.quit()
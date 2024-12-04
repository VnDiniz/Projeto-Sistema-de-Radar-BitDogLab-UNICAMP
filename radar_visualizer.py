import pygame
import serial
import math
import time

# Configurações da tela
WIDTH, HEIGHT = 1200, 800  # Tela duplicada
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2 + 200  # Centro ajustado
MAX_DISTANCE = 20  # Distância máxima do sensor HC-SR04 (20 cm)
RADAR_RADIUS = 500  # Raio duplicado
POINT_LIFETIME = 0.3  # Tempo que cada ponto permanece na tela (em segundos)
SWEEP_WIDTH = 4  # Largura da linha de varredura do radar

# Inicializa o pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Radar")
clock = pygame.time.Clock()

# Configuração da comunicação serial
serial_port = serial.Serial('COM4', 115200)

# Fonte para o texto
font = pygame.font.SysFont('Arial', 40)  # Fonte maior

# Lista para armazenar as últimas 10 medições
points = []

def draw_radar(sweep_angle, current_angle, current_distance):
    # Limpa a tela
    screen.fill((0, 0, 0))
    
    # Desenha o semicirculo do radar (ângulo de 0° a 180°)
    pygame.draw.arc(screen, (0, 100, 0), (CENTER_X - RADAR_RADIUS, CENTER_Y - RADAR_RADIUS, RADAR_RADIUS * 2, RADAR_RADIUS * 2), 0, math.pi, 4)

    # Desenha os semicirculos de distâncias (0cm, 5cm, 10cm, 15cm, 20cm)
    for i in range(0, MAX_DISTANCE + 1, 5):
        scaled_radius = (i / MAX_DISTANCE) * RADAR_RADIUS
        pygame.draw.arc(screen, (0, 100, 0), (CENTER_X - scaled_radius, CENTER_Y - scaled_radius, scaled_radius * 2, scaled_radius * 2), 0, math.pi, 2)

        # Posiciona os rótulos de distância fora do semicirculo, abaixo da borda direita
        if i > 0:
            distance_text = font.render(f"{i}cm", True, (255, 255, 255))
            text_rect = distance_text.get_rect(center=(CENTER_X + scaled_radius, CENTER_Y + 50))  # Abaixo do semicirculo
            screen.blit(distance_text, text_rect)

    # Desenha as linhas de referência do semicirculo superior e rótulos de ângulo
    for i in range(0, 181, 30):
        radians = math.radians(i)
        end_x = CENTER_X + RADAR_RADIUS * math.cos(radians)
        end_y = CENTER_Y - RADAR_RADIUS * math.sin(radians)
        pygame.draw.line(screen, (0, 100, 0), (CENTER_X, CENTER_Y), (end_x, end_y), 2)
        
        # Aumenta a distância para os rótulos
        label_distance = RADAR_RADIUS + 40  # Ajusta para a escala maior
        label_x = CENTER_X + label_distance * math.cos(radians)
        label_y = CENTER_Y - label_distance * math.sin(radians)
        
        # Desenha o texto para os ângulos
        angle_text = font.render(f"{i}°", True, (255, 255, 255))
        text_rect = angle_text.get_rect(center=(label_x, label_y))
        screen.blit(angle_text, text_rect)

    # Desenha as últimas 10 medições com transparência crescente
    for idx, (angle, distance, _) in enumerate(points):
        alpha = int(255 * ((idx + 1) / len(points)))  # Calcula a transparência (mais antigo, mais transparente)
        color = (0, 255, 0, alpha)

        # Cria uma surface temporária para desenhar com alpha
        radar_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        # Desenha a linha de varredura
        radians = math.radians(angle)
        end_x = CENTER_X + RADAR_RADIUS * math.cos(radians)
        end_y = CENTER_Y - RADAR_RADIUS * math.sin(radians)
        pygame.draw.line(radar_surface, color, (CENTER_X, CENTER_Y), (end_x, end_y), SWEEP_WIDTH)

        # Desenha o ponto correspondente à distância
        if distance <= MAX_DISTANCE:
            scaled_distance = (distance / MAX_DISTANCE) * RADAR_RADIUS
            point_x = CENTER_X + scaled_distance * math.cos(radians)
            point_y = CENTER_Y - scaled_distance * math.sin(radians)
            pygame.draw.circle(radar_surface, (255, 0, 0, alpha), (int(point_x), int(point_y)), 10)

        # Blita a surface com transparência
        screen.blit(radar_surface, (0, 0))

    # Exibe o ângulo e a distância atuais na parte inferior
    angle_text = font.render(f"Ângulo: {current_angle:.1f}°", True, (255, 255, 255))
    distance_text = font.render(f"Distância: {current_distance:.2f} cm" if current_distance <= MAX_DISTANCE else "---", True, (255, 255, 255))
    
    screen.blit(angle_text, (40, HEIGHT - 120))
    screen.blit(distance_text, (40, HEIGHT - 60))

def main():
    running = True
    sweep_angle = 0  # Ângulo de varredura do radar
    current_angle = 0  # Armazenar o último ângulo lido
    current_distance = 0  # Armazenar a última distância lida

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Recebe os dados via serial
        if serial_port.in_waiting > 0:
            try:
                data = serial_port.readline().decode('utf-8').strip()

                if data:  # Verifica se a linha não está vazia
                    print("Dados recebidos:", data)
                    current_angle, current_distance = map(float, data.split(','))

                    # Atualiza o ângulo de varredura com o valor recebido
                    sweep_angle = current_angle

                    # Adiciona o ponto à lista com o timestamp atual
                    points.append((current_angle, current_distance, time.time()))

                    # Limita a lista às últimas 10 medições
                    if len(points) > 10:
                        points.pop(0)

                    draw_radar(sweep_angle, current_angle, current_distance)
                else:
                    print("Linha vazia recebida, ignorada.")

            except Exception as e:
                print(f"Erro ao processar dados: {e}")

        # Desenha o radar com a linha de varredura no ângulo atual
        draw_radar(sweep_angle, current_angle, current_distance)

        # Atualiza a tela
        pygame.display.flip()
        clock.tick(60)  # FPS

    # Fecha a comunicação serial e pygame
    serial_port.close()
    pygame.quit()

if __name__ == "__main__":
    main()
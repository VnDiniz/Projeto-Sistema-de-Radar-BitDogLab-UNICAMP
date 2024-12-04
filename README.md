# Sistema de Radar na BitDogLab

Este projeto foi desenvolvido durante a disciplina EA076 - Laboratório de Sistemas Embarcados da UNICAMP pelo Vinicius Diniz Reolon e Thiago Masanori Hata, e tem como objetivo simular um Sistema de Radar, através da placa BitDogLab. Ele utiliza um sensor ultrassônico **HC-SR04** montado sobre um microservo **SG90** para realizar varreduras de 0 a 180 graus, capturando distâncias de objetos em até 20 cm. Os dados são enviados para um computador via serial, onde um programa em **Python** plota as medições em tempo real em um radar gráfico.

<img src="https://i.ibb.co/CbpFyY2/Projeto-Sistema-de-Radar.jpg" alt="Projeto Sistema de Radar" width="950">

---

## 💻 **Como Usar**
1. Clone o repositório:
   ```bash
   git clone https://github.com/VnDiniz/Projeto-Sistema-de-Radar-BitDogLab-UNICAMP.git

2. Configure os componentes:
  - Conecte o hardware conforme indicado na seção de montagem.
  - Certifique-se de que a placa está configurada com o firmware MicroPython.

3. Carregue o código na placa:
  - Abra o código no Thonny IDE.
  - Faça o upload para a BitDogLab.

4. Execute o código do radar:
  - Execute o código para plotar o radar no computador.

---

## ⚙️ **Componentes Utilizados**
- **BitDogLab (RP2040)**: Placa base para o projeto.
- **HC-SR04**: Sensor ultrassônico para medir distâncias.
- **SG90**: Microservo para movimentação do sensor.
- **OLED SSD1306**: Display para exibir os dados de ângulo e distância.
- **Buzzer**: Para sinalização sonora proporcional à distância.
- **Matriz de LEDs (opcional)**: Para futuras implementações de visualização.

---

## 🛠️ **Montagem**
1. Conecte o sensor ultrassônico **HC-SR04** no servo SG90.
2. Conecte os pinos do HC-SR04:
   - **Trigger**: Pino 17  _(GPIO17)_.
   - **Echo**: Pino 16  _(GPIO16)_.
3. Conecte o servo SG90 no pino **10 (PWM)**  _(GPIO10)_.
4. Conecte o display OLED aos pinos:
   - **SCL**: Pino 15  _(padrão BitDogLab)_.
   - **SDA**: Pino 14  _(padrão BitDogLab)_.
5. Conecte o buzzer no pino **21**  _(padrão BitDogLab)_.
6. (Opcional) Conecte a matriz de LEDs ao pino **7**  _(padrão BitDogLab)_.

---

## 💻 **Código MicroPython (BitDogLab)**
O código para o microcontrolador movimenta o micro servo de 0° a 180°, captura as medições de distância do sensor e envia os dados via serial para o computador. Certifique-se de configurar corretamente os pinos de acordo com o hardware conectado.<br/><br/>
_Obs: lembre-se de salvar o código na placa com o nome main.py e depois fechar o Thonny, para liberar o barramento Serial para o código da visualização gráfica._

### **Saída Serial**
Os dados são enviados no formato:
ângulo,distância

Exemplo:
45,10.35

---

## 🖥️ **Visualização Gráfica com Python**
Um programa em **Python** utiliza os dados recebidos via serial para plotar as medições em um radar gráfico.

### **Requisitos**
- **Bibliotecas Python**:
  - `pygame`
  - `serial`
  - `math`
  - `time`
- **Configuração da Porta Serial**:
  - Certifique-se de alterar `'COM4'` no código para a porta serial utilizada pelo microcontrolador.

### **Código Python**
O código está disponível no repositório e permite:
- Exibir o radar em um painel gráfico interativo.
- Mostrar os ângulos e distâncias atuais em tempo real.
- Atualizar dinamicamente os pontos no radar, com persistência limitada para destacar medições recentes.

### **Execução**
1. Instale as dependências necessárias usando:
   ```bash
   pip install pygame pyserial
2. Execute o código com:
   ```bash
   python radar_visualizer.py
3. Certifique-se de que o microcontrolador está conectado e enviando dados via serial.

---

   ## 📋 **Detalhes do Radar Gráfico**
- **Tela**: 1200x800 pixels.
- **Raio do Radar**: 500 pixels.
- **Distância Máxima**: 20 cm (escalada para o gráfico).
- **Persistência de Ponto**: 10 medições recentes com transparência crescente.

---

## 💭 **Futuras Implementações**
- Melhorar a visualização gráfica com novas opções de cores e temas.
- Adicionar suporte para salvar os dados do radar em um arquivo para análises posteriores.
- Implementar visualização em tempo real na matriz de LEDs.

---

## 🤝 **Contribuições**
Contribuições são bem-vindas!<br/>
Caso tenha dúvidas ou sugestões, entre em contato através da aba Issues ou diretamente pelo e-mail: vini_reolon@hotmail.com.

---

🚀 Divirta-se explorando a BitDogLab com este projeto!
   

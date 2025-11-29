# 📱Projeto FlexIA Connect: Concepção e Arquitetura

---

## 💡 1. Resumo da Ideia (Visão Geral)

O **Projeto FlexIA Connect** propõe o desenvolvimento de um **totem interativo com inteligência artificial**, a ser instalado em locais de visitação educativa e cultural.

### 🎯 Objetivo
Oferecer uma experiência **inovadora, inclusiva e divertida** aos visitantes, promovendo a **personalização** e enriquecendo a interação dos usuários. O sistema deve funcionar de forma **autônoma**, reduzindo a necessidade de equipes presenciais.

### 🧩 Problema que resolve
O projeto aborda o desafio de **criar soluções digitais inteligentes** para experiências interativas em espaços culturais e de lazer, auxiliando na:
- Engajamento de visitantes;  
- Coleta de dados relevantes;  
- Oferecimento de experiências digitais diferenciadas.

---

## 💥 2. Justificativa

A solução se insere no contexto da **Flexmedia**, empresa que busca transformar espaços físicos em **ambientes inteligentes** com uso de **IA, sensores e sistemas em nuvem**.  
A Flexmedia atua em **Segurança, Automação, Broadcast, Telecom** e **ITS (Intelligent Transport System)**.

### 🚀 Valor do Projeto

O Totem IA Connect é **flexível e escalável**, podendo ser oferecido como **produto white label** a outros clientes.

#### Benefícios:
- **Customização e Integração:** Suporte a diferentes APIs (tradução, reconhecimento de imagem, analytics).  
- **Gestão Centralizada:** Backend multi-institucional (museus, parques, aquários).  
- **Melhoria Contínua:** Coleta e análise de dados em tempo real.

---

## 🏠 3. Arquitetura da Solução

A arquitetura técnica abrange **hardware, software e nuvem**, detalhando o fluxo de dados e a interconexão dos componentes.

| **Componente** | **Detalhe da Arquitetura** |
|----------------|-----------------------------|
| **Hardware / Sensores** | Uso de **ESP32 e/ou ESP32-CAM**, microcontroladores econômicos e eficientes para coleta de dados na borda. Inclui sensores de presença ou toque. |
| **Comunicação de Borda** | Protocolo **MQTT (Message Queuing Telemetry Transport)** para transmissão leve de dados de telemetria para a nuvem. |
| **Infraestrutura de Nuvem (Cloud)** | **Google Cloud Platform (GCP)**: uso de **IoT Core** e **Cloud Functions** para gerenciamento de IoT e processamento inicial. |
| **Módulos de IA/ML** | Integração com **GCP Vertex AI** e **APIs prontas** (Google Vision, Google Translate) para reconhecimento de imagem e tradução. |
| **Armazenamento de Dados** | **BigQuery** para telemetria e métricas de uso; **Firestore (NoSQL)** para conteúdo e perfis de usuário. |
| **Saídas/Funcionalidades** | Comunicação via **voz e/ou texto**, com filtro de ruído, geração de **áudio, legendas, quizzes e fotos com AR**. |

---

## ⚙️ 4. Tecnologias Utilizadas

Toolkit técnico priorizando **integração** e **Machine Learning**.

| **Categoria** | **Tecnologia/Serviço** | **Justificativa da Escolha (Baseado no Toolkit)** |
|----------------|-------------------------|--------------------------------------------------|
| **Hardware e IoT** | ESP32 e/ou ESP32-CAM | Microcontroladores econômicos e eficientes, ideais para coleta de dados na borda e uso de sensores/câmeras. |
| **Linguagem (Backend/ML)** | Python | Ideal para backend, APIs e modelos de ML, devido à ampla biblioteca e suporte. |
| **Linguagem (Firmware)** | C/C++ | Necessário para o desenvolvimento eficiente de firmware em microcontroladores. |
| **Comunicação** | MQTT | Protocolo leve e eficiente para telemetria e comunicação entre borda e nuvem. |
| **Infraestrutura de Nuvem** | Google Cloud Platform (IoT Core, Cloud Functions) | Gerenciamento de IoT e microserviços serverless para ingestão e processamento inicial. |
| **Plataforma IA/ML** | GCP Vertex AI / APIs de IA prontas | Vertex AI para modelos customizados; APIs prontas garantem funcionalidades como tradução e reconhecimento. |
| **Visualização/Analytics** | Looker Studio (ou similar) | Dashboards em nuvem para análise de dados e métricas de engajamento. |

### 📈 Diagrama da Arquitetura

![alt text](https://flexai-connect-flow.edgeone.app/arquitetura-diagrama.png)

---

## 🏦 5. Estratégia de Coleta de Dados

O sistema coleta informações para medir o engajamento e fornecer **analytics** aos clientes.

### 📊 Tipos de Dados
- **Métricas de Uso:** Interações, perguntas mais feitas, idiomas utilizados.  
- **Dados do Usuário:** Perfil e preferências.  
- **Feedback:** Avaliação da experiência pelo visitante.

### ⚙️ Fontes e Método de Coleta
- **Fontes:** Sensores (presença, toque, câmeras) e interação por voz ou toque.  
- **Método:** Coleta na borda com ESP32.  
- **Ingestão/Processamento:** Dados transmitidos via **MQTT** → processados pelo **GCP Cloud Functions**.  
- **Armazenamento:**  
  - Telemetria e métricas → **BigQuery**  
  - Conteúdo e perfis → **Firestore (NoSQL)**  
- **Feedback:** QR Code no totem para salvar informações ou fornecer avaliação em tempo real.

---

## 🧑‍💻 6. Plano de Desenvolvimento

### 🏁 Etapas Iniciais (Sprint 1)
1. Definição do escopo e justificativa.  
2. Estruturação da arquitetura técnica (hardware, software, nuvem).  
3. Escolha das tecnologias e justificativas.  
4. Estratégia de coleta de dados (simulada ou planejada).  
5. Plano inicial de desenvolvimento e divisão de responsabilidades.  

### 🔄 Próximas Etapas (Pós-Sprint 1)
- **MVP:** Desenvolvimento da funcionalidade central.  
- **Customização:** Personalização visual para diferentes clientes.  
- **Atualizações de Conteúdo:** Suporte a atualizações periódicas.  
- **Escalabilidade:** Suporte a múltiplos totens em diferentes locais.

### 👥 Distribuição de Tarefas

#### 1. **Jonatan Viotti / Gabriel Oliveira (Conceituação, Toolkit e Gestão do Repositório)**
Jonatan será o responsável por garantir que a proposta seja bem apresentada e que o ambiente de entrega esteja impecável.  
- **Conceituação:** Elaboração do título do projeto e redação do resumo da ideia (*O que é? Para que serve? Qual problema resolve?*).  
- **Justificativa:** Redação da justificativa, demonstrando a relevância da solução para a **FlexMedia**.  
- **Tecnologias Utilizadas:** Listagem e justificativa do toolkit técnico (linguagens de programação, frameworks, bibliotecas de IA).  

---

#### 2. **Arthur Bruttel (Camada de Borda e Telemetria)**
Arthur focará na definição da interface física e nos mecanismos de coleta de dados brutos.  
- **Definição de Hardware:** Detalhamento da camada de borda, especificando o uso de **ESP32 e/ou ESP32-CAM**, sensores de presença e displays.  
- **Integração ao Ambiente:** Definição de como o totem se integrará ao ambiente (interação por voz ou toque).  
- **Estratégia de Coleta de Telemetria:** Definição dos tipos de dados (métricas de engajamento) e fontes primárias de dados gerados pelos sensores.

---

#### 3. **Gabriel Oliveira / Samuel Rocha (Infraestrutura e Serviços de Nuvem)**
Gabriel será o responsável por estruturar a arquitetura na nuvem e os serviços de integração, um requisito crucial para a solução.  
- **Infraestrutura de Nuvem:** Seleção e justificativa dos serviços em **cloud computing** (GCP, AWS ou Azure), com foco em ingestão, processamento e deployment.  
- **Diagrama de Arquitetura:** Criação do esboço da arquitetura da solução (diagrama), ilustrando o fluxo de dados entre hardware, cloud e APIs.  
- **APIs e Serviços:** Definição das APIs e serviços de integração necessários para o dashboard.

---

#### 4. **Samuel Rocha / Roberson Pedrosa (IA/ML, Dados e Processamento)**
Samuel focará na inteligência da solução e na gestão dos dados.  
- **Modelos de IA/ML:** Proposição e descrição das possibilidades de aplicação de **Machine Learning**, como visão computacional ou análise de padrões.  
- **Estrutura de Dados:** Detalhamento de como os dados serão armazenados (local ou nuvem) e processados (seleção de BigQuery, Firestore etc.).  
- **Método de Coleta:** Explicação da estratégia de coleta de dados (simulada ou planejada), definindo o método de coleta (ex: streaming via **MQTT**).

---

#### 5. **Roberson Pedrosa / Jonatan Viotti (Gestão, Segurança e Privacidade)**
Roberson será responsável por garantir a coerência do plano de desenvolvimento e tratar dos aspectos críticos de segurança e ética.  
- **Plano de Desenvolvimento:** Elaboração das etapas do projeto (ciclo de vida) e do cronograma simplificado.  
- **Divisão de Tarefas:** Finalização do item “Plano inicial de desenvolvimento e divisão de responsabilidades.”  
- **Segurança e Privacidade:** Definição das estratégias para proteger dados sensíveis (**criptografia, anonimização, controle de acesso**) e garantia da ética em IA (**evitando vieses**).


---

## 🔒 7. Segurança e Privacidade

A **segurança da informação** e a **privacidade dos usuários** são requisitos cruciais para o projeto **FlexIA Connect**. A solução foi planejada para proteger dados sensíveis, garantir conformidade com boas práticas de segurança e ética em IA.

### 🛡️ Estratégia de Segurança

| **Estratégia** | **Descrição e Cuidado** |
|----------------|-------------------------|
| **Proteção de Dados** | **Criptografia:** Implementação de **SSL/TLS** para dados em trânsito e criptografia de disco para dados em repouso, protegendo informações sensíveis armazenadas no **BigQuery** e **Firestore**. |
| **Anonimização e Privacidade** | Os dados de perfil coletados pela **ESP32-CAM** serão **anonimizados ou pseudonimizados** imediatamente após a inferência na **Cloud Function**, removendo identificadores pessoais. |
| **Controle de Acesso** | Implementação de **IAM (Identity and Access Management)** no GCP para garantir que apenas usuários autorizados (membros da **FlexMedia** ou clientes específicos) tenham acesso a dashboards e APIs. |
| **Ética em IA** | Realização de **auditorias regulares dos modelos de IA** para evitar vieses (*Bias Avoidance*) na classificação e recomendação, garantindo que a personalização seja **justa e transparente** para todos os perfis de usuários. |

### 🔑 Considerações Finais
- A proteção de dados é tratada de forma **holística**, cobrindo desde a coleta na borda até o armazenamento e processamento na nuvem.  
- A ética em IA é um pilar do projeto, assegurando que a personalização das interações seja segura, inclusiva e responsável.  
- A combinação de criptografia, anonimização e controle de acesso garante **confiança e conformidade**, fortalecendo a reputação da FlexMedia no fornecimento de soluções inovadoras e seguras.


---

## 🧭 Conclusão

O **Totem IA Connect** representa um passo estratégico na transformação de espaços físicos em **ambientes inteligentes**, combinando **IA, IoT, nuvem e interatividade**.  
O projeto visa **potencializar o engajamento**, **melhorar a experiência do visitante** e **gerar valor** tanto para a **Flexmedia** quanto para instituições parceiras.

---
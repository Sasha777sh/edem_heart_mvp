import asyncio
import numpy as np
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import json
import random
from brain import EDEMBrain

# --- ЯДРО: LIVING NEURON ---
class LivingNeuron:
    def __init__(self, name="HeartScaler", target_freq=0.1, buffer_size=64):
        self.name = name
        self.target_freq = target_freq
        self.buffer_size = buffer_size
        self.energy = 0.1
        self.buffer = np.zeros(buffer_size)
        self.age = 0
        self.activation_threshold = 0.5

    def calculate_physics(self, signal):
        A = np.std(signal) * 2
        if A < 0.01: A = 0.0
        
        t = np.arange(len(signal))
        ref_sin = np.sin(2 * np.pi * self.target_freq * t)
        ref_cos = np.cos(2 * np.pi * self.target_freq * t)
        
        score_sin = np.dot(signal, ref_sin) / len(signal)
        score_cos = np.dot(signal, ref_cos) / len(signal)
        
        power = 2 * np.sqrt(score_sin**2 + score_cos**2)
        total_power = np.std(signal) + 1e-9
        R = np.clip(power / total_power, 0, 1) if total_power > 0.1 else 0
        S = 1.0 - R
        
        E_input = (A * R) - (S * 0.1)
        return E_input, {"A": float(A), "R": float(R), "S": float(S)}

    def breathe(self, input_sample):
        self.buffer = np.roll(self.buffer, -1)
        self.buffer[-1] = input_sample
        self.age += 1
        
        dE, metrics = self.calculate_physics(self.buffer)
        
        self.energy = self.energy * 0.95 + dE * 0.1
        self.energy = np.clip(self.energy, 0.0, 5.0)
        
        # Начисление PULSE
        pulse_gained = 0.0
        if self.energy > 1.0:
            pulse_gained = 0.01 * self.energy 
            
        return {
            "energy": float(self.energy),
            "metrics": metrics,
            "pulse_gained": pulse_gained
        }

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import json
import random
import os
from brain import EDEMBrain

# ... (LivingNeuron class remains same)

# --- SERVER ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store state for each connection
connection_states = {} 

neuron = LivingNeuron()
brain_engine = EDEMBrain()

@app.get("/")
async def get():
    # Read HTML file from frontend directory
    # Adjust path assuming valid pwd or relative structure
    file_path = os.path.join(os.path.dirname(__file__), "../frontend/index.html")
    with open(file_path, "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client connected")
    
    # Init state for this connection
    connection_states[id(websocket)] = {"bpm_avg": None}
    
    total_pulse = 0.0
    
    try:
        while True:
            # Ждем данные
            data = await websocket.receive_text()
            msg = json.loads(data)
            
            signal_input = 0.0
            
            # --- INPUT: AUDIO (Microphone) ---
            if "signal" in msg:
                signal_input = float(msg["signal"]) * 5.0
                if random.random() < 0.01: # Log ~1% of packets
                    print(f"🎤 MIC INPUT: {signal_input:.2f}")
                
            # --- INPUT: POLAR (Heart Rate) ---
            elif "type" in msg and msg["type"] == "biometric":
                bpm = float(msg["bpm"])
                
                # Logic for HRV simulation
                state_store = connection_states[id(websocket)]
                
                if state_store["bpm_avg"] is None:
                     state_store["bpm_avg"] = bpm
                
                # Calculate running average
                state_store["bpm_avg"] = state_store["bpm_avg"] * 0.9 + bpm * 0.1
                
                avg = state_store["bpm_avg"]
                diff = bpm - avg
                
                # SENSITIVITY
                signal_input = diff * 2.0 
                signal_input += np.random.normal(0, 0.2) # Alive noise
                
                # Debug print to prove calculation happens
                # print(f"BPM: {bpm} | AVG: {avg:.1f} | SIG: {signal_input:.2f}")

            # Живой нейрон обрабатывает сигнал
            state = neuron.breathe(signal_input)
            total_pulse += state["pulse_gained"]
            
            # 4. Чат-Логика (Психический Интерфейс)
            if "chat_message" in msg:
                user_text = msg["chat_message"]
                selected_voice = msg.get("selected_voice", "SHADOW") 
                
                # Запрашиваем "Мозг"
                voice_data = brain_engine.get_system_prompt(
                    voice_str=selected_voice,
                    energy=state["energy"], 
                    user_text=user_text
                )
                
                # Генерируем ответ
                response_text = brain_engine.mock_response(voice_data, user_text)
                
                # Отправляем ответ чата
                await websocket.send_json({
                    "type": "chat_response",
                    "voice": voice_data["voice"],
                    "energy_level": voice_data["energy_level"],
                    "text": response_text
                })

            # Отправляем телеметрию
            response = {
                "type": "telemetry",
                "energy": state["energy"],
                "metrics": state["metrics"],
                "total_pulse": total_pulse,
                "debug_signal": signal_input
            }
            
            await websocket.send_json(response)
            
    except Exception as e:
        print(f"Connection closed: {e}")

@app.get("/shadow")
async def get_shadow_reader():
    """Serve the Shadow Reader Mini App"""
    try:
        file_path = os.path.join(os.path.dirname(__file__), "../frontend/shadow_reader.html")
        with open(file_path, "r") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Error: shadow_reader.html not found</h1>", status_code=404)

from pydantic import BaseModel
class ShadowRequest(BaseModel):
    text: str
    context: str = ""

from shadow_reader import ShadowReader
shadow_engine = ShadowReader() # Initialize once

@app.post("/api/shadow_analyze")
async def api_shadow_analyze(req: ShadowRequest):
    """API Endpoint for Shadow Reader analysis"""
    return shadow_engine.analyze_text(req.text, req.context)

if __name__ == "__main__":
    import uvicorn
    # Listen on all interfaces to be accessible
    uvicorn.run(app, host="0.0.0.0", port=8000)
# Force reload for brain updates

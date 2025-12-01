# Arquivo: src/core/schemas.py
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime
from typing import Optional

class InteracaoSchema(BaseModel):
    """
    O Contrato de Dados Oficial da FlexMedia.
    Garante que nada sujo entre no Banco de Dados.
    """
    # Validação de Tipos e Obrigatoriedade
    timestamp: str = Field(..., description="Data hora formatada YYYY-MM-DD HH:MM:SS")
    id_sensor: str = Field(..., min_length=3, description="Identificador do totem")
    
    # Validação de Intervalos (Sanitização)
    tempo_permanencia: float = Field(..., ge=0.0, description="Segundos. Não pode ser negativo.")
    tempo_interacao: float = Field(..., ge=0.0, description="Segundos. Não pode ser negativo.")
    
    tipo_interacao: str = Field(..., description="Classificação (Engajado, Normal, etc)")
    
    # Campos V3 (Opcionais mas validados)
    acao_usuario: str = Field(default="Nenhuma")
    tempo_resposta_ms: int = Field(default=0, ge=0)
    status_sistema: str = Field(default="N/A")

    # --- 1. PADRONIZAÇÃO (Standardization) ---
    @field_validator('id_sensor', 'tipo_interacao', 'status_sistema')
    @classmethod
    def padronizar_textos(cls, v: str) -> str:
        """Garante que IDs e códigos sejam sempre limpos (strip) e capitalizados corretamente."""
        return v.strip()

    @field_validator('tempo_permanencia', 'tempo_interacao')
    @classmethod
    def arredondar_valores(cls, v: float) -> float:
        """Padroniza unidades para 2 casas decimais."""
        return round(v, 2)

    # --- 2. REGRA DE NEGÓCIO (Business Logic) ---
    @model_validator(mode='after')
    def validar_consistencia(self):
        """Validações cruzadas entre campos."""
        # Regra: Tempo de interação nunca pode ser maior que o tempo de permanência
        if self.tempo_interacao > self.tempo_permanencia:
            raise ValueError(f"Inconsistência: Interação ({self.tempo_interacao}s) maior que Permanência ({self.tempo_permanencia}s)")
        
        # Regra: Se interagiu, precisa ter uma classificação válida
        if self.tempo_interacao > 0 and self.tipo_interacao == "N/A":
            self.tipo_interacao = "Desconhecido"
            
        return self

    class Config:
        # Permite converter automaticamente objetos ORM se precisarmos no futuro
        from_attributes = True
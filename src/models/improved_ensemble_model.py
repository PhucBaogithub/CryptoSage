"""Improved ensemble prediction model combining multiple architectures."""

from typing import Any, Dict, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
from torch.optim import Adam
from torch.utils.data import DataLoader, TensorDataset

from ..utils import get_logger

logger = get_logger(__name__)


class ImprovedEnsembleModel(nn.Module):
    """Ensemble model combining Transformer, LSTM, and GRU for better predictions."""
    
    def __init__(
        self,
        input_size: int,
        hidden_size: int = 128,
        num_heads: int = 8,
        num_layers: int = 3,
        dropout: float = 0.2,
        output_size: int = 1,
    ):
        """Initialize improved ensemble model.
        
        Args:
            input_size: Input feature dimension
            hidden_size: Hidden dimension
            num_heads: Number of attention heads
            num_layers: Number of layers
            dropout: Dropout rate
            output_size: Output dimension
        """
        super().__init__()
        
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # Input projection
        self.input_projection = nn.Linear(input_size, hidden_size)
        
        # Transformer branch
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=hidden_size,
            nhead=num_heads,
            dim_feedforward=hidden_size * 4,
            dropout=dropout,
            batch_first=True,
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # LSTM branch
        self.lstm = nn.LSTM(
            input_size=hidden_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout,
            batch_first=True,
        )
        
        # GRU branch
        self.gru = nn.GRU(
            input_size=hidden_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout,
            batch_first=True,
        )
        
        # Attention layer for combining branches
        self.attention = nn.MultiheadAttention(
            embed_dim=hidden_size,
            num_heads=num_heads,
            dropout=dropout,
            batch_first=True,
        )
        
        # Output layers
        self.fc1 = nn.Linear(hidden_size * 3, hidden_size * 2)
        self.fc2 = nn.Linear(hidden_size * 2, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)
        
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(dropout)
        self.layer_norm = nn.LayerNorm(hidden_size)
        
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Forward pass.
        
        Args:
            x: Input tensor (batch_size, seq_len, input_size)
            
        Returns:
            Tuple of (predictions, confidence)
        """
        # Project input
        x_proj = self.input_projection(x)
        x_proj = self.layer_norm(x_proj)
        
        # Transformer branch
        transformer_out = self.transformer(x_proj)
        transformer_out = transformer_out[:, -1, :]  # Take last timestep
        
        # LSTM branch
        lstm_out, _ = self.lstm(x_proj)
        lstm_out = lstm_out[:, -1, :]  # Take last timestep
        
        # GRU branch
        gru_out, _ = self.gru(x_proj)
        gru_out = gru_out[:, -1, :]  # Take last timestep
        
        # Combine branches with attention
        combined = torch.stack([transformer_out, lstm_out, gru_out], dim=1)
        attn_out, _ = self.attention(combined, combined, combined)
        attn_out = attn_out.mean(dim=1)  # Average attention outputs
        
        # Concatenate all branches
        ensemble_out = torch.cat([transformer_out, lstm_out, gru_out], dim=1)
        
        # Final layers
        out = self.fc1(ensemble_out)
        out = self.relu(out)
        out = self.dropout(out)
        
        out = self.fc2(out)
        out = self.relu(out)
        out = self.dropout(out)
        
        predictions = self.fc3(out)
        
        # Calculate confidence based on ensemble agreement
        confidence = torch.sigmoid(torch.abs(transformer_out - lstm_out).mean(dim=1, keepdim=True))
        confidence = 1.0 - confidence  # Invert: high agreement = high confidence
        
        return predictions, confidence


class ImprovedPredictionModel:
    """Wrapper for improved ensemble prediction model."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize model.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Model parameters
        self.input_size = self.config.get('input_size', 20)
        self.hidden_size = self.config.get('hidden_size', 128)
        self.num_heads = self.config.get('num_heads', 8)
        self.num_layers = self.config.get('num_layers', 3)
        self.dropout = self.config.get('dropout', 0.2)
        self.output_size = self.config.get('output_size', 1)
        
        # Training parameters
        self.learning_rate = self.config.get('learning_rate', 0.001)
        self.batch_size = self.config.get('batch_size', 32)
        self.epochs = self.config.get('epochs', 100)
        
        self.model = ImprovedEnsembleModel(
            input_size=self.input_size,
            hidden_size=self.hidden_size,
            num_heads=self.num_heads,
            num_layers=self.num_layers,
            dropout=self.dropout,
            output_size=self.output_size,
        ).to(self.device)
        
        self.optimizer = Adam(self.model.parameters(), lr=self.learning_rate)
        self.criterion = nn.MSELoss()
        self.is_trained = False
        
        logger.info(f"Initialized ImprovedEnsembleModel on {self.device}")
    
    def train_model(self, X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
        """Train the model.
        
        Args:
            X: Training features (n_samples, seq_len, n_features)
            y: Training targets (n_samples, output_size)
            
        Returns:
            Training history
        """
        # Convert to tensors
        X_tensor = torch.FloatTensor(X).to(self.device)
        y_tensor = torch.FloatTensor(y).to(self.device)
        
        # Create dataset
        dataset = TensorDataset(X_tensor, y_tensor)
        dataloader = DataLoader(dataset, batch_size=self.batch_size, shuffle=True)
        
        history = {'loss': [], 'val_loss': []}
        
        self.model.train()
        for epoch in range(self.epochs):
            epoch_loss = 0
            for batch_X, batch_y in dataloader:
                self.optimizer.zero_grad()
                
                predictions, _ = self.model(batch_X)
                loss = self.criterion(predictions, batch_y)
                
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                self.optimizer.step()
                
                epoch_loss += loss.item()
            
            avg_loss = epoch_loss / len(dataloader)
            history['loss'].append(avg_loss)
            
            if (epoch + 1) % 10 == 0:
                logger.info(f"Epoch {epoch + 1}/{self.epochs}, Loss: {avg_loss:.6f}")
        
        self.is_trained = True
        logger.info("Model training completed")
        return history
    
    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Make predictions.
        
        Args:
            X: Input features (n_samples, seq_len, n_features)
            
        Returns:
            Tuple of (predictions, confidence)
        """
        if not self.is_trained:
            raise RuntimeError("Model must be trained before prediction")
        
        self.model.eval()
        with torch.no_grad():
            X_tensor = torch.FloatTensor(X).to(self.device)
            predictions, confidence = self.model(X_tensor)
            
            return predictions.cpu().numpy(), confidence.cpu().numpy()


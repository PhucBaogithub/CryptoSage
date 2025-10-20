"""Short-term trading signal model (intraday)."""

from typing import Any, Dict, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
from torch.optim import Adam
from torch.utils.data import DataLoader, TensorDataset

from ..utils import get_logger
from .base_model import BaseModel

logger = get_logger(__name__)


class ShortTermSignalModel(nn.Module):
    """Short-term trading signal model."""
    
    def __init__(
        self,
        input_size: int,
        hidden_size: int,
        num_heads: int,
        num_layers: int,
        dropout: float = 0.1,
    ):
        """Initialize short-term signal model.
        
        Args:
            input_size: Input feature dimension
            hidden_size: Hidden dimension
            num_heads: Number of attention heads
            num_layers: Number of transformer layers
            dropout: Dropout rate
        """
        super().__init__()
        
        self.input_projection = nn.Linear(input_size, hidden_size)
        
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=hidden_size,
            nhead=num_heads,
            dim_feedforward=hidden_size * 4,
            dropout=dropout,
            batch_first=True,
        )
        
        self.transformer_encoder = nn.TransformerEncoder(
            encoder_layer,
            num_layers=num_layers,
        )
        
        # Signal head: probability of up/down/neutral
        self.signal_head = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size // 2, 3),  # up, down, neutral
            nn.Softmax(dim=-1),
        )
        
        # Confidence head: confidence in the signal
        self.confidence_head = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size // 2, 1),
            nn.Sigmoid(),
        )
    
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Forward pass.
        
        Args:
            x: Input tensor (batch_size, seq_len, input_size)
            
        Returns:
            Tuple of (signal_probs, confidence)
        """
        # Project input
        x = self.input_projection(x)
        
        # Encode
        encoded = self.transformer_encoder(x)
        
        # Use last hidden state
        last_hidden = encoded[:, -1, :]
        
        # Generate signals
        signal_probs = self.signal_head(last_hidden)
        confidence = self.confidence_head(last_hidden)
        
        return signal_probs, confidence


class ShortTermModel(BaseModel):
    """Short-term trading signal model wrapper."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize short-term model.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__("ShortTermModel", config)
        self.build_model()
    
    def build_model(self) -> None:
        """Build the model architecture."""
        config = self.config
        
        self.model = ShortTermSignalModel(
            input_size=config.get("input_size", 50),
            hidden_size=config.get("hidden_size", 128),
            num_heads=config.get("num_heads", 8),
            num_layers=config.get("num_layers", 3),
            dropout=config.get("dropout", 0.1),
        ).to(self.device)
        
        logger.info("Short-term model built")
    
    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
    ) -> Dict[str, Any]:
        """Train the model.
        
        Args:
            X_train: Training features (n_samples, seq_len, n_features)
            y_train: Training targets (n_samples, 3) - probabilities for up/down/neutral
            X_val: Validation features
            y_val: Validation targets
            
        Returns:
            Training history
        """
        # Preprocess
        X_train = self.preprocess_features(X_train.reshape(-1, X_train.shape[-1]), fit=True)
        X_train = X_train.reshape(-1, self.config.get("input_length", 60), X_train.shape[-1])
        
        if X_val is not None:
            X_val = self.preprocess_features(X_val.reshape(-1, X_val.shape[-1]))
            X_val = X_val.reshape(-1, self.config.get("input_length", 60), X_val.shape[-1])
        
        # Create datasets
        train_dataset = TensorDataset(
            torch.FloatTensor(X_train),
            torch.FloatTensor(y_train),
        )
        
        train_loader = DataLoader(
            train_dataset,
            batch_size=self.config.get("batch_size", 64),
            shuffle=True,
        )
        
        # Optimizer and loss
        optimizer = Adam(self.model.parameters(), lr=self.config.get("learning_rate", 0.0005))
        criterion = nn.CrossEntropyLoss()
        
        # Training loop
        history = {"train_loss": [], "val_loss": []}
        epochs = self.config.get("epochs", 50)
        patience = self.config.get("early_stopping_patience", 10)
        best_val_loss = float("inf")
        patience_counter = 0
        
        for epoch in range(epochs):
            # Training
            self.model.train()
            train_loss = 0.0
            
            for X_batch, y_batch in train_loader:
                X_batch = X_batch.to(self.device)
                y_batch = y_batch.to(self.device)
                
                optimizer.zero_grad()
                signal_probs, confidence = self.model(X_batch)
                
                # Get target class (argmax of y_batch)
                target_class = torch.argmax(y_batch, dim=1)
                loss = criterion(signal_probs, target_class)
                
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item()
            
            train_loss /= len(train_loader)
            history["train_loss"].append(train_loss)
            
            # Validation
            if X_val is not None:
                self.model.eval()
                with torch.no_grad():
                    X_val_tensor = torch.FloatTensor(X_val).to(self.device)
                    y_val_tensor = torch.FloatTensor(y_val).to(self.device)
                    
                    signal_probs, confidence = self.model(X_val_tensor)
                    target_class = torch.argmax(y_val_tensor, dim=1)
                    val_loss = criterion(signal_probs, target_class).item()
                    
                    history["val_loss"].append(val_loss)
                    
                    if val_loss < best_val_loss:
                        best_val_loss = val_loss
                        patience_counter = 0
                    else:
                        patience_counter += 1
                    
                    if patience_counter >= patience:
                        logger.info(f"Early stopping at epoch {epoch}")
                        break
            
            if (epoch + 1) % 10 == 0:
                logger.info(f"Epoch {epoch + 1}/{epochs}, Train Loss: {train_loss:.6f}")
        
        self.is_trained = True
        logger.info("Model training completed")
        return history
    
    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Make predictions.
        
        Args:
            X: Input features (n_samples, seq_len, n_features)
            
        Returns:
            Tuple of (signal_probs, confidence)
        """
        if not self.is_trained:
            raise RuntimeError("Model must be trained before prediction")
        
        # Preprocess
        X = self.preprocess_features(X.reshape(-1, X.shape[-1]))
        X = X.reshape(-1, self.config.get("input_length", 60), X.shape[-1])
        
        self.model.eval()
        with torch.no_grad():
            X_tensor = torch.FloatTensor(X).to(self.device)
            signal_probs, confidence = self.model(X_tensor)
            
            return signal_probs.cpu().numpy(), confidence.cpu().numpy()


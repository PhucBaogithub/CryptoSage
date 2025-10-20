"""Base model class for all prediction models."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import numpy as np
import pandas as pd
import torch
from sklearn.preprocessing import StandardScaler

from ..utils import get_logger

logger = get_logger(__name__)


class BaseModel(ABC):
    """Abstract base class for prediction models."""
    
    def __init__(
        self,
        model_name: str,
        config: Dict[str, Any],
        device: Optional[str] = None,
    ):
        """Initialize base model.
        
        Args:
            model_name: Name of the model
            config: Configuration dictionary
            device: Device to use ("cpu" or "cuda")
        """
        self.model_name = model_name
        self.config = config
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        
        logger.info(f"Initialized {model_name} on device {self.device}")
    
    @abstractmethod
    def build_model(self) -> None:
        """Build the model architecture."""
        pass
    
    @abstractmethod
    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
    ) -> Dict[str, Any]:
        """Train the model.
        
        Args:
            X_train: Training features
            y_train: Training targets
            X_val: Validation features
            y_val: Validation targets
            
        Returns:
            Training history/metrics
        """
        pass
    
    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions.
        
        Args:
            X: Input features
            
        Returns:
            Predictions
        """
        pass
    
    def preprocess_features(self, X: np.ndarray, fit: bool = False) -> np.ndarray:
        """Preprocess features using standardization.
        
        Args:
            X: Input features
            fit: Whether to fit the scaler
            
        Returns:
            Preprocessed features
        """
        if fit:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = self.scaler.transform(X)
        
        return X_scaled
    
    def save_model(self, path: str) -> None:
        """Save model to disk.
        
        Args:
            path: Path to save model
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        if self.model is not None:
            torch.save(self.model.state_dict(), path)
            logger.info(f"Model saved to {path}")
    
    def load_model(self, path: str) -> None:
        """Load model from disk.
        
        Args:
            path: Path to load model from
        """
        path = Path(path)
        
        if not path.exists():
            raise FileNotFoundError(f"Model file not found: {path}")
        
        if self.model is not None:
            self.model.load_state_dict(torch.load(path, map_location=self.device))
            self.is_trained = True
            logger.info(f"Model loaded from {path}")
    
    def get_model_summary(self) -> Dict[str, Any]:
        """Get model summary.
        
        Returns:
            Dictionary with model information
        """
        return {
            "model_name": self.model_name,
            "device": self.device,
            "is_trained": self.is_trained,
            "config": self.config,
        }


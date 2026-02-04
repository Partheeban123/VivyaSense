"""
GRU-based Fall Detection Model
Analyzes pose keypoint sequences to detect falls
"""
import torch
import torch.nn as nn


class FallDetectionGRU(nn.Module):
    """
    GRU model for fall detection based on pose keypoint sequences
    
    Architecture:
    - Input: Sequence of flattened keypoints (17 keypoints * 2 coordinates = 34 features)
    - GRU layers: Process temporal sequence
    - Dropout: Regularization
    - Output: Fall probability (sigmoid activation)
    """
    
    def __init__(
        self,
        input_size: int = 34,  # 17 keypoints * 2 coordinates (x, y)
        hidden_size: int = 64,
        num_layers: int = 2,
        output_size: int = 1,
        dropout_prob: float = 0.6
    ):
        """
        Initialize GRU model

        Args:
            input_size: Number of input features (34 for 17 keypoints)
            hidden_size: Number of features in hidden state
            num_layers: Number of recurrent layers
            output_size: Number of output features (1 for binary classification)
            dropout_prob: Dropout probability for regularization
        """
        super(FallDetectionGRU, self).__init__()

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.output_size = output_size

        # GRU layers
        self.gru = nn.GRU(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout_prob if num_layers > 1 else 0
        )

        # Batch normalization
        self.bn = nn.BatchNorm1d(hidden_size)

        # Dropout layer
        self.dropout = nn.Dropout(dropout_prob)

        # Fully connected layers (3 layers: 64 -> 32 -> 16 -> 1)
        self.fc1 = nn.Linear(hidden_size, 32)
        self.fc2 = nn.Linear(32, 16)
        self.fc3 = nn.Linear(16, output_size)

        # Activation functions
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        """
        Forward pass

        Args:
            x: Input tensor of shape (batch_size, sequence_length, input_size)

        Returns:
            Output tensor of shape (batch_size, output_size) with fall probability
        """
        # GRU forward pass
        # out shape: (batch_size, sequence_length, hidden_size)
        # h_n shape: (num_layers, batch_size, hidden_size)
        out, h_n = self.gru(x)

        # Take the output from the last time step
        # out[:, -1, :] shape: (batch_size, hidden_size)
        out = out[:, -1, :]

        # Batch normalization
        out = self.bn(out)

        # Apply dropout
        out = self.dropout(out)

        # First fully connected layer with ReLU
        out = self.fc1(out)
        out = self.relu(out)
        out = self.dropout(out)

        # Second fully connected layer with ReLU
        out = self.fc2(out)
        out = self.relu(out)
        out = self.dropout(out)

        # Third fully connected layer (output)
        out = self.fc3(out)

        # Sigmoid activation
        out = self.sigmoid(out)

        return out
    
    def predict(self, x, threshold: float = 0.5):
        """
        Make prediction with threshold
        
        Args:
            x: Input tensor
            threshold: Classification threshold
        
        Returns:
            Tuple of (probability, is_fall)
        """
        self.eval()
        with torch.no_grad():
            probability = self.forward(x)
            is_fall = probability > threshold
        return probability.item(), is_fall.item()


def load_fall_detection_model(
    model_path: str,
    device: str = 'cpu',
    input_size: int = 34,
    hidden_size: int = 64,
    num_layers: int = 2,
    dropout_prob: float = 0.6
) -> FallDetectionGRU:
    """
    Load pre-trained fall detection model
    
    Args:
        model_path: Path to model weights (.pth file)
        device: Device to load model on ('cpu' or 'cuda')
        input_size: Input size (must match training)
        hidden_size: Hidden size (must match training)
        num_layers: Number of layers (must match training)
        dropout_prob: Dropout probability (must match training)
    
    Returns:
        Loaded model in evaluation mode
    """
    model = FallDetectionGRU(
        input_size=input_size,
        hidden_size=hidden_size,
        num_layers=num_layers,
        output_size=1,
        dropout_prob=dropout_prob
    )
    
    # Load weights
    model.load_state_dict(torch.load(model_path, map_location=device))
    
    # Set to evaluation mode
    model.eval()
    
    # Move to device
    model.to(device)
    
    return model


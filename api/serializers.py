"""Create your api serializers here."""
import numpy as np
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import serializers


class NpEncoder(DjangoJSONEncoder):
    """Encoder for numpy object."""

    def default(self, o):
        """Serialize implementation of NpEncoder serializer.

        Args:
          o: The object you want to serialize.

        Returns:
          The serialized object.
        """
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        return super().default(o)


class NotificationSerializer(serializers.Serializer):
    """Serialize Notification data."""

    title = serializers.CharField(max_length=200)
    body = serializers.CharField(max_length=200)
    token = serializers.CharField()

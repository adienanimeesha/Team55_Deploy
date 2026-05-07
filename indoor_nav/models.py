from django.db import models


class Node(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    building = models.CharField(max_length=20, blank=True)
    floor = models.CharField(max_length=20, blank=True)
    type = models.CharField(max_length=50, blank=True)
    label = models.CharField(max_length=200, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    uq_maps_identifier = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.label or self.id


class Edge(models.Model):
    from_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='edges_from')
    to_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='edges_to')

    def __str__(self):
        return f"{self.from_node_id} → {self.to_node_id}"
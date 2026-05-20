from django.test import TestCase
from indoor_nav.models import Node, Edge
from indoor_nav.pathfinding import dijkstra


class DijkstraTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print('\n--- Setting up test data ---')

        # Building 62, Floor 1
        cls.b62_f1_room = Node.objects.create(
            id='b62_f1_room', building='62', floor='1', type='room', label='Room 101',
            lat=-27.4987, lng=153.0120
        )
        cls.b62_f1_corridor = Node.objects.create(
            id='b62_f1_corridor', building='62', floor='1', type='corridor', label='Corridor F1',
            lat=-27.4988, lng=153.0121
        )
        cls.b62_f1_stairs = Node.objects.create(
            id='b62_f1_stairs', building='62', floor='1', type='stairs', label='Stairs F1',
            lat=-27.4989, lng=153.0122
        )

        # Building 62, Floor 2
        cls.b62_f2_stairs = Node.objects.create(
            id='b62_f2_stairs', building='62', floor='2', type='stairs', label='Stairs F2',
            lat=-27.4989, lng=153.0122
        )
        cls.b62_f2_corridor = Node.objects.create(
            id='b62_f2_corridor', building='62', floor='2', type='corridor', label='Corridor F2',
            lat=-27.4988, lng=153.0123
        )
        cls.b62_f2_room = Node.objects.create(
            id='b62_f2_room', building='62', floor='2', type='room', label='Room 201',
            lat=-27.4987, lng=153.0124
        )

        # Building 63, Floor 1
        cls.b63_entry = Node.objects.create(
            id='b63_entry', building='63', floor='1', type='corridor', label='Building 63 Entry',
            lat=-27.4991, lng=153.0121
        )
        cls.b63_f1_room = Node.objects.create(
            id='b63_f1_room', building='63', floor='1', type='room', label='Room 197',
            lat=-27.4992, lng=153.0122
        )

        # Edges — Building 62 Floor 1
        Edge.objects.create(from_node=cls.b62_f1_room, to_node=cls.b62_f1_corridor, weight=10)
        Edge.objects.create(from_node=cls.b62_f1_corridor, to_node=cls.b62_f1_stairs, weight=15)

        # Stairs between floors
        Edge.objects.create(from_node=cls.b62_f1_stairs, to_node=cls.b62_f2_stairs, weight=20)

        # Edges — Building 62 Floor 2
        Edge.objects.create(from_node=cls.b62_f2_stairs, to_node=cls.b62_f2_corridor, weight=15)
        Edge.objects.create(from_node=cls.b62_f2_corridor, to_node=cls.b62_f2_room, weight=10)

        # Inter-building
        Edge.objects.create(from_node=cls.b62_f1_corridor, to_node=cls.b63_entry, weight=40)
        Edge.objects.create(from_node=cls.b63_entry, to_node=cls.b63_f1_room, weight=10)

        print('Nodes created: 8')
        print('Edges created: 7')

    def test_same_floor_same_building(self):
        print('\n[Test 1] Same floor, same building: Room 101 → Corridor F1')
        path, cost = dijkstra('b62_f1_room', 'b62_f1_corridor')
        print(f'  Path: {" → ".join(n.label for n in path)}')
        print(f'  Cost: {cost}')
        self.assertIsNotNone(path)
        self.assertEqual(path[0].id, 'b62_f1_room')
        self.assertEqual(path[-1].id, 'b62_f1_corridor')
        self.assertEqual(cost, 10)
        print('  PASSED')

    def test_cross_floor_via_stairs(self):
        print('\n[Test 2] Cross floor via stairs: Room 101 (F1) → Room 201 (F2)')
        path, cost = dijkstra('b62_f1_room', 'b62_f2_room')
        print(f'  Path: {" → ".join(n.label for n in path)}')
        print(f'  Cost: {cost}')
        self.assertIsNotNone(path)
        self.assertEqual(path[0].id, 'b62_f1_room')
        self.assertEqual(path[-1].id, 'b62_f2_room')
        node_ids = [n.id for n in path]
        self.assertIn('b62_f1_stairs', node_ids)
        self.assertIn('b62_f2_stairs', node_ids)
        print('  PASSED')

    def test_cross_building(self):
        print('\n[Test 3] Cross building: Room 101 (Building 62) → Room 197 (Building 63)')
        path, cost = dijkstra('b62_f1_room', 'b63_f1_room')
        print(f'  Path: {" → ".join(n.label for n in path)}')
        print(f'  Cost: {cost}')
        self.assertIsNotNone(path)
        self.assertEqual(path[0].id, 'b62_f1_room')
        self.assertEqual(path[-1].id, 'b63_f1_room')
        print('  PASSED')

    def test_no_path(self):
        print('\n[Test 4] No path: Room 101 → Isolated Room (no edges)')
        Node.objects.create(
            id='isolated', building='62', floor='1', type='room', label='Isolated Room',
            lat=-27.5000, lng=153.0130
        )
        path, cost = dijkstra('b62_f1_room', 'isolated')
        print(f'  Path: {path}')
        print(f'  Cost: {cost}')
        self.assertIsNone(path)
        self.assertIsNone(cost)
        print('  PASSED')

    def test_same_start_and_end(self):
        print('\n[Test 5] Same start and end: Room 101 → Room 101')
        path, cost = dijkstra('b62_f1_room', 'b62_f1_room')
        print(f'  Path: {" → ".join(n.label for n in path)}')
        print(f'  Cost: {cost}')
        self.assertIsNotNone(path)
        self.assertEqual(len(path), 1)
        self.assertEqual(cost, 0)
        print('  PASSED')

    def test_invalid_node_id(self):
        print('\n[Test 6] Invalid node ID: Room 101 → does_not_exist')
        path, cost = dijkstra('b62_f1_room', 'does_not_exist')
        print(f'  Path: {path}')
        print(f'  Cost: {cost}')
        self.assertIsNone(path)
        self.assertIsNone(cost)
        print('  PASSED')
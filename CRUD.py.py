class Camera:
    def __init__(self, camera_id, location, status='active'):
        self.camera_id = camera_id
        self.location = location
        self.status = status
        self.footage = []

    def add_footage(self, footage_id):
        self.footage.append(footage_id)

    def __repr__(self):
        return f"Camera(camera_id={self.camera_id}, location='{self.location}', status='{self.status}')"


class Footage:
    def __init__(self, footage_id, camera_id, timestamp, description=""):
        self.footage_id = footage_id
        self.camera_id = camera_id
        self.timestamp = timestamp
        self.description = description

    def __repr__(self):
        return f"Footage(footage_id={self.footage_id}, camera_id={self.camera_id}, timestamp='{self.timestamp}', description='{self.description}')"


class SurveillanceCameraManager:
    def __init__(self):
        self.cameras = {}
        self.footages = {}

    def create_camera(self, camera_id, location):
        if camera_id not in self.cameras:
            camera = Camera(camera_id, location)
            self.cameras[camera_id] = camera
            print(f"Camera {camera_id} created.")
        else:
            print(f"Camera {camera_id} already exists.")

    def read_camera(self, camera_id):
        return self.cameras.get(camera_id, "Camera not found.")

    def update_camera(self, camera_id, location=None, status=None):
        camera = self.cameras.get(camera_id)
        if camera:
            if location:
                camera.location = location
            if status:
                camera.status = status
            print(f"Camera {camera_id} updated.")
        else:
            print("Camera not found.")

    def delete_camera(self, camera_id):
        if camera_id in self.cameras:
            del self.cameras[camera_id]
            print(f"Camera {camera_id} deleted.")
        else:
            print("Camera not found.")

    def monitor_surveillance_cameras(self, camera_id):
        camera = self.cameras.get(camera_id)
        if camera:
            print(f"Monitoring camera {camera_id} at {camera.location}. Status: {camera.status}")
        else:
            print("Camera not found.")

    def create_footage(self, footage_id, camera_id, timestamp, description=""):
        if camera_id in self.cameras:
            footage = Footage(footage_id, camera_id, timestamp, description)
            self.footages[footage_id] = footage
            self.cameras[camera_id].add_footage(footage_id)
            print(f"Footage {footage_id} created for camera {camera_id}.")
        else:
            print("Camera not found.")

    def review_camera_footage(self, footage_id):
        footage = self.footages.get(footage_id)
        if footage:
            print(f"Reviewing footage: {footage}")
        else:
            print("Footage not found.")


import unittest
from datetime import datetime
from io import StringIO
import sys

# Assuming the classes are defined in a module named surveillance
# from surveillance import SurveillanceCameraManager, Camera, Footage

class TestSurveillanceCameraManager(unittest.TestCase):
    def setUp(self):
        self.manager = SurveillanceCameraManager()
        self.manager.create_camera('cam1', 'Entrance')
        self.manager.create_camera('cam2', 'Parking Lot')

    def test_create_camera(self):
        self.assertEqual(len(self.manager.cameras), 2)
        self.manager.create_camera('cam1', 'Entrance')
        self.assertEqual(len(self.manager.cameras), 2)  # Should not create duplicate

    def test_read_camera(self):
        camera = self.manager.read_camera('cam1')
        self.assertEqual(camera.camera_id, 'cam1')
        self.assertEqual(camera.location, 'Entrance')
        
        self.assertEqual(self.manager.read_camera('nonexistent'), "Camera not found.")

    def test_update_camera(self):
        self.manager.update_camera('cam1', location='Lobby', status='inactive')
        camera = self.manager.read_camera('cam1')
        self.assertEqual(camera.location, 'Lobby')
        self.assertEqual(camera.status, 'inactive')

    def test_delete_camera(self):
        self.manager.delete_camera('cam2')
        self.assertIsNone(self.manager.cameras.get('cam2'))
        self.manager.delete_camera('cam2')  # Should not raise error

    def test_monitor_surveillance_cameras(self):
        captured_output = StringIO()
        sys.stdout = captured_output  # Redirect stdout to capture print statements
        self.manager.monitor_surveillance_cameras('cam1')
        sys.stdout = sys.__stdout__  # Reset redirect
        output = captured_output.getvalue().strip()
        self.assertIn("Monitoring camera cam1", output)

    def test_create_footage(self):
        self.manager.create_footage('footage1', 'cam1', '2024-09-25 10:00:00', 'Visitor entry.')
        self.assertIn('footage1', self.manager.footages)
        self.assertIn('footage1', self.manager.cameras['cam1'].footage)

    def test_review_camera_footage(self):
        self.manager.create_footage('footage1', 'cam1', '2024-09-25 10:00:00', 'Visitor entry.')
        captured_output = StringIO()
        sys.stdout = captured_output  # Redirect stdout to capture print statements
        self.manager.review_camera_footage('footage1')
        sys.stdout = sys.__stdout__  # Reset redirect
        output = captured_output.getvalue().strip()
        self.assertIn("Reviewing footage:", output)

    def test_review_nonexistent_footage(self):
        captured_output = StringIO()
        sys.stdout = captured_output  # Redirect stdout to capture print statements
        self.manager.review_camera_footage('nonexistent')
        sys.stdout = sys.__stdout__  # Reset redirect
        output = captured_output.getvalue().strip()
        self.assertEqual(output, "Footage not found.")


if __name__ == '__main__':
    unittest.main()

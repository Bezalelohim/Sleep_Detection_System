class VehicleController:
    def __init__(self):
        self.current_speed = 0
        self.emergency_active = False

    def initiate_emergency_stop(self):
        if not self.emergency_active:
            self.emergency_active = True
            self.gradual_stop()
    
    def gradual_stop(self):
        """
        Simulated gradual stop - in a real implementation, 
        this would interface with the vehicle's control systems
        """
        while self.current_speed > 0:
            # Reduce speed by 5 units per second
            self.current_speed = max(0, self.current_speed - 5)
            if self.current_speed == 0:
                self.park_vehicle()
    
    def park_vehicle(self):
        """
        Simulated parking procedure - in a real implementation,
        this would interface with the vehicle's autonomous systems
        """
        print("Emergency: Vehicle safely parked on the side of the road") 
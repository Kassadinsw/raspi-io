import unittest
from raspi_io import GPIO
from raspi_io.utility import scan_server


class TestGPIO(unittest.TestCase):
    def setUp(self):
        self.gpio = GPIO(scan_server(timeout=0.03)[0], verbose=0)

    def tearDown(self):
        del self.gpio

    def test_setmode(self):
        self.assertEqual(self.gpio.setmode(123), False)
        self.assertEqual(self.gpio.setmode(GPIO.BCM), True)
        self.assertEqual(self.gpio.setmode(GPIO.BOARD), False)

    def test_setup(self):
        self.assertEqual(self.gpio.setup(21, 123), False)
        self.assertEqual(self.gpio.setup(123, GPIO.OUT), False)

        self.assertEqual(self.gpio.setup(21, GPIO.IN), True)
        self.assertEqual(self.gpio.setup(20, GPIO.IN), True)

    def test_input(self):
        self.assertEqual(self.gpio.input(21), None)
        self.assertEqual(self.gpio.input(22), None)
        self.assertEqual(self.gpio.setup([21, 22], GPIO.IN), True)
        self.assertEqual(self.gpio.input(21), 0)
        self.assertEqual(self.gpio.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP), True)
        self.assertEqual(self.gpio.input(22), 1)

    def test_output(self):
        self.assertEqual(self.gpio.output(21, 1), False)
        self.assertEqual(self.gpio.setup(21, GPIO.OUT), True)
        self.assertEqual(self.gpio.output(21, 1), True)
        self.assertEqual(self.gpio.output(21, 0), True)

    def test_cleanup(self):
        self.assertEqual(self.gpio.cleanup(123), False)
        self.assertEqual(self.gpio.cleanup([21, 22]), True)


if __name__ == "__main__":
    unittest.main()

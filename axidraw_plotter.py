"""
AxiDraw Plotter Integration

Provides integration with the AxiDraw pen plotter for physical output.
"""

from typing import Optional
import warnings


class AxiDrawPlotter:
    """
    Interface for controlling AxiDraw pen plotters.
    
    This class provides a simple interface to the AxiDraw API for
    plotting SVG files.
    """
    
    def __init__(self):
        """Initialize the AxiDraw plotter interface."""
        self.plotter = None
        self._available = False
        
        try:
            from pyaxidraw import axidraw
            self.axidraw_module = axidraw
            self._available = True
        except ImportError:
            warnings.warn(
                "AxiDraw library not available. Install it to use plotter features.\n"
                "Visit: https://axidraw.com/doc/py_api/#installation"
            )
    
    def is_available(self) -> bool:
        """
        Check if AxiDraw library is available.
        
        Returns:
            True if the library is installed and available
        """
        return self._available
    
    def connect(self) -> bool:
        """
        Connect to the AxiDraw plotter.
        
        Returns:
            True if connection successful
        """
        if not self._available:
            print("AxiDraw library not available")
            return False
        
        try:
            self.plotter = self.axidraw_module.AxiDraw()
            self.plotter.interactive()
            
            if not self.plotter.connect():
                print("Failed to connect to AxiDraw")
                return False
            
            print("Successfully connected to AxiDraw")
            return True
        except Exception as e:
            print(f"Error connecting to AxiDraw: {e}")
            return False
    
    def plot_svg(
        self,
        svg_file: str,
        pen_down_speed: int = 25,
        pen_up_speed: int = 75,
        pen_down_delay: int = 0,
        pen_up_delay: int = 0,
        auto_rotate: bool = True
    ) -> bool:
        """
        Plot an SVG file.
        
        Args:
            svg_file: Path to the SVG file to plot
            pen_down_speed: Speed when pen is down (1-100)
            pen_up_speed: Speed when pen is up (1-100)
            pen_down_delay: Delay after pen down (ms)
            pen_up_delay: Delay after pen up (ms)
            auto_rotate: Automatically rotate page for best fit
            
        Returns:
            True if plotting successful
        """
        if not self._available:
            print("AxiDraw library not available")
            return False
        
        if self.plotter is None:
            print("Not connected to AxiDraw. Call connect() first.")
            return False
        
        try:
            # Configure plotter settings
            self.plotter.options.speed_pendown = pen_down_speed
            self.plotter.options.speed_penup = pen_up_speed
            self.plotter.options.delay_down = pen_down_delay
            self.plotter.options.delay_up = pen_up_delay
            self.plotter.options.auto_rotate = auto_rotate
            
            # Plot the file
            print(f"Plotting {svg_file}...")
            self.plotter.plot_setup(svg_file)
            self.plotter.plot_run()
            
            print("Plotting complete!")
            return True
        except Exception as e:
            print(f"Error plotting: {e}")
            return False
    
    def preview_svg(self, svg_file: str) -> bool:
        """
        Preview an SVG file without plotting.
        
        Args:
            svg_file: Path to the SVG file to preview
            
        Returns:
            True if preview successful
        """
        if not self._available:
            print("AxiDraw library not available")
            return False
        
        try:
            if self.plotter is None:
                self.plotter = self.axidraw_module.AxiDraw()
                self.plotter.interactive()
            
            # Set preview mode
            self.plotter.options.preview = True
            self.plotter.plot_setup(svg_file)
            
            print(f"Preview of {svg_file} prepared")
            return True
        except Exception as e:
            print(f"Error previewing: {e}")
            return False
    
    def disconnect(self) -> None:
        """Disconnect from the AxiDraw plotter."""
        if self.plotter is not None:
            try:
                self.plotter.disconnect()
                print("Disconnected from AxiDraw")
            except Exception as e:
                print(f"Error disconnecting: {e}")
            finally:
                self.plotter = None
    
    def move_to_home(self) -> bool:
        """
        Move the plotter to home position.
        
        Returns:
            True if successful
        """
        if not self._available or self.plotter is None:
            print("Plotter not available or not connected")
            return False
        
        try:
            self.plotter.moveto(0, 0)
            return True
        except Exception as e:
            print(f"Error moving to home: {e}")
            return False
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()


def plot_svg_file(
    svg_file: str,
    pen_down_speed: int = 25,
    pen_up_speed: int = 75,
    auto_connect: bool = True
) -> bool:
    """
    Convenience function to plot an SVG file with default settings.
    
    Args:
        svg_file: Path to SVG file
        pen_down_speed: Speed when drawing (1-100)
        pen_up_speed: Speed when moving (1-100)
        auto_connect: Automatically connect and disconnect
        
    Returns:
        True if successful
    """
    plotter = AxiDrawPlotter()
    
    if not plotter.is_available():
        print("AxiDraw library not installed")
        return False
    
    if auto_connect:
        with plotter:
            return plotter.plot_svg(
                svg_file,
                pen_down_speed=pen_down_speed,
                pen_up_speed=pen_up_speed
            )
    else:
        return plotter.plot_svg(
            svg_file,
            pen_down_speed=pen_down_speed,
            pen_up_speed=pen_up_speed
        )

import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fft import fft
from matplotlib.animation import FuncAnimation

class WaterfallSpectrogram:
    def __init__(self):
        # Audio parameters
        self.sample_rate = 44100  # Hz
        self.block_size = 2048
        self.window = np.hanning(self.block_size)
        
        # Spectrogram parameters
        self.history_size = 100  # Number of frames to keep in history
        self.spectrogram_data = np.zeros((self.block_size//2, self.history_size))
        
        # Create figure and subplot
        self.fig = plt.figure(figsize=(10, 6))
        self.ax = self.fig.add_subplot(111)
        
        # Initialize plot with transposed data
        self.image = self.ax.imshow(
            self.spectrogram_data,
            aspect='auto',
            origin='lower',
            cmap='Greys',
            interpolation='nearest',
            extent=[0, self.history_size, 220, 880]
        )
        
        # Labels and title
        self.ax.set_xlabel('Time Frame')
        self.ax.set_ylabel('Frequency (Hz)')
        self.ax.set_title('Waterfall Spectrogram')
        
        # Add frequency ticks in kHz
        freq_ticks = np.linspace(220, 880, 5)
        freq_labels = [f'{f}Hz' for f in freq_ticks]
        self.ax.set_yticks(freq_ticks)
        self.ax.set_yticklabels(freq_labels)
        
        # Buffer for audio data
        self.audio_buffer = np.zeros(self.block_size)
    
    def audio_callback(self, indata, frames, time, status):
        """Callback function to process audio data"""
        self.audio_buffer = indata[:, 0]
    
    def update_plot(self, frame):
        """Update function for animation"""
        # Apply window function and compute FFT
        windowed = self.audio_buffer * self.window
        spectrum = fft(windowed)
        magnitude = np.abs(spectrum[:self.block_size//2])
        
        # Convert to dB scale (with small offset to avoid log(0))
        magnitude_db = 20 * np.log10(magnitude + 1e-6)
        
        # Roll the spectrogram data horizontally and update the last column
        self.spectrogram_data = np.roll(self.spectrogram_data, -1, axis=1)
        self.spectrogram_data[:, -1] = magnitude_db
        
        # Update plot
        self.image.set_array(self.spectrogram_data)
        
        # Update color scale
        vmin = np.min(self.spectrogram_data)
        vmax = np.max(self.spectrogram_data)
        self.image.set_clim(vmin, vmax)
        
        return [self.image]
    
    def start(self):
        # Start audio stream
        stream = sd.InputStream(
            channels=1,
            samplerate=self.sample_rate,
            blocksize=self.block_size,
            callback=self.audio_callback
        )
        
        # Create animation
        ani = FuncAnimation(
            self.fig,
            self.update_plot,
            interval=30,  # Update every 30ms
            blit=True
        )
        
        # Start stream and show plot
        with stream:
            plt.show()

if __name__ == "__main__":
    spectrogram = WaterfallSpectrogram()
    spectrogram.start()
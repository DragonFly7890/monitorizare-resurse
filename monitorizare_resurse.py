import psutil
import GPUtil
import time
import logging
from datetime import datetime
from plyer import notification

# Configurare fisier de log
logging.basicConfig(
    filename="log_temperaturi.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Praguri de alertă
CPU_THRESHOLD = 80
GPU_THRESHOLD = 80
TEMP_THRESHOLD = 75

def alerta(titlu, mesaj):
    notification.notify(
        title=f"[ALERTĂ] {titlu}",
        message=mesaj,
        timeout=5
    )

def monitorizare():
    while True:
        cpu_percent = psutil.cpu_percent(interval=1)

        if cpu_percent > CPU_THRESHOLD:
            mesaj = f"CPU peste prag: {cpu_percent}%"
            logging.warning(mesaj)
            alerta("CPU", mesaj)
        else:
            logging.info(f"CPU OK: {cpu_percent}%")

        # Afișare top procese consumatoare de CPU
        print("\nProcese cu CPU > 10%:")
        for proc in psutil.process_iter(['name', 'cpu_percent']):
            try:
                if proc.info['cpu_percent'] > 10:
                    print(f" - {proc.info['name']}: {proc.info['cpu_percent']}%")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Monitorizare GPU
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            if gpu.load * 100 > GPU_THRESHOLD:
                mesaj = f"GPU peste prag: {gpu.load*100:.1f}%"
                logging.warning(mesaj)
                alerta("GPU", mesaj)
            else:
                logging.info(f"GPU OK: {gpu.load*100:.1f}%")

            if gpu.temperature > TEMP_THRESHOLD:
                mesaj = f"Temperatură GPU mare: {gpu.temperature}°C"
                logging.warning(mesaj)
                alerta("Temperatură GPU", mesaj)
            else:
                logging.info(f"Temperatură GPU OK: {gpu.temperature}°C")

        print("---- Aștept 5 secunde ----\n")
        time.sleep(5)

if __name__ == "__main__":
    monitorizare()

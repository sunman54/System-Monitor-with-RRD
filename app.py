import time
import rrdtool
import psutil

# RRD dosyası adı
rrd_file = 'system_usage.rrd'

# RRD dosyasını oluştur
rrdtool.create(
    rrd_file,
    '--step', '10',  # 10 saniyede bir veri toplanacak
    'DS:cpu:GAUGE:20:0:100',  # CPU kullanımı (0-100%)
    'DS:ram:GAUGE:20:0:U',    # RAM kullanımı (byte cinsinden)
    'DS:net_in:COUNTER:20:0:U',  # Ağ girişi (byte cinsinden)
    'DS:net_out:COUNTER:20:0:U', # Ağ çıkışı (byte cinsinden)
    'RRA:AVERAGE:0.5:1:360'   # 1 saatlik veri (360 * 10 saniye)
)

def get_net_io():
    """Ağ giriş/çıkış verisini döndürür."""
    net = psutil.net_io_counters()
    return net.bytes_recv, net.bytes_sent

def update_rrd(cpu_usage, ram_usage, net_in, net_out):
    """RRD dosyasını sistem metrikleri ile günceller."""

    rrdtool.update(rrd_file, f'N:{cpu_usage}:{ram_usage}:{net_in}:{net_out}')
    print(f"Updated RRD: CPU {cpu_usage}%, RAM {ram_usage} bytes, Net In {net_in} bytes, Net Out {net_out} bytes")

# 1 saat boyunca 10 saniyede bir veri toplama
try:
    for _ in range(360):  # 360 döngü (10 saniye x 360 = 3600 saniye = 1 saat)
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().used
        net_in, net_out = get_net_io()
        update_rrd(cpu_usage, ram_usage, net_in, net_out)
        time.sleep(10)
except KeyboardInterrupt:
    print("Script interrupted by user")

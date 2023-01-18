import pymysql
import spidev
import time

db=None
cur=None

db=pymysql.connect(host='192.168.0.177', user='root',password='1234' ,db='mysql', charset='utf8')


def analog_read(channel):
	r=spi.xfer2([1,(0x08+channel)<<4,0])
	adc_out=((r[1]&0x03)<<8)+r[2]
	return adc_out
	
	
spi=spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000


try:
	while True:
		adc=analog_read(3)
		voltage=adc*(3.3/1023/5)*1000
		temperature=voltage/10.0
		print("%4d/1023=>%5.3f V => %4.1f C" % (adc,voltage,temperature))
		cur=db.cursor()
		sql="INSERT INTO temperature(TEMP) VALUES(%4.1f)"% temperature
		print(sql)
		
		cur.execute(sql)
		
		db.commit()
		
		time.sleep(10)
		
except KeyboardInterrupt:
	pass
finally:
	spi.close()	

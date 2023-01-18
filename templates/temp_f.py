from flask import Flask,request,render_template
import pymysql




app=Flask(__name__)


@app.route("/")
def temp():
	db=None
	cur=None

	db=pymysql.connect(host='192.168.22.94',user='root',password='1234' ,db='mysql',charset='utf8')

	cur=db.cursor()
	sql="SELECT DATATIME, TEMP FROM temperature ORDER BY DATATIME DESC LIMIT 50"
	
	cur.execute(sql)
	
	result = cur.fetchall()
	
	return render_template("lm35_service.html",result=result)
			
		
if __name__=='__main__':
	app.run(debug=True,port=80,host='0.0.0.0')
	

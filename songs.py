from sqlalchemy import create_engine, MetaData, Table

def getSongs():
	engine = create_engine("mysql+pymysql://root:@localhost/ontag")
	metadata = MetaData(bind=engine)
	con = engine.connect()
    
	res = con.execute("select id,name from songs order by RAND() limit 100")

	songs = {}
	for row in res:
		songinfo = {"name": row['name']}
		songs[row['id']] = {"songinfo": songinfo}

	return songs
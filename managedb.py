import psycopg2

# Connect to  postgres DB
conn = psycopg2.connect("dbname=tfmdb user=tfm password=Tfm123456 port=5433")
conn.autocommit=True
# Open a cursor to perform database operations
cur = conn.cursor()
cur_select = conn.cursor()
cur_update = conn.cursor()

cur.execute("delete from c")
cur.execute("delete from e")
cur.execute("delete from d")

cur.execute("SELECT distinct id,latitud,longitud FROM establecimiento e join asignacionmec m on e.id=m.establecimiento_id where departamento='Alto Paraná' order by 1;")

for index, row in enumerate(cur,start=1):     
    cur_update.execute("insert into e(nro,lat,long,id) values("+str(index)+","+str(row[1])+","+str(row[2])+",'"+str(row[0])+"')")


cur.execute("SELECT distinct nro_documento,latitud,longitud FROM docente d join asignacionmec m on d.nro_documento=m.docente_id where departamento='Alto Parana' and latitud is not null order by 1;")

for index, row in enumerate(cur,start=1):     
    cur_update.execute("insert into d(nro,lat,long) values("+str(index)+","+str(row[1])+","+str(row[2])+")")


cur.execute("SELECT curso_id,turno_id,seccion,institucion_id,establecimiento_id FROM asignacionmec order by seccion_id;")

for index, row in enumerate(cur,start=1):    
    cur_select.execute("select nro from e where id='"+row[4]+"'") 
    for row2 in cur_select:
        cur_update.execute("insert into c(nro,g,t,s,i,e) values("+str(index)+","+str(row[0])+","+str(row[1])+",'"+str(row[2])+"',"+str(row[3])+","+str(row2[0])+")")

cur_update.close()
cur.close()
conn.close()
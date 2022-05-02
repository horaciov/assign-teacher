#data of Problem Assign Teacher
import psycopg2



def init(maxDistance):
    #Maximum distance on kilometers
    global Dmax, C, D, E
    Dmax=maxDistance
    #Class
    conn = psycopg2.connect("dbname=tfmdb user=tfm password=Tfm123456 port=5433")
    cur = conn.cursor()
    
    C = []
    cur.execute("select nro,g,t,s,i,e from c order by 1")
    print("Load C...")
    for row in cur:
        C.append([row[1],row[2],row[3],row[4],row[5]])
   
    #Teachers
    D=[]
    cur.execute("select nro,lat,long from d order by 1")
    print("Load D...")
    for row in cur:
        D.append([row[0],row[1],row[2]])

    #Establishment
    E=[]
    cur.execute("select nro,lat,long from e order by 1")
    print("Load E...")
    for row in cur:
        E.append([row[0],row[1],row[2]])

    cur.close()
    conn.close()




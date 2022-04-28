#data of Problem Assign Teacher



def init(maxDistance):
    #Maximum distance on kilometers
    global Dmax, C, D, E
    Dmax=maxDistance
    #Class
    C = [
        [1,1,1,1,1],
        [1,1,1,2,2],
        [1,2,1,3,3],
        [2,2,1,1,1],
        [2,2,1,2,2],
        [2,1,1,3,3]
    ]

    #Teachers
    D=[
        [1,3,4],
        [2,0,9],
        [3,4,3],
        [4,0,4]
    ]

    #Establishment
    E=[
        [1,1,5],
        [2,3,7],
        [3,9,2]
    ]




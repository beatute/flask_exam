from app import db, Movie, Actor

movie1 = Movie(title="Murder Mystery 2", country="USA", released="2023-03-31", runtime=89, 
               about="Now full-time detectives struggling to get their private eye agency.")
movie2 = Movie(title="Titanic: 100 Years On", country="USA", released="2012-03-01", runtime=70, 
               about="The unsinkable floating palace set sail from Southampton on 10th April 1912 on her maiden voyage to New York.")
movie3 = Movie(title="The Wolf of Wall Street", country="USA", released="2013-12-25", runtime=180, 
               about="In the height of the free-flowing cash of the 1980s, stock broker Jordan Belfort transforms from a Wall Street newcomer to an unethical corrupt IPO cowboy.")

actor1 = Actor(name="Audrey", surname="Spitz")
actor2 = Actor(name="Nick", surname="Spitz")
actor3 = Actor(name="Leonardo", surname="DiCaprio")
actor4 = Actor(name="Donnie", surname="Azoff")

movie1.actors.append(actor1)
movie1.actors.append(actor2)
movie2.actors.append(actor3)
movie3.actors.append(actor3)
movie3.actors.append(actor4)

db.create_all()
db.session.add_all([movie1, movie2, movie3])
db.session.add_all([actor1, actor2, actor3, actor4])



db.session.commit()
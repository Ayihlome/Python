from sqlalchemy import create_engine, Column, Float, String, Integer, ForeignKey, CheckConstraint, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Define base
Base = declarative_base()

# Define engine
engine = create_engine('sqlite:///testdb.db', echo=False) #change echo to false later

# Session maker, a session will be called for every connection to the server(see server file)
SessionLocal = sessionmaker(bind=engine)

class Movies(Base):
    __tablename__ = "Movies"
    
    movie_id = Column("movie_id", Integer, primary_key=True, index=True)
    title = Column("title", String, nullable=False)
    cinema_room = Column("cinema_room", Integer, CheckConstraint('cinema_room >= 1 AND cinema_room <= 7'))
    release_date = Column("release_date", Date)
    end_date = Column("end_date", Date)
    tickets_available = Column("tickets_available", Integer, CheckConstraint('tickets_available >= 0'))
    ticket_price = Column("ticket_price", Float, CheckConstraint('ticket_price >= 0'))
    
    # Relationship with the sales table for easy access to related data
    sales = relationship("Sales", back_populates="movie")
    
    def __init__(self, title, cinema_room, release_date, end_date, tickets_available, ticket_price ):
        self.title = title
        self.cinema_room = cinema_room
        self.release_date = release_date
        self.end_date = end_date
        self.tickets_available = tickets_available
        self.ticket_price = ticket_price
    
    def as_dict(self):
        return {
            "movie_id": self.movie_id,
            "title": self.title,
            "cinema_room": self.cinema_room,
            "release_date": str(self.release_date),
            "end_date": str(self.end_date),
            "tickets_available": self.tickets_available,
            "ticket_price": self.ticket_price
        }


class Sales(Base):
    __tablename__ = "Sales"
    
    sales_id = Column("sales_id", Integer, primary_key=True, index=True)
    movie_id = Column("movie_id", Integer, ForeignKey("Movies.movie_id"))
    customer_name = Column("customer_name", String, nullable=False)
    number_of_tickets = Column("number_of_tickets", Integer, CheckConstraint('number_of_tickets >= 0'))
    total = Column("total", Float)
    
    # Relationship with the movies table for easy access to related data
    movie = relationship("Movies", back_populates="sales")
    
    def __init__(self, movie_id, customer_name, number_of_tickets, total):
        self.movie_id = movie_id
        self.customer_name = customer_name
        self.number_of_tickets = number_of_tickets
        self.total = total
    
    def as_dict (self):
        return{
        "movie" : self.movie_id,  
        "customer name": self.customer_name,  
        "Number of tickets": self.number_of_tickets,
        "total" : self.total
        }
    
    # def addMovie(self, title, cinema_room, release_date, end_date, tickets_available, ticket_price ):
    # newMovie = Movies(title, cinema_room, release_date, end_date, tickets_available, ticket_price)
    # db_session.add(newMovie)
    # db_session.commit()
    # return newMovie

def startupDB():
    Base.metadata.create_all(bind=engine) 
    # basically says: if table doesn't already exist create it now

def addMovie(db_session, title, cinema_room, release_date, end_date, tickets_available, ticket_price ):
    newMovie = Movies(title, cinema_room, release_date, end_date, tickets_available, ticket_price)
    db_session.add(newMovie)
    db_session.commit()
    return newMovie

def updateMovie(db_session, movie_id, newData):
    newEntry = db_session.query(Movies).filter_by(movie_id=movie_id).update(newData)
    db_session.commit()
    return newEntry

def changeNoOfTickets (db_session, movie_id, newAmount):
    newEntry = db_session.query(Movies).filter_by(movie_id=movie_id).update({
        "tickets_available": newAmount
    })
    db_session.commit()
    return newEntry

def deleteMovie(db_session, movie_id):
    deleteItem = db_session.query(Movies).filter_by(movie_id=movie_id).first()
    db_session.delete(deleteItem)
    db_session.commit()

def showAll (db_session):
    return db_session.query(Movies).all()

def sale (db_session, movie_id, customer_name, number_of_tickets):
    # check if movie exists
    movie = db_session.query(Movies).filter_by(movie_id=movie_id).first()
    if not movie:
        return {"status": "error","error": "Invalid input"}
    
    totalPrice = movie.ticket_price * number_of_tickets
    
    newSale = Sales(movie_id=movie_id, customer_name=customer_name, number_of_tickets=number_of_tickets, total=totalPrice)
    # update the movie tickets available
    db_session.query(Movies).filter_by(movie_id=movie.movie_id).update({
        "tickets_available": movie.tickets_available - number_of_tickets #sold
    })
    db_session.commit()
    return newSale.as_dict()

if __name__ == "__main__":
    startupDB()
    # When this file runs, it creates all the tables
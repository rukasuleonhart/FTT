from sqlalchemy.orm import registry, Mapped, relationship, mapped_column
from sqlalchemy import func, ForeignKey
from datetime import datetime

table_registry = registry()

@table_registry.mapped_as_dataclass
# ==============================================================================================================================#
 #                                               👤 U S U A R I O S                                                            #                                      
# ==============================================================================================================================#
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(default=func.current_timestamp())
    updated_at: Mapped[datetime] = mapped_column(default=func.current_timestamp())
    is_active: Mapped[bool] = mapped_column(default=True)

# ==============================================================================================================================#
 #                                                   🏠 S A L A S                                                              #                      
# ==============================================================================================================================#
class Room:
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    number: Mapped[int]
    capacity: Mapped[int]
    resource: Mapped[str]
    exclusive: Mapped[str] = mapped_column(unique=True)
    block_id: Mapped[int] = mapped_column(ForeignKey("blocks.id"))

    # 👥 Relacionamento: cada sala pertence a um bloco
    fk_block_with_room: Mapped["Block"] = relationship("Block", back_populates="fk_room_with_block")
    fk_reservation_with_room: Mapped[list["Reservation"]] = relationship(
       "Reservation", back_populates="fk_room_with_reservation", cascade='all, delete-orphan')

# ==============================================================================================================================#
 #                                                  🏣  B L O C O S                                                            #                              
# ==============================================================================================================================#
class Block:
    __tablename__ = 'blocks'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    identifier: Mapped[str]
        
    # 👥 Relacionamento: um bloco pode ter várias salas
    fk_room_with_block: Mapped[list["Room"]] = relationship("Room", back_populates="fk_block_with_room", cascade='all, delete-orphan')

# ==============================================================================================================================#
 #                                                 📓 R E S E R V A S                                                          #                
# ==============================================================================================================================#

class Reservation:
    __tablename__ = 'reservations'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    start_time: Mapped[datetime] = mapped_column(default=func.current_timestamp())
    end_time: Mapped[datetime] = mapped_column(default=func.current_timestamp())
    coordinator: Mapped[str] = mapped_column(unique=True)
    reason: Mapped[str]
    status: Mapped[bool]

    # 👥 Relacionamento: cada reserva pertence a uma sala
    fk_room_with_reservation: Mapped["Room"] = relationship(
        "Room", back_populates="fk_reservation_with_room"
    )



    

    

    

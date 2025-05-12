from backend.app.models import db
from backend.app.models.basemodel import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Message(BaseModel):
    __tablename__ = 'message'

    sender_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)

    # 时间字段继承自 BaseModel: created_gmt, updated_gmt

    sender = relationship("User", foreign_keys=[sender_id], backref="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], backref="received_messages")

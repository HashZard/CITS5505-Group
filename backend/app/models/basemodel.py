import logging
import json
import datetime

from backend.app.models import db

db_logger = logging.getLogger('db_logger')
db_logger.propagate = False  # indicate that this logger should not propagate to the root logger

class BaseModel(db.Model):
    __abstract__ = True  # indicate that this is an abstract model

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    created_gmt = db.Column(db.DateTime, server_default=db.func.now())
    updated_gmt = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def to_dict(self):
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)

            # change datetime to ISO format
            if isinstance(value, datetime.datetime):
                result[column.name] = value.isoformat()

            # 反序列化 JSON 数据（如果字段已经是 JSON 格式的字符串）
            elif isinstance(value, str):
                try:
                    result[column.name] = json.loads(value)  # 假设可以反序列化为 JSON
                except (json.JSONDecodeError, TypeError):
                    result[column.name] = value  # 如果反序列化失败，则保持原始字符串

            # 默认处理（直接存储字段值）
            else:
                result[column.name] = value

        return result

    def __repr__(self):
        """返回模型对象的字符串表示"""
        return f"<{self.__class__.__name__} {self.to_dict()}>"

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
            db_logger.info(f"Data inserted into database: {self}")
            return True
        except Exception as e:
            db.session.rollback()
            db_logger.error(f"Database insertion failed: {str(e)}")
            return False
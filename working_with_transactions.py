from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.exc import SQLAlchemyError

# Базовый класс для декларативных моделей
Base = declarative_base()


# Определение моделей (таблиц)
class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    # Связь один ко многим
    orders = relationship('Order', back_populates='customer')


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_item = Column(Float, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)

    # Связь с клиентом
    customer = relationship('Customer', back_populates='orders')


# Функция для создания подключения к базе данных
def get_engine():
    return create_engine('postgresql+psycopg2://YOUR_USER:YOUR_PASSWORD@localhost:YOUR_PORT/YOUR_DATABASE')


# Функция для создания таблиц
def create_tables(engine):
    Base.metadata.create_all(engine)


# Функция для добавления данных
def add_customer_and_order(session, customer_name, customer_email, product_name, quantity, price):
    try:
        new_customer = Customer(name=customer_name, email=customer_email)
        new_order = Order(product_name=product_name, quantity=quantity, price_per_item=price, customer=new_customer)

        session.add(new_customer)
        session.add(new_order)
        session.commit()

        print(f"Added customer '{customer_name}' with an order '{product_name}'")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error: {e}")


# Функция для сложного запроса
def get_customer_total_spent(session):
    result = session.query(
        Customer.name,
        func.sum(Order.quantity * Order.price_per_item).label('total_spent')
    ).join(Order).group_by(Customer.id).all()

    for name, total_spent in result:
        print(f"Customer: {name}, Total Spent: {total_spent}")


# Основная логика работы с базой данных
def main():
    engine = get_engine()

    # Создание таблиц
    create_tables(engine)

    # Создание сессии
    Session = sessionmaker(bind=engine)
    session = Session()

    # Добавление клиента и заказа
    add_customer_and_order(session, 'Alice', 'alice@example.com', 'Laptop', 1, 1000.0)
    add_customer_and_order(session, 'Bob', 'bob@example.com', 'Smartphone', 2, 500.0)

    # Запрос на получение суммы потраченных денег каждым клиентом
    print("\nTotal spent by each customer:")
    get_customer_total_spent(session)

    # Закрытие сессии
    session.close()


if __name__ == "__main__":
    main()
